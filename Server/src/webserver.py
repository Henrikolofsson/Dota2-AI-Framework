import json

from bottle import request, response, Bottle


def setup_web_server(settings_filename, radiant_bot_framework, dire_bot_framework) -> Bottle:
    """Defines the web server routes and return the Bottle app instance."""
    app = Bottle()

    @app.get("/api/party")
    def party():
        return json.dumps(radiant_bot_framework.get_party())

    @app.get("/api/enemy_party")
    def party():
        return json.dumps([
            "npc_dota_hero_bane",
            "npc_dota_hero_batrider",
            "npc_dota_hero_dazzle",
            "npc_dota_hero_wisp",
            "npc_dota_hero_lich",
        ])

    @app.get("/api/settings")
    def settings():
        with open(settings_filename) as f:
            return f.read()

    @app.post("/api/game_ended")
    def game_ended():
        return {'status': 'ok', 'message': 'not implemented'}

    @app.post("/api/update")
    def update():
        return update_game_state(radiant_bot_framework)

    @app.post("/api/radiant_update")
    def radiant_update():
        return update_game_state(radiant_bot_framework)

    @app.post("/api/dire_update")
    def dire_update():
        return update_game_state(dire_bot_framework)

    return app


def update_game_state(bot_framework):
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
    return commands


