-- 0 = home, 1 = secret shop
local item_shop_availability = {
    item_blink = 0,
    item_blades_of_attack = 0,
    item_broadsword = 0,
    item_chainmail = 0,
    item_claymore = 0,
    item_helm_of_iron_will = 0,
    item_javelin = 0,
    item_mithril_hammer = 0,
    item_quarterstaff = 0,
    item_quelling_blade = 0,
    item_faerie_fire = 0,
    item_infused_raindrop = 0,
    item_wind_lace = 0,
    item_ring_of_protection = 0,
    item_stout_shield = 0,
    item_recipe_moon_shard = 0,
    item_moon_shard = 0,
    item_gauntlets = 0,
    item_slippers = 0,
    item_mantle = 0,
    item_branches = 0,
    item_belt_of_strength = 0,
    item_boots_of_elves = 0,
    item_robe = 0,
    item_circlet = 0,
    item_ogre_axe = 0,
    item_blade_of_alacrity = 0,
    item_staff_of_wizardry = 0,
    item_gloves = 0,
    item_lifesteal = 0,
    item_ring_of_regen = 0,
    item_sobi_mask = 0,
    item_boots = 0,
    item_gem = 0,
    item_cloak = 0,
    item_cheese = 0,
    item_magic_stick = 0,
    item_recipe_magic_wand = 0,
    item_magic_wand = 0,
    item_ghost = 0,
    item_clarity = 0,
    item_enchanted_mango = 0,
    item_flask = 0,
    item_dust = 0,
    item_bottle = 0,
    item_ward_observer = 0,
    item_ward_sentry = 0,
    item_recipe_ward_dispenser = 0,
    item_ward_dispenser = 0,
    item_tango = 0,
    item_tango_single = 0,
    item_courier = 0,
    item_tpscroll = 0,
    item_recipe_travel_boots = 0,
    item_recipe_travel_boots_2 = 0,
    item_travel_boots = 0,
    item_travel_boots_2 = 0,
    item_recipe_phase_boots = 0,
    item_phase_boots = 0,
    item_ring_of_health = 0,
    item_void_stone = 0,
    item_recipe_power_treads = 0,
    item_power_treads = 0,
    item_recipe_hand_of_midas = 0,
    item_hand_of_midas = 0,
    item_recipe_oblivion_staff = 0,
    item_oblivion_staff = 0,
    item_recipe_pers = 0,
    item_pers = 0,
    item_recipe_poor_mans_shield = 0,
    item_poor_mans_shield = 0,
    item_recipe_bracer = 0,
    item_bracer = 0,
    item_banana = 0,
    item_recipe_wraith_band = 0,
    item_wraith_band = 0,
    item_recipe_null_talisman = 0,
    item_null_talisman = 0,
    item_recipe_mekansm = 0,
    item_mekansm = 0,
    item_recipe_vladmir = 0,
    item_vladmir = 0,
    item_flying_courier = 0,
    item_recipe_buckler = 0,
    item_buckler = 0,
    item_recipe_ring_of_basilius = 0,
    item_ring_of_basilius = 0,
    item_recipe_pipe = 0,
    item_pipe = 0,
    item_recipe_urn_of_shadows = 0,
    item_urn_of_shadows = 0,
    item_recipe_headdress = 0,
    item_headdress = 0,
    item_recipe_sheepstick = 0,
    item_sheepstick = 0,
    item_recipe_orchid = 0,
    item_orchid = 0,
    item_recipe_bloodthorn = 0,
    item_bloodthorn = 0,
    item_recipe_echo_sabre = 0,
    item_echo_sabre = 0,
    item_recipe_cyclone = 0,
    item_cyclone = 0,
    item_recipe_aether_lens = 0,
    item_aether_lens = 0,
    item_recipe_force_staff = 0,
    item_force_staff = 0,
    item_recipe_hurricane_pike = 0,
    item_hurricane_pike = 0,
    item_recipe_dagon = 0,
    item_recipe_dagon_2 = 0,
    item_recipe_dagon_3 = 0,
    item_recipe_dagon_4 = 0,
    item_recipe_dagon_5 = 0,
    item_dagon = 0,
    item_dagon_2 = 0,
    item_dagon_3 = 0,
    item_dagon_4 = 0,
    item_dagon_5 = 0,
    item_recipe_necronomicon = 0,
    item_recipe_necronomicon_2 = 0,
    item_recipe_necronomicon_3 = 0,
    item_necronomicon = 0,
    item_necronomicon_2 = 0,
    item_necronomicon_3 = 0,
    item_recipe_ultimate_scepter = 0,
    item_ultimate_scepter = 0,
    item_recipe_refresher = 0,
    item_refresher = 0,
    item_recipe_assault = 0,
    item_assault = 0,
    item_recipe_heart = 0,
    item_heart = 0,
    item_recipe_black_king_bar = 0,
    item_black_king_bar = 0,
    item_aegis = 0,
    item_recipe_shivas_guard = 0,
    item_shivas_guard = 0,
    item_recipe_bloodstone = 0,
    item_bloodstone = 0,
    item_recipe_sphere = 0,
    item_sphere = 0,
    item_recipe_lotus_orb = 0,
    item_lotus_orb = 0,
    item_recipe_vanguard = 0,
    item_vanguard = 0,
    item_recipe_crimson_guard = 0,
    item_crimson_guard = 0,
    item_recipe_blade_mail = 0,
    item_blade_mail = 0,
    item_recipe_soul_booster = 0,
    item_soul_booster = 0,
    item_recipe_hood_of_defiance = 0,
    item_hood_of_defiance = 0,
    item_recipe_rapier = 0,
    item_rapier = 0,
    item_recipe_monkey_king_bar = 0,
    item_monkey_king_bar = 0,
    item_recipe_radiance = 0,
    item_radiance = 0,
    item_recipe_butterfly = 0,
    item_butterfly = 0,
    item_recipe_greater_crit = 0,
    item_greater_crit = 0,
    item_recipe_basher = 0,
    item_basher = 0,
    item_recipe_bfury = 0,
    item_bfury = 0,
    item_recipe_manta = 0,
    item_manta = 0,
    item_recipe_lesser_crit = 0,
    item_lesser_crit = 0,
    item_recipe_dragon_lance = 0,
    item_dragon_lance = 0,
    item_recipe_armlet = 0,
    item_armlet = 0,
    item_recipe_invis_sword = 0,
    item_invis_sword = 0,
    item_recipe_silver_edge = 0,
    item_silver_edge = 0,
    item_recipe_sange_and_yasha = 0,
    item_sange_and_yasha = 0,
    item_recipe_satanic = 0,
    item_satanic = 0,
    item_recipe_mjollnir = 0,
    item_mjollnir = 0,
    item_recipe_skadi = 0,
    item_skadi = 0,
    item_recipe_sange = 0,
    item_sange = 0,
    item_recipe_helm_of_the_dominator = 0,
    item_helm_of_the_dominator = 0,
    item_recipe_maelstrom = 0,
    item_maelstrom = 0,
    item_recipe_desolator = 0,
    item_desolator = 0,
    item_recipe_yasha = 0,
    item_yasha = 0,
    item_recipe_mask_of_madness = 0,
    item_mask_of_madness = 0,
    item_recipe_diffusal_blade = 0,
    item_recipe_diffusal_blade_2 = 0,
    item_diffusal_blade = 0,
    item_diffusal_blade_2 = 0,
    item_recipe_ethereal_blade = 0,
    item_ethereal_blade = 0,
    item_recipe_soul_ring = 0,
    item_soul_ring = 0,
    item_recipe_arcane_boots = 0,
    item_arcane_boots = 0,
    item_recipe_octarine_core = 0,
    item_octarine_core = 0,
    item_orb_of_venom = 0,
    item_blight_stone = 0,
    item_recipe_ancient_janggo = 0,
    item_ancient_janggo = 0,
    item_recipe_medallion_of_courage = 0,
    item_medallion_of_courage = 0,
    item_recipe_solar_crest = 0,
    item_solar_crest = 0,
    item_smoke_of_deceit = 0,
    item_tome_of_knowledge = 0,
    item_recipe_veil_of_discord = 0,
    item_veil_of_discord = 0,
    item_recipe_guardian_greaves = 0,
    item_guardian_greaves = 0,
    item_recipe_rod_of_atos = 0,
    item_rod_of_atos = 0,
    item_recipe_iron_talon = 0,
    item_iron_talon = 0,
    item_recipe_abyssal_blade = 0,
    item_abyssal_blade = 0,
    item_recipe_heavens_halberd = 0,
    item_heavens_halberd = 0,
    item_recipe_ring_of_aquila = 0,
    item_ring_of_aquila = 0,
    item_recipe_tranquil_boots = 0,
    item_tranquil_boots = 0,
    item_shadow_amulet = 0,
    item_recipe_glimmer_cape = 0,
    item_glimmer_cape = 0,
    item_halloween_candy_corn = 0,
    item_mystery_hook = 0,
    item_mystery_arrow = 0,
    item_mystery_missile = 0,
    item_mystery_toss = 0,
    item_mystery_vacuum = 0,
    item_halloween_rapier = 0,
    item_greevil_whistle = 0,
    item_greevil_whistle_toggle = 0,
    item_present = 0,
    item_winter_stocking = 0,
    item_winter_skates = 0,
    item_winter_cake = 0,
    item_winter_cookie = 0,
    item_winter_coco = 0,
    item_winter_ham = 0,
    item_winter_kringle = 0,
    item_winter_mushroom = 0,
    item_winter_greevil_treat = 0,
    item_winter_greevil_garbage = 0,
    item_winter_greevil_chewy = 0,
    item_river_painter = 0,
    item_river_painter2 = 0,
    item_river_painter3 = 0,
    item_river_painter4 = 0,
    item_river_painter5 = 0,
    item_river_painter6 = 0,
    item_platemail = 1,
    item_ultimate_orb = 1,
    item_talisman_of_evasion = 1,
    item_demon_edge = 1,
    item_eagle = 1,
    item_reaver = 1,
    item_relic = 1,
    item_hyperstone = 1,
    item_mystic_staff = 1,
    item_energy_booster = 1,
    item_point_booster = 1,
    item_vitality_booster = 1,
}

return item_shop_availability