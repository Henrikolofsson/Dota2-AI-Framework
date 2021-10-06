import random
import os
import datetime

from src.game.Building import Building

from src.game.Hero import Hero

# Io Luna
sniperSkills = [1, 1, 5, 1, 1, 2, 2, 0, 5, 0, 2, 0, 2, 0, 2, 0]
sniperItems = ["item_mithril_hammer", "item_javelin", "item_power_treads", "item_wraith_band"]

viperSkills = [1, 1, 5, 1, 1, 2, 2, 0, 5, 0, 2, 0, 2, 0]
viperItems = ["item_dragon_lance", "item_power_treads", "item_wraith_band"]

thdSkills = [1, 1, 5, 1, 1, 0, 0, 2, 5, 2, 0, 2, 0, 2]
thdItems = ["item_veil_of_discord", "item_ring_of_basilius"]

lunaSkills = [5, 0, 0, 0, 5, 2, 2, 1, 1, 1, 1, 2, 2, 0]
lunaItems = ["item_yasha", "item_dragon_lance", "item_power_treads", "item_wraith_band"] #item_mask_of_madness

ioItems = ["item_mekansm", "item_headdress"]
ioSkills = [0, 5, 2, 6, 2, 2, 1, 5, 1, 1, 1, 2, 0]

attack_range = 800
attack_range_close = 250

safe_point = 0;
fallback_point = 0;

jungle_camps_bot = [
    [6300, -3600, 128], #lane check
    [4600, -3600, 128],  # hard camp t1 #4800, -3800, 128
    [3600, -4350, 128],  # small camp #3400, -4400, 128
    [2500, -4100, 128],  # medium camp t2 # 1300, -4900, 128
    [10, -4300, 128],  # medium camp # 10, -3400, 128
    [800, -2550, 128],  # medium close mid t1 #200, -2400, 128
    [-1800, -4100, 128],  # medium close mid t2 #-1800, -3900, 128

]

jungle_camps_top_dire = [
    [1500, 3200, 128],  # close mid t1 #-750, 2300, 128
    [-1500, 3400, 128],  # mid camp # -150, 3600, 128 #last
    [-1850, 4500, 128],  # camp close top t2 #-550, 5100, 128
    [-3050, 4750, 128],  # small camp #-2600, 4750, 128
    [-4250, 3600, 128]  # camp close to t1 rad #-4250, 3600, 128
]

class IoLuna:
    # constructor, initialize non-gamestate related things here
    def __init__(self, world):
        self.party = [
            "npc_dota_hero_sniper",
            "npc_dota_hero_viper",
            "npc_dota_hero_jakiro",
            "npc_dota_hero_luna",
            "npc_dota_hero_wisp",
        ]
        self.hero_position = {
            "npc_dota_hero_sniper": "MID",
            "npc_dota_hero_viper": "TOP",
            "npc_dota_hero_jakiro": "TOP",
            "npc_dota_hero_luna": "BOT",
            "npc_dota_hero_wisp": "BOT"
        }
        self.hero_position_original = self.hero_position.copy()
        self.reset_lane_timer = datetime.datetime.now()
        self.world = world
        print("THIS IS IoLuna")

    # This runs once at the beginning of the game. Do gamestate related initialization here.
    def initialize(self, heroes):
        self.top_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_top").getOrigin()
        self.mid_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_mid").getOrigin()
        self.bot_fallback_point = self.world.find_entity_by_name(
            "dota_goodguys_tower1_bot").getOrigin()

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

        if self.world.gameticks % 50 == 0:
            self.tower_check(hero)

        if hero.getAbilityPoints() > 0 and self.check_skill_list(hero):
            if hero.getName() == "npc_dota_hero_sniper" and len(sniperSkills) > 0:
                hero.level_up(sniperSkills.pop())
            elif hero.getName() == "npc_dota_hero_viper" and len(viperSkills) > 0:
                hero.level_up(viperSkills.pop())
            elif hero.getName() == "npc_dota_hero_jakiro" and len(thdSkills) > 0:
                hero.level_up(thdSkills.pop())
            elif hero.getName() == "npc_dota_hero_luna" and len(lunaSkills) > 0:
                hero.level_up(lunaSkills.pop())
            elif hero.getName() == "npc_dota_hero_wisp" and len(ioSkills) > 0:
                hero.level_up(ioSkills.pop())
            return

        ebt1 = self.world.find_entity_by_name("dota_badguys_tower1_bot")
        ett1 = self.world.find_entity_by_name("dota_badguys_tower1_top")
        emt1 = self.world.find_entity_by_name("dota_badguys_tower1_mid")
        ebt2 = self.world.find_entity_by_name("dota_badguys_tower2_bot")
        ett2 = self.world.find_entity_by_name("dota_badguys_tower2_top")
        emt2 = self.world.find_entity_by_name("dota_badguys_tower2_mid")

        if hero.getName() == "npc_dota_hero_viper" and self.gold_check(hero) and not ett1:
            hero.move(-6826, -7261, 256)
            if self.world.get_distance_pos(hero.getOrigin(), (
                    -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 7 == 0:
                self.check_for_purchase(hero)
            return
        elif hero.getName() == "npc_dota_hero_jakiro" and self.gold_check(hero) and not ett1:
            hero.move(-6826, -7261, 256)
            if self.world.get_distance_pos(hero.getOrigin(), (
                    -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 7 == 0:
                self.check_for_purchase(hero)
            return
        elif hero.getName() == "npc_dota_hero_sniper" and self.gold_check(hero) and not emt1:
            hero.move(-6826, -7261, 256)
            if self.world.get_distance_pos(hero.getOrigin(), (
                    -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 7 == 0:
                self.check_for_purchase(hero)
            return
        elif hero.getName() == "npc_dota_hero_luna" and self.gold_check(hero) and not ebt1:
            hero.move(-6826, -7261, 256)
            if self.world.get_distance_pos(hero.getOrigin(), (
                    -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 7 == 0:
                self.check_for_purchase(hero)
            return
        elif hero.getName() == "npc_dota_hero_wisp" and self.gold_check(hero) and not ebt1:
            hero.move(-6826, -7261, 256)
            if self.world.get_distance_pos(hero.getOrigin(), (
                    -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 7 == 0:
                self.check_for_purchase(hero)
            return

        if self.world.get_distance_pos(hero.getOrigin(), (
        -6826, -7261, 256)) < 150 and hero.getGold() > 600 and self.world.gameticks % 5 == 0:
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

        if hero.getName() == "npc_dota_hero_luna" and ebt1:
            self.push_lane_new(hero, fallback_point)
        elif hero.getName() == "npc_dota_hero_luna" and not ebt2 and not ett2 and not emt2:
            self.push_lane_new(
                hero,
                fallback_point)
        elif hero.getName() == "npc_dota_hero_luna" and not ebt1 and hero.getLevel() < 11:
            self.jungle_bot(hero)
        elif hero.getName() == "npc_dota_hero_wisp":
            self.push_lane_wisp(hero, fallback_point)
        else:
            self.push_lane(hero, fallback_point)

    def push_lane_wisp(self, hero, fallback_position):

        hero.fallback_position = fallback_position
        lane_partner = self.world.find_entity_by_name("npc_dota_hero_luna")
        lane_partner_pos = self.world.find_entity_by_name("npc_dota_hero_luna").getOrigin()
        #heroes = self.world.get_allies_in_range(hero, 1000)
        #heroes = [e for e in heroes if isinstance(e, Hero)]
        enemiesClose = self.world.get_enemies_in_range(hero, 300)
        enemiesClose = [e for e in enemiesClose if isinstance(e, Hero)]

        enemies = self.world.get_enemies_in_range(hero, 800)
        enemyHeroes = [e for e in enemies if isinstance(e, Hero)]

        #spells for testing
        #spirits = hero.getAbilities()[str(1)]
        #overcharge = hero.getAbilities()[str(2)]

        self.enemy_hero(hero)

        self.use_Mech(hero)
        if hero.command:
            return True

        self.cast_spells_wisp(hero)
        if hero.command:
            return True


        if self.world.get_distance_units(hero, lane_partner) < 1200:
            cast = self.world.get_id(lane_partner)
            hero.cast_target_unit(0, cast)
            if self.world.get_distance_units(hero, lane_partner) < 700 and self.world.get_distance_units(hero,
                                                                                                         lane_partner) > 400:
                hero.move(*lane_partner_pos)
                return

        #For testing
        #if enemyHeroes and hero.getLevel() > 1 and overcharge.getCooldownTimeRemaining() == 0:
           #hero.cast_no_target(2)
            #hero.cast_toggle(2)
            #hero.cast(2, position=enemyHeroes[0].getOrigin())
            #ability = hero.getAbilities()[str(2)]
            #if ability.getCooldownTimeRemaining() > 0:
                #print(" charge PASS")

            #print("overcharge " + overcharge.getCooldownTimeRemaining())

        #if enemyHeroes and hero.getLevel() > 2 and spirits.getCooldownTimeRemaining() == 0:
            #hero.cast_no_target(1)
            #hero.cast_toggle(1)
            #hero.cast(1, position=enemyHeroes[0].getOrigin())
            #ability = hero.getAbilities()[str(1)]
            #if ability.getCooldownTimeRemaining() > 0:
                #print("spirits PASS")
            #print("overcharge " + overcharge.getCooldownTimeRemaining())
            #cast_no_target, ability index
            #cast_toggle, ab index
            #hero.cast(ability.getAbilityIndex(), position=enemy.getOrigin())

            #print("spirits " + str(spirits.getCooldownTimeRemaining()))

        elif enemyHeroes:
            for e in enemyHeroes:
                if e.getHealth() < 200:
                    hero.attack(self.world.get_id(e))
                if e.getHealth() > hero.getHealth():
                    hero.move(*hero.fallback_position)
                else:
                    self.cast_spells_wisp(hero)
                    if hero.command:
                        return True
                    hero.attack(self.world.get_id(e))
        if enemiesClose:
            for e in enemiesClose:
                if e.getHealth() < 200:
                    hero.attack(self.world.get_id(e))
                if e.getHealth() > hero.getHealth():
                    hero.move(*hero.fallback_position)
                else:
                    hero.attack(self.world.get_id(e))
            return

        if self.world.get_distance_units(hero,
                                         lane_partner) > 700 and lane_partner.isAlive() and hero.getHealth() > 190:
            hero.move(*lane_partner_pos)
            return

        allies = self.world.get_allies_in_range(hero, 700)
        allies = [e for e in allies if not isinstance(e, Hero)]
        for a in allies:
            if a.isDeniable():
                hero.attack(self.world.get_id(a))
                return

    def push_lane_new(self, hero, fallback_position):

        hero.fallback_position = fallback_position
        enemiesClose = self.world.get_enemies_in_range(hero, 370)
        standing_in_creeps = [e for e in enemiesClose if not isinstance(e, Hero)]
        enemiesFar = self.world.get_enemies_in_range(hero, 575)
        enemyHeroesClose = [e for e in enemiesClose if isinstance(e, Hero)]
        enemyCreeps = [e for e in enemiesFar if not isinstance(e, Hero)]
        allied_creeps = self.world.get_allies_in_range(hero, 800)

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

        enemies = self.world.get_enemies_in_range(hero, 450)
        enemies = [e for e in enemies if isinstance(e, Hero)]

        if enemies:
            for e in enemies:
                if e.getHealth() > hero.getHealth():
                    hero.move(*hero.fallback_position)
            return


        self.use_ability_on_enemy(hero)
        if hero.command:
            return True

        if self.check_if_tower_range(hero) and not hero.has_creep_group and len(hero.follow_creeps) < 2:
            hero.move(*hero.fallback_position)
            return
        if self.check_if_tower_range(hero) and hero.getHealth() < 600:# and hero.getLevel() < 3:
            hero.move(*hero.fallback_position)
            return
        if hero.has_creep_group and len(hero.follow_creeps) > 1 and self.world.get_enemies_in_range(hero, 700):
            attacking = True
        else:
            attacking = False
        if hero.has_creep_group and len(hero.follow_creeps) > 1 and not attacking:

            follow = hero.follow_creeps[0]
            for c in hero.follow_creeps:
                if self.world.get_distance_pos(hero.getOrigin(), c.getOrigin()) < self.world.get_distance_pos(
                        hero.getOrigin(), follow.getOrigin()):
                    follow = c

            self.follow_unit(hero, c)

        elif hero.has_creep_group and len(hero.follow_creeps) > 1 and attacking:
            if hero.getHasTowerAggro():
                print("tower aggro and attacking")
                hero.move(*hero.fallback_position)
                return
            elif len(standing_in_creeps) > 2 and hero.getLevel() < 4:
                print("in creep grp")
                hero.move(*hero.fallback_position)
                return
            elif enemyHeroesClose:
                for e in enemyHeroesClose:
                    if e.getHealth() < 200:
                        hero.attack(self.world.get_id(e))
                    if e.getHealth() < hero.getHealth():
                        hero.attack(self.world.get_id(e))
            elif enemyCreeps:
                for e in enemyCreeps:
                    if e.getHealth() < 145:
                        hero.attack(self.world.get_id(e))
            elif self.check_if_tower_range(hero) and not enemyCreeps and hero.getHealth() > 620:
                self.attack_building_if_in_range(hero)
            elif allied_creeps:
                for a in allied_creeps:
                    if a.isDeniable() and a.getHealth() < 50:
                        hero.attack(self.world.get_id(a))
            elif enemyCreeps:
                target = enemyCreeps[0]
                for e in enemyCreeps:
                    if e.getHealth()> target.getHealth():
                        target = e
                hero.attack(self.world.get_id(e))

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

        if self.check_if_tower_range(hero) and not hero.has_creep_group and len(hero.follow_creeps) < 1:#WAS 2 HERE
            hero.move(*hero.fallback_position)
            return
        if self.check_if_tower_range(hero) and hero.getLevel() < 3 or hero.getHealth() < 600:
            hero.move(*hero.fallback_position)
            return
        if hero.has_creep_group and len(hero.follow_creeps) > 1 and self.world.get_enemies_in_range(hero, 600):
            attacking = True
        else:
            attacking = False
        if hero.has_creep_group and len(hero.follow_creeps) > 1 and not attacking:

            follow = hero.follow_creeps[0]
            for c in hero.follow_creeps:
                if self.world.get_distance_pos(hero.getOrigin(), c.getOrigin()) < self.world.get_distance_pos(
                        hero.getOrigin(), follow.getOrigin()):
                    follow = c

            self.follow_unit(hero, c)

            self.attack_low_creeps(hero)

        elif hero.has_creep_group and len(hero.follow_creeps) > 1 and attacking:
            if hero.getHasTowerAggro():
                print("tower aggro and attacking")
                hero.move(fallback_point)
                return
            if not self.attack_low_creeps(hero):
                self.attack_building_if_in_range(hero)

        elif hero.has_creep_group and len(hero.follow_creeps) > 2:
            print("attack tower")
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

    def jungle_bot(self, hero): #  Jungle bot HERE
        enemyHeroes = self.world.get_enemies_in_range(hero, 800)
        enemyHeroes = [e for e in enemyHeroes if isinstance(e, Hero)]
        creeps = self.world.get_enemies_in_range(hero, 1800)
        creeps = [e for e in enemyHeroes if isinstance(e, Hero)]

        if enemyHeroes:
            target = enemyHeroes[0]
            hero.attack(self.world.get_id(target))


        self.use_ability_on_enemy(hero)
        if hero.command:
            return True


        if self.world.get_enemies_in_range(hero, 1800):
            if enemyHeroes:
                hero.attack(self.world.get_id(enemyHeroes[0]))
            elif creeps:
                hero.attack(self.world.get_id(creeps[0]))
            else:
                self.attack_jungle_creeps(hero)

        if self.world.get_distance_pos(hero.getOrigin(),
                                       jungle_camps_bot[6]) > 400 and not self.world.get_enemies_in_range(hero, 500):
            hero.move(*jungle_camps_bot[6])
            return

        if self.world.get_distance_pos(hero.getOrigin(), jungle_camps_bot[6]) < 400:
            coords = jungle_camps_bot.pop()
            jungle_camps_bot.insert(0, coords)

    def attack_jungle_creeps(self, hero):
        enemies = self.world.get_enemies_in_range(hero, attack_range)
        if enemies:
            target = enemies[0]
            for e in enemies:
                if e.getHealth() > target.getHealth():  # > for glaive value
                    target = e
            hero.attack(self.world.get_id(e))

    def buy(self, hero, item):
        hero.buy(item)

    #checks for gold, if enough back to shop and buy
    def gold_check(self, hero):
        if hero.getName() == "npc_dota_hero_sniper":
            if len(sniperItems) == 0:
                return False
            elif len(sniperItems) == 1 and hero.getGold() > 1600:
                return True
            elif len(sniperItems) == 2 and hero.getGold() > 1100:
                return True
            elif len(sniperItems) == 3 and hero.getGold() > 1400:
                return True
        elif hero.getName() == "npc_dota_hero_viper":
            if len(viperItems) == 0:
                return False
            elif len(viperItems) == 1 and hero.getGold() > 1900:
                return True
            elif len(viperItems) == 2 and hero.getGold() > 1400:
                return True
        elif hero.getName() == "npc_dota_hero_jakiro":
            if len(thdItems) == 0:
                return False
            elif len(thdItems) == 1 and hero.getGold() > 1100:
                return True
            elif len(thdItems) == 2 and hero.getGold() > 1400:
                return True
        elif hero.getName() == "npc_dota_hero_luna":
            if len(lunaItems) == 0:
                return False
            elif len(lunaItems) == 1 and hero.getGold() > 2050:
                return True
            elif len(lunaItems) == 2 and hero.getGold() > 1900:
                return True
            elif len(lunaItems) == 3 and hero.getGold() > 1400:
                return True
        elif hero.getName() == "npc_dota_hero_wisp":
            if len(ioItems) == 0:
                return False
            elif len(ioItems) == 1 and hero.getGold() > 1450:
                return True

    def check_for_purchase(self, hero):
        if hero.getGold() > 550:
            if hero.getName() == "npc_dota_hero_sniper" and len(sniperItems) > 0:
                self.buy(hero, sniperItems.pop())

            elif hero.getName() == "npc_dota_hero_viper" and len(viperItems) > 0:
                self.buy(hero, viperItems.pop())

            elif hero.getName() == "npc_dota_hero_jakiro" and len(thdItems) > 0:
                self.buy(hero, thdItems.pop())

            elif hero.getName() == "npc_dota_hero_luna" and len(lunaItems) > 0:
                self.buy(hero, lunaItems.pop())

            elif hero.getName() == "npc_dota_hero_wisp" and len(ioItems) > 0:
                self.buy(hero, ioItems.pop())
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
            elif enemies and self.check_if_tower_range(hero):  # TRY FOR CREEPS UNDER TOWER
                target = random.choice(enemies)
            else:
                target = random.choice(enemies)
                hero.noop()
            if target.getHealth() < 90:
                hero.attack(self.world.get_id(target))
                # hero.attack(target)
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
            # print("attack building")
            return True
        return False

    def use_ability_on_enemy(self, hero):
        enemies = self.world.get_enemies_in_range(hero, 700)
        enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
        enemyBuildingAndHeroes = [e for e in enemies if isinstance(e, Building) or isinstance(e, Hero)]
        enemyBuilding = [e for e in enemies if isinstance(e, Building)]

        if hero.getName() == "npc_dota_hero_viper":
            enemies = self.world.get_enemies_in_range(hero, 550)
            enemyHeroes = [e for e in enemies if isinstance(e, Hero)]
            if enemyHeroes:
                for e in enemyHeroes:
                    if e.getHealth() < 300 and hero.getLevel() > 5:
                        if self.world.get_distance_pos(hero.getOrigin(),
                                                       e.getOrigin()) > 500:
                            hero.move(*e.getOrigin())
                        else:
                            enemy = self.world.get_id(e)
                            hero.cast_target_unit(0, enemy)  # ability index and target

            if enemyHeroes and hero.getMana() > 50:
                for e in enemyHeroes:
                    if e.getHealth() < 250:
                        enemy = self.world.get_id(e)
                        hero.cast_target_unit(0, enemy)
                    else:
                        enemy = self.world.get_id(enemyHeroes[0])
                        hero.cast_target_unit(0, enemy)

        if hero.getName() == "npc_dota_hero_jakiro":
            if enemyBuildingAndHeroes and hero.getMana() > 50:
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
            elif enemyHeroes and len(enemies) < 5 and hero.getLevel() > 9:
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
            elif enemyHeroesUlt and hero.getLevel() > 5 and hero.getMana() > 175 and enemyHeroesUlt[0].getHealth() < 300:
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

    # retreat to fountain
    def retreat_to_fountain(self, hero):
        if hero.getHealth() < 180:
            hero.move(-6826, -7261, 256)
            return True

    def heal_in_fountain(self, hero):
        fountain = (-6826, -7261, 256)
        if hero.getHealth() < 320:
            return True

    def back_when_alone(self, hero):
        # print(str(hero.getName()) + " is alone, going back")
        hero.move(*hero.fallback_position)

    def tower_check(self, hero):

        ett2 = self.world.find_entity_by_name("dota_badguys_tower2_top")
        ebt2 = self.world.find_entity_by_name("dota_badguys_tower2_bot")
        emt1 = self.world.find_entity_by_name("dota_badguys_tower1_mid")
        emt2 = self.world.find_entity_by_name("dota_badguys_tower2_mid")

        if not emt1:
            self.mid_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_top").getOrigin()

        if not ebt2:
            self.bot_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_mid").getOrigin()

        if not ett2:
            self.mid_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_mid").getOrigin()
            self.top_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_mid").getOrigin()

        if not emt2 and ebt2:
            self.mid_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_bot").getOrigin()
            self.top_fallback_point = self.world.find_entity_by_name(
                "dota_goodguys_tower1_bot").getOrigin()

    def use_Mech(self, hero):
        allies = self.world.get_allies_in_range(hero, 1200)
        allies = [e for e in allies if isinstance(e, Hero)]
        items = hero.get_items()
        item = "item_mekansm"
        item_names = [n["name"] for n in items.values() if n]
        if item in item_names:
            for a in allies:
                if a.getHealth() < 750:
                    hero.use_item(0)

    def check_skill_list(self, hero):
        if hero.getName() == "npc_dota_hero_sniper" and len(sniperSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_viper" and len(viperSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_jakiro" and len(thdSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_luna" and len(lunaSkills) > 0:
            return True
        elif hero.getName() == "npc_dota_hero_wisp" and len(ioSkills) > 0:
            return True
        else:
            return False

    def cast_spells_wisp(self, hero):
        sniper = self.world.find_entity_by_name("npc_dota_hero_sniper")
        sniperpos = self.world.find_entity_by_name("npc_dota_hero_sniper").getOrigin()
        viper = self.world.find_entity_by_name("npc_dota_hero_viper")
        viperpos = self.world.find_entity_by_name("npc_dota_hero_viper").getOrigin()
        jakiro = self.world.find_entity_by_name("npc_dota_hero_jakiro")
        jakiropos = self.world.find_entity_by_name("npc_dota_hero_jakiro").getOrigin()

        allies = [
            sniper,
            viper,
            jakiro,
        ]

        enemies = self.world.get_enemies_in_range(hero, 700)
        enemyHeroes = [e for e in enemies if isinstance(e, Hero)]

        creeps = self.world.get_enemies_in_range(hero, 750)
        creeps = [e for e in enemies if not isinstance(e, Hero)]

        if hero.getLevel() > 5 and hero.getHealth() > 700:
            for a in allies:
                e = self.world.get_enemies_in_range(a, 1000)
                eh = [e for e in enemies if isinstance(e, Hero)]
                if len(eh) > 0:
                    if a.getName() == "npc_dota_hero_sniper":
                        hero.cast_target_point(5, sniperpos)
                        hero.cast_target_unit(5, sniper)
                    elif a.getName() == "npc_dota_hero_viper":
                        hero.cast_target_point(5, viperpos)
                        hero.cast_target_unit(5, viper)
                    else:
                        hero.cast_target_point(5, jakiropos)
                        hero.cast_target_unit(5, jakiro)
            ability = hero.getAbilities()[str(5)]
            #Testing
            #if ability.getCooldownTimeRemaining() > 0:
                #print("RELO PASS")

        if hero.getLevel() > 4 and creeps and hero.getMana() > 200:
            hero.cast_no_target(2)
            hero.cast_toggle(2)
            hero.cast(2, hero.getOrigin())

        if hero.getLevel() > 2 and enemyHeroes:
            roll = random.getrandbits(2)
            if roll == 0:
                hero.cast_no_target(2)
                hero.cast_toggle(2)
                hero.cast(2, hero.getOrigin())
                ability = hero.getAbilities()[str(2)]
                #Testing
                #if ability.getCooldownTimeRemaining() > 0:
                    #print(" charge PASS")

                #print("overcharge " + overcharge.getCooldownTimeRemaining())

            elif roll == 1:
                hero.cast_no_target(1)
                hero.cast_toggle(1)
                hero.cast(1, hero.getOrigin())
                #Testing
                #ability = hero.getAbilities()[str(1)]
                #if ability.getCooldownTimeRemaining() > 0:
                    #print("spirits PASS")
            elif roll == 3 and hero.getMana() > 240:
                hero.cast_no_target(2)
                hero.cast_toggle(2)
                hero.cast(2, hero.getOrigin())
