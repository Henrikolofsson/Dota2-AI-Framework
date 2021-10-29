from base_bot import BaseBot
from game.player_hero import PlayerHero
from game.world import World
from framework import RADIANT_TEAM, DIRE_TEAM

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

class TestBotSkillAbilityTwiceAtStart(BaseBot):
    '''
    Tests:
    - No hero should level up ability without ability points.
    '''
    
    _world: World
    _team: int
    party: list[str]
    _heroes: list[PlayerHero]

    def __init__(self, world: World, team: int) -> None:
        self._world = world
        self._team = team
        self.party = party[team]

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes

    def actions(self, hero: PlayerHero) -> None:
        if hero.get_ability_points() >= 0:
            hero.level_up(0)