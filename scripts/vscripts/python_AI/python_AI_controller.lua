-- imports
local Python_AI_setup = require "python_AI.python_AI_setup"



-- Python_AI_controller
local Python_AI_controller = {}



---@param radiant_heroes table
---@param dire_heroes table
function Python_AI_controller:Initialize_bot_thinking(radiant_heroes, dire_heroes)
    Python_AI_setup:Initialize_bot_thinking(radiant_heroes, dire_heroes)
end



return Python_AI_controller