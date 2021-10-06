import random
import os
import datetime
from src.game.Building import Building
from src.game.Hero import Hero

# JUNGLE
sniperSkills = [1, 1, 5, 1, 1, 2, 2, 0, 5, 0, 2, 0, 2, 0]
sniperItems = ["item_mithril_hammer", "item_mithril_hammer", "item_belt_of_strength", "item_wraith_band",
               "item_blight_stone", "item_gloves", "item_lifesteal",
               "item_boots", "item_wraith_band", "item_wraith_band"]

viperSkills = [1, 1, 5, 1, 1, 2, 2, 0, 5, 0, 2, 0, 2, 0]
viperItems = ["item_boots", "item_wraith_band", "item_wraith_band", "item_wraith_band", "item_wraith_band"]

thdSkills = [1, 1, 5, 1, 1, 0, 0, 2, 5, 2, 0, 2, 0, 2]
thdItems = ["item_boots", "item_recipe_mekansm", "item_chainmail", "item_buckler",
            "item_headdress"]

vsSkills = [1, 1, 5, 1, 1, 5, 2, 0, 2, 0, 2, 0, 2, 0]
vsItems = ["item_boots", "item_vladmir", "item_recipe_vladmir", "item_blades_of_attack",
           "item_buckler", "item_ring_of_basilius"]

lunaSkills = [0, 2, 5, 2, 2, 0, 1, 1, 5, 1, 1, 0, 2, 0]
lunaItems = ["item_sange_and_yasha", "item_ogre_axe", "item_yasha", "item_recipe_yasha", "item_blade_of_alacrity",
             "item_lifesteal", "item_quarterstaff", "item_belt_of_strength", "item_boots",
             "item_gloves", "item_wraith_band", "item_wraith_band"]

tideSkills = [0, 0, 5, 0, 0, 1, 1, 2, 5, 2, 1, 2, 1, 2]
tideItems = ["item_blades_of_attack", "item_chainmail", "item_lifesteal", "item_boots", "item_buckler",
             "item_ring_of_basilius", "item_bracer"]

# 6 radiant bot camps
jungle_camps_bot = [
    [-1800, -3900, 128],  # medium close mid t2
    [200, -2400, 128],  # medium close mid t1
    [10, -3400, 128],  # medium camp
    [1300, -4900, 128],  # medium camp t2
    [3400, -4400, 128],  # small camp
    [4800, -3800, 128]  # hard camp t1
]
jungle_camps_top_radiant = [
    [-3850, 1200, 128],
    [-4850, -300, 128],
    [-2650, -600, 128]
]


jungle_camps_top_dire = [
    [1500, 3200, 128],  # close mid t1 #-750, 2300, 128
    [-1500, 3400, 128],  # mid camp # -150, 3600, 128 #last
    [-1850, 4500, 128],  # camp close top t2 #-550, 5100, 128
    [-3050, 4750, 128],  # small camp #-2600, 4750, 128
    [-4250, 3600, 128]  # camp close to t1 rad #-4250, 3600, 128
]

attack_range = 800
attack_range_close = 250

safe_point = 0;
fallback_point = 0;

class Jungle:

    # constructor, initialize non-gamestate related things here
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_sniper",
            "npc_dota_hero_tidehunter",
            "npc_dota_hero_jakiro",
            "npc_dota_hero_luna",
            "npc_dota_hero_vengefulspirit",
        ]
        self.hero_position = {
            "npc_dota_hero_sniper": "MID",
            "npc_dota_hero_tidehunter": "TOP",
            "npc_dota_hero_jakiro": "TOP",
            "npc_dota_hero_luna": "BOT",
            "npc_dota_hero_vengefulspirit": "BOT"
        }
        self.hero_position_original = self.hero_position.copy()
        self.reset_lane_timer = datetime.datetime.now()
        self.world = world
        print("THIS IS Jungle")

    # This runs once at the beginning of the game. Do gamestate related initialization here.
    def initialize(self, heroes):
        self.top_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_top").getOrigin()
        self.mid_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_mid").getOrigin()
        self.bot_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_bot").getOrigin()
        print(str(self.top_fallback_point))
        print(str(self.mid_fallback_point))
        print(str(self.bot_fallback_point))
        now = datetime.datetime.now()
        print("Current date and time: ")
        print(str(now))

    # This method is called once per hero every game tick. You get the current hero as parameter.
    def actions(self, hero):

        if not hero.isAlive():
            return

        if self.world.gameticks < 5:
            hero.move(-6826, -7261, 256)
            return

        if self.world.gameticks == 5:
            self.check_for_purchase(hero)
            return

        if self.world.gameticks % 100 == 0:
            self.tower_check(hero)

        if hero.getAbilityPoints() > 0 and self.check_skill_list(hero):
            if hero.getName() == "npc_dota_hero_sniper" and len(sniperSkills) > 0:
                hero.level_up(sniperSkills.pop())
            elif hero.getName() == "npc_dota_hero_tidehunter" and len(tideSkills) > 0:
                hero.level_up(tideSkills.pop())
            elif hero.getName() == "npc_dota_hero_jakiro" and len(thdSkills) > 0:
                hero.level_up(thdSkills.pop())
            elif hero.getName() == "npc_dota_hero_luna" and len(lunaSkills) > 0:
                hero.level_up(lunaSkills.pop())
            elif hero.getName() == "npc_dota_hero_vengefulspirit" and len(vsSkills) > 0:
                hero.level_up(vsSkills.pop())
            else:
                return
            return

        if self.gold_check(hero):
            hero.move(-6826, -7261, 256)
            if self.world.get_distance_pos(hero.getOrigin(), (
                    -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 7 == 0:
                self.check_for_purchase(hero)

            return

        if self.world.get_distance_pos(hero.getOrigin(), (
                -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 3 == 0:
            self.check_for_purchase(hero)

        fallback_point = self.get_hero_fallback_point(hero)

        if hero.getHasTowerAggro():
            hero.move(*fallback_point)

        if self.retreat_to_fountain(hero):
            return
        if self.heal_in_fountain(hero):
            return

        if hero.getHasTowerAggro():
            self.flee_if_tower_aggro(hero, fallback_point)
        if self.flee_if_tower_aggro(hero, fallback_point):
            return

        ebt1 = self.world.find_entity_by_name("dota_badguys_tower1_bot")
        ett1 = self.world.find_entity_by_name("dota_badguys_tower1_top")

        ability = hero.getAbilities()[str(5)]

        # jungles after t1 dead, until level 10 and when ult is on CD
        if hero.getName() == "npc_dota_hero_luna" and not ebt1 and hero.getLevel() < 10 and ability.getCooldownTimeRemaining() > 10:
            self.jungle_bot(hero)
        #jungles until level 10
        elif hero.getName() == "npc_dota_hero_tidehunter" and not ett1 and hero.getLevel() < 10:
            self.jungle_top_dire(hero)
        else:
            self.push_lane(
                hero,
                fallback_point)

    def jungle_bot(self, hero):

        self.use_ability_on_enemy(hero)

        if self.world.get_enemies_in_range(hero, 500):
            self.attack_jungle_creeps(hero)

        if self.world.get_distance_pos(hero.getOrigin(),
                                       jungle_camps_bot[5]) > 400 and not self.world.get_enemies_in_range(hero, 500):
            hero.move(*jungle_camps_bot[5])
            return

        if self.world.get_distance_pos(hero.getOrigin(), jungle_camps_bot[5]) < 400:
            coords = jungle_camps_bot.pop()
            jungle_camps_bot.insert(0, coords)

    def jungle_top_dire(self, hero):

        if self.world.get_enemies_in_range(hero, 500):
            self.attack_jungle_creeps(hero)

        if self.world.get_distance_pos(hero.getOrigin(),
                                       jungle_camps_top_dire[4]) > 400 and not self.world.get_enemies_in_range(hero,
                                                                                                               500):
            hero.move(*jungle_camps_top_dire[4])
            return

        if self.world.get_distance_pos(hero.getOrigin(), jungle_camps_top_dire[4]) < 400:
            coords = jungle_camps_top_dire.pop()
            jungle_camps_top_dire.insert(0, coords)

    def jungle_top_radiant(self, hero):
        self.use_ability_on_enemy(hero)

        if self.world.get_enemies_in_range(hero, 500):
            self.attack_jungle_creeps(hero)

        if self.world.get_distance_pos(hero.getOrigin(),
                                       jungle_camps_top_radiant[2]) > 400 and not self.world.get_enemies_in_range(hero,
                                                                                                                  500):
            hero.move(*jungle_camps_top_radiant[2])
            return

        if self.world.get_distance_pos(hero.getOrigin(), jungle_camps_top_radiant[2]) < 400:
            coords = jungle_camps_top_radiant.pop()
            jungle_camps_top_radiant.insert(0, coords)

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

        self.enemy_hero(hero)

        # Try to use mech
        if hero.getName() == "npc_dota_hero_jakiro":
            allies = self.world.get_allies_in_range(hero, 1200)
            allies = [e for e in allies if isinstance(e, Hero)]
            if allies:
                for a in allies:
                    if a.getHealth() < 400:
                        self.use_Mech(hero)

        if hero.getName() == "npc_dota_hero_luna":
            self.use_MoM(hero)

        if self.check_if_tower_range(hero) and hero.getLevel() < 4 and hero.getHealth() < 500:
            hero.move(*hero.fallback_position)
            return
        if self.check_if_tower_range(hero) and not hero.has_creep_group and len(hero.follow_creeps) < 2:
            hero.move(*hero.fallback_position)
            return
        if self.check_if_tower_range(hero) and hero.getLevel() < 3:
            hero.move(*hero.fallback_position)
            return
        if hero.has_creep_group and len(hero.follow_creeps) > 1 and self.world.get_enemies_in_range(hero, 600):
            attacking = True
        else:
            attacking = False
        if hero.has_creep_group and len(hero.follow_creeps) > 1 and not attacking:

            self.follow_unit(hero, hero.follow_creeps[len(hero.follow_creeps) - 1])
            self.attack_low_creeps(hero)

        elif hero.has_creep_group and len(hero.follow_creeps) > 1 and attacking:
            if hero.getHasTowerAggro():
                hero.move(fallback_point)
                return
            if not self.attack_low_creeps(hero):
                self.attack_building_if_in_range(hero)

        elif hero.has_creep_group and len(hero.follow_creeps) > 2:
            self.attack_building_if_in_range(hero)

        elif hero.has_creep_group and len(hero.follow_creeps) <= 1:
            hero.has_creep_group = False
            hero.follow_creeps = []

        elif not hero.has_creep_group:
            self.back_when_alone(hero)
            follow_creeps = self.get_closes_creep_group(hero)
            if follow_creeps:
                hero.follow_creeps = follow_creeps
                hero.has_creep_group = True
            else:
                hero.move(*hero.fallback_position)

    def buy(self, hero, item):
        hero.buy(item)

    # checks for gold, if enough and has items, back to shop and buy
    def gold_check(self, hero):
        if hero.getName() == "npc_dota_hero_sniper" and len(sniperItems) == 0:
            return False
        elif hero.getName() == "npc_dota_hero_tidehunter" and len(tideItems) == 0:
            return False
        elif hero.getName() == "npc_dota_hero_jakiro" and len(thdItems) == 0:
            return False
        elif hero.getName() == "npc_dota_hero_luna" and len(lunaItems) == 0:
            return False
        elif hero.getName() == "npc_dota_hero_vengefulspirit" and len(vsItems) == 0:
            return False
        elif hero.getGold() > 1200:
            return True
        else:
            return False

    def check_for_purchase(self, hero):
        if hero.getGold() > 550:
            if hero.getName() == "npc_dota_hero_sniper" and len(sniperItems) > 0:
                self.buy(hero, sniperItems.pop())

            elif hero.getName() == "npc_dota_hero_tidehunter" and len(tideItems) > 0:
                self.buy(hero, tideItems.pop())

            elif hero.getName() == "npc_dota_hero_jakiro" and len(thdItems) > 0:
                self.buy(hero, thdItems.pop())

            elif hero.getName() == "npc_dota_hero_luna" and len(lunaItems) > 0:
                self.buy(hero, lunaItems.pop())

            elif hero.getName() == "npc_dota_hero_vengefulspirit" and len(vsItems) > 0:
                self.buy(hero, vsItems.pop())
            else:
                return

    def enemy_hero(self, hero):
        enemies = self.world.get_enemies_in_range(hero, attack_range_close)
        enemies = [e for e in enemies if isinstance(e, Hero)]

        if enemies:
            for e in enemies:
                if e.getHealth() > hero.getHealth():
                    hero.move(*hero.fallback_position)
            return

    def attack_jungle_creeps(self, hero):
        enemies = self.world.get_enemies_in_range(hero, attack_range)
        if hero.getName() == "npc_dota_hero_tidehunter":
            enemies = self.world.get_enemies_in_range(hero, 375)
            if enemies and len(enemies) >= 2:
                hero.cast_no_target(2)
        elif enemies:
            target = enemies[0]
            for e in enemies:
                if e.getHealth() > target.getHealth():  #for glaive value
                    target = e
            hero.attack(self.world.get_id(e))

    def attack_low_creeps(self, hero):

        self.use_ability_on_enemy(hero)
        if hero.command:
            return True

        enemies = self.world.get_enemies_in_range(hero, attack_range)
        enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
        if enemyHeroes:
            for e in enemyHeroes:
                if e.getHealth() < 150 and not self.check_if_tower_range(hero):
                    hero.attack(self.world.get_id(e))
                    return
        if enemies:
            if enemyHeroes and not self.check_if_tower_range(hero):
                target = random.choice(enemyHeroes)
            elif enemies and self.check_if_tower_range(hero):
                target = random.choice(enemies)
            else:
                target = random.choice(enemies)
                hero.noop()
            if target.getHealth() < 60:
                hero.attack(self.world.get_id(target))
                return True
            else:

                return False
        return False

    def attack_building_if_in_range(self, hero):
        enemyUnits = self.world.get_enemies_in_range(hero, attack_range)
        enemyUnits = [e for e in enemyUnits if not isinstance(e, Building)]
        if len(enemyUnits) > 1:
            return

        enemies = self.world.get_enemies_in_range(hero, attack_range)
        enemies = [e for e in enemies if isinstance(e, Building)]
        if enemies:
            target = enemies[0]
            hero.attack(self.world.get_id(target))
            return True
        return False

    def use_ability_on_enemy(self, hero):
        enemies = self.world.get_enemies_in_range(hero, 550)
        enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
        enemyBuildingAndHeroes = [e for e in enemies if isinstance(e, Building) or isinstance(e, Hero)]
        enemyBuilding = [e for e in enemies if isinstance(e, Building)]

        if hero.getName() == "npc_dota_hero_vengefulspirit":
            enemies = self.world.get_enemies_in_range(hero, 575)
            enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
            if enemyHeroes and len(enemies) < 2:
                target = enemyHeroes[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(0, enemy)  # ability index and target
            elif enemyHeroes:
                for e in enemyHeroes:
                    if e.getHealth() < 250:
                        target = e
                        enemy = self.world.get_id(target)
                        hero.cast_target_unit(0, enemy)

        if hero.getName() == "npc_dota_hero_tidehunter":
            enemies = self.world.get_enemies_in_range(hero, 375)
            enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
            if len(enemies) >= 2:
                hero.cast_no_target(2)
            if enemyHeroes and hero.getLevel() >= 10:
                for e in enemyHeroes:
                    if e.getHealth() < 250:
                        target = e
                        enemy = self.world.get_id(target)
                        hero.cast_target_unit(0, enemy)
            if len(enemyHeroes) >= 2 and hero.getLevel() > 5:
                hero.cast_no_target(5)
            if enemyHeroes and hero.getLevel() > 5:
                for e in enemyHeroes:
                    if e.getHealth() < 300:
                        hero.cast_no_target(5)
        if hero.getName() == "npc_dota_hero_jakiro":
            roll = random.getrandbits(1)
            if enemyBuildingAndHeroes and hero.getMana() > 50 and roll == 0:
                target = enemyBuildingAndHeroes[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(2, enemy)  # ability index and target
            elif enemyHeroes and hero.getMana() > 150 and hero.getLevel() > 1:
                target = enemyHeroes[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(0, enemy)
            elif enemyBuilding:
                target = enemyBuilding[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(2, enemy)
            if not enemyHeroes and enemies:
                target = enemies[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(2, enemy)
            if not enemyHeroes and enemies and hero.getMana() > 150 and hero.getLevel() > 1:
                target = enemies[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(0, enemy)

        if hero.getName() == "npc_dota_hero_luna":
            enemies = self.world.get_enemies_in_range(hero, 800)
            enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
            if enemyHeroes and len(enemies) < 2:
                target = enemyHeroes[0]
                enemy = self.world.get_id(target)
                hero.cast_target_unit(0, enemy)
            elif enemyHeroes and len(enemies) < 5 and hero.getLevel() >= 6:
                if self.world.get_distance_pos(hero.getOrigin(),
                                               enemies[0].getOrigin()) < 300:
                    hero.cast_no_target(5)
            elif enemyHeroes:
                for e in enemyHeroes:
                    if e.getHealth() < 250:
                        target = e
                        enemy = self.world.get_id(target)
                        hero.cast_target_unit(0, enemy)
        if hero.getName() == "npc_dota_hero_sniper":
            enemies = self.world.get_enemies_in_range(hero, 550)
            enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
            enemiesUlt = self.world.get_enemies_in_range(hero, 3000)
            enemyHeroesUlt = [e for e in enemiesUlt if isinstance(e, Hero)]
            if enemyHeroes and hero.getMana() > 150:
                target = enemyHeroes[0]
                enemy = self.world.get_id(target)
                hero.cast_target_area(0, target.getOrigin())
            elif enemyHeroesUlt and hero.getLevel() > 5 and hero.getMana() > 175 and enemyHeroesUlt[
                0].getHealth() < 300:
                hero.cast_target_unit(5, self.world.get_id(enemyHeroesUlt[0]))

    def flee_if_tower_aggro(self, hero, safepoint):
        if hero.getHasTowerAggro():
            hero.move(*safepoint)
            return True
        return False

    def check_if_tower_range(self, hero):
        enemies = self.world.get_enemies_in_range(hero, attack_range)
        enemies = [e for e in enemies if isinstance(e, Building)]
        if enemies:
            if self.world.get_distance_pos(hero.getOrigin(),
                                           enemies[0].getOrigin()) < attack_range:
                return True
        return False

    def get_hero_fallback_point(self, hero):
        hero_name = hero.getName()
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
        friendly_creeps = self.world.get_friendly_creeps(hero)
        creeps_by_distance = {}
        for creep in friendly_creeps:
            distance = self.world.get_distance_units(hero, creep)
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
            distance = self.world.get_distance_units(closest_creep, creep)
            creeps_by_distance[distance] = creep

        creep_group.append(closest_creep)
        for distance in sorted(creeps_by_distance.keys())[:3]:
            creep_group.append(creeps_by_distance[distance])

        return creep_group

    def follow_unit(self, hero, unit):
        hero.move(*unit.getOrigin())

    def retreat_to_fountain(self, hero):
        if hero.getHealth() < 180:
            hero.move(-6826, -7261, 256)
            return True

    def heal_in_fountain(self, hero):
        fountain = (-6826, -7261, 256)
        if hero.getHealth() < 320:
            # hero.move(-6826, -7261, 256)
            return True

    def back_when_alone(self, hero):
        hero.move(*hero.fallback_position)

    def tower_check(self, hero):

        ebt1 = self.world.find_entity_by_name("dota_badguys_tower1_bot")

        ett2 = self.world.find_entity_by_name(
            "dota_badguys_tower2_top")
        ebt2 = self.world.find_entity_by_name(
            "dota_badguys_tower2_bot")
        hero_name = hero.getName()

        if not ebt1:
            if self.hero_position[hero_name] == "BOT":
                self.top_fallback_point = self.world.find_entity_by_name(
                    "dota_goodguys_tower1_mid").getOrigin()

        if not ett2:
            if self.hero_position[hero_name] == "TOP":
                self.top_fallback_point = self.world.find_entity_by_name(
                    "dota_goodguys_tower1_mid").getOrigin()

        if not ebt2:
            self.bot_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_mid").getOrigin()

    def use_MoM(self, hero):
        enemies = self.world.get_enemies_in_range(hero, attack_range)
        enemyHeroes = [e for e in enemies if isinstance(e, Hero)]

        items = hero.get_items()
        item = "item_mask_of_madness"
        item_names = [n["name"] for n in items.values() if n]
        if item in item_names and len(enemies) > 2 or enemyHeroes:
            hero.use_item(3)

    def use_Mech(self, hero):
        items = hero.get_items()
        item = "item_mekansm"
        item_names = [n["name"] for n in items.values() if n]
        if item in item_names:
            hero.use_item(1)

    def check_skill_list(self, hero):
        if hero.getName() == "npc_dota_hero_sniper" and len(sniperSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_tidehunter" and len(tideSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_jakiro" and len(thdSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_luna" and len(lunaSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_vengefulspirit" and len(vsSkills) > 0:
            return True
        else:
            return False
