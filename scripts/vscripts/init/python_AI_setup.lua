-- imports
local Python_AI_thinking = require "python_AI.python_AI_thinking"



-- constants
local ONE_SECOND_DELAY = 1.0



-- Bot_thinking_setup
local Python_AI_setup = {}
Python_AI_setup.hero_setup = nil



---@param hero table
function Python_AI_setup:Set_context_think_for_hero(hero)
    hero:SetContextThink(
        function()
            return Python_AI_thinking:OnThink(hero)
        end
    )
end

---@param heroes table
function Python_AI_setup:Set_context_think_for_heroes(heroes)
    for _index, hero in ipairs(heroes) do
        Python_AI_setup:Set_context_think_for_hero(hero)
    end
end

function Python_AI_setup:Initialize_bot_thinking_when_all_heroes_chosen()
    local hero_setup = Python_AI_setup.hero_setup

    if not hero_setup:All_players_have_chosen_hero() then
        return ONE_SECOND_DELAY
    end

    Python_AI_setup:Set_context_think_for_heroes(hero_setup.radiant_heroes)
    Python_AI_setup:Set_context_think_for_heroes(hero_setup.dire_heroes)
end

---@param hero_setup table
function Python_AI_setup:Initialize_bot_thinking(hero_setup)
    Python_AI_setup.hero_setup = hero_setup
    Timers:CreateTimer(Python_AI_setup.Initialize_bot_thinking_when_all_heroes_chosen)
end

return Python_AI_setup