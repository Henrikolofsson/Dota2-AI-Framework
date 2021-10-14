-- imports
local Python_AI_thinking = require "python_AI.python_AI_thinking"
local Dota2AI = require "python_AI._json_helpers"



-- Python_AI_setup
local Python_AI_setup = {}



---@param hero table
function Python_AI_setup:Set_context_think_for_hero(hero)
    hero:SetContextThink(
        "Python_AI_thinking:OnThink",
        function()
            return Python_AI_thinking:OnThink(hero)
        end,
        0.33
    )
end

---@param heroes table
function Python_AI_setup:Set_context_think_for_heroes(heroes, route)
    Timers:CreateTimer(
        function()

            local world = Dota2AI:JSONWorld(heroes[1])

            local body = package.loaded["game/dkjson"].encode({["world"] = world})
        
            local request = CreateHTTPRequestScriptVM("POST", "http://localhost:8080/api/" .. route)
            request:SetHTTPRequestHeaderValue("Accept", "application/json")
            request:SetHTTPRequestHeaderValue("X-Jersey-Tracing-Threshold", "VERBOSE")
            request:SetHTTPRequestRawPostBody("application/json", body)
            request:Send(
                function(result)
                    local actions = package.loaded["game/dkjson"].decode(result["Body"])
                    if actions then
                        for strhero, cmd in pairs(actions) do
                            print("Commands for " .. strhero)
                            DeepPrintTable(cmd)
                        end
                    end
                end
            )

            return 0.33
        end
    )
end

---@param radiant_heroes table
---@param dire_heroes table
function Python_AI_setup:Initialize_bot_thinking(radiant_heroes, dire_heroes)
    Python_AI_setup:Set_context_think_for_heroes(radiant_heroes, "radiant_update")
    Python_AI_setup:Set_context_think_for_heroes(dire_heroes, "dire_update")
end



return Python_AI_setup