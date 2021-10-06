import importlib
import json
import sys
from typing import Union, Any
from library.bottle.bottle import run, post, get, request
import os
from os import path

# To run from CMD: python framework.py --bot BOTNAME --folder FOLDER_NUMBER --dif DIFFICULTY_NAME

# Possible bot names:
# BotExample
# TeamUJIDota2Bot
# FiveManMid
# NEBot

# Possible folders:
# 0
# 1
# 2
# 3

from src.BotFramework import BotFramework

FRAMEWORK: BotFramework
bot_name = "BotExample"
teamuji_folder = "competition.teamUji."
sebastian_folder = "competition.teamSebastian."
teamnebot_folder = "competition.teamNebot."
selected_folder = ""
attempt_nmb = 1
final_save_path = ""
difficulty = "easy"


def getCompetitionBot(folder_selection: str) -> str:
    switcher = {
        "0": "",
        "1": teamuji_folder,
        "2": sebastian_folder,
        "3": teamnebot_folder,
    }

    choice: Union[str, None] = switcher.get(folder_selection)

    if choice is None:
        return ""
    return choice


if len(sys.argv) > 2 and sys.argv[1] == "--bot":
    bot_name = sys.argv[2]

if len(sys.argv) > 4 and sys.argv[3] == "--folder":
    selected_folder = getCompetitionBot(sys.argv[4])
    bot_name = sys.argv[2]

if len(sys.argv) > 6 and sys.argv[5] == "--dif":
    difficulty = str(sys.argv[6])

exec("from src.bots.{1}{0} import {0}".format(bot_name, selected_folder))
exec("FRAMEWORK = BotFramework({0})".format(bot_name))


while path.exists("data/" + bot_name + "/" + difficulty + "/" + str(attempt_nmb)):
    attempt_nmb = attempt_nmb + 1

print(attempt_nmb)
print(difficulty)
final_save_path = "data/" + bot_name + "/" + difficulty + "/" + str(attempt_nmb)
print(final_save_path)
os.makedirs(final_save_path)

settings_filename = 'settings.json'


def open_bot_class(directory: str, name: str) -> Any:
    # It's intuitive to write bot path using slashes but import_module expects dots.
    dir_with_bots = directory.replace('/', '.')
    module = importlib.import_module(dir_with_bots + name)
    bot_cls = getattr(module, name)
    return bot_cls


def exit_with_error(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)


try:
    with open(settings_filename) as f:
        settings = json.loads(f.read())
        base_dir = settings['base_dir_bots']
        radiant_bot_name = settings['radiant_bot_name']
        dire_bot_name = settings['dire_bot_name']
        difficulty = settings['difficulty']

        radiant_bot = open_bot_class(base_dir, radiant_bot_name)
        dire_bot = open_bot_class(base_dir, dire_bot_name)
except FileNotFoundError:
    exit_with_error(f"Couldn't open {settings_filename}.")
except json.decoder.JSONDecodeError:
    exit_with_error(f"Malformed JSON file: {settings_filename}")
except KeyError as key_error:
    exit_with_error(f"Couldn't open required key from {settings_filename}: {key_error}")
except ModuleNotFoundError as module_error:
    exit_with_error(f"Couldn't find the module with the bot class: {module_error}")
except AttributeError as attr_error:
    exit_with_error(f"You probably gave the bot class a different name than the file "
                    f"that it's in: {attr_error}")


@get("/api/party")
def party():
    global FRAMEWORK
    return json.dumps(FRAMEWORK.get_party())


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





@post("/api/update")
def update():
    post_data = request.body.read()
    # Dump data to file
    f = open("gamedata.txt", "w+")
    f.write(post_data.decode("utf-8"))
    f.close()

    world = json.loads(post_data)

    FRAMEWORK.update(world)
    FRAMEWORK.generate_bot_commands()
    commands = FRAMEWORK.receive_bot_commands()

    return json.dumps(commands)


run(host="localhost", port=8080, debug=False, quiet=True)
