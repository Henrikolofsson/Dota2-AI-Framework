import random
import math

from src.game.BaseEntity import BaseEntity
from src.game.BaseNPC import BaseNPC
from src.game.Hero import Hero
from src.game.Tower import Tower
from src.game.Building import Building
from src.game.Tree import Tree


def get_entity_lane(entity):
    """
    判断小兵属于哪一路
    """
    x, y, z = entity.getOrigin()
    if x - y > 1500:
        return 'bot'
    if y - x > 1500:
        return 'top'
    return 'mid'


def get_target_tower(world, lane):
    """
    判断正在推进的目标敌方防御塔（或基地）
    """
    for i in (1, 2, 3):
        target_tower = world.find_entity_by_name('dota_badguys_tower{}_{}'.format(i, lane))
        if target_tower and target_tower.isAlive():
            return target_tower

    mid_rax_range = world.find_entity_by_name('bad_rax_range_mid')
    mid_rax_melee = world.find_entity_by_name('bad_rax_melee_mid')

    if mid_rax_melee:
        return mid_rax_melee
    if mid_rax_range:
        return mid_rax_range

    tower4_bot = world.find_entity_by_name('dota_badguys_tower4_bot')
    tower4_top = world.find_entity_by_name('dota_badguys_tower4_top')

    if not tower4_bot and not tower4_top:  # 两个四塔都已经拆掉了，返回基地
        return world.find_entity_by_name('dota_badguys_fort')
    if tower4_bot and not tower4_top:  # 下路四塔还在，上路四塔掉了，返回下路四塔
        return tower4_bot
    if tower4_top and not tower4_bot:  # 上路四塔还在，下路四塔掉了，返回上路四塔
        return tower4_top

    # 两个四塔都在，返回对应分路的四塔做为目标
    if lane == 'bot':
        return tower4_bot
    if lane == 'top':
        return tower4_top
    # 两个四塔都在，且分路为中路，选择血量少的一个做为目标
    if lane == 'mid':
        return tower4_bot if tower4_bot.getHealth() < tower4_top.getHealth() else tower4_top

def get_friendly_frontline_creep(world, lane):
    """
    获取最前线的友方小兵
    """
    frontline_entity = world.find_entity_by_name('dota_goodguys_tower1_{}'.format(lane))
    x, y, z = frontline_entity.getOrigin()
    max_origin_sum = x + y

    target_tower = get_target_tower(world, lane)

    counts = 0

    for entity in world.entities.values():
        if entity.getName() != 'npc_dota_creep_lane' or entity.getTeam() != 2 or get_entity_lane(entity) != lane:
            continue

        if in_front(entity, target_tower):  # 忽略在敌方防御塔后面的友方小兵
            continue

        x, y, z = entity.getOrigin()
        origin_sum = x + y
        if origin_sum > max_origin_sum:
            max_origin_sum = origin_sum
            frontline_entity = entity
            counts += 1

    # if counts <= 1:
    #     frontline_entity = world.find_entity_by_name('dota_goodguys_tower1_{}'.format(lane))

    return frontline_entity

# def get_friendly_frontline_creep(world, lane):
#     """
#     获取最前线的友方小兵
#     """
#     buildingNames = [
#         "dota_goodguys_tower1_{}",
#         "dota_goodguys_tower2_{}",
#         "dota_goodguys_tower3_{}",
#         "dota_goodguys_tower4_top",
#         "dota_goodguys_tower4_bot",
#         "good_rax_melee_{}",
#         "good_rax_range_{}",
#         "ent_dota_fountain_good",
#         "dota_goodguys_fort"
#     ]
#
#     frontline_entity = world.find_entity_by_name('dota_goodguys_tower1_{}'.format(lane))
#     target_tower = None
#     max_origin_sum = 0
#     next = 0
#
#     while frontline_entity is None:
#         if next != 3 or next != 4 or next != 7 or next != 8:
#             frontline_entity = world.find_entity_by_name(buildingNames[next].format(lane))
#         else:
#             frontline_entity = world.find_entity_by_name(buildingNames[next])
#         next = next + 1
#
#     if frontline_entity is not None:
#         x, y, z = frontline_entity.getOrigin()
#         max_origin_sum = x + y
#
#         target_tower = get_target_tower(world, lane)
#
#     counts = 0
#
#     for entity in world.entities.values():
#         if entity.getName() != 'npc_dota_creep_lane' or entity.getTeam() != 2 or get_entity_lane(entity) != lane:
#             continue
#
#         if target_tower is not None and in_front(entity, target_tower):  # 忽略在敌方防御塔后面的友方小兵
#             continue
#
#         x, y, z = entity.getOrigin()
#         origin_sum = x + y
#         if origin_sum > max_origin_sum:
#             max_origin_sum = origin_sum
#             frontline_entity = entity
#             counts += 1
#
#     # if counts <= 1:
#     #     frontline_entity = world.find_entity_by_name('dota_goodguys_tower1_{}'.format(lane))
#
#     return frontline_entity


def get_safe_frontline_pos(world, lane, frontline_entity=None):
    """
    获取前线安全位置（己方小兵身后）
    """
    if not frontline_entity:
        frontline_entity = get_friendly_frontline_creep(world, lane)

    x, y, z = frontline_entity.getOrigin()
    if frontline_entity.getMaxMana() > 0:  # 最前线的友方小兵为远程兵
        return x - random.randrange(40, 60), y - random.randrange(40, 60), z
    else:  # 最前线的友方小兵为近战兵
        return x - random.randrange(250, 370), y - random.randrange(250, 270), z


def in_front(entity_or_position1, entity_or_position2):
    """
    判断position1是否比position2更加靠前
    """
    if isinstance(entity_or_position1, BaseEntity):
        entity_or_position1 = entity_or_position1.getOrigin()
    if isinstance(entity_or_position2, BaseEntity):
        entity_or_position2 = entity_or_position2.getOrigin()

    x1, y1, z1 = entity_or_position1
    x2, y2, z2 = entity_or_position2
    return x1 + y1 > x2 + y2 + 200


def in_front_melee(entity_or_position1, entity_or_position2):
    """
    判断position1是否比position2更加靠前
    """
    if isinstance(entity_or_position1, BaseEntity):
        entity_or_position1 = entity_or_position1.getOrigin()
    if isinstance(entity_or_position2, BaseEntity):
        entity_or_position2 = entity_or_position2.getOrigin()

    x1, y1, z1 = entity_or_position1
    x2, y2, z2 = entity_or_position2
    return x1 + y1 + 200 > x2 + y2


def get_enemies_in_range(world, entity, range):
    enemies = {}
    for ent_id, ent in world.entities.items():
        if isinstance(ent, Tree):
            continue
        if ent.getTeam() != 3:
            continue
        if world.get_distance_units(entity, ent) > range:
            continue
        if ent.isAlive():
            enemies[int(ent_id)] = ent
    return enemies


def get_least_hp_enemy_creep_in_range(world, hero):
    """
    获取攻击范围内的血量最少的敌方小兵
    """
    enemy_creep = {}
    least_hp = 99999

    for entity_id, entity in world.entities.items():
        if entity.getTeam() != 3:
            continue
        if isinstance(entity, Tree):
            continue
        if world.get_distance_units(hero, entity) > hero.getAttackRange():
            continue
        if not entity.isAlive():
            continue
        if "bad_filler" in entity.getName() and entity.getName() != "bad_filler_3":
            continue
        entity_hp = entity.getHealth()
        if entity_hp < least_hp:
            enemy_creep = {}
            least_hp = entity_hp
            enemy_creep[int(entity_id)] = entity

    return enemy_creep


def get_badguys_fort(world):
    """
    获取攻击范围内的血量最少的敌方小兵
    """
    enemy_creep = {}
    for entity_id, entity in world.entities.items():
        if entity.getName() == "dota_badguys_fort":
            enemy_creep[int(entity_id)] = entity

    return enemy_creep


def get_least_hp_enemy_creep_in_melee(world, hero, enemy_distance=600):
    """
    获取攻击范围内的血量最少的敌方小兵
    """
    enemy_creep = {}
    least_hp = 99999
    for entity_id, entity in world.entities.items():
        if entity.getTeam() != 3:
            continue
        if isinstance(entity, Tree):
            continue
        if world.get_distance_units(hero, entity) > enemy_distance:
            continue
        if not entity.isAlive():
            continue
        entity_hp = entity.getHealth()
        if entity_hp < least_hp:
            enemy_creep = {}
            least_hp = entity_hp
            enemy_creep[int(entity_id)] = entity

    return enemy_creep


def get_max_hp_enemy_creep_in_range(world, hero, enemy_distance=900):
    """
    获取攻击范围内的血量最多的敌方小兵
    """
    enemy_creep = {}
    max_hp = 1
    for entity_id, entity in world.entities.items():
        if entity.getTeam() != 3:
            continue
        if isinstance(entity, Tree) or isinstance(entity, Hero):
            continue
        if not entity.isAlive():
            continue
        if world.get_distance_units(hero, entity) < enemy_distance:
            entity_hp = entity.getHealth()
            if entity_hp > max_hp:
                enemy_creep = {}
                max_hp = entity_hp
                enemy_creep[int(entity_id)] = entity
    return enemy_creep


def get_least_hp_unit(units):
    """
    获取攻击范围内的血量最少的单位
    """
    target = {}
    least_hp = 99999

    for units_id, units_ent in units.items():
        entity_hp = units_ent.getHealth()
        if entity_hp < least_hp:
            target = {}
            least_hp = entity_hp
            target[int(units_id)] = units_ent
    return target


def get_least_hp_building(units):
    """
    获取攻击范围内的血量最少的单位
    """
    target = {}
    least_hp = 99999
    building_name = ['bad_rax_range_mid', 'bad_rax_melee_mid', 'dota_badguys_fort']
    for units_id, units_ent in units.items():
        if (isinstance(units_ent, Tower) or units_ent.getName() in building_name) and \
                units_ent.get_team() == 3 and units_ent.is_alive():
            entity_hp = units_ent.getHealth()
            entity_max_hp = units_ent.getMaxHealth()
            if entity_hp < least_hp and (entity_hp / entity_max_hp) < 1:
                target = {}
                least_hp = entity_hp
                target[int(units_id)] = units_ent
    return target


def get_enemy_hero_count_in_range(world, hero, radius):
    """
    获取一定半径内敌方英雄的数量
    """
    enemy_hero_count = 0
    for entity in world.entities.values():
        if isinstance(entity, Hero) and entity.get_team() == 3 and world.get_distance_units(hero, entity) < radius:
            if entity.is_alive():
                enemy_hero_count += 1
    return enemy_hero_count


def get_our_creep_count_in_enemy_tower_range(world, tower, radius=900):
    """
    获取一定半径内敌方英雄的数量
    """
    count = 0
    for entity in world.entities.values():
        if entity.getName() == 'npc_dota_creep_lane' and entity.getTeam() == 2 and \
                world.get_distance_units(tower, entity) < radius:
            if entity.isAlive() and (entity.getMaxHealth() > 490 or entity.getMaxMana() > 200):
                count += 1
    return count


def get_enemy_tower_in_range(world, hero, radius):
    """
    获取一定半径内敌方防御塔
    """
    building_name = ['bad_rax_range_mid', 'bad_rax_melee_mid', 'dota_badguys_fort']
    nan_building = ['dota_badguys_tower2_bot', 'dota_badguys_tower2_top']
    enemy_tower_count = 0
    enemy_towers = {}
    for entity_id, entity in world.entities.items():
        if entity.getName() in nan_building:
            continue
        if isinstance(entity, Tower) and entity.get_team() == 3 and world.get_distance_units(hero, entity) < radius:
            if entity.is_alive() and entity.getName() not in building_name:
                enemy_tower_count += 1
                enemy_towers[entity_id] = entity
                # if len(enemy_towers) > 0:
                #     return enemy_tower_count, enemy_towers
        elif entity.getName() in building_name and world.get_distance_units(hero, entity) < radius + 300:
            if entity.is_alive():
                enemy_tower_count += 1
                enemy_towers[int(entity_id)] = entity
    return enemy_tower_count, enemy_towers


def get_enemy_tower_in_range_pugna(world, hero, radius):
    """
    获取一定半径内敌方防御塔
    """
    building_name = ['bad_rax_range_mid', 'bad_rax_melee_mid', 'dota_badguys_fort']
    nan_building = ['dota_badguys_tower2_bot', 'dota_badguys_tower2_top']
    enemy_tower_count = 0
    enemy_towers = []
    enemy_towers_name = []
    for entity_id, entity in world.entities.items():
        if entity.getName() in nan_building:
            continue
        if isinstance(entity, Tower) and entity.get_team() == 3 and world.get_distance_units(hero, entity) < radius:
            if entity.is_alive():
                enemy_tower_count += 1
                enemy_towers.append(entity)
                enemy_towers_name.append(entity.getName())
        elif entity.getName() in building_name and world.get_distance_units(hero, entity) < radius + 300:
            if entity.is_alive():
                enemy_tower_count += 1
                enemy_towers.append(entity)
                enemy_towers_name.append(entity.getName())
    return enemy_tower_count, enemy_towers, enemy_towers_name


def get_enemy_creep_count_in_range(world, hero, radius):
    """
    获取一定半径内敌方英雄的数量
    """
    enemy_hero_count = 0
    for entity in world.entities.values():
        if isinstance(entity, Hero) and entity.get_team() == 3 and world.get_distance_units(hero, entity) < radius:
            if entity.is_alive():
                enemy_hero_count += 1
    return enemy_hero_count


def in_safe_position(world, hero):
    """
    判断英雄是否处于安全位置
    如果在敌方防御塔攻击范围内，且前方友方小兵的血量总和小于300，则判断为不安全
    """
    creep_hp_sum = 0

    lane = get_entity_lane(hero)
    target_tower = get_target_tower(world, lane)

    for entity in world.entities.values():
        if entity.getName() == 'npc_dota_creep_lane' and entity.getTeam() == 2 and get_entity_lane(entity) == lane \
                and in_front(target_tower, entity) and in_front(entity, hero):
            creep_hp_sum += entity.getHealth()
            continue

    return world.get_distance_units(target_tower, hero) >= target_tower.getAttackRange() or creep_hp_sum >= 300


def get_distance_unit_position(unit, position):
    x1, y1, z1 = unit.getOrigin()
    x2, y2, z2 = position
    return math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))


def use_tp(hero, target):
    hero.use_item('item_tpscroll', target=target)


def use_item(hero):
    slot = None
    item_name = hero.get_items()
    for item in hero.get_items().values():
        if item and item["name"] == item_name:
            slot = item["slot"]
            break
    if slot is not None:
        hero.use_item(slot)


def is_at_home(world, hero):
    """
    判断一个英雄是否在家（泉水），可以购买物品
    """
    fountain_good_pos = (-7539, -6167, 400)
    if world.get_distance_pos(hero.getOrigin(), fountain_good_pos) <= 1100:
        return True
    return False


def get_hero_ability(hero):
    q_ability = None
    w_ability = None
    e_ability = None
    r_ability = None

    if '0' in hero.getAbilities().keys():
        q_ability = hero.getAbilities()['0']
    if '1' in hero.getAbilities().keys():
        w_ability = hero.getAbilities()['1']
    if '2' in hero.getAbilities().keys():
        e_ability = hero.getAbilities()['2']
    if '5' in hero.getAbilities().keys():
        r_ability = hero.getAbilities()['5']
    return q_ability, w_ability, e_ability, r_ability