from typing import Union
from game.enums.ability_behavior import AbilityBehavior
from game.courier import Courier
from game.ability import Ability
from game.hero import Hero
from game.position import Position
from game.unit import Unit
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

home_position = {
    RADIANT_TEAM: Position(-6774, -6311, 256),
    DIRE_TEAM: Position(6910, 6200, 256),
}

secret_shop_position = {
    RADIANT_TEAM: Position(-5077, 1893, 256),
    DIRE_TEAM: Position(4875, -1286, 256),
}

class TestBotBasicSmart(BaseBot):
    '''
    Tests:
    
    Basic AI.
    - Heroes buy boots of speed at game start.
    - Heroes level up abilities. Will prioritize ultimates.
    - Heroes moves home when hp is less than 30 % of max hp.
    - Heroes moves back to fight when hp is greater than 90 % of max hp.
    - Heroes use town portal scroll to teleport to lane if at home, hp greater than 90 % of max hp and scroll is available.
    - Heroes attack enemy hero if enemy hero has less than 65 % of max hp. Will prioritize casting spells before normal attack.
    - Heroes attempt to get last hits and denies.
    - Heroes "hard"-flee when attacked by tower.
    - Heroes "soft"-flee when attacked by creeps or heroes.
    - Puck, Pugna, Razor, Warlock, Weaver, Winter Wyvern and Witch Doctor buy energy booster using courier which delivers it to the hero to create arcane boots.
    - Puck, Pugna, Razor, Warlock, Weaver, Winter Wyvern and Witch Doctor use arcane boots when they've lost 175 mana or more.
    - Pudge, Razor and Windrunner buy blades of attack and chainmail using courier which delivers it to the hero to create phase boots.
    - Pudge, Razor and Windrunner use phase boots whenever possible.
    '''
    
    _world: World
    _team: int
    party: list[str]
    _heroes: list[PlayerHero]
    _should_move_home: dict[str, bool]
    _home_position: Position
    _secret_shop_position: Position
    _lane_tower_positions: dict[str, Position]
    _courier_moving_to_secret_shop: dict[str, bool]
    _courier_transferring_items: dict[str, bool]

    def __init__(self, world: World, team: int) -> None:
        self._world = world
        self._team = team
        self.party = party[team]
        self._should_move_home = {}
        self._home_position = home_position[team]
        self._secret_shop_position = secret_shop_position[team]
        self._lane_tower_positions = {}
        self._courier_moving_to_secret_shop = {}
        self._courier_transferring_items = {}

    def initialize(self, heroes: list[PlayerHero]) -> None:
        self._heroes = heroes
        for hero in heroes:
            self._should_move_home[hero.get_name()] = False
            self._courier_moving_to_secret_shop[hero.get_name()] = False
            self._courier_transferring_items[hero.get_name()] = False

    def actions(self, hero: PlayerHero) -> None:
        if self._world.get_game_ticks() == 1 and not self._lane_tower_positions:
            for lane_tower_name in [
                "dota_goodguys_tower1_top",
                "dota_goodguys_tower1_mid",
                "dota_goodguys_tower1_bot",
                "dota_badguys_tower1_top",
                "dota_badguys_tower1_mid",
                "dota_badguys_tower1_bot",
            ]:
                tower: Union[Unit, None] = self._world.get_unit_by_name(lane_tower_name)
                if tower is not None:
                    self._lane_tower_positions[lane_tower_name] = tower.get_position()

        if self._world.get_game_ticks() == 1:
            hero.buy("item_boots")
            return

        if self.get_better_boots(hero):
            return
        
        if self.use_arcane_boots(hero):
            return

        if self.use_phase_boots(hero):
            return

        self.make_choice(hero)

    def make_choice(self, hero: PlayerHero) -> None:
        if self.level_up_ability(hero):
            return

        if self.hero_name_match_any(hero, ["puck", "pudge"]):
            self.push_lane(hero, "dota_goodguys_tower1_top")

        elif self.hero_name_match_any(hero, ["pugna"]):
            self.push_lane(hero, "dota_goodguys_tower1_mid")

        elif self.hero_name_match_any(hero, ["queenofpain", "razor"]):
            self.push_lane(hero, "dota_goodguys_tower1_bot")

        elif self.hero_name_match_any(hero, ["warlock", "weaver"]):
            self.push_lane(hero, "dota_badguys_tower1_top")

        elif self.hero_name_match_any(hero, ["windrunner"]):
            self.push_lane(hero, "dota_badguys_tower1_mid")

        elif self.hero_name_match_any(hero, ["winter_wyvern", "witch_doctor"]):
            self.push_lane(hero, "dota_badguys_tower1_bot")

    def hero_name_match_any(self, hero: PlayerHero, matches: list[str]) -> bool:
        for match in matches:
            if hero.get_name() == "npc_dota_hero_" + match:
                return True
        return False

    def level_up_ability(self, hero: PlayerHero) -> bool:
        if hero.get_ability_points() > 0:
            if self.level_up_ultimate(hero):
                return True

            for ability in hero.get_abilities():
                if ability.get_level() < ability.get_max_level() \
                and hero.get_level() >= ability.get_hero_level_required_to_level_up():
                    hero.level_up(ability.get_ability_index())
                    return True

        return False

    def level_up_ultimate(self, hero: PlayerHero) -> bool:
        for ability in hero.get_abilities():
            level_required = ability.get_hero_level_required_to_level_up()
            if (level_required == 6 or level_required == 12 or level_required == 18) \
            and ability.get_level() < ability.get_max_level() \
            and hero.get_level() >= level_required:
                hero.level_up(ability.get_ability_index())
                return True

        return False

    def use_arcane_boots(self, hero: PlayerHero) -> bool:
        if self.has_arcane_boots(hero) \
        and hero.get_max_mana() - hero.get_mana() >= 175:
            for item in hero.get_items():
                if item.get_name() == "item_arcane_boots" \
                and item.get_cooldown_time_remaining() == 0:
                    hero.use_item(item.get_slot())
                    return True

        return False

    def use_phase_boots(self, hero: PlayerHero) -> bool:
        if self.has_phase_boots(hero):
            for item in hero.get_items():
                if item.get_name() == "item_phase_boots" \
                and item.get_cooldown_time_remaining() == 0:
                    hero.use_item(item.get_slot())
                    return True

        return False

    def has_boots(self, hero: PlayerHero) -> bool:
        for item in hero.get_items():
            if item.get_name() == "item_boots":
                return True
        return False

    def get_better_boots(self, hero: PlayerHero) -> bool:
        if self.hero_name_match_any(hero, ["puck", "pugna", "queenofpain", "warlock", "weaver", "winter_wyvern", "witch_doctor"]):
            if self.has_boots(hero):
                return self.get_arcane_boots(hero)
        
        if self.hero_name_match_any(hero, ["pudge", "razor", "windrunner"]):
            if self.has_boots(hero):
                return self.get_phase_boots(hero)

        return False

    def get_arcane_boots(self, hero: PlayerHero) -> bool:
        if not self.courier_has_energy_booster(hero) and hero.get_gold() < 800 or self.courier_is_dead(hero):
            return False
        
        if not self.courier_has_energy_booster(hero) and self._world.get_distance_between_positions(self.get_courier_position(hero), self._secret_shop_position) < 500:
            hero.buy("item_energy_booster")
            return True

        if self.courier_has_energy_booster(hero) and not self._courier_transferring_items[hero.get_name()]:
            hero.courier_transfer_items()
            self._courier_transferring_items[hero.get_name()] = True
            self._courier_moving_to_secret_shop[hero.get_name()] = False
            return True

        if not self.courier_has_energy_booster(hero) and not self._courier_moving_to_secret_shop[hero.get_name()]:
            hero.courier_secret_shop()
            self._courier_moving_to_secret_shop[hero.get_name()] = True
            return True

        return False

    def get_phase_boots(self, hero: PlayerHero) -> bool:
        if self.courier_is_dead(hero):
            return False

        if not self.courier_has_blades_of_attack(hero) and hero.get_gold() >= 450:
            hero.buy("item_blades_of_attack")
            return True

        if not self.courier_has_chainmail(hero) and hero.get_gold() >= 550:
            hero.buy("item_chainmail")
            return True

        if self.courier_has_blades_of_attack(hero) and self.courier_has_chainmail(hero) and not self._courier_transferring_items[hero.get_name()]:
            hero.courier_transfer_items()
            self._courier_transferring_items[hero.get_name()] = True
            return True

        return False

    def courier_is_dead(self, hero: PlayerHero) -> bool:
        return self._world.get_entity_by_id(hero.get_courier_id()) is None

    def has_arcane_boots(self, hero: PlayerHero) -> bool:
        for item in hero.get_items():
            if item.get_name() == "item_arcane_boots":
                return True
        return False

    def has_phase_boots(self, hero: PlayerHero) -> bool:
        for item in hero.get_items():
            if item.get_name() == "item_phase_boots":
                return True
        return False

    def courier_has_energy_booster(self, hero: PlayerHero) -> bool:
        courier = self._world.get_entity_by_id(hero.get_courier_id())

        if isinstance(courier, Courier):
            for item in courier.get_items():
                if item.get_name() == "item_energy_booster":
                    return True
        return False

    def courier_has_blades_of_attack(self, hero: PlayerHero) -> bool:
        courier = self._world.get_entity_by_id(hero.get_courier_id())

        if isinstance(courier, Courier):
            for item in courier.get_items():
                if item.get_name() == "item_blades_of_attack":
                    return True
        return False

    def courier_has_chainmail(self, hero: PlayerHero) -> bool:
        courier = self._world.get_entity_by_id(hero.get_courier_id())

        if isinstance(courier, Courier):
            for item in courier.get_items():
                if item.get_name() == "item_chainmail":
                    return True
        return False

    def get_courier_position(self, hero: PlayerHero) -> Position:
        courier = self._world.get_entity_by_id(hero.get_courier_id())
        assert courier is not None
        return courier.get_position()

    def push_lane(self, hero: PlayerHero, lane_tower_name: str) -> None:
        lane_tower_position: Position = self._lane_tower_positions[lane_tower_name]


        if hero.get_health() > 0.90 * hero.get_max_health():
            self._should_move_home[hero.get_name()] = False
            if self._world.get_distance_between_positions(hero.get_position(), self._home_position) < 1250:
                if hero.use_tp_scroll(lane_tower_position):
                    return
        elif hero.get_health() < 0.30 * hero.get_max_health():
            self._should_move_home[hero.get_name()] = True

        if self._should_move_home[hero.get_name()]:
            hero.move(*self._home_position)
            return


        if self.is_near_allied_creeps(hero) and not hero.get_has_tower_aggro():
            enemy_hero_to_attack: Union[Hero, None] = self.get_enemy_hero_to_attack(hero)
            creep_to_last_hit: Union[Unit, None] = self.get_creep_to_last_hit(hero)
            creep_to_deny: Union[Unit, None] = self.get_creep_to_deny(hero)
            if enemy_hero_to_attack is not None\
            and (
                enemy_hero_to_attack.get_health() < 0.65 * enemy_hero_to_attack.get_max_health() or\
                hero.get_mana() == hero.get_max_mana()
            ):
                ability: Union[Ability, None] = self.get_ability_to_cast(hero)
                if ability is not None:
                    behavior: int = ability.get_behavior()
                    if behavior & AbilityBehavior.UNIT_TARGET.value:
                        hero.cast_target_unit(ability.get_ability_index(), enemy_hero_to_attack.get_id())
                    elif behavior & AbilityBehavior.NO_TARGET.value:
                        hero.cast_no_target(ability.get_ability_index())
                    elif behavior & AbilityBehavior.AOE.value:
                        hero.cast_target_area(ability.get_ability_index(), enemy_hero_to_attack.get_position())
                    elif behavior & AbilityBehavior.POINT.value:
                        hero.cast_target_point(ability.get_ability_index(), enemy_hero_to_attack.get_position())
                    elif behavior & AbilityBehavior.CHANNELLED.value:
                        hero.cast(
                            ability_index=ability.get_ability_index(),
                            target_id=enemy_hero_to_attack.get_id(),
                            position=enemy_hero_to_attack.get_position(),
                        )
                else:
                    hero.attack(enemy_hero_to_attack.get_id())

            elif creep_to_last_hit is not None:
                hero.attack(creep_to_last_hit.get_id())
            elif creep_to_deny is not None:
                hero.attack(creep_to_deny.get_id())
            elif hero.get_has_aggro():
                hero.move(*lane_tower_position)
            elif enemy_hero_to_attack is not None:
                hero.attack(enemy_hero_to_attack.get_id())
            elif self.should_move_closer_to_allied_creeps(hero):
                self.follow(hero, self.get_closest_allied_creep(hero))
            else:
                hero.stop()
        else:
            hero.move(*lane_tower_position)

    def follow(self, hero: PlayerHero, to_follow: Unit) -> None:
        hero.move(*to_follow.get_position())

    def get_ability_to_cast(self, hero: PlayerHero) -> Union[Ability, None]:
        for i in range(4):
            ability: Ability = hero.get_abilities()[i]
            behavior: int = ability.get_behavior()
            if ability.get_level() > 0 \
            and ability.get_cooldown_time_remaining() == 0 \
            and (
                behavior & AbilityBehavior.UNIT_TARGET.value or\
                behavior & AbilityBehavior.NO_TARGET.value or\
                behavior & AbilityBehavior.AOE.value or\
                behavior & AbilityBehavior.POINT.value or\
                behavior & AbilityBehavior.CHANNELLED.value
            ) \
            and ability.get_mana_cost() <= hero.get_mana():
                return ability

    def should_move_closer_to_allied_creeps(self, hero: PlayerHero) -> bool:
        return not self._world.get_enemies_in_range_of(hero, 575)

    def get_creep_to_deny(self, hero: PlayerHero) -> Union[Unit, None]:
        closest_allied_creeps = self.get_closest_allied_creeps(hero)

        closest_allied_creeps.sort(key=lambda creep: self._world.get_distance_between_units(hero, creep))

        for creep in closest_allied_creeps:
            if creep.is_deniable() and creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def get_closest_allied_creeps(self, hero: PlayerHero) -> list[Unit]:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_allied_creeps: list[Unit] = []

        for creep in creeps:
            if self._world.get_distance_between_units(hero, creep) < 600:
                close_allied_creeps.append(creep)

        return close_allied_creeps

    def get_enemy_hero_to_attack(self, hero: PlayerHero) -> Union[Hero, None]:
        enemy_heroes: list[Hero] = self.get_closest_enemy_heroes(hero)
        heroes_with_hp: dict[Hero, int] = {}

        for enemy_hero in enemy_heroes:
            heroes_with_hp[enemy_hero] = enemy_hero.get_health()

        if len(heroes_with_hp) == 0:
            return

        return min(heroes_with_hp.keys(), key=(lambda enemy_hero: heroes_with_hp[enemy_hero]))
        
    def get_closest_enemy_heroes(self, hero: PlayerHero) -> list[Hero]:
        enemy_heroes: list[Hero] = self._world.get_enemy_heroes_of(hero)
        close_enemy_heroes: list[Hero] = []

        for enemy_hero in enemy_heroes:
            if self._world.get_distance_between_units(hero, enemy_hero) < 1250:
                close_enemy_heroes.append(enemy_hero)

        return close_enemy_heroes

    def get_creep_to_last_hit(self, hero: PlayerHero) -> Union[Unit, None]:
        closest_enemy_creeps = self.get_closest_enemy_creeps(hero)

        for creep in closest_enemy_creeps:
            if creep.get_health() < hero.get_attack_damage() + 40:
                return creep

    def is_near_allied_creeps(self, hero: PlayerHero) -> bool:
        allied_creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        close_allies: list[Unit] = self._world.get_allies_in_range_of(hero, 750)

        for ally in close_allies:
            if ally in allied_creeps:
                return True
        return False

    def get_closest_enemy_creeps(self, hero: PlayerHero) -> list[Unit]:
        creeps: list[Unit] = self._world.get_enemy_creeps_of(hero)
        close_enemy_creeps: list[Unit] = []

        for creep in creeps:
            if self._world.get_distance_between_units(hero, creep) < 500 or self._world.get_distance_between_units(hero, creep) < hero.get_attack_range():
                close_enemy_creeps.append(creep)

        return close_enemy_creeps

    def get_closest_allied_creep(self, hero: PlayerHero) -> Unit:
        creeps: list[Unit] = self._world.get_allied_creeps_of(hero)
        creeps_with_distance_to_hero: dict[Unit, float] = {}

        for allied_creep in creeps:
            creeps_with_distance_to_hero[allied_creep] = self._world.get_distance_between_units(hero, allied_creep)

        return min(creeps_with_distance_to_hero.keys(), key=(lambda allied_creep: creeps_with_distance_to_hero[allied_creep]))