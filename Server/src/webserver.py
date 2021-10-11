import json

from bottle import request, response, Bottle


def setup_web_server(settings_filename, framework) -> Bottle:
    app = Bottle()

    @app.get("/api/party")
    def party():
        return json.dumps(framework.get_party())

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

    # @post("/api/chat")
    # def chat():
    #     postdata = request.json

    #     # print(postdata)
    #     return json.dumps("ok")

    # @post("/api/game_ended")
    # def game_ended():

    #     post_data = request.body.read()
    #     # Dump data to file
    #     f = open(final_save_path + "/final_data.txt", "w+")
    #     f.write(post_data.decode("utf-8"))
    #     f.close()

    #     # postdata = request.body.read()

    #     # print(postdata)
    #     return json.dumps("ok")

    @app.post("/api/update")
    def update():
        if request.content_type != 'application/json':
            response.status = 415
            return {'status': 'error', 'message': 'This API only understands JSON'}

        # If the JSON document is large (bigger than the Bottle constant MEMFILE_MAX) then
        # requests.json will contain the json as a string and we need a separate parsing step.
        # Otherwise request.json will already have parsed the JSON into a dict.
        raw_json = request.json
        parsed_json = json.loads(raw_json) if type(raw_json) == str else raw_json

        with open("../gamedata.txt", "w+") as f:
            f.write(str(parsed_json))

        framework.update(parsed_json)
        framework.generate_bot_commands()
        commands = framework.receive_bot_commands()
        return commands
    
    return app