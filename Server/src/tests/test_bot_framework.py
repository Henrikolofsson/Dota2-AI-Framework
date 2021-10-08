import json

from importlib import import_module
from BotFramework import BotFramework


def test_update_game_state_runtime():
    """Simple test of the game state update function. Only makes sure that it doesn't cause a runtime error.
    Note: does not in any way verify that update does what it's supposed to do."""
    with open('tests/game_data.json') as f:
        data = json.loads(f.read())

    module = import_module('bots.BotExample')
    bot_cls = getattr(module, 'BotExample')
    bot_framework = BotFramework(bot_cls)
    bot_framework.update(data)


def test_fail():
    assert 1 != 2
