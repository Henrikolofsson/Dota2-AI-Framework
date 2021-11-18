-- imports
local Python_AI_thinking = require "python_AI.python_AI_thinking"



-- Python_AI_setup
local Python_AI_setup = {}



---@param heroes table
function Python_AI_setup:Set_context_think_for_heroes(heroes)
    Timers:CreateTimer(
        "UpdateForTeam" .. tostring(heroes[1]:GetTeam()),
        {
            ---@return number
            callback = function()
                Python_AI_thinking:On_think(heroes)
                return 0.33
            end
        }
    )
end

---@param radiant_heroes table
---@param dire_heroes table
function Python_AI_setup:Initialize_bot_thinking(radiant_heroes, dire_heroes)
    self:Set_statistics_collection(radiant_heroes, dire_heroes)

    self:Set_context_think_for_heroes(radiant_heroes)
    if not Settings.should_dire_be_native_bots then
        self:Set_context_think_for_heroes(dire_heroes)
    end
end

---@param radiant_heroes table
---@param dire_heroes table
function Python_AI_setup:Set_statistics_collection(radiant_heroes, dire_heroes)
    --[[
        Creates a timer that runs the Python_AI_thinking:Collect_and_send_statistics
        function once every @collection_interval seconds.
    ]]
    local collection_interval = 5

    Timers:CreateTimer(
        "CollectStatistics",
        {
            ---@return number
            callback = function()
                Python_AI_thinking:Collect_and_send_statistics(radiant_heroes, dire_heroes)
                return collection_interval
            end
        }
    )
end


return Python_AI_setup