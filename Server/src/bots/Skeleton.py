from src.base_bot import BaseBot
from src.game.world import World
from src.game.player_hero import PlayerHero

from src.framework import DIRE_TEAM, RADIANT_TEAM


class Skeleton(BaseBot):
    """A bot inherits from BaseBot"""
    heroes: list[PlayerHero]

    def __init__(self, world: World, team: int):
        """The team parameter can be used if the bot has different behaviour depending
        on if it's a Radiant or Dire bot. Possible values are RADIANT_TEAM (2) and DIRE_TEAM (3)."""
        self.party = [
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_pudge",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_lina",
            "npc_dota_hero_chen",
        ]
        self.world = world

    def initialize(self, heroes: list[PlayerHero]):
        """This method will run once when the game is starting before the actions method
        start getting called. In this method you can setup variables and values
        that will be used later in your code.
        """
        self.heroes = heroes

    def actions(self, hero: PlayerHero):
        """This method will run once for each hero during every gametick. This is the
        starting point for your code commanding the different heroes."""
        # I'ts good to wait a few gameticks until we issue the first command
        if self.world.gameticks == 5:
            hero.move(0, 0, 256)
