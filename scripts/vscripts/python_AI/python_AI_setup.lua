-- imports
local Python_AI_thinking = require "python_AI.python_AI_thinking"
local World_data_builder = require "python_AI.world_data_builder"



-- Python_AI_setup
local Python_AI_setup = {}



---@param heroes table
function Python_AI_setup:Set_context_think_for_heroes(heroes)
    Timers:CreateTimer(
        function()
            Python_AI_thinking:On_think(heroes)
            return 0.33
        end
    )
end

---@param radiant_heroes table
---@param dire_heroes table
function Python_AI_setup:Initialize_bot_thinking(radiant_heroes, dire_heroes)
    Python_AI_setup:Set_context_think_for_heroes(radiant_heroes)
    Python_AI_setup:Set_context_think_for_heroes(dire_heroes)
end



return Python_AI_setup