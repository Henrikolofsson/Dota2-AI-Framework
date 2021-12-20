from game.ability import Ability
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_puck",
        "npc_dota_hero_pudge",
        "npc_dota_hero_pugna",
        "npc_dota_hero_queenofpain",
        "npc_dota_hero_razor",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_warlock",
        "npc_dota_hero_weaver",
        "npc_dota_hero_windrunner",
        "npc_dota_hero_winter_wyvern",
        "npc_dota_hero_witch_doctor",
    ],
}

class TestBotBasicSmart(BaseBot):
    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]

    def __init__(self, world: World) -> None:
        self._world = world
        self._party = party[world.get_team()]

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes