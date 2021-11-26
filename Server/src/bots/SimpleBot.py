from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_bane",
        "npc_dota_hero_batrider",
        "npc_dota_hero_dazzle",
        "npc_dota_hero_wisp",
        "npc_dota_hero_lich",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_brewmaster",
        "npc_dota_hero_doom_bringer",
        "npc_dota_hero_abyssal_underlord",
        "npc_dota_hero_beastmaster",
        "npc_dota_hero_axe",
    ]
}


class SimpleBot(BaseBot):
    """This bot moves all heroes to the center of the map."""
    heroes: list[PlayerHero]
    world: World

    def __init__(self, world: World, team: int):
        self.world = world
        self.party = party[team]
        print(self.party)

    def get_party(self) -> list[str]:
        return self.party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self.heroes = heroes

    def actions(self, hero: PlayerHero) -> None:
        hero.move(0, 0, 0)
