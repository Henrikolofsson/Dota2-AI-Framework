import random
import time
import datetime
from src.bots.competition.teamNebot.config import *
from src.bots.competition.teamNebot.utils import *


class NEBot:
    def __init__(self, world):
        self.party = party_3
        self.hero_position = hero_position_3
        self.hero_abilities_up_order = hero_abilities_up_order
        self.hero_items = hero_items
        self.ability_mana_cost = ability_mana_cost

        self.hero_position_original = self.hero_position.copy()
        self.reset_lane_timer = datetime.datetime.now()
        self.world = world

        self.tower1_mid_pos = None
        self.tower1_bot_pos = None
        self.tower1_top_pos = None
        self.fort_pos = None

        self.last_mk_use_time = 0.
        self.last_pb_use_time = {
            "npc_dota_hero_pugna": 0.,
            "npc_dota_hero_venomancer": 0.,
            "npc_dota_hero_jakiro": 0.,
            "npc_dota_hero_crystal_maiden": 0.,
            "npc_dota_hero_dragon_knight": 0.,
        }
        self.last_aj_use_time = {
            "npc_dota_hero_pugna": 0.,
            "npc_dota_hero_venomancer": 0.,
            "npc_dota_hero_jakiro": 0.,
            "npc_dota_hero_crystal_maiden": 0.,
            "npc_dota_hero_dragon_knight": 0.,
        }

        self.begin_time = None
        self.tome_of_knowledge_hero = None
        self.tome_of_knowledge_num = 0

        self.pugna_ = {}

        print("TEAM NEBOT!")

    def initialize(self, heroes):
        """
        This method will run once when the game is starting before the actions method
        start getting called. In this method you can setup variables and values
        that will be used later in your code.
        """
        print("Initializing MyBot with the following heroes:")

        for hero in heroes:
            print(hero.getName())

        self.tower1_mid_pos = self.world.find_entity_by_name("dota_goodguys_tower1_mid").getOrigin()
        self.tower1_bot_pos = self.world.find_entity_by_name("dota_goodguys_tower1_bot").getOrigin()
        self.tower1_top_pos = self.world.find_entity_by_name("dota_goodguys_tower1_top").getOrigin()
        self.fort_pos = self.world.find_entity_by_name("dota_goodguys_fort").getOrigin()

        self.line_safe_pos = {
            'top': (-5735, 5800, 128),
            'mid': self.tower1_mid_pos,
            'bot': (6180, -5146, 128)
        }

        self.tower_1_pos = {
            'top': self.tower1_top_pos,
            'mid': self.tower1_mid_pos,
            'bot': self.tower1_bot_pos
        }

        self.begin_time = time.time()

    def actions(self, hero):
        hero_name, hero_level, hero_gold = hero.getName(), hero.getLevel(), hero.getGold()

        if not hero.isAlive():
            return

        # 加点
        if hero.getAbilityPoints() > 0:
            ability_index = self.hero_abilities_up_order[hero.getName()]['order'][hero_level - 1]
            if ability_index != -1:  # 应该不可能是-1，但还是加个判断保险
                print(hero.getName(), 'get ability of index ', str(ability_index))
                hero.level_up(ability_index)
                return

        # 出装
        if is_at_home(self.world, hero) and time.time() - self.begin_time > 610 and self.tome_of_knowledge_num == 0:
            item = "item_tome_of_knowledge"
            if hero.getGold() >= 75:
                hero.buy(item)
                self.tome_of_knowledge_num += 1
                self.tome_of_knowledge_hero = hero.getName()
                return

        if is_at_home(self.world, hero) and len(self.hero_items[hero_name]) > 0:
            item, price = self.hero_items[hero_name][0]
            if hero.getGold() >= price:
                hero.buy(item)
                self.hero_items[hero_name].popleft()
                return

        if hero_name == "npc_dota_hero_pugna":
            if len(self.pugna_) == 0:
                for entity_id, entity in self.world.entities.items():
                    if entity.getName() == "npc_dota_hero_pugna":
                        self.pugna_[entity_id] = entity
            self.action_pugna(hero)
        elif hero_name == "npc_dota_hero_venomancer":
            self.action_venomancer(hero)
        elif hero_name == "npc_dota_hero_jakiro":
            self.action_jakiro(hero)
        elif hero_name == "npc_dota_hero_crystal_maiden":
            self.action_cm(hero)
        elif hero_name == "npc_dota_hero_dragon_knight":
            self.action_dragon_knight(hero)

    def action_venomancer(self, hero):
        self.push_lane_venomancer(hero)

    def action_pugna(self, hero):
        self.push_lane_pugna(hero)

    def action_jakiro(self, hero):
        self.push_lane_jakiro(hero)

    def action_cm(self, hero):
        self.push_lane_cm(hero)

    def action_dragon_knight(self, hero):
        self.push_lane_dragon_knight(hero)

    def push_lane_venomancer(self, hero):
        hp_p = hero.getHealth() / hero.getMaxHealth()
        mp_p = hero.getMana() / hero.getMaxMana()
        hero_mp = hero.getMana()

        venomancer_position = self.hero_position[hero.getName()]
        safe_tower_pos = self.tower_1_pos[venomancer_position]
        random_position = (random.randint(-50, 100), random.randint(-50, 100), 0)
        safe_tower_pos = [x - y for x, y in zip(safe_tower_pos, random_position)]

        if hero.getHasTowerAggro() and hero.getGold() < 2000:
            hero.move(*safe_tower_pos)
            return

        if hp_p < 0.19 and hero.getGold() < 2000:
            hero.move(*safe_tower_pos)
            return

        if self.use_tome_of_knowledge(hero):
            return

        if self.use_mk(hero):
            return

        if self.use_phase_boots(hero):
            return

        if self.use_mango(hero):
            return

        if len(self.get_close_allies(hero, 1400)) < 4:
            safe_frontline_pos = get_safe_frontline_pos(self.world, venomancer_position)
            enemy_tower_counts, enemy_towers = get_enemy_tower_in_range(self.world, hero, 1200)
            if enemy_tower_counts >= 1:
                enemy_tower = list(enemy_towers.values())[0]
                creep_count = get_our_creep_count_in_enemy_tower_range(self.world, enemy_tower, 900)
                if creep_count <= 1:
                    hero.move(*safe_tower_pos)
                    return
            if self.world.get_distance_pos(hero.getOrigin(), safe_frontline_pos) > 500:
                hero.move(*safe_frontline_pos)
                return
            if self.escape(hero, 250):
                hero.move(-7456, -6938, 400)
                return

        q_ability = None
        e_ability = None
        r_ability = None

        if '0' in hero.getAbilities().keys():
            q_ability = hero.getAbilities()['0']
        if '2' in hero.getAbilities().keys():
            e_ability = hero.getAbilities()['2']
        if '5' in hero.getAbilities().keys():
            r_ability = hero.getAbilities()['5']

        q_level = q_ability.getLevel()
        e_level = e_ability.getLevel()
        r_level = r_ability.getLevel()

        q_ability_cost = self.ability_mana_cost[hero.getName()]['q_ability'][q_level]
        e_ability_cost = self.ability_mana_cost[hero.getName()]['e_ability'][e_level]
        r_ability_cost = self.ability_mana_cost[hero.getName()]['r_ability'][r_level]

        if e_ability:
            if (e_level >= 4 or (e_level >= 3 and not self.world.find_entity_by_name('dota_badguys_tower1_bot'))) \
                    and self.hero_position[hero.getName()] != 'mid':
                self.change_line(hero)
                return

        if q_ability and get_enemy_hero_count_in_range(self.world, hero, 700) >= 1:
            if q_level > 0 and q_ability.getCooldownTimeRemaining() == 0 and hero_mp > q_ability_cost:
                enemy_heros = self.get_close_enemy_heros(hero, 700)
                target_enemy_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_point(0, position=list(target_enemy_hero.values())[0].getOrigin())
                hero.command["npc_dota_hero_venomancer"]["command"] = "CAST_ABILITY_TARGET_POINT"
                return

        if e_ability and get_enemy_hero_count_in_range(self.world, hero, 600) >= 1 and hero_mp > e_ability_cost:
            enemy_heros = self.get_close_enemy_heros(hero, 600)
            target_enemy_hero = get_least_hp_unit(enemy_heros)
            if e_level > 0 and e_ability.getCooldownTimeRemaining() == 0:
                hero.cast_target_point(2, position=list(target_enemy_hero.values())[0].getOrigin())
                hero.command["npc_dota_hero_venomancer"]["command"] = "CAST_ABILITY_TARGET_POINT"
                return

        if r_ability and get_enemy_hero_count_in_range(self.world, hero, 575) >= 3 and hero_mp > r_ability_cost:
            if r_level > 0 and r_ability.getCooldownTimeRemaining() == 0:
                hero.cast_no_target(5)
                return

        frontline_entity = get_friendly_frontline_creep(self.world, venomancer_position)
        safe_frontline_pos = get_safe_frontline_pos(self.world, venomancer_position, frontline_entity)
        safe_frontline_pos = [x - y for x, y in zip(safe_frontline_pos, random_position)]

        if e_ability and e_level > 0 and e_ability.getCooldownTimeRemaining() == 0 \
                and frontline_entity.isAttacking() and hero_mp > e_ability_cost:
            hero.cast_target_point(2, position=frontline_entity.getOrigin())
            hero.command["npc_dota_hero_venomancer"]["command"] = "CAST_ABILITY_TARGET_POINT"
            return

        fort_hp = 1
        for entity_id, entity in self.world.entities.items():
            if entity.getName() == 'dota_badguys_fort':
                fort_hp = entity.getHealth() / entity.getMaxHealth()
        if fort_hp == 1:
            if self.world.get_distance_pos(hero.getOrigin(), safe_frontline_pos) > 300 or \
                    in_front(hero, frontline_entity):
                hero.move(*safe_frontline_pos)
                return
        elif fort_hp < 1:
            enemy_creep = get_badguys_fort(self.world)
            hero.attack(list(enemy_creep.keys())[0])
            return

        if self.attack_logic(hero, attack_range=450):
            return

    def push_lane_pugna(self, hero):
        hp_p = hero.getHealth() / hero.getMaxHealth()
        mp_p = hero.getMana() / hero.getMaxMana()
        hero_mp = hero.getMana()

        pugna_position = self.hero_position[hero.getName()]
        if hero.getOrigin()[0] >= -3000:
            safe_tower_pos = self.line_safe_pos[pugna_position]
        else:
            safe_tower_pos = self.tower_1_pos[pugna_position]

        random_position = (random.randint(-50, 100), random.randint(-50, 100), 0)
        safe_tower_pos = [x - y for x, y in zip(safe_tower_pos, random_position)]

        if hero.getOrigin()[0] >= -900 and hero.getOrigin()[1] >= 5321:
            hero.move(*safe_tower_pos)
            return

        if hero.getHasTowerAggro() and hero.getGold() < 1300:
            hero.move(*safe_tower_pos)
            return

        if hp_p < 0.18 and hero.getGold() < 1300:
            hero.move(*safe_tower_pos)
            return

        if self.use_tome_of_knowledge(hero):
            return

        if self.use_phase_boots(hero):
            return

        if self.use_mango(hero):
            return

        if self.use_aj(hero):
            return

        close_allies_heros_num = len(self.get_close_allies_heros(hero, 500))
        if close_allies_heros_num <= 3:
            if self.back_safe_pos(hero, pugna_position, safe_tower_pos):
                return

        q_ability, w_ability, e_ability, r_ability = get_hero_ability(hero)

        q_level = q_ability.getLevel()
        w_level = w_ability.getLevel()
        e_level = e_ability.getLevel()
        r_level = r_ability.getLevel()

        q_ability_cost = self.ability_mana_cost[hero.getName()]['q_ability'][q_level]
        w_ability_cost = self.ability_mana_cost[hero.getName()]['w_ability'][w_level]
        e_ability_cost = self.ability_mana_cost[hero.getName()]['e_ability'][e_level]
        r_ability_cost = self.ability_mana_cost[hero.getName()]['r_ability'][r_level]

        if (hero.getLevel() >= 5 or not self.world.find_entity_by_name('dota_badguys_tower2_mid')) \
            and self.hero_position[hero.getName()] != 'mid' and \
                not self.world.find_entity_by_name('dota_badguys_tower1_top'):
            enemy_heros = self.get_close_enemy_heros(hero, 700)
            enemy_creeps = get_enemies_in_range(self.world, hero, 700)
            if len(enemy_creeps) - len(enemy_heros) <= 0:
                self.change_line(hero)
                return

        if q_ability:
            if q_level > 0 and q_ability.getCooldownTimeRemaining() == 0 and hero_mp > q_ability_cost:
                enemy_tower_counts, enemy_towers, enemy_towers_name = \
                    get_enemy_tower_in_range_pugna(self.world, hero, 800)
                if ('dota_badguys_tower4_bot' in enemy_towers_name or 'dota_badguys_tower4_top' in enemy_towers_name) \
                        and (
                        'bad_rax_range_mid' not in enemy_towers_name and 'bad_rax_melee_mid' not in enemy_towers_name):
                    target_tower = random.choice(enemy_towers)
                    x, y, z = target_tower.getOrigin()
                    hero.cast_target_area(0, position=(5026, 4545, z))
                    return
                elif enemy_tower_counts == 1:
                    target_tower = enemy_towers[0]
                    x, y, z = target_tower.getOrigin()
                    hero.cast_target_area(0, position=(x - 180, y - 180, z))
                    return
                elif 'dota_badguys_tower3_mid' in enemy_towers_name:
                    target_tower = random.choice(enemy_towers)
                    x, y, z = target_tower.getOrigin()
                    hero.cast_target_area(0, position=(4090, 3576, z))
                    return
                elif 'bad_rax_range_mid' in enemy_towers_name or 'bad_rax_melee_mid' in enemy_towers_name:
                    target_tower = random.choice(enemy_towers)
                    x, y, z = target_tower.getOrigin()
                    hero.cast_target_area(0, position=(4440, 3916, z))
                    return

                if get_enemy_hero_count_in_range(self.world, hero, 600) >= 2:
                    enemy_heros = self.get_close_enemy_heros(hero, 600)
                    target_enemy_hero = get_least_hp_unit(enemy_heros)
                    hero.cast_target_area(0, position=list(target_enemy_hero.values())[0].getOrigin())
                    return

                q_enemies = get_enemies_in_range(self.world, hero, 600)
                if len(q_enemies) >= 3 and mp_p > 0.5:
                    target_unit = random.choice(list(q_enemies.values()))
                    hero.cast_target_area(0, position=target_unit.getOrigin())
                    return

        if w_ability and get_enemy_hero_count_in_range(self.world, hero, 400) >= 1:
            if w_level > 0 and r_ability.getLevel() > 0 and w_ability.getCooldownTimeRemaining() == 0 and \
                    r_ability.getCooldownTimeRemaining() == 0 and hero.getMana() > (w_ability_cost + r_ability_cost):
                enemy_heros = self.get_close_enemy_heros(hero, 400)
                target_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_unit(1, target=list(target_hero.keys())[0])
                return
            elif w_level > 1 and w_ability.getCooldownTimeRemaining() == 0 and \
                    q_ability.getCooldownTimeRemaining() == 0 and hero.getMana() > (w_ability_cost + q_ability_cost):
                enemy_heros = self.get_close_enemy_heros(hero, 400)
                target_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_unit(1, target=list(target_hero.keys())[0])
                return

        if e_ability and get_enemy_hero_count_in_range(self.world, hero, 1600) >= 6 and hero.getMana() > e_ability_cost:
            if e_level > 0 and e_ability.getCooldownTimeRemaining() == 0:
                hero.cast_target_point(2, position=hero.getOrigin())
                hero.command["npc_dota_hero_pugna"]["command"] = "CAST_ABILITY_TARGET_POINT"
                return

        if r_ability and get_enemy_hero_count_in_range(self.world, hero, 400) >= 1 and hero.getMana() > r_ability_cost:
            if r_level > 0 and r_ability.getCooldownTimeRemaining() == 0:
                enemy_heros = self.get_close_enemy_heros(hero, 400)
                target_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_unit(5, target=list(target_hero.keys())[0])
                return

        fort_hp = 1
        for entity_id, entity in self.world.entities.items():
            if entity.getName() == 'dota_badguys_fort':
                fort_hp = entity.getHealth() / entity.getMaxHealth()

        if fort_hp == 1:
            if self.back_creep_pos(hero, pugna_position, random_position, distance=200, attack_type='range'):
                return
        elif fort_hp < 1:
            enemy_creep = get_badguys_fort(self.world)
            hero.attack(list(enemy_creep.keys())[0])
            return

        if self.attack_logic(hero, attack_range=630):
            return

    def push_lane_jakiro(self, hero):
        hp_p = hero.getHealth() / hero.getMaxHealth()
        mp_p = hero.getMana() / hero.getMaxMana()
        hero_mp = hero.getMana()

        jakiro_position = self.hero_position[hero.getName()]
        if hero.getOrigin()[0] >= -3000:
            safe_tower_pos = self.line_safe_pos[jakiro_position]
        else:
            safe_tower_pos = self.tower_1_pos[jakiro_position]

        random_position = (random.randint(-50, 100), random.randint(-50, 100), 0)
        safe_tower_pos = [x - y for x, y in zip(safe_tower_pos, random_position)]

        if hero.getOrigin()[0] >= -900 and hero.getOrigin()[1] >= 5321:
            hero.move(*safe_tower_pos)
            return

        if hero.getHasTowerAggro() and hero.getGold() < 1500:
            hero.move(*safe_tower_pos)
            return

        if hp_p < 0.17 and hero.getGold() < 1500:
            hero.move(*safe_tower_pos)
            return

        if self.use_tome_of_knowledge(hero):
            return

        if self.use_phase_boots(hero):
            return

        if self.use_mango(hero):
            return

        if self.use_aj(hero):
            return

        close_allies_heros_num = len(self.get_close_allies_heros(hero, 500))
        if close_allies_heros_num <= 3:
            if self.back_safe_pos(hero, jakiro_position, safe_tower_pos):
                return

        q_ability, w_ability, e_ability, r_ability = get_hero_ability(hero)

        q_level = q_ability.getLevel()
        w_level = w_ability.getLevel()
        e_level = e_ability.getLevel()
        r_level = r_ability.getLevel()

        q_ability_cost = self.ability_mana_cost[hero.getName()]['q_ability'][q_level]
        w_ability_cost = self.ability_mana_cost[hero.getName()]['w_ability'][w_level]
        e_ability_cost = self.ability_mana_cost[hero.getName()]['e_ability'][e_level]
        r_ability_cost = self.ability_mana_cost[hero.getName()]['r_ability'][r_level]

        if hero.getLevel() >= 5 and self.hero_position[hero.getName()] != 'mid' and \
                not self.world.find_entity_by_name('dota_badguys_tower1_top'):
            enemy_heros = self.get_close_enemy_heros(hero, 700)
            enemy_creeps = get_enemies_in_range(self.world, hero, 700)
            if len(enemy_creeps) - len(enemy_heros) <= 0:
                self.change_line(hero)
                return

        if hero.getLevel() >= 10:
            e_range = 925
            attack_range = 725
        else:
            e_range = 600
            attack_range = 400

        if q_ability:
            if q_level > 0 and q_ability.getCooldownTimeRemaining() == 0 and hero_mp > q_ability_cost:
                q_enemies = get_enemies_in_range(self.world, hero, 750)
                if len(q_enemies) >= 4:
                    target_unit = list(q_enemies.keys())[0]
                    hero.cast_target_unit(0, target=target_unit)
                    return
                if get_enemy_hero_count_in_range(self.world, hero, 750) >= 2:
                    enemy_heros = self.get_close_enemy_heros(hero, 750)
                    target_enemy_hero = get_least_hp_unit(enemy_heros)
                    hero.cast_target_unit(0, target=list(target_enemy_hero.keys())[0])
                    return

        if w_ability and get_enemy_hero_count_in_range(self.world, hero, 400) >= 2 and hero_mp > w_ability_cost:
            if w_level > 0 and w_ability.getCooldownTimeRemaining() == 0:
                enemy_heros = self.get_close_enemy_heros(hero, 400)
                target_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_point(1, position=list(target_hero.values())[0].getOrigin())
                hero.command["npc_dota_hero_jakiro"]["command"] = "CAST_ABILITY_TARGET_POINT"
                return

        if e_ability:
            if e_level > 0 and e_ability.getCooldownTimeRemaining() == 0 and hero_mp > e_ability_cost:
                enemy_tower_counts, enemy_towers = get_enemy_tower_in_range(self.world, hero, e_range)
                # if enemy_tower_counts >= 1:
                #     target_tower = get_least_hp_building(enemy_towers)
                #     if len(target_tower) >= 1:
                #         hero.cast_target_unit(2, target=list(target_tower.keys())[0])
                #         return
                if enemy_tower_counts >= 1:
                    target_tower = get_least_hp_unit(enemy_towers)
                    hero.cast_target_unit(2, target=list(target_tower.keys())[0])
                    return

                enemy_heros = self.get_close_enemy_heros(hero, e_range)
                if enemy_heros:
                    target_enemy_hero = get_least_hp_unit(enemy_heros)
                    hero.cast_target_unit(2, target=list(target_enemy_hero.keys())[0])
                    return

                e_enemies = get_enemies_in_range(self.world, hero, e_range)
                if len(e_enemies) >= 3:
                    target_unit = list(e_enemies.keys())[0]
                    hero.cast_target_unit(2, target=target_unit)
                    return

        if r_ability and get_enemy_hero_count_in_range(self.world, hero, 400) >= 2 and hero_mp > r_ability_cost:
            if r_level > 0 and r_ability.getCooldownTimeRemaining() == 0:
                enemy_heros = self.get_close_enemy_heros(hero, 400)
                target_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_point(5, position=list(target_hero.values())[0].getOrigin())
                hero.command["npc_dota_hero_jakiro"]["command"] = "CAST_ABILITY_TARGET_POINT"
                return

        fort_hp = 1
        for entity_id, entity in self.world.entities.items():
            if entity.getName() == 'dota_badguys_fort':
                fort_hp = entity.getHealth() / entity.getMaxHealth()

        if fort_hp == 1:
            if self.back_creep_pos(hero, jakiro_position, random_position, distance=200, attack_type='range'):
                return
        elif fort_hp < 1:
            enemy_creep = get_badguys_fort(self.world)
            hero.attack(list(enemy_creep.keys())[0])
            return

        if self.attack_logic(hero, attack_range=attack_range):
            return

    def push_lane_cm(self, hero):
        hp_p = hero.getHealth() / hero.getMaxHealth()
        mp_p = hero.getMana() / hero.getMaxMana()
        hero_mp = hero.getMana()

        cm_position = self.hero_position[hero.getName()]
        if hero.getOrigin()[1] >= -4855:
            safe_tower_pos = self.line_safe_pos[cm_position]
        else:
            safe_tower_pos = self.tower_1_pos[cm_position]
        random_position = (random.randint(-50, 100), random.randint(-50, 100), 0)
        safe_tower_pos = [x - y for x, y in zip(safe_tower_pos, random_position)]

        if hero.getOrigin()[0] >= 5493 and hero.getOrigin()[1] >= -600:
            hero.move(*safe_tower_pos)
            return

        if hero.getHasTowerAggro() and hero.getGold() < 1200:
            hero.move(*safe_tower_pos)
            return

        if hp_p < 0.4 and hero.getGold() < 1200:
            hero.move(*safe_tower_pos)
            return

        close_allies_heros_num = len(self.get_close_allies_heros(hero, 500))
        if close_allies_heros_num <= 3:
            if self.back_safe_pos(hero, cm_position, safe_tower_pos):
                return

        if self.use_tome_of_knowledge(hero):
            return

        if self.use_mango(hero):
            return

        if self.use_flask(hero, 600, 0.3, target_hero='npc_dota_hero_pugna'):
            return

        if hero.getLevel() >= 5 and self.hero_position[hero.getName()] != 'mid' and \
                not self.world.find_entity_by_name('dota_badguys_tower1_bot'):
            enemy_heros = self.get_close_enemy_heros(hero, 700)
            enemy_creeps = get_enemies_in_range(self.world, hero, 700)
            if len(enemy_creeps) - len(enemy_heros) <= 0:
                self.change_line(hero)
                return

        q_ability, w_ability, e_ability, r_ability = get_hero_ability(hero)

        q_level = q_ability.getLevel()
        w_level = w_ability.getLevel()
        r_level = r_ability.getLevel()

        q_ability_cost = self.ability_mana_cost[hero.getName()]['q_ability'][q_level]
        w_ability_cost = self.ability_mana_cost[hero.getName()]['w_ability'][w_level]
        r_ability_cost = self.ability_mana_cost[hero.getName()]['r_ability'][r_level]

        if q_ability:
            # if (q_level >= 3 or not self.world.find_entity_by_name('dota_badguys_tower2_mid')) and \
            #         self.hero_position[hero.getName()] != 'mid' and \
            #         not self.world.find_entity_by_name('dota_badguys_tower1_bot'):
            #     enemy_heros = self.get_close_enemy_heros(hero, 700)
            #     enemy_creeps = get_enemies_in_range(self.world, hero, 700)
            #     if len(enemy_creeps) - len(enemy_heros) <= 0:
            #         self.change_line(hero)
            #         return

            if q_level > 0 and q_ability.getCooldownTimeRemaining() == 0 and hero_mp > q_ability_cost:
                q_enemies = get_enemies_in_range(self.world, hero, 700)
                if len(q_enemies) >= 3:
                    target_unit = list(q_enemies.values())[0]
                    hero.cast_target_area(0, position=target_unit.getOrigin())
                    return

                if get_enemy_hero_count_in_range(self.world, hero, 700) >= 2:
                    enemy_heros = self.get_close_enemy_heros(hero, 700)
                    target_enemy_hero = get_least_hp_unit(enemy_heros)
                    hero.cast_target_area(0, position=list(target_enemy_hero.values())[0].getOrigin())
                    return

        if w_ability and get_enemy_hero_count_in_range(self.world, hero, 550) >= 1 and hero_mp > w_ability_cost:
            if w_level > 0 and w_ability.getCooldownTimeRemaining() == 0:
                enemy_heros = self.get_close_enemy_heros(hero, 550)
                target_enemy_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_unit(1, target=list(target_enemy_hero.keys())[0])
                return

        if r_ability and get_enemy_hero_count_in_range(self.world, hero, 400) >= 2 and hero_mp > r_ability_cost:
            if r_level > 0 and r_ability.getCooldownTimeRemaining() == 0:
                hero.cast_no_target(5)
                return

        fort_hp = 1
        for entity_id, entity in self.world.entities.items():
            if entity.getName() == 'dota_badguys_fort':
                fort_hp = entity.getHealth() / entity.getMaxHealth()

        if fort_hp == 1:
            if self.back_creep_pos(hero, cm_position, random_position, distance=300, attack_type='range'):
                return
        elif fort_hp < 1:
            enemy_creep = get_badguys_fort(self.world)
            hero.attack(list(enemy_creep.keys())[0])
            return

        if self.attack_logic(hero, attack_range=600):
            return

    def push_lane_dragon_knight(self, hero):
        hp_p = hero.getHealth() / hero.getMaxHealth()
        mp_p = hero.getMana() / hero.getMaxMana()
        hero_mp = hero.getMana()

        dragon_knight_position = self.hero_position[hero.getName()]
        if hero.getOrigin()[1] >= -4855:
            safe_tower_pos = self.line_safe_pos[dragon_knight_position]
        else:
            safe_tower_pos = self.tower_1_pos[dragon_knight_position]
        random_position = (random.randint(-50, 100), random.randint(-50, 100), 0)
        safe_tower_pos = [x - y for x, y in zip(safe_tower_pos, random_position)]

        q_ability, w_ability, e_ability, r_ability = get_hero_ability(hero)

        q_level = q_ability.getLevel()
        w_level = w_ability.getLevel()
        e_level = e_ability.getLevel()
        r_level = r_ability.getLevel()

        q_ability_cost = self.ability_mana_cost[hero.getName()]['q_ability'][q_level]
        w_ability_cost = self.ability_mana_cost[hero.getName()]['w_ability'][w_level]
        r_ability_cost = self.ability_mana_cost[hero.getName()]['r_ability'][r_level]

        if hero.getOrigin()[0] >= 5493 and hero.getOrigin()[1] >= -600:
            hero.move(*safe_tower_pos)
            return

        if hero.getHasTowerAggro() and hero.getGold() < 1300:
            if e_level < 3 or hp_p < 0.6:
                hero.move(*safe_tower_pos)
                return

        if hp_p < 0.25 and hero.getGold() < 1300:
            hero.move(*safe_tower_pos)
            return

        if self.use_tome_of_knowledge(hero):
            return

        if self.use_phase_boots(hero):
            return

        if self.use_mango(hero):
            return

        if self.use_aj(hero):
            return

        if len(self.get_close_allies(hero, 1400)) < 4 and e_level < 4:
            safe_frontline_pos = get_safe_frontline_pos(self.world, dragon_knight_position)
            enemy_tower_counts, enemy_towers = get_enemy_tower_in_range(self.world, hero, 1000)
            if enemy_tower_counts >= 1:
                enemy_tower = list(enemy_towers.values())[0]
                creep_count = get_our_creep_count_in_enemy_tower_range(self.world, enemy_tower, 900)
                if creep_count <= 1:
                    hero.move(*safe_tower_pos)
                    return
            if self.world.get_distance_pos(hero.getOrigin(), safe_frontline_pos) > 500:
                hero.move(*safe_frontline_pos)
                return
            if self.escape(hero, 250):
                hero.move(-7456, -6938, 400)
                return

        if (hero.getLevel() >= 6 or not self.world.find_entity_by_name('dota_badguys_tower2_mid')) \
                and self.hero_position[hero.getName()] != 'mid' and \
                not self.world.find_entity_by_name('dota_badguys_tower1_bot'):
            enemy_heros = self.get_close_enemy_heros(hero, 700)
            enemy_creeps = get_enemies_in_range(self.world, hero, 700)
            if len(enemy_creeps) - len(enemy_heros) <= 0:
                self.change_line(hero)
                return

        attack_range = hero.getAttackRange()
        if attack_range > 350:
            w_range = 400
        else:
            w_range = 150

        if q_ability:
            if q_level > 0 and q_ability.getCooldownTimeRemaining() == 0 and hero_mp > q_ability_cost:
                q_enemies = get_enemies_in_range(self.world, hero, 600)
                if len(q_enemies) >= 4:
                    target_unit = list(q_enemies.keys())[0]
                    hero.cast_target_unit(0, target=target_unit)
                    return
                enemy_heros = self.get_close_enemy_heros(hero, 600)
                if len(enemy_heros) >= 1:
                    target_unit = list(enemy_heros.keys())[0]
                    hero.cast_target_unit(0, target=target_unit)
                    return

        if w_ability and get_enemy_hero_count_in_range(self.world, hero, w_range) >= 1:
            if w_level > 0 and w_ability.getCooldownTimeRemaining() == 0 and hero_mp > w_ability_cost:
                enemy_heros = self.get_close_enemy_heros(hero, w_range)
                target_hero = get_least_hp_unit(enemy_heros)
                hero.cast_target_unit(1, target=list(target_hero.keys())[0])
                return

        if r_ability and hero_mp > r_ability_cost:
            if r_level > 0 and r_ability.getCooldownTimeRemaining() == 0:
                enemy_tower_counts, enemy_towers = get_enemy_tower_in_range(self.world, hero, 600)
                enemy_heros = self.get_close_enemy_heros(hero, 600)
                if enemy_tower_counts >= 1 or len(enemy_heros) >= 2:
                    hero.cast_no_target(5)
                    return

        fort_hp = 1
        for entity_id, entity in self.world.entities.items():
            if entity.getName() == 'dota_badguys_fort':
                fort_hp = entity.getHealth() / entity.getMaxHealth()
        if fort_hp == 1:
            if self.back_creep_pos(hero, dragon_knight_position, random_position, distance=500, attack_type='melee'):
                return
        elif fort_hp < 1:
            enemy_creep = get_badguys_fort(self.world)
            hero.attack(list(enemy_creep.keys())[0])
            return

        if self.attack_logic(hero, attack_range=attack_range):
            return

        enemy_tower_counts, enemy_towers = get_enemy_tower_in_range(self.world, hero, 800)
        if enemy_tower_counts >= 1:
            if hero.isAttacking():
                return
            target_tower = get_least_hp_building(enemy_towers)
            if len(target_tower) >= 1:
                hero.attack(list(target_tower.keys())[0])
                # target_tower = sorted(list(enemy_towers.keys()))[-1]
                # hero.attack(target_tower)
                print(list(enemy_towers.values())[-1].getName())
                return

        enemy_creep = get_least_hp_enemy_creep_in_melee(self.world, hero, 1000)
        if enemy_creep:
            if hero.isAttacking():
                return
            hero.attack(list(enemy_creep.keys())[0])
            return

    def use_item(self, hero, item_name):
        slot = None
        for item in hero.get_items().values():
            if item and item["name"] == item_name:
                slot = item["slot"]
                # print(item, slot)
        return slot

    def use_flask(self, hero, distance, hp, target_hero=None):
        slot = self.use_item(hero, 'item_flask')
        target = self.get_least_hp_close_allies_heros(hero, distance, hp)
        if slot is not None and target:
            if target_hero and target_hero == list(target.values())[0].getName():
                hero.use_item(slot, target=list(target.keys())[0])
                return True
            else:
                hero.use_item(slot, target=list(target.keys())[0])
                return True
        return False

    # def use_mango(self, hero):
    #     slot = self.use_item(hero, 'item_enchanted_mango')
    #     if len(self.pugna_) > 0:
    #         pugna_id, pugna_entity = list(self.pugna_.keys())[0], list(self.pugna_.values())[0]
    #     else:
    #         pugna_id, pugna_entity = None, None
    #     if slot is not None and (time.time() - self.begin_time) > 480:
    #         if pugna_entity and pugna_id:
    #             if (pugna_entity.getMana() / pugna_entity.getMaxMana()) < 0.15 and \
    #                     self.world.get_distance_units(hero, pugna_entity) < 400:
    #                 hero.use_item(slot, target=pugna_id)
    #                 return True
    #         elif (hero.getMana() / hero.getMaxMana()) < 0.15:
    #             hero.use_item(slot)
    #             return True
    #     return False

    def use_mango(self, hero):
        slot = self.use_item(hero, 'item_enchanted_mango')
        if slot is not None and (time.time() - self.begin_time) > 240:
            if (hero.getMana() / hero.getMaxMana()) < 0.15:
                hero.use_item(slot)
                return True
        return False

    def use_mk(self, hero):
        allies_heros = self.get_close_allies_heros(hero, 1200)
        least_hp_hero = list(get_least_hp_unit(allies_heros).values())[0]
        if (least_hp_hero.getHealth() / least_hp_hero.getMaxHealth()) < 0.4 and hero.getMana() > 200:
            slot = self.use_item(hero, 'item_mekansm')
            if slot is not None and (time.time() - self.last_mk_use_time > 66):
                self.last_mk_use_time = time.time()
                hero.use_item(slot)
                return True
        return False

    def use_phase_boots(self, hero):
        slot = self.use_item(hero, 'item_phase_boots')
        if slot is not None and (time.time() - self.last_pb_use_time[hero.getName()] > 9):
            self.last_pb_use_time[hero.getName()] = time.time()
            hero.use_item(slot)
            return True
        return False

    def use_aj(self, hero):
        slot = self.use_item(hero, 'item_ancient_janggo')
        if slot is not None and (time.time() - self.last_aj_use_time[hero.getName()] > 33):
            allies_heros = self.get_close_allies_heros(hero, 1200)
            if len(allies_heros) >= 4 and hero.isAttacking():
                self.last_aj_use_time[hero.getName()] = time.time()
                hero.use_item(slot)
                return True
        return False

    def use_tome_of_knowledge(self, hero):
        if hero.getName() == self.tome_of_knowledge_hero:
            slot = self.use_item(hero, 'item_tome_of_knowledge')
            if slot is not None:
                hero.use_item(slot)
                self.tome_of_knowledge_hero = None
                return True
        return False

    def back_home(self, hero):
        hero.move(-6970, -6417, 256)
        print('going home!')
        return

    def get_close_enemy_heros(self, hero, enemy_distance=1600):
        enemy_heros = {}
        for entid, ent in self.world.entities.items():
            if ent.getTeam() == hero.getTeam():
                continue
            if isinstance(ent, Building):
                continue
            if isinstance(ent, Tree):
                continue
            if self.world.get_distance_units(hero, ent) < enemy_distance and isinstance(ent, Hero):
                enemy_heros[int(entid)] = ent
        return enemy_heros

    def get_close_allies_heros(self, hero, distance=1600):
        allies_heros = {}
        for entid, ent in self.world.entities.items():
            if isinstance(ent, Building):
                continue
            if isinstance(ent, Tree):
                continue
            if ent.getTeam() == hero.getTeam() and self.world.get_distance_units(hero, ent) < distance \
                    and isinstance(ent, Hero):
                allies_heros[int(entid)] = ent
        return allies_heros

    def get_least_hp_close_allies_heros(self, hero, distance=1600, hp=0.3):
        target = {}
        least_hp = 99999
        for entid, ent in self.world.entities.items():
            if isinstance(ent, Building):
                continue
            if isinstance(ent, Tree):
                continue
            if ent.getTeam() == hero.getTeam() and self.world.get_distance_units(hero, ent) < distance \
                    and isinstance(ent, Hero):
                entity_hp = ent.getHealth()
                entity_max_hp = ent.getMaxHealth()
                if entity_hp < least_hp and (entity_hp / entity_max_hp) < hp:
                    target = {}
                    least_hp = entity_hp
                    target[int(entid)] = ent
        return target

    def get_close_allies(self, hero, distance=1600):
        allies_ids = {}
        for entid, ent in self.world.entities.items():
            if isinstance(ent, Building):
                continue
            if isinstance(ent, Tree):
                continue
            if ent.getTeam() == hero.getTeam() and self.world.get_distance_units(hero, ent) < distance:
                allies_ids[int(entid)] = ent
        return allies_ids

    def change_line(self, hero):
        self.hero_position[hero.getName()] = 'mid'

    def escape(self, hero, radius=250):
        hp_p = hero.getHealth() / hero.getMaxHealth()
        enemy_heroes_count = get_enemy_hero_count_in_range(self.world, hero, radius)
        if hp_p < 0.16 and enemy_heroes_count >= 2:
            return True
        return False

    def back_safe_pos(self, hero, position, safe_tower_pos):
        if len(self.get_close_allies(hero, 1400)) < 4:
            safe_frontline_pos = get_safe_frontline_pos(self.world, position)
            enemy_tower_counts, enemy_towers = get_enemy_tower_in_range(self.world, hero, 1200)
            if enemy_tower_counts >= 1:
                enemy_tower = list(enemy_towers.values())[0]
                creep_count = get_our_creep_count_in_enemy_tower_range(self.world, enemy_tower, 900)
                if creep_count <= 1:
                    hero.move(*safe_tower_pos)
                    return True
            if self.world.get_distance_pos(hero.getOrigin(), safe_frontline_pos) > 500:
                hero.move(*safe_frontline_pos)
                return True
            if self.escape(hero, 250):
                hero.move(-7456, -6938, 400)
                return True
        return False

    def back_creep_pos(self, hero, position, random_position, distance, attack_type):
        frontline_entity = get_friendly_frontline_creep(self.world, position)
        safe_frontline_pos = get_safe_frontline_pos(self.world, position, frontline_entity)
        safe_frontline_pos = [x - y for x, y in zip(safe_frontline_pos, random_position)]
        if attack_type == 'range':
            if self.world.get_distance_pos(hero.getOrigin(), safe_frontline_pos) > distance or \
                    in_front(hero, frontline_entity):
                hero.move(*safe_frontline_pos)
                return True
        else:
            if self.world.get_distance_pos(hero.getOrigin(), safe_frontline_pos) > distance:
                hero.move(*safe_frontline_pos)
                return True
        return False

    def attack_logic(self, hero, attack_range):
        enemy_heros = self.get_close_enemy_heros(hero, attack_range + 150)
        if enemy_heros:
            if hero.isAttacking():
                return False
            target_enemy_hero = get_least_hp_unit(enemy_heros)
            hero.attack(list(target_enemy_hero.keys())[0])
            return True

        enemy_creep = get_least_hp_enemy_creep_in_range(self.world, hero)
        if enemy_creep:
            if hero.isAttacking():
                return False
            hero.attack(list(enemy_creep.keys())[0])
            return True

        return False
