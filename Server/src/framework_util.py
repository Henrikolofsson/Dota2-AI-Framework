import importlib
import sys

from typing import Any

class BotClassError(Exception):
    pass


def load_class(path: str, filename: str, class_name: str) -> Any:
    """Loads a class, 'class_name' from 'path/filename'. The function
    returns the class as a value, not an instance of that class."""
    try:
        # It's intuitive to write path using slashes but import_module expects dots.
        dir_with_bots = path.replace('/', '.')
        filename_without_py = filename[:-3] if filename[-3:] == '.py' else filename
        module = importlib.import_module(dir_with_bots + filename_without_py)
        bot_cls = getattr(module, class_name)
        return bot_cls
    except ModuleNotFoundError as moduleError:
        raise BotClassError(moduleError)


def exit_with_error(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)
