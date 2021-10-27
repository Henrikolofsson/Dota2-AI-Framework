-- imports
local World_data_builder = require "python_AI.world_data_builder"
local Update_handler = require "python_AI.update_handler"
local Command_controller = require "python_AI.commands.command_controller"



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


return Python_AI_thinking