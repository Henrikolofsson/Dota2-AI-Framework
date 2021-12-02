-- imports
local World_data_builder = require "python_AI.world_data_builder"
local Update_handler = require "python_AI.update_handler"
local Command_controller = require "python_AI.commands.command_controller"
local Utilities = require "utilities.utilities"



-- Python_AI_thinking
local Python_AI_thinking = {}

---@param heroes table
---@param commands table
function Python_AI_thinking.On_update(heroes, commands)
    if not commands then
        return
    end
    for _index, hero in ipairs(heroes) do
        for _index, command in ipairs(commands) do
            for strhero, cmd in pairs(command) do
                if hero:GetName() == strhero then
                    if cmd.target ~= nil then
                        cmd.target = tonumber(cmd.target)
                    end
                    Command_controller:Parse_hero_command(hero, cmd)
                end
            end
        end
    end
end

---@param heroes table
---@return number
function Python_AI_thinking:On_think(heroes)
    Python_AI_thinking:Before_world_building(heroes)

    local all_entities = World_data_builder:Get_all_entities(heroes[1])

    Update_handler:Update(all_entities, heroes, self.On_update)
end

---@param heroes table
function Python_AI_thinking:Before_world_building(heroes)
    --[[
        Called before building the world data to ensure that
        certain aspects of the game world are in the correct
        state. For example, courier levels should be equal to
        hero levels (in Dota, couriers automatically level up
        with the hero, but this does not happen when the heroes
        are FakeClients)
    ]]
    for _, hero_entity in ipairs(heroes) do
        local player_id = hero_entity:GetPlayerOwnerID()
        local courier_entity = PlayerResource:GetPreferredCourierForPlayer(player_id)
        local hero_level = hero_entity:GetLevel()
        local courier_level = courier_entity:GetLevel()

        if courier_level < hero_level then
            -- The API "documentation" says that UpgradeCourier takes an int and
            -- upgrades the courier that number of times. This is not correct.
            -- UpgradeCourier sets the courier level to the integer that is passed
            -- to it and can even downgrade a courier. E.g., UpgradeCourier(1)
            -- on a level 3 courier will set it to level 1, not level 4.
            courier_entity:UpgradeCourier(hero_level)
        end
    end
end

---@param radiant_heroes table of radiant hero entities.
---@param dire_heroes table of dire hero entities.
function Python_AI_thinking:Collect_and_send_statistics(radiant_heroes, dire_heroes, game_number)
    --[[
        Collects game statistics and sends them to the statistics route on the
        Python web server.
    ]]
    local statistics = Python_AI_thinking:Collect_statistics(radiant_heroes, dire_heroes, game_number)
    Python_AI_thinking:Send_statistics(statistics)
end


---@param radiant_heroes table of radiant hero entities.
---@param dire_heroes table of dire hero entities.
function Python_AI_thinking:Collect_statistics(radiant_heroes, dire_heroes, game_number)
    local heroes = Utilities:Concat_lists(radiant_heroes, dire_heroes)
    local stats = {}
    local fields = {}

    stats["game_number"] = game_number

    -- General game statistics that are not tied to a particular hero.

    -- There is also GameRules:GetGameTime() but that one includes time in menus.
    -- Menu time is turned off in this command by setting the first argument to false.
    fields["game_time"] = GameRules:GetDOTATime(false, true)

    -- Hero specific stats.
    for i, hero in ipairs(heroes) do
        fields[(i - 1) .. "_id"] = hero:GetPlayerID()
        fields[(i - 1) .. "_team"] = hero:GetTeam()
        fields[(i - 1) .. "_name"] = hero:GetName()
        fields[(i - 1) .. "_gold"] = hero:GetGold()
    end

    stats["fields"] = fields

    return stats
end


---@param statistics table to be sent to the server.
function Python_AI_thinking:Send_statistics(statistics)
    local route = "http://localhost:8080/api/statistics"
    local body = package.loaded["game/dkjson"].encode(statistics)

    local request = CreateHTTPRequestScriptVM("POST", route)
    request:SetHTTPRequestHeaderValue("Accept", "application/json")
    request:SetHTTPRequestRawPostBody("application/json", body)
    request:Send(
        ---@param result table
        function(result)
            -- currently ignoring response.
        end
    )
end


return Python_AI_thinking