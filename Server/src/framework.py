import importlib
import json
import sys

from typing import Any

from BotFramework import BotFramework
from webserver import setup_web_server


settings_filename = '../settings.json'

def load_class(path: str, filename: str, class_name: str) -> Any:
    """Loads a class, 'class_name' from 'path/filename'. The function
    returns the class as a value, not an instance of that class."""
    # It's intuitive to write path using slashes but import_module expects dots.
    dir_with_bots = path.replace('/', '.')
    filename_without_py = filename[:-3] if filename[-3:] == '.py' else filename
    module = importlib.import_module(dir_with_bots + filename_without_py)
    bot_cls = getattr(module, class_name)
    return bot_cls


def exit_with_error(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    try:
        with open(settings_filename) as f:
            settings = json.loads(f.read())

        base_dir = settings['base_dir_bots']
        radiant_bot_filename = settings['radiant_bot_filename']
        radiant_bot_class_name = settings['radiant_bot_class_name']
        dire_bot_filename = settings['dire_bot_filename']
        dire_bot_class_name = settings['dire_bot_class_name']
        difficulty = settings['difficulty']

        radiant_bot = load_class(base_dir, radiant_bot_filename, radiant_bot_class_name)
        dire_bot = load_class(base_dir, dire_bot_filename, dire_bot_class_name)

        framework = BotFramework(radiant_bot)
        webserver = setup_web_server(framework)
        webserver.run(host="localhost", port=8080, debug=False, quiet=False)
    except FileNotFoundError as fe:
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

