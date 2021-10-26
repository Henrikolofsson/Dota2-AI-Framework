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


class CourierBot(BaseBot):
    """This bot does nothing for 30 game ticks, then moves the couriers to the heroes."""
    heroes: list[PlayerHero]
    world: World

    def __init__(self, world: World, team):
        self.world = world
        self.party = party[team]
        print('Loaded CourierBot')

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self.heroes = heroes

    def actions(self, hero: PlayerHero) -> None:
        if self.world.get_game_ticks() == 30 and hero.get_name() == "npc_dota_hero_bane":
            print(f'issued move_to_hero for hero: {hero}')
            hero.courier_move_to_hero()

        if self.world.get_game_ticks() == 60 and hero.get_name() == "npc_dota_hero_bane":
            print(f'issued retrieve for hero: {hero}')
            hero.courier_retrieve()

        if self.world.get_game_ticks() == 100 and hero.get_name() == "npc_dota_hero_bane":
            print(f'issued move_to_hero for hero: {hero}')
            hero.courier_move_to_hero()

        if self.world.get_game_ticks() == 150 and hero.get_name() == "npc_dota_hero_bane":
            print(f'issued retrieve for hero: {hero}')
            hero.courier_retrieve()
