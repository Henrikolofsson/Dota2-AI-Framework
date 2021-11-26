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

    def __init__(self, world: World):
        self.world = world
        self.party = party[world.get_team()]
        print('Loaded CourierBot')

    def get_party(self) -> list[str]:
        return self.party

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self.heroes = heroes

    def actions(self, hero: PlayerHero, game_ticks: int) -> None:
        if self.world.get_game_ticks() == 5:
            tower = self.world.get_unit_by_name('dota_goodguys_tower2_bot')
            tower_pos = tower.get_position()
            hero.move(tower_pos.x, tower_pos.y, tower_pos.z)

        if self.world.get_game_ticks() == 10:
            tower = self.world.get_unit_by_name('dota_goodguys_tower2_bot')
            tower_pos = tower.get_position()
            hero.courier_move_to_position(tower_pos.x, tower_pos.y, tower_pos.z)

        if self.world.get_game_ticks() == 50:
            hero.buy("item_clarity")

        if self.world.get_game_ticks() == 60:
            hero.courier_transfer_items()



