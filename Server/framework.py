import json
import sys
from library.bottle.bottle import run, post, get, request
import os.path
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

BOTNAME = "BotExample"
teamuji_folder = "competition.teamUji."
sebastian_folder = "competition.teamSebastian."
teamnebot_folder = "competition.teamNebot."
selected_folder = ""
ATTEMPT_NMB = 1
FINAL_SAVE_PATH = ""
DIFFICULTY = "easy"


def getCompetitionBot(folder_selection):
    switcher = {
        0: "",
        1: teamuji_folder,
        2: sebastian_folder,
        3: teamnebot_folder
    }

    return switcher.get(int(folder_selection))


if len(sys.argv) > 2 and sys.argv[1] == "--bot":
    BOTNAME = sys.argv[2]

if len(sys.argv) > 4 and sys.argv[3] == "--folder":
    selected_folder = getCompetitionBot(sys.argv[4])
    BOTNAME = sys.argv[2]

if len(sys.argv) > 6 and sys.argv[5] == "--dif":
    DIFFICULTY = str(sys.argv[6])

exec("from src.bots.{1}{0} import {0}".format(BOTNAME, selected_folder))
exec("FRAMEWORK = BotFramework({0})".format(BOTNAME))


while path.exists("data/" + BOTNAME + "/" + DIFFICULTY + "/" + str(ATTEMPT_NMB)):
    ATTEMPT_NMB = ATTEMPT_NMB + 1

print(ATTEMPT_NMB)
print(DIFFICULTY)
FINAL_SAVE_PATH = "data/" + BOTNAME + "/" + DIFFICULTY + "/" + str(ATTEMPT_NMB)
print(FINAL_SAVE_PATH)
os.makedirs(FINAL_SAVE_PATH)

@get("/api/party")
def party():
    global FRAMEWORK
    return json.dumps(FRAMEWORK.get_party())


@post("/api/chat")
def chat():
    postdata = request.body.read()

    # print(postdata)
    return json.dumps("ok")

@post("/api/game_ended")
def game_ended():

    post_data = request.body.read()
    # Dump data to file
    f = open(FINAL_SAVE_PATH + "/final_data.txt", "w+")
    f.write(post_data.decode("utf-8"))
    f.close()

    # postdata = request.body.read()

    # print(postdata)
    return json.dumps("ok")


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
