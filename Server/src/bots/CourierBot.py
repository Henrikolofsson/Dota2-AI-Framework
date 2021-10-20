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
        print(self.party)

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self.heroes = heroes

    def actions(self, hero: PlayerHero) -> None:
        # Only issue move command to courier on this specific game tick to
        # see how it behaves if the command is not continuously issued.
        if self.world.get_game_ticks() == 30:
            print(f'moved courier to {hero}')
            # hero.move_courier_to_hero()
            pass
        