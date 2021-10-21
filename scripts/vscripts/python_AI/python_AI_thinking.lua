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
    local all_entities = World_data_builder:Get_all_entities(heroes[1])

    Update_handler:Update(all_entities, heroes, self.On_update)
end



return Python_AI_thinking