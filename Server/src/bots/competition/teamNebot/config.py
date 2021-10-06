from collections import deque


party = [
    "npc_dota_hero_skeleton_king",
    "npc_dota_hero_death_prophet",
    "npc_dota_hero_pugna",
    "npc_dota_hero_venomancer",
    "npc_dota_hero_crystal_maiden",
]

party_1 = [
    "npc_dota_hero_pugna",
    "npc_dota_hero_leshrac",
    "npc_dota_hero_venomancer",
    "npc_dota_hero_jakiro",
    "npc_dota_hero_crystal_maiden",
]


party_2 = [
    "npc_dota_hero_pugna",
    "npc_dota_hero_clinkz",
    "npc_dota_hero_venomancer",
    "npc_dota_hero_jakiro",
    "npc_dota_hero_crystal_maiden",
]

party_3 = [
    "npc_dota_hero_jakiro",
    "npc_dota_hero_dragon_knight",
    "npc_dota_hero_venomancer",
    "npc_dota_hero_pugna",
    "npc_dota_hero_crystal_maiden",
]

hero_position = {
    "npc_dota_hero_skeleton_king": "bot",
    "npc_dota_hero_death_prophet": "mid",
    "npc_dota_hero_pugna": "top",
    "npc_dota_hero_venomancer": "top",
    "npc_dota_hero_crystal_maiden": "bot"
}

hero_position_1 = {
    "npc_dota_hero_leshrac": "bot",
    "npc_dota_hero_venomancer": "mid",
    "npc_dota_hero_pugna": "top",
    "npc_dota_hero_jakiro": "top",
    "npc_dota_hero_crystal_maiden": "bot"
}

hero_position_2 = {
    "npc_dota_hero_clinkz": "bot",
    "npc_dota_hero_venomancer": "mid",
    "npc_dota_hero_pugna": "top",
    "npc_dota_hero_jakiro": "top",
    "npc_dota_hero_crystal_maiden": "bot"
}

hero_position_3 = {
    "npc_dota_hero_dragon_knight": "bot",
    "npc_dota_hero_venomancer": "mid",
    "npc_dota_hero_pugna": "top",
    "npc_dota_hero_jakiro": "top",
    "npc_dota_hero_crystal_maiden": "bot"
}


hero_abilities_up_order = {
    "npc_dota_hero_skeleton_king": {
        'level': -1,
        'order': [0, 2, 1, 1, 1, 5, 1, 2, 2, 7, 2, 5, 0, 0, 9, 0, -1, 5, -1, 11, -1, -1, -1, -1, 12, -1, -1, -1, -1]
    },
    "npc_dota_hero_death_prophet": {
        'level': -1,
        'order': [0, 2, 0, 2, 0, 5, 0, 2, 2, 6, 1, 5, 1, 1, 9, 1, -1, 5, -1, 10, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
    "npc_dota_hero_pugna": {
        'level': -1,
        'order': [0, 1, 0, 1, 0, 5, 0, 1, 1, 7, 2, 5, 2, 2, 8, 2, -1, 5, -1, 10, -1, -1, -1, -1, 12, -1, -1, -1, -1]
    },
    "npc_dota_hero_venomancer": {
        'level': -1,
        'order': [2, 1, 2, 1, 2, 1, 2, 1, 0, 7, 0, 0, 0, 5, 8, 5, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
    "npc_dota_hero_crystal_maiden": {
        'level': -1,
        'order': [2, 0, 2, 0, 2, 0, 2, 0, 1, 6, 1, 1, 1, 5, 8, 5, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
    "npc_dota_hero_leshrac": {
        'level': -1,
        'order': [2, 1, 2, 1, 2, 1, 2, 1, 5, 6, 0, 5, 0, 0, 8, 0, -1, 5, -1, 11, -1, -1, -1, -1, 12, -1, -1, -1, -1]
    },
    "npc_dota_hero_jakiro": {
        'level': -1,
        'order': [2, 0, 2, 0, 2, 0, 2, 0, 1, 5, 1, 1, 1, 5, 8, 5, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },

    "npc_dota_hero_clinkz": {
        'level': -1,
        'order': [1, 0, 1, 0, 1, 5, 1, 0, 0, 6, 2, 5, 2, 2, 9, 2, -1, 5, -1, 11, -1, -1, -1, -1, 12, -1, -1, -1, -1]
    },
    "npc_dota_hero_windrunner": {
        'level': -1,
        'order': [2, 1, 2, 1, 5, 2, 2, 1, 1, 6, 0, 5, 0, 0, 9, 0, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
    "npc_dota_hero_dragon_knight": {
        'level': -1,
        'order': [2, 0, 2, 0, 2, 5, 2, 0, 0, 6, 1, 5, 1, 1, 8, 1, -1, 5, -1, 10, -1, -1, -1, -1, 12, -1, -1, -1, -1]
    },
    "npc_dota_hero_huskar": {
        'level': -1,
        'order': [1, 2, 2, 1, 2, 5, 2, 1, 1, 7, 0, 5, 0, 0, 8, 0, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
    "npc_dota_hero_tidehunter": {
        'level': -1,
        'order': [2, 1, 2, 1, 2, 5, 2, 1, 1, 7, 0, 5, 0, 0, 9, 0, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
    "npc_dota_hero_undying": {
        'level': -1,
        'order': [2, 1, 2, 1, 2, 5, 2, 1, 1, 7, 0, 5, 0, 0, 9, 0, -1, 5, -1, 11, -1, -1, -1, -1, 13, -1, -1, -1, -1]
    },
}

# 技能蓝耗
ability_mana_cost = {
    'npc_dota_hero_venomancer': {
        'q_ability': [9999, 125, 125, 125, 125],
        'e_ability': [9999, 20, 22, 24, 26],
        'r_ability': [9999, 200, 300, 400],
    },
    'npc_dota_hero_pugna': {
        'q_ability': [9999, 85, 105, 125, 145],
        'w_ability': [9999, 60, 60, 60, 60],
        'e_ability': [9999, 80, 80, 80, 80],
        'r_ability': [9999, 125, 175, 225],
    },
    'npc_dota_hero_crystal_maiden': {
        'q_ability': [9999, 130, 145, 160, 175],
        'w_ability': [9999, 140, 145, 150, 155],
        'r_ability': [9999, 200, 400, 600],
    },
    'npc_dota_hero_jakiro': {
        'q_ability': [9999, 140, 150, 160, 170],
        'w_ability': [9999, 100, 100, 100, 100],
        'e_ability': [9999, 0, 0, 0, 0],
        'r_ability': [9999, 220, 330, 440],
    },
    'npc_dota_hero_death_prophet': {
        'q_ability': [9999, 85, 110, 135, 160],
        'w_ability': [9999, 80, 90, 100, 110],
        'e_ability': [9999, 80, 80, 80, 80],
        'r_ability': [9999, 250, 350, 450],
    },
    'npc_dota_hero_dragon_knight': {
        'q_ability': [9999, 90, 100, 110, 120],
        'w_ability': [9999, 100, 100, 100, 100],
        'd_ability': [9999, 100],
        'r_ability': [9999, 50, 50, 50],
    },
    'npc_dota_hero_leshrac': {
        'q_ability': [9999, 80, 100, 120, 140],
        'w_ability': [9999, 95, 120, 135, 155],
        'e_ability': [9999, 80, 100, 120, 140],
        'd_ability': [9999, 75],
        'r_ability': [9999, 70, 70, 70],
    },
}


# 剧毒术士出装：
venomancer_items = deque([
    ("item_headdress", 425),  # 恢复头巾
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_boots", 500),  # 速度之靴
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ('item_chainmail', 450),  # 锁子甲
    ('item_recipe_mekansm', 900),  # 梅肯
    ('item_wraith_band', 510),
    ('item_wraith_band', 510),
    ('item_wraith_band', 510),
    ('item_wraith_band', 510)
])

# 帕格纳出装
pugna_items = deque([
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_boots", 500),  # 速度之靴
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ('item_chainmail', 450),  # 锁子甲
    ("item_headdress", 425),  # 恢复头巾
    ('item_blades_of_attack', 450),
    ('item_robe', 450),  # 法师长袍
    ('item_belt_of_strength', 450),  # 力量腰带
    ("item_wind_lace", 250),  # 风灵之纹
    ("item_recipe_ancient_janggo", 550),  # 韧鼓
])

# 杰奇洛出装
jakiro_items = deque([
    ('item_buckler', 375),
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_boots", 500),  # 速度之靴
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ("item_wind_lace", 250),  # 风灵之纹
    ('item_belt_of_strength', 450),  # 力量腰带
    ('item_robe', 450),  # 法师长袍
    ("item_recipe_ancient_janggo", 550),  # 韧鼓
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
])

# 水晶室女出装
cm_items = deque([
    ("item_headdress", 425),  # 恢复头巾
    ("item_enchanted_mango", 70),  # 芒果
    ("item_enchanted_mango", 70),  # 芒果
    ("item_boots", 500),  # 速度之靴
    ("item_ring_of_regen", 175),  # 回复戒指
    ("item_wind_lace", 250),  # 风灵之纹
    ("item_ring_of_basilius", 425),  # 王者之戒
    ("item_flask", 110),  # 治疗药膏
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510)
])

# 龙骑士出装
dragon_knight_items = deque([
    ("item_boots", 500),  # 速度之靴
    ("item_enchanted_mango", 70),  # 芒果
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ('item_belt_of_strength', 450),  # 力量腰带
    ("item_wind_lace", 250),  # 风灵之纹
    ('item_robe', 450),  # 法师长袍
    ("item_recipe_ancient_janggo", 550),  # 韧鼓
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510)
])

# 拉希克出装：
leshrac_items = deque([
    ("item_boots", 500),  # 速度之靴
    ('item_buckler', 375),
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ('item_ring_of_basilius', 425),
    ('item_blades_of_attack', 450),
    ('item_lifesteal', 900),
    ('item_recipe_vladmir', 600),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
])

# 克林克兹出装：
clinkz_items = deque([
    ("item_boots", 500),  # 速度之靴
    ('item_gloves', 450),
    ('item_boots_of_elves', 450),
    ('item_wraith_band', 510),
    ('item_wraith_band', 510),
    ('item_wraith_band', 510),
    ('item_wraith_band', 510),
])

# 风行者出装：
windrunner_items = deque([
    ("item_boots", 500),  # 速度之靴
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ('item_blight_stone', 300),
    ('item_mithril_hammer', 1600),
    ('item_mithril_hammer', 1600),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
    ('item_null_talisman', 510),
])

# 哈斯卡出装
huskar_items = deque([
    ("item_boots", 500),  # 速度之靴
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ('item_lifesteal', 900),
    ('item_buckler', 375),
    ('item_ring_of_basilius', 425),
    ('item_recipe_vladmir', 600),
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510)
])

# 潮汐猎人出装
tidehunter_items = deque([
    ("item_boots", 500),  # 速度之靴
    ('item_chainmail', 550),
    ('item_blades_of_attack', 450),
    ('item_lifesteal', 900),
    ('item_buckler', 375),
    ('item_ring_of_basilius', 425),
    ('item_recipe_vladmir', 600),
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510)
])

# 不朽尸王出装
undying_items = deque([
    ("item_headdress", 425),  # 恢复头巾
    ("item_boots", 500),  # 速度之靴
    ('item_gloves', 450),
    ('item_boots_of_elves', 450),
    ('item_chainmail', 450),  # 锁子甲
    ('item_recipe_mekansm', 900),  # 梅肯
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510),
    ('item_bracer', 510)
])

hero_items = {
    "npc_dota_hero_pugna": pugna_items,
    "npc_dota_hero_leshrac": leshrac_items,
    "npc_dota_hero_venomancer": venomancer_items,
    "npc_dota_hero_jakiro": jakiro_items,
    "npc_dota_hero_crystal_maiden": cm_items,
    "npc_dota_hero_clinkz": clinkz_items,
    "npc_dota_hero_windrunner": windrunner_items,
    "npc_dota_hero_dragon_knight": dragon_knight_items,
    "npc_dota_hero_huskar": huskar_items,
    "npc_dota_hero_tidehunter": tidehunter_items,
    "npc_dota_hero_undying": undying_items,
}

secret_shop = ['item_hyperstone', 'item_platemail', 'item_energy_booster',
               'item_vitality_booster', 'item_pers', 'item_ultimate_orb']

secret_shop_position = [(-5038, 1872, 128), (4768, -1185, 128)]


towers = {
    'our_towers': {
        'top': ['dota_goodguys_tower1_top', 'dota_goodguys_tower2_top', 'dota_goodguys_tower3_top'],
        'mid': ['dota_goodguys_tower1_mid', 'dota_goodguys_tower2_mid', 'dota_goodguys_tower3_mid'],
        'bot': ['dota_goodguys_tower1_bot', 'dota_goodguys_tower2_bot', 'dota_goodguys_tower3_bot'],
        'inter': ['dota_goodguys_tower4_top', 'dota_goodguys_tower4_bot']
        },
    'enemy_towers': {
        'top': ['dota_badguys_tower1_top', 'dota_badguys_tower2_top', 'dota_badguys_tower3_top'],
        'mid': ['dota_badguys_tower1_mid', 'dota_badguys_tower2_mid', 'dota_badguys_tower3_mid'],
        'bot': ['dota_badguys_tower1_bot', 'dota_badguys_tower2_bot', 'dota_badguys_tower3_bot'],
        'inter': ['dota_badguys_tower4_top', 'dota_badguys_tower4_bot']
    }
}

buildings = {
    'our_buildings': {
        'top': ['good_rax_range_top', 'good_rax_melee_top'],
        'mid': ['good_rax_range_mid', 'good_rax_melee_mid'],
        'bot': ['good_rax_range_bot', 'good_rax_melee_bot'],
        'inter': ['dota_goodguys_fort', 'ent_dota_fountain_good']
        },
    'enemy_buildings': {
        'top': ['bad_rax_range_top', 'bad_rax_melee_top'],
        'mid': ['bad_rax_range_mid', 'bad_rax_melee_mid'],
        'bot': ['bad_rax_range_bot', 'bad_rax_melee_bot'],
        'inter': ['dota_badguys_fort', 'ent_dota_fountain_bad']
    }
}