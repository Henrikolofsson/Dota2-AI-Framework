import random
import os
import datetime
import time
from src.game.Building import Building
from src.game.Hero import Hero

class TeamUJIDota2Bot:

    def __init__(self, world):
        # Name of the five heros to be used
        # The list of all heros' names is at: 
        #    https://www.dota2.com/heroes/?l=english
        #    https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools/Scripting/Heroes_internal_names
        self.party = [
            "npc_dota_hero_axe",
            "npc_dota_hero_brewmaster",
            "npc_dota_hero_juggernaut",
            "npc_dota_hero_abyssal_underlord",
            "npc_dota_hero_troll_warlord"
        ]
        # Initial positions of the heros. BOT means bottom
        self.hero_position = {
            "npc_dota_hero_axe": "MID",
            "npc_dota_hero_brewmaster": "MID",
            "npc_dota_hero_juggernaut": "MID", #npc_dota_hero_snapfire
            "npc_dota_hero_abyssal_underlord": "MID",
            "npc_dota_hero_troll_warlord": "MID"
        }

        self.hero_position_original = self.hero_position.copy()
        self.reset_lane_timer = datetime.datetime.now()
        # World is the game state
        self.world = world

        print("TEAM UJI!")

    def initialize(self, heroes):
        #print("/////////////////////")
        #print("Ver 0.5,  Running away when low on hp.")


        # The place that you go back to be safe
        #Bad guys towers
        self.badguys_tower1 = self.world.find_entity_by_name(
            "dota_badguys_tower1_mid")
        self.badguys_tower2 = self.world.find_entity_by_name(
            "dota_badguys_tower2_mid")
        self.badguys_tower3 = self.world.find_entity_by_name(
            "dota_badguys_tower3_mid")

        # The name of the entities that can be searched are: ......
        self.top_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_top").getOrigin()
        self.mid_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_mid").getOrigin()
        self.bot_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_bot").getOrigin()
        self.mid_push_point1 = self.badguys_tower1.getOrigin()
        self.mid_push_point2 = self.badguys_tower2.getOrigin()
        self.mid_push_point3 = self.badguys_tower3.getOrigin()


    def actions(self, hero):
        if not hero.isAlive():
            return

        #if hero.getName() == "npc_dota_hero_axe":
        #    return

        # TODO: world coordinates
        # -6826, -7261 -> shop
        if self.world.gameticks < 5:
            hero.move(-6635, -6694, 256)
            return

        if self.world.gameticks == 5:
            if hero.getGold() >= 140:
                hero.buy("item_gauntlets") #item_boots, "item_blades_of_attack"
                #hero.buy("item_tpscroll")
                return
        # TODO where are the information of the items that can be bought: https://dota2.fandom.com/wiki/Cheats
        if self.world.gameticks == 6: #Bots start with 582 gold coins (sometimes).
            if hero.getGold() >= 140: #Depends on the speed with which they are picked, since the initial gold decreses as a penalty for not picking.
                hero.buy("item_gauntlets") #item_aguntlets adds +3 strength, thus making AA stronger.
                if hero.getName() == "npc_dota_hero_brewmaster":
                    return
                return

        if self.world.gameticks == 7:
            if hero.getGold() >= 140:
                hero.buy("item_gauntlets")
                return

        if self.world.gameticks == 8:
            if hero.getGold() >= 50:
                hero.buy("item_branches")
                return

        if self.world.gameticks == 9:
            if hero.getName() == "npc_dota_hero_brewmaster":
                items = hero.get_items()
                item_names = [n["name"] for n in items.values() if n]
                #print(*item_names)

        if hero.getOrigin()[0] < -6260 and hero.getOrigin()[1] < -5758 and (
            (hero.getGold() >= 500 and not self.check_for_item(hero, "item_boots", 1) or (hero.getGold() >= 1000 and not self.check_for_item(hero, "item_broadsword", 2)))
            ):

            items = hero.get_items()
            item_names = [n["name"] for n in items.values() if n]

            if (len(item_names) < 6):
                #print("Less than 6 items")
                if (hero.getOrigin()[0] < -6635):
                    hero.move(-6635, -6694, 256)
                    #print(hero.getName() + " is moving to shop.")
                    return
                else:
                    if not self.check_for_item(hero, "item_boots", 1):
                        #print(hero.getName() + " is trying to buy boots.")
                        hero.buy("item_boots") #item_arcane_boots
                    elif hero.getGold() >= 1000:
                        hero.buy("item_broadsword")
                    return
            else:
                if (self.check_for_item(hero, "item_branches", 1)):
                    for item in hero.get_items().values():
                        if item and item["name"] == "item_branches":
                            hero.sell(item["slot"])
                #print("more than 5 items, cant buy.")

        # Select one ability by random, except if it is an Ultimate Level (6, 12, 18), level up the ultimate; or a Tree level
        if hero.getAbilityPoints() > 0:
            #print(hero.get_items()["0"]["name"])
            if hero.getLevel() == 6 or hero.getLevel() == 12 or hero.getLevel() == 18:
                if (hero.getName() == "npc_dota_hero_abyssal_underlord"):
                    hero.level_up(random.randint(0, 2))
                    return
                hero.level_up(5)
            elif hero.getLevel() == 10 or hero.getLevel() == 15 or hero.getLevel() == 20 or hero.getLevel() == 25:
                hero.level_up(14)
            else:
                hero.level_up(random.randint(0, 2))
            return

        self.decide_lane()
        fallback_point = self.get_hero_fallback_point(hero)
        #if self.flee_if_low_health(hero, fallback_point):
        #    return
        if self.flee_if_tower_aggro(hero, fallback_point):
            return
        self.push_lane(hero, fallback_point)

    def decide_lane(self):
        last_reset = (datetime.datetime.now() - self.reset_lane_timer).seconds
        heroes = self.world._get_player_heroes()
        lane = None
        lane_deaths = -1
        for hero in heroes:
            if hero.getDeaths() > lane_deaths:
                lane_deaths = hero.getDeaths()
                lane = self.hero_position[hero.getName()]

        if last_reset > 300 and self.hero_position != self.hero_position_original:
            #print("Resetting hero lanes")
            self.hero_position = self.hero_position_original.copy()
        elif last_reset > 300 and lane_deaths % 5 == 0:
            self.reset_lane_timer = datetime.datetime.now()
            #print("Heros are pushing {}".format(lane))
            for hero in self.hero_position:
                self.hero_position[hero] = lane


    # Attacks random enemy if in range prioritizing enemy heroes
    def attack_anything_if_in_range(self, hero):
        enemies = self.world.get_enemies_in_range(hero, 500)
        if enemies:
            enemy_heroes = [e for e in enemies if isinstance(e, Hero)] # Checks enemies to see if any of them are heroes, if so then appends it to enemy_heroes
            if enemy_heroes:                        # Checks if there are any heros in range and targets it
                target = random.choice(enemy_heroes)
            else:                                   # If no hero is in range it will target a random enemy in attack range
                target = enemies[0]
            hero.attack(self.world.get_id(target))
            return True
        return False

    def attack_building_if_in_range(self, hero): #TODO check for creep group, if not, go to safe point.
        if bool(random.getrandbits(1)):
            self.use_ability_on_enemy(hero)
            if hero.command:
                return True

        enemies = self.world.get_enemies_in_range(hero, 500) #TODO test with less distance.
        if enemies:
            enemy_creeps = [e for e in enemies if not isinstance(e, (Building, Hero))] #Check if there are minions
            #If there are, attack them first,
            if enemy_creeps:
                target = enemy_creeps[0]
                hero.attack(self.world.get_id(target))
                return True
            #then proceed to attack the tower once the wave is cleared.
            else:
                enemy_building = [e for e in enemies if isinstance(e, Building)]
                if enemy_building:
                    target = enemy_building[0]
                    hero.attack(self.world.get_id(target))
                    return True

    def attack_unit_if_in_range(self, hero):
        if bool(random.getrandbits(1)):
            self.use_ability_on_enemy(hero)
            if hero.command:
                return True

        enemies = self.world.get_enemies_in_range(hero, 500)
        enemies = [e for e in enemies if not isinstance(e, Building)]
        if enemies:
            target = enemies[0]
            hero.attack(self.world.get_id(target))
            #time.sleep(2) #Adding "cooldown" to attacks, so hero doesn't change target multiple times before finishing an attack. Doesn't work with sleep().
            return True
        return False

    def use_ability_on_enemy(self, hero):
        abilities = []

        for ability in hero.getAbilities().values():
            if ability.getLevel() < 1:
                continue
            if ability.getAbilityDamageType(
            ) == ability.DOTA_ABILITY_BEHAVIOR_POINT:
                continue
            if ability.getCooldownTimeRemaining() > 0:
                continue
            abilities.append(ability)

        if not abilities:
            #print("No abilities for" + hero.getName())
            return

        enemies = self.world.get_enemies_in_range(hero, 500)
        if not enemies:
            return

        ability = random.choice(abilities)
        enemy = random.choice(enemies)

        if (ability.getBehavior()
                & ability.DOTA_ABILITY_BEHAVIOR_UNIT_TARGET) > 0:
            hero.cast(ability.getAbilityIndex(),
                      target=self.world.get_id(enemy))
        else:
            hero.cast(ability.getAbilityIndex(), position=enemy.getOrigin())

    def push_lane(self, hero, fallback_position):
        hero.fallback_position = fallback_position

        if not hasattr(hero, "in_lane"):
            hero.in_lane = False

        if not hasattr(hero, "follow_creeps"):
            hero.follow_creeps = []

        if not hasattr(hero, "has_creep_group"):
            hero.has_creep_group = False

        if not hero.in_lane:
            hero.move(*hero.fallback_position)
            if self.world.get_distance_pos(hero.getOrigin(),
                                           hero.fallback_position) < 300:
                hero.in_lane = True
            return

        for creep in hero.follow_creeps:
            if self.world.get_id(creep) and creep.isAlive():
                continue
            hero.follow_creeps.remove(creep)

        if hero.has_creep_group and len(hero.follow_creeps) > 1:
            if self.attack_building_if_in_range(hero) or self.attack_unit_if_in_range(hero):
                return
            self.follow_unit(hero, hero.follow_creeps[0])
        elif hero.has_creep_group and len(hero.follow_creeps) <= 1:
            #print("No creep group: " + hero.getName())
            hero.has_creep_group = False
            hero.follow_creeps = []
        elif not hero.has_creep_group:
            #print("Looking for creep group:" + hero.getName())
            follow_creeps = self.get_closes_creep_group(hero)
            if follow_creeps:
                hero.follow_creeps = follow_creeps
                hero.has_creep_group = True
            else:
                #print("Moving to safepoint:" + hero.getName())
                hero.move(*hero.fallback_position)

    def flee_if_tower_aggro(self, hero, safepoint):
        if hero.getHasTowerAggro():
            hero.move(*safepoint)
            return True
        return False

    def flee_if_low_health(self, hero, safepoint):
        if hero.getHealth() / hero.getMaxHealth() < 0.33:
            hero.move(*safepoint)
            #print("Running to safepoint: " + hero.getName())
            return True
        return False

    def close_friendly_creeps(self, hero):
        creeps = self.world.get_friendly_creeps(hero)
        close_creeps = []
        for c in creeps:
            if self.world.get_distance_units(c, hero) < 1000:
                close_creeps.append(c)
        return close_creeps

    def get_hero_fallback_point(self, hero):
        hero_name = hero.getName()
        fallback_point = None
        if self.badguys_tower1.isAlive(): #
            if self.hero_position[hero_name] == "TOP":
                fallback_point = self.top_fallback_point
            elif self.hero_position[hero_name] == "MID":
                fallback_point = self.mid_fallback_point
            elif self.hero_position[hero_name] == "BOT":
                fallback_point = self.bot_fallback_point
        else:
            if not self.badguys_tower3.isAlive():
                fallback_point = self.mid_push_point3
            elif not self.badguys_tower2.isAlive():
                fallback_point = self.mid_push_point2
            else:
                fallback_point = self.mid_push_point1

        return fallback_point

    def get_closes_creep_group(self, hero):
        creep_group = []
        friendly_creeps = self.world.get_friendly_creeps(hero)
        creeps_by_distance = {}
        for creep in friendly_creeps:
            distance = self.world.get_distance_units(hero, creep)
            creeps_by_distance[distance] = creep

        if not creeps_by_distance:
            return creep_group

        closest_creep_distance = min(creeps_by_distance.keys())
        closest_creep = creeps_by_distance[closest_creep_distance]
        if closest_creep_distance > 1000:
            return creep_group

        creeps_by_distance = {}
        for creep in friendly_creeps:
            if creep == closest_creep:
                continue
            distance = self.world.get_distance_units(closest_creep, creep)
            creeps_by_distance[distance] = creep

        creep_group.append(closest_creep)
        for distance in sorted(creeps_by_distance.keys())[:3]:
            creep_group.append(creeps_by_distance[distance])

        return creep_group

    def follow_unit(self, hero, unit):
        if self.world.get_distance_pos(hero.getOrigin(), unit.getOrigin()) > 100:
            #print(hero.getName() + "following a unit")
            hero.move(*unit.getOrigin())

    def level_up_brewmaster(self, hero):
        if hero.getLevel() == 1:
            hero.level_up(0)
        elif hero.getLevel() < 6:
            hero.level_up(2)
        elif hero.getLevel() < 10:
            hero.level_up(0)
        elif hero.getLevel() == 6 or hero.getLevel() == 12 or hero.getLevel() == 18:
            hero.level_up(5)
        elif hero.getLevel() == 10 or hero.getLevel() == 15 or hero.getLevel() == 20 or hero.getLevel() == 25:
            hero.level_up(6)
        return

    def check_for_item(self, hero, i, num):
        items = hero.get_items()
        item_names = [n["name"] for n in items.values() if n]
        count = 0

        for item in item_names:
            if item == i:
                count += 1
                if count == num:
                    return True