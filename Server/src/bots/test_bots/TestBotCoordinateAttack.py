from game.ability import Ability
from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM
from random import Random

party = {
    RADIANT_TEAM: [
        "npc_dota_hero_brewmaster",
        "npc_dota_hero_doom_bringer",
        "npc_dota_hero_abyssal_underlord",
        "npc_dota_hero_beastmaster",
        "npc_dota_hero_axe",
    ],
    DIRE_TEAM: [
        "npc_dota_hero_bane",
        "npc_dota_hero_batrider",
        "npc_dota_hero_dazzle",
        "npc_dota_hero_wisp",
        "npc_dota_hero_lich",
    ],
}

class TestBotCoordinateAttack(BaseBot):

    '''
    Tests:
    - Move group of heroes to river to surround a dire hero
    - Use attacks in synch to test coordination
    '''

    _world: World
    _party: list[str]
    _heroes: list[PlayerHero]
    _hero_information: dict
    _abilities_leveled: bool
    _abilities: list[Ability]

    def __init__(self, world: World) -> None:
        self._world = world
        self._party = party[world.get_team()]
        self._abilities_leveled = False
        self._hero_information = {
            "npc_dota_hero_brewmaster" : {
                "x": 1800,
                "y": -2200,
                "ability_leveled" : False
            },
            "npc_dota_hero_doom_bringer" : {
                "x": 2000,
                "y": -1800,
                "ability_leveled" : False
            },
            "npc_dota_hero_abyssal_underlord" : {
                "x": 2200,
                "y": -2000,
                "ability_leveled" : False
            },
            "npc_dota_hero_beastmaster" : {
                "x": 2000,
                "y": -2300,
                "ability_leveled" : False
            },
            "npc_dota_hero_axe" : {
                "x": 1800,
                "y": -1800,
                "ability_leveled" : False
            }
        }

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        if game_ticks >= 15:
            if hero.get_name() == "npc_dota_hero_bane":
                self._move_dire_to_river(hero)
            if hero.get_team() == 2:
                if not self._move_hero_to_position(hero):
                    self._abilities = hero.get_abilities()
                    #Ability behaviour 4: Self targeting
                    #Ability Behaviour 8: Unit Target
                    #Ability Behaviour 48: Point & AOE
                    if self._abilities[1].get_behavior() == 4: 
                         hero.cast(1)
                    elif self._abilities[1].get_behavior() == 8:
                         hero.cast(1, self._world.get_unit_by_name("npc_dota_hero_bane").get_id())
                    elif self._abilities[1].get_behavior() == 48:
                        hero.cast_target_point(1, self._world.get_unit_by_name("npc_dota_hero_bane").get_position())
                if self._hero_information[hero.get_name()]["ability_leveled"] is False:
                    hero.level_up(1)
                    self._hero_information[hero.get_name()]["ability_leveled"] = True                

                
    def _move_dire_to_river(self, hero: PlayerHero) -> None:
        if hero.get_position().x > 2010 and hero.get_position().y > -2105:
                hero.move(2000, -2100, 0)

    def _move_hero_to_position(self, hero: PlayerHero) -> bool:
        if hero.get_position().x != self._hero_information[hero.get_name()]["x"]:
            if hero.get_position().y != self._hero_information[hero.get_name()]["y"]:
                hero.move(self._hero_information[hero.get_name()]["x"], self._hero_information[hero.get_name()]["y"], 0)
                return True
        return False
