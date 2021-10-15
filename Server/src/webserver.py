import json
from enum import Enum, auto

from bottle import request, response, Bottle


class ServerState(Enum):
    """"
    When a new Dota game starts, settings should be loaded from the /api/settings route before
    game state updates are processed. The server therefore starts in the SETTINGS state
    and only moves to the UPDATE state once the settings have been sent. In the UPDATE state the
    server is allowed to update the game state and run the bot AI.

    HTTP requests from Dota have very long timeouts and are buffered within the game even when this
    server is turned off (the API supposedly supports lowering these timeouts but experimentation
    has shown these to have no effect).

    Restarting the server on the same port and starting a new Dota game can lead to game updates
    from the previous game being received by the server before the settings are requested for the
    new game. By using this state machine, we avoid having to fully restart Dota between matches
    to flush old updates.
    """
    SETTINGS = auto()
    UPDATE = auto()


def setup_web_server(settings_filename, radiant_bot_framework, dire_bot_framework) -> Bottle:
    """Defines the web server routes and return the Bottle app instance."""
    app = Bottle()
    state = ServerState.SETTINGS

    @app.get("/api/settings")
    def settings():
        nonlocal state

        if state != ServerState.SETTINGS:
            response.status = 406
            return {'status:': 'error', 'message': 'invalid server state in settings'}

        r_party = radiant_bot_framework.get_party()
        d_party = dire_bot_framework.get_party()
        with open(settings_filename) as f:
            user_settings = json.loads(f.read())

        user_settings['radiant_party_names'] = r_party
        user_settings['dire_party_names'] = d_party

        state = ServerState.UPDATE
        return json.dumps(user_settings)

    @app.post("/api/game_ended")
    def game_ended():
        return {'status': 'ok', 'message': 'not implemented'}

    @app.post("/api/update")
    def update():
        return update_game_state(radiant_bot_framework, state)

    @app.post("/api/radiant_update")
    def radiant_update():
        return update_game_state(radiant_bot_framework, state)

    @app.post("/api/dire_update")
    def dire_update():
        return update_game_state(dire_bot_framework, state)

    return app


def update_game_state(bot_framework, state):
    if state != ServerState.UPDATE:
        response.status = 406
        return {'status:': 'error', 'message': 'invalid server state in update game state'}

    if request.content_type != 'application/json':
        response.status = 415
        return {'status': 'error', 'message': 'This API only understands JSON'}

    # If the JSON document is large (bigger than the Bottle constant MEMFILE_MAX) then
    # requests.json will contain the json as a string and we need a separate parsing step.
    # Otherwise request.json will already have parsed the JSON into a dict.
    raw_json = request.json
    parsed_json = json.loads(raw_json) if type(raw_json) == str else raw_json

    bot_framework.update(parsed_json)
    bot_framework.generate_bot_commands()
    commands = bot_framework.receive_bot_commands()
    return json.dumps(commands)


