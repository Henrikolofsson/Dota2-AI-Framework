-- imports
local Python_AI_thinking = require "python_AI.python_AI_thinking"



-- Bot_thinking_setup
local Python_AI_setup = {}
Python_AI_setup.hero_setup = nil



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
function Python_AI_setup:Set_context_think_for_heroes(heroes)
    for _index, hero in ipairs(heroes) do
        Python_AI_setup:Set_context_think_for_hero(hero)
    end
end

function Python_AI_setup:Initialize_bot_thinking(radiant_heroes, dire_heroes)
    Python_AI_setup:Set_context_think_for_heroes(radiant_heroes)
    Python_AI_setup:Set_context_think_for_heroes(dire_heroes)
end



return Python_AI_setup