import random
import datetime
from game.position import Position
from game.ability import Ability
from game.enums.ability_behavior import AbilityBehavior
from game.player_hero import PlayerHero
from game.world import World

from base_bot import BaseBot
from game.building import Building


class BotExampleDire(BaseBot):

    world: World

    def __init__(self, world: World, team: int):
        self._party = [
            "npc_dota_hero_bane",
            "npc_dota_hero_batrider",
            "npc_dota_hero_dazzle",
            "npc_dota_hero_wisp",
            "npc_dota_hero_lich",
        ]
        self.hero_position = {
            "npc_dota_hero_bane": "MID",
            "npc_dota_hero_batrider": "TOP",
            "npc_dota_hero_dazzle": "TOP",
            "npc_dota_hero_wisp": "BOT",
            "npc_dota_hero_lich": "BOT"
        }
        self.hero_position_original = self.hero_position.copy()
        self.reset_lane_timer = datetime.datetime.now()
        self.world = world

        print("init")

    def get_party(self) -> list[str]:
        return self._party

    def initialize(self, heroes):
        self.top_fallback_point = self.world.get_unit_by_name(
            "dota_badguys_tower1_top").get_position().to_list()
        self.mid_fallback_point = self.world.get_unit_by_name(
            "dota_badguys_tower1_mid").get_position().to_list()
        self.bot_fallback_point = self.world.get_unit_by_name(
            "dota_badguys_tower1_bot").get_position().to_list()

        print("initialize")

    def actions(self, hero: PlayerHero):

        print("actions!" + hero.get_name())
        if not hero.is_alive():
            return

        if self.world.get_game_ticks() < 5:
            hero.move(-6826, -7261, 256)
            return

        if self.world.get_game_ticks() == 5:
            self.buy_ring_of_regen(hero)
            return

        if hero.get_ability_points() > 0:
            hero.level_up(random.randint(0, 4))
            return

        self.decide_lane()
        fallback_point = self.get_hero_fallback_point(hero)
        if self.flee_if_tower_aggro(hero, fallback_point):
            return
        self.push_lane(
            hero,
            fallback_point)

    def decide_lane(self):
        last_reset = (datetime.datetime.now() - self.reset_lane_timer).seconds
        heroes = self.world.get_player_heroes()
        lane = None
        lane_deaths = -1
        for hero in heroes:
            if hero.get_deaths() > lane_deaths:
                lane_deaths = hero.get_deaths()
                lane = self.hero_position[hero.get_name()]

        if last_reset > 300 and self.hero_position != self.hero_position_original:
            print("Resetting hero lanes")
            self.hero_position = self.hero_position_original.copy()
        elif last_reset > 300 and lane_deaths % 5 == 0:
            self.reset_lane_timer = datetime.datetime.now()
            print("Heros are pushing {}".format(lane))
            for hero in self.hero_position:
                self.hero_position[hero] = lane

    def buy_healing_salve(self, hero: PlayerHero):
        if hero.get_gold() > 110:
            pass

    def buy_ring_of_regen(self, hero: PlayerHero):
        hero.buy("item_ring_of_regen")

    def attack_anything_if_in_range(self, hero: PlayerHero):
        enemies = self.world.get_enemies_in_attack_range_of(hero)
        if enemies:
            target = random.choice(enemies)
            hero.attack(target.get_id())
            return True
        return False

    def attack_building_if_in_range(self, hero: PlayerHero):
        if bool(random.getrandbits(1)):
            self.use_ability_on_enemy(hero)
            if hero._command:
                return True
        enemies = self.world.get_enemies_in_range_of(hero, 700)
        enemies = [e for e in enemies if isinstance(e, Building)]
        if enemies:
            target = enemies[0]
            hero.attack(target.get_id())
            return True
        return False

    def attack_unit_if_in_range(self, hero: PlayerHero):
        if bool(random.getrandbits(1)):
            self.use_ability_on_enemy(hero)
            if hero._command:
                return True

        enemies = self.world.get_enemies_in_range_of(hero, 500)
        enemies = [e for e in enemies if not isinstance(e, Building)]
        if enemies:
            target = random.choice(enemies)
            hero.attack(target.get_id())
            return True
        return False

    def use_ability_on_enemy(self, hero: PlayerHero):
        abilities: list[Ability] = []

        for ability in hero.get_abilities():
            if ability.get_level() < 1:
                continue
            if ability.get_ability_damage_type(
            ) == AbilityBehavior.POINT:
                continue
            if ability.get_cooldown_time_remaining() > 0:
                continue
            abilities.append(ability)

        if not abilities:
            print("No abilities for" + hero.get_name())
            return

        enemies = self.world.get_enemies_in_range_of(hero, 500)
        if not enemies:
            return

        ability = random.choice(abilities)
        enemy = random.choice(enemies)

        if (ability.get_behavior()
                & AbilityBehavior.UNIT_TARGET.value) > 0:
            hero.cast(ability.get_ability_index(),
                      target_id=enemy.get_id())
        else:
            hero.cast(ability.get_ability_index(), position=enemy.get_position().to_list())

    def push_lane(self, hero: PlayerHero, fallback_position):
        hero.fallback_position = fallback_position

        if not hasattr(hero, "in_lane"):
            hero.in_lane = False

        if not hasattr(hero, "follow_creeps"):
            hero.follow_creeps = []

        if not hasattr(hero, "has_creep_group"):
            hero.has_creep_group = False

        if not hero.in_lane:
            hero.move(*hero.fallback_position)
            if self.world.get_distance_between_positions(hero.get_position(),
                                           Position(*hero.fallback_position)) < 300:
                hero.in_lane = True
            return

        for creep in hero.follow_creeps:
            if creep.get_id() and creep.is_alive():
                continue
            hero.follow_creeps.remove(creep)

        if hero.has_creep_group and len(hero.follow_creeps) > 1:
            if self.attack_building_if_in_range(
                    hero) or self.attack_unit_if_in_range(hero):
                return
            self.follow_unit(hero, hero.follow_creeps[0])
        elif hero.has_creep_group and len(hero.follow_creeps) <= 1:
            hero.has_creep_group = False
            hero.follow_creeps = []
        elif not hero.has_creep_group:
            follow_creeps = self.get_closes_creep_group(hero)
            if follow_creeps:
                hero.follow_creeps = follow_creeps
                hero.has_creep_group = True
            else:
                hero.move(*hero.fallback_position)

    def flee_if_tower_aggro(self, hero: PlayerHero, safepoint):
        if hero.get_has_tower_aggro():
            hero.move(*safepoint)
            return True
        return False

    def close_friendly_creeps(self, hero: PlayerHero):
        creeps = self.world.get_allied_creeps_of(hero)
        close_creeps = []
        for c in creeps:
            if self.world.get_distance_between_units(c, hero) < 1000:
                close_creeps.append(c)
        return close_creeps

    def get_hero_fallback_point(self, hero: PlayerHero):
        hero_name = hero.get_name()
        fallback_point = None
        if self.hero_position[hero_name] == "TOP":
            fallback_point = self.top_fallback_point
        elif self.hero_position[hero_name] == "MID":
            fallback_point = self.mid_fallback_point
        elif self.hero_position[hero_name] == "BOT":
            fallback_point = self.bot_fallback_point
        return fallback_point

    def get_closes_creep_group(self, hero):
        creep_group = []
        friendly_creeps = self.world.get_allied_creeps_of(hero)
        creeps_by_distance = {}
        for creep in friendly_creeps:
            distance = self.world.get_distance_between_units(hero, creep)
            creeps_by_distance[distance] = creep

        if not creeps_by_distance:
            return creep_group

        closest_creep_distance = min(creeps_by_distance.keys())
        closest_creep = creeps_by_distance[closest_creep_distance]
        if closest_creep_distance > 700:
            return creep_group

        creeps_by_distance = {}
        for creep in friendly_creeps:
            if creep == closest_creep:
                continue
            distance = self.world.get_distance_between_units(closest_creep, creep)
            creeps_by_distance[distance] = creep

        creep_group.append(closest_creep)
        for distance in sorted(creeps_by_distance.keys())[:3]:
            creep_group.append(creeps_by_distance[distance])

        return creep_group

    def follow_unit(self, hero, unit):
        hero.move(*unit.getOrigin())
