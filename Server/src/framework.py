import json

from bot_framework import BotFramework
from framework_util import exit_with_error, load_class, BotClassError
from webserver import setup_web_server
from pathlib import Path

RADIANT_TEAM = 2
DIRE_TEAM = 3
settings_directory = Path(__file__).parent.parent
settings_filename = settings_directory / 'settings.json'

if __name__ == '__main__':
    try:
        with open(settings_filename) as f:
            settings = json.loads(f.read())

        base_dir = settings['base_dir_bots']
        radiant_bot_filename = settings['radiant_bot_filename']
        radiant_bot_class_name = settings['radiant_bot_class_name']
        dire_bot_filename = settings['dire_bot_filename']
        dire_bot_class_name = settings['dire_bot_class_name']
        difficulty = settings['native_bots_difficulty']
        number_of_games = settings['number_of_games']

        radiant_bot = load_class(base_dir, radiant_bot_filename, radiant_bot_class_name)
        dire_bot = load_class(base_dir, dire_bot_filename, dire_bot_class_name)

        radiant_bot_framework = BotFramework(radiant_bot, RADIANT_TEAM)
        dire_bot_framework = BotFramework(dire_bot, DIRE_TEAM)
        webserver = setup_web_server(settings_filename, radiant_bot_framework, dire_bot_framework, number_of_games)
        webserver.run(server='waitress', host="localhost", port=8080, debug=False, quiet=False)
        webserver.close()
    except FileNotFoundError as fe:
        exit_with_error(f"Couldn't open {settings_filename}.")
    except json.decoder.JSONDecodeError:
        exit_with_error(f"Malformed JSON file: {settings_filename}")
    except KeyError as key_error:
        exit_with_error(f"Couldn't open required key from {settings_filename}: {key_error}")
    except BotClassError as bot_error:
        exit_with_error(f"Couldn't import the bot class: {bot_error}")