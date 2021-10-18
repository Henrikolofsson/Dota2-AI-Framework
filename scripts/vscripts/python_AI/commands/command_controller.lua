local Command_controller = {}











-- A little help function that returns the shoptype for a given model name
-- Explanation: the defualt dota map models shops as entities of the class trigger_shop
-- that class has an attribute shoptype that's exactly what we need here
-- Unfortunately, that attribute does not seem to be exposed to the LUA API
-- Lucky for us, the trigger all have uniquely named model names, even though they don't appear on the map
-- we can use that to hard code the shoptypes ourselves
--
-- This may obviously break in between patches. It may not even work on themed maps
--
-- Note: Shops seem to have multiple triggers, with the exception of the radiant home shop
-- @returns the type for a given modelname: 0 for home, 1 for side and 2 for secret shop. -1 in the case of an error
function GetShopType(modelname)
    if modelname == "maps/dota/entities/unnamed_11.vmdl" then --radiant home
        return 0
    elseif modelname == "maps/dota/entities/unnamed_12.vmdl" then --dire home
        return 0
    elseif modelname == "maps/dota/entities/unnamed_18.vmdl" then --radiant secret
        return 2
    elseif modelname == "maps/dota/entities/unnamed_19.vmdl" then --dire secret
        return 2
    elseif modelname == "maps/dota/entities/unnamed_20.vmdl" then --dire side
        return 1
    elseif modelname == "maps/dota/entities/unnamed_23.vmdl" then --dire home
        return 0
    elseif modelname == "maps/dota/entities/unnamed_26.vmdl" then --radiant side
        return 1
    elseif modelname == "maps/dota/entities/unnamed_33.vmdl" then --radiant side
        return 2
    elseif modelname == "maps/dota/entities/unnamed_34.vmdl" then --dire secret
        return 2
    elseif modelname == "maps/dota/entities/unnamed_37.vmdl" then --dire side
        return 1
    elseif modelname == "maps/dota/entities/unnamed_39.vmdl" then --radiant side
        return 1
    else
        Warning("Unknown shop " .. modelname)
        return -1
    end
end

-- This function is generated from the game's item.txt
-- It returns truw if a given item name can be bought in a certain shop type
-- 0 = home, 1 = side, 2 = secret shop
function IsAvailableInShop(itemname, shoptype)
    if itemname == "item_blink" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_blades_of_attack" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_broadsword" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_chainmail" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_claymore" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_helm_of_iron_will" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_javelin" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mithril_hammer" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_platemail" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_quarterstaff" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_quelling_blade" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_faerie_fire" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_infused_raindrop" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_wind_lace" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ring_of_protection" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_stout_shield" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_recipe_moon_shard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_moon_shard" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_gauntlets" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_slippers" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_mantle" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_branches" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_belt_of_strength" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_boots_of_elves" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_robe" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_circlet" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ogre_axe" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_blade_of_alacrity" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_staff_of_wizardry" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ultimate_orb" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_gloves" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_lifesteal" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_ring_of_regen" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_sobi_mask" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_boots" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_gem" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_cloak" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_talisman_of_evasion" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_cheese" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_magic_stick" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_recipe_magic_wand" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_magic_wand" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ghost" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_clarity" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_enchanted_mango" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_flask" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dust" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_bottle" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_ward_observer" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ward_sentry" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_ward_dispenser" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ward_dispenser" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_tango" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_tango_single" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_courier" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_tpscroll" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_recipe_travel_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_travel_boots_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_travel_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_travel_boots_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_phase_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_phase_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_demon_edge" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_eagle" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_reaver" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_relic" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_hyperstone" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_ring_of_health" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_void_stone" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_mystic_staff" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_energy_booster" then
        return MatchShopType(true, true, shoptype)
    elseif itemname == "item_point_booster" then
        return MatchShopType(true, false, shoptype)
    elseif itemname == "item_vitality_booster" then
        return MatchShopType(true, true, shoptype)
    elseif itemname == "item_recipe_power_treads" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_power_treads" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_hand_of_midas" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_hand_of_midas" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_oblivion_staff" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_oblivion_staff" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_pers" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_pers" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_poor_mans_shield" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_poor_mans_shield" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_bracer" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_bracer" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_banana" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_recipe_wraith_band" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_wraith_band" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_null_talisman" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_null_talisman" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_mekansm" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mekansm" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_vladmir" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_vladmir" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_flying_courier" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_buckler" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_buckler" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_ring_of_basilius" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ring_of_basilius" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_pipe" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_pipe" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_urn_of_shadows" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_urn_of_shadows" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_headdress" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_headdress" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_sheepstick" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_sheepstick" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_orchid" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_orchid" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_bloodthorn" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_bloodthorn" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_echo_sabre" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_echo_sabre" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_cyclone" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_cyclone" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_aether_lens" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_aether_lens" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_force_staff" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_force_staff" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_hurricane_pike" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_hurricane_pike" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_dagon" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_dagon_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_dagon_3" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_dagon_4" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_dagon_5" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dagon" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dagon_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dagon_3" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dagon_4" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dagon_5" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_necronomicon" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_necronomicon_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_necronomicon_3" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_necronomicon" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_necronomicon_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_necronomicon_3" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_ultimate_scepter" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ultimate_scepter" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_refresher" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_refresher" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_assault" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_assault" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_heart" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_heart" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_black_king_bar" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_black_king_bar" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_aegis" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_shivas_guard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_shivas_guard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_bloodstone" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_bloodstone" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_sphere" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_sphere" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_lotus_orb" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_lotus_orb" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_vanguard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_vanguard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_crimson_guard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_crimson_guard" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_blade_mail" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_blade_mail" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_soul_booster" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_soul_booster" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_hood_of_defiance" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_hood_of_defiance" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_rapier" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_rapier" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_monkey_king_bar" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_monkey_king_bar" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_radiance" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_radiance" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_butterfly" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_butterfly" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_greater_crit" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_greater_crit" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_basher" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_basher" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_bfury" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_bfury" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_manta" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_manta" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_lesser_crit" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_lesser_crit" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_dragon_lance" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_dragon_lance" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_armlet" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_armlet" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_invis_sword" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_invis_sword" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_silver_edge" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_silver_edge" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_sange_and_yasha" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_sange_and_yasha" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_satanic" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_satanic" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_mjollnir" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mjollnir" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_skadi" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_skadi" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_sange" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_sange" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_helm_of_the_dominator" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_helm_of_the_dominator" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_maelstrom" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_maelstrom" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_desolator" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_desolator" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_yasha" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_yasha" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_mask_of_madness" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mask_of_madness" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_diffusal_blade" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_diffusal_blade_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_diffusal_blade" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_diffusal_blade_2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_ethereal_blade" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ethereal_blade" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_soul_ring" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_soul_ring" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_arcane_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_arcane_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_octarine_core" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_octarine_core" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_orb_of_venom" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_blight_stone" then
        return MatchShopType(false, true, shoptype)
    elseif itemname == "item_recipe_ancient_janggo" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ancient_janggo" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_medallion_of_courage" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_medallion_of_courage" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_solar_crest" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_solar_crest" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_smoke_of_deceit" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_tome_of_knowledge" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_veil_of_discord" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_veil_of_discord" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_guardian_greaves" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_guardian_greaves" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_rod_of_atos" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_rod_of_atos" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_iron_talon" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_iron_talon" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_abyssal_blade" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_abyssal_blade" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_heavens_halberd" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_heavens_halberd" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_ring_of_aquila" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_ring_of_aquila" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_tranquil_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_tranquil_boots" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_shadow_amulet" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_recipe_glimmer_cape" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_glimmer_cape" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_halloween_candy_corn" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mystery_hook" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mystery_arrow" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mystery_missile" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mystery_toss" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_mystery_vacuum" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_halloween_rapier" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_greevil_whistle" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_greevil_whistle_toggle" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_present" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_stocking" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_skates" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_cake" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_cookie" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_coco" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_ham" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_kringle" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_mushroom" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_greevil_treat" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_greevil_garbage" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_winter_greevil_chewy" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_river_painter" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_river_painter2" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_river_painter3" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_river_painter4" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_river_painter5" then
        return MatchShopType(false, false, shoptype)
    elseif itemname == "item_river_painter6" then
        return MatchShopType(false, false, shoptype)
    else
        Warning(itemname .. " is unknown")
        return false
    end
end

-- @param secret item requires secret shop
-- @param item is also available in side shop
-- @param shoptype the shop the hero is in in
-- @returns true if
--		the item requires a secret shop and the hero is in such,
--		or if the hero is in the side shop and its also available there
--		else
function MatchShopType(secret, side, shoptype)
    if shoptype == 2 then
        return secret
    elseif shoptype == 1 then
        return side
    else
        return not secret
    end
end

function PingNearestShop(eHero)
    --ping nearest shop
    local nearest = nil
    local nearestDistance = 21200 --15000 is the edge size of the map, so the longest distance is the hypotenuse = 21200
    eShop = Entities:FindByClassname(nil, "trigger_shop")
    while eShop ~= nil do
        local d = CalcDistanceBetweenEntityOBB(eHero, eShop)
        if nearestDistance > d then
            nearestDistance = d
            nearest = eShop:GetOrigin()
        end
        eShop = Entities:FindByClassname(eShop, "trigger_shop")
    end
    MinimapEvent(eHero:GetTeam(), eHero, nearest.x, nearest.y, DOTA_MINIMAP_EVENT_HINT_LOCATION, 1)
end
















local function BitAND(a, b) --Bitwise and
    local p, c = 1, 0
    while a > 0 and b > 0 do
        local ra, rb = a % 2, b % 2
        if ra + rb > 1 then
            c = c + p
        end
        a, b, p = (a - ra) / 2, (b - rb) / 2, p * 2
    end
    return c
end

-- Main entry function --
function Command_controller:ParseHeroCommand(eHero, result)
    -- local result = package.loaded["game/dkjson"].decode(reply)
    local command = result.command

    --TODO deal with abilities that the hero can interrupt
    local eAbility = eHero:GetCurrentActiveAbility()
    if eAbility then
        self:Noop(eHero, result)
        Warning("active not null")
        return
    end
    print(result)
    if command == "MOVE" then
        self:MoveTo(eHero, result)
    elseif command == "LEVELUP" then
        self:LevelUp(eHero, result)
    elseif command == "ATTACK" then
        self:Attack(eHero, result)
    elseif command == "CAST" then
        self:Cast(eHero, result)
    elseif command == "BUY" then
        self:Buy(eHero, result)
    elseif command == "SELL" then
        self:Sell(eHero, result)
    elseif command == "USE_ITEM" then
        self:UseItem(eHero, result)
    elseif command == "NOOP" then
        self:Noop(eHero, result)
    elseif command == "CAST_ABILITY_TOGGLE" then
        self:CastAbilityToggle(eHero, result)
    elseif command == "CAST_ABILITY_NO_TARGET" then
        self:CastAbilityNoTarget(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_POINT" then
        self:CastAbilityTargetPoint(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_AREA" then
        self:CastAbilityTargetArea(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT" then
        self:CastAbilityTargetUnit(eHero, result)
    elseif command == "CAST_ABILITY_VECTOR_TARGETING" then
        self:CastAbilityVectorTargeting(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT_AOE" then
        self:CastAbilityTargetUnitAOE(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_COMBO_TARGET_POINT_UNIT" then
        self:CastAbilityComboTargetPointUnit(eHero, result)
    else
        self.Error = true
        Warning(eHero:GetName() .. " sent invalid command " .. reply)
    end
end


-- Buying items --
function Command_controller:Buy(eHero, result)
    local itemName = result.item
    local itemCost = GetItemCost(itemName)

    if eHero:GetGold() < itemCost then
        Warning(eHero:GetName() .. " tried to buy " .. itemName .. " but couldn't afford it")
        return
    end

    local targetSlot = -1
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_6, 1 do
        if not eHero:GetItemInSlot(i) then
            targetSlot = i
            break
        end
    end

    --TODO item availability is missing

    if targetSlot < 0 then
        Warning(eHero:GetName() .. " tried to buy " .. itemName .. " but has no space left")
        --TODO buy into stash
        return
    end

    local eShop = Entities:FindByClassnameWithin(nil, "trigger_shop", eHero:GetOrigin(), 0.01)
    if eShop then
        local shopType = GetShopType(eShop:GetModelName())

        if IsAvailableInShop(itemName, shopType) then
            local eItem = CreateItem(itemName, eHero, eHero)
            EmitSoundOn("General.Buy", eHero)
            eHero:AddItem(eItem)
            eHero:SpendGold(itemCost, DOTA_ModifyGold_PurchaseItem) --should the reason take DOTA_ModifyGold_PurchaseConsumable into account?
        else
            --TODO ping actually the right shop
            PingNearestShop(eHero)
            Warning("Shop is of type " .. shopType)
            return
        end
    else
        PingNearestShop(eHero)
        return
    end

    Say(nil, eHero:GetName() .. " bought " .. itemName, false)
end

function Command_controller:Sell(eHero, result)
    local slot = result.slot

    if eHero:CanSellItems() then
        local eItem = eHero:GetItemInSlot(slot)
        if eItem then
            --TODO GetCost does not return the value altered, i.e. halved
            EmitSoundOn("General.Sell", eHero)
            eHero:ModifyGold(eItem:GetCost(), true, DOTA_ModifyGold_SellItem) -- Claims sell-operation gives reliable gold. (Second param = true)
            eHero:RemoveItem(eItem)
        else
            Warning("No item in slot " .. slot)
        end
    else
        PingNearestShop(eHero)
        Warning("Bot tried to sell item outside shop")
    end
end

function Command_controller:Noop(eHero, result)
    --Noop
end

function Command_controller:MoveTo(eHero, result)
    eHero:MoveToPosition(Vector(result.x, result.y, result.z))
    Say(nil, eHero:GetName() .. " moving to " .. result.x .. ", " .. result.y .. ", " .. result.z, false)
end

function Command_controller:LevelUp(eHero, result)
    local abilityPoints = eHero:GetAbilityPoints()
    if abilityPoints <= 0 then
        Warning(eHero:GetName() .. " has no ability points. Why am I levelling up?")
        return
    end

    local abilityIndex = result.abilityIndex

    local ability = eHero:GetAbilityByIndex(abilityIndex)
    if ability:GetLevel() == ability:GetMaxLevel() then
        Warning(eHero:GetName() .. ": " .. ability:GetName() .. " is maxed out")
        return
    end
    ability:UpgradeAbility(false)
    eHero:SetAbilityPoints(abilityPoints - 1) --UpgradeAbility doesn't decrease the ability points
    Say(nil, eHero:GetName() .. " levelled up ability " .. abilityIndex, false)
end

function Command_controller:Attack(eHero, result)
    --Might want to check attack range
    --eHero:PerformAttack(EntIndexToHScript(result.target), true, true, false, true)
    eHero:MoveToTargetToAttack(EntIndexToHScript(result.target))
    Say(nil, eHero:GetName() .. " attacking " .. result.target, false)
end

function Command_controller:Cast(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)

    if eAbility and eAbility ~= nil then
        self:UseAbility(eHero, eAbility)
    end
end

function Command_controller:UseItem(eHero, result)
    local slot = result.slot
    local eItem = eHero:GetItemInSlot(slot)
    Warning("Hero" .. eHero:GetName() .. "is attempting to use item " .. eItem:GetName())
    if eItem then
        self:UseAbility(eHero, eItem)
    else
        Warning("Bot tried to use item in empty slot")
    end
end

function Command_controller:CastAbilityToggle(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        -- eAbility:OnToggle()
        eHero:CastAbilityToggle(eAbility, player)
    end
end

function Command_controller:CastAbilityNoTarget(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityNoTarget(eAbility, player)
    end
end

function Command_controller:CastAbilityTargetPoint(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
    end
end

function Command_controller:CastAbilityTargetArea(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
    end
end

function Command_controller:CastAbilityTargetUnit(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        local target = EntIndexToHScript(result.target)
        eHero:CastAbilityOnTarget(target, eAbility, player)
    end
end

function Command_controller:CastAbilityVectorTargeting(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
    end
end

function Command_controller:CastAbilityTargetUnitAOE(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        local target = EntIndexToHScript(result.target)
        eHero:CastAbilityOnTarget(target, eAbility, player)
    end
end

function Command_controller:CastAbilityComboTargetPointUnit(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local behavior = eAbility:GetBehavior()
        local player = eHero:GetPlayerOwnerID()
        if (BitAND(behaviour, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET)) then
            local target = EntIndexToHScript(result.target)
            eHero:CastAbilityOnTarget(target, eAbility, player)
        elseif (BitAND(behaviour, DOTA_ABILITY_BEHAVIOR_POINT)) then
            eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
        end
    end
end

function Command_controller:SetupAbility(eHero, eAbility)
    local level = eAbility:GetLevel()
    local manaCost = eAbility:GetManaCost(level)
    if eHero:GetMana() < manaCost then
        Warning("Bot tried to use ability without mana")
        return false
    elseif eAbility:GetCooldownTimeRemaining() > 0 then
        Warning("Bot tried to use ability still on cooldown")
        return false
    end
    return true
end

function Command_controller:UseAbility(eHero, eAbility)
    local level = eAbility:GetLevel()
    local manaCost = eAbility:GetManaCost(level)
    local player = eHero:GetPlayerOwnerID()
    local behavior = eAbility:GetBehavior()

    if level == 0 then
        Warning("Bot tried to use ability without level")
        return
    end

    if eHero:GetMana() < manaCost then
        Warning("Bot tried to use ability without mana")
    elseif eAbility:GetCooldownTimeRemaining() > 0 then
        Warning("Bot tried to use ability still on cooldown")
    else
        if not eAbility:IsItem() then
            eAbility:StartCooldown(eAbility:GetCooldown(level))
            eAbility:PayManaCost()
            eAbility:OnSpellStart()
        end

        --There is some logic missing here to check for range and make the hero face the right direction
        if (BitAND(behavior, DOTA_ABILITY_BEHAVIOR_NO_TARGET)) then
            Say(nil, eHero:GetName() .. " casting " .. eAbility:GetName(), false)
            eHero:CastAbilityNoTarget(eAbility, player)
        elseif (BitAND(behavior, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET)) then
            local target = EntIndexToHScript(result.target)
            if target:IsAlive() then
                Say(nil, eHero:GetName() .. " casting " .. eAbility:GetName() .. " on unit " .. target:GetName(), false)
                eHero:CastAbilityOnTarget(target, eAbility, player)
            end
        elseif (BitAND(behavior, DOTA_ABILITY_BEHAVIOR_POINT)) then
            Say(
                nil,
                eHero:GetName() ..
                    " casting " .. eAbility:GetName() .. " on " .. result.x .. ", " .. result.y .. ", " .. result.z,
                false
            )
            eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
        else
            Warning(eHero:GetName() .. " sent invalid cast command " .. behavior)
            self._Error = true
        end
    end
end


return Command_controller