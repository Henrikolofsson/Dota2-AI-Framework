local Hero_setup_controller = require "init.hero_setup.hero_setup_controller"
local Utilities = require "utilities.utilities"

local Statistics = {}

-- Collects the statistics that are sent to the /api/game_ended route
---@param game_number integer
---@return table
function Statistics:Collect_end_game(game_number)
    local stats = {}
    local radiant_heroes = Hero_setup_controller:Get_radiant_heroes()
    local dire_heroes = Hero_setup_controller:Get_dire_heroes()
    local heroes = Utilities:Concat_lists(radiant_heroes, dire_heroes)

    stats["game_number"] = game_number
    stats["end_stats"] = {}
    stats["end_stats"]["game_time"] = GameRules:GetDOTATime(false, true)
    stats["end_stats"]["radiant"] = {}
    stats["end_stats"]["dire"] = {}

    for _, hero in ipairs(heroes) do
        local hero_stats = Statistics:Hero_end_game_stats(hero)
        local hero_name = hero:GetName()
        local team = hero:GetTeam() == 2 and "radiant" or "dire"
        stats["end_stats"][team][hero_name] = hero_stats
    end

    return stats
end

-- Collects end game statistics for a specific hero.
---@param hero CDOTA_BaseNPC_Hero
---@return table
function Statistics:Hero_end_game_stats(hero)
    local stats = {}
    stats["id"] = hero:GetPlayerID()
    stats["kills"] = hero:GetKills()
    stats["deaths"] = hero:GetDeaths()
    stats["assists"] = hero:GetAssists()
    stats["net_worth"] = 0 -- ?
    stats["items"] = 0 -- ??
    stats["backpack"] = 0 -- ??
    stats["buffs"] = 0 -- ??
    stats["last_hits"] = hero:GetLastHits()
    stats["denies"] = hero:GetDenies()
    stats["gold_per_min"] = 0 -- ??
    stats["bounty_runes"] = 0 -- ??
    stats["xpm"] = 0 -- ??
    return stats
end



-- todo: Refactor and put the other statistics functions here from Python_AI.


return Statistics