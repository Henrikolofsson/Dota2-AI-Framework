-- imports
local World_data_builder = require "python_AI.world_data_builder"
local Update_handler = require "python_AI.update_handler"
local Command_controller = require "python_AI.commands.command_controller"



-- Python_AI_thinking
local Python_AI_thinking = {}

local printcount = 0

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
                    Command_controller:ParseHeroCommand(hero, cmd)
                end
            end
        end
    end
end

---@param heroes table
---@return number
function Python_AI_thinking:On_think(heroes)
    local all_entities = World_data_builder:Get_all_entities(heroes[1])

    -- if heroes[1]:GetTeam() == DOTA_TEAM_GOODGUYS then
    --     print(
    --         heroes[1]:GetName() .. " has tower aggro: " .. tostring(all_entities[heroes[1]:entindex()].hasTowerAggro)
    --     )
    -- end

    printcount = printcount + 1
    if printcount == 60 and heroes[1]:GetTeam() == DOTA_TEAM_GOODGUYS then
        Timers:CreateTimer({
            endTime = 5.0,
            callback = function()
                local tree_count = 0
                print("Can be seen by " .. heroes[1]:GetName() .. ":")
                for entity_index, entity in pairs(all_entities) do
                    if entity.type == "Tree" then
                        tree_count = tree_count + 1
                    else
                        print("type:")
                        print("--- " .. entity.type)
                        print("------ " .. entity.name)
                    end
                end
                print("number of trees: " .. tostring(tree_count))
            end
        })
    end

    Update_handler:Update(all_entities, heroes, self.On_update)
end



return Python_AI_thinking