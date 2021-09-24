Event_listeners = require "listeners/event_listener"

local Setup = {}

function Setup:SetBotThinkingEnabled()
    local GameMode = GameRules:GetGameModeEntity()
    GameMode:SetBotThinkingEnabled(true)
end

function Setup:Remove_all_game_rule_starting_delays()
    GameRules:SetShowcaseTime(1)
    GameRules:SetStrategyTime(1)
    GameRules:SetHeroSelectionTime(1)
    GameRules:SetCustomGameSetupTimeout(1)
    GameRules:SetPreGameTime(5)
    --Game.SetRemainingSetupTime(4);
end

function Setup:Grant_global_vision()
    SendToServerConsole("dota_all_vision 1")
end

function Setup:Auto_launch_custom_game()
    Timers:CreateTimer({
        endTime = 1,
        callback = function()
            GameRules:FinishCustomGameSetup()
        end
    })
end

function Setup:Developer_setups()
    Setup:SetBotThinkingEnabled()
    Setup:Remove_all_game_rule_starting_delays()
    Setup:Grant_global_vision()
end

function Setup:Add_listeners()
    Event_listeners:Add_on_game_rules_state_change()
end

function Setup:Run()
    print("Running setup")

    Setup:Auto_launch_custom_game()
    Setup:Developer_setups()

    Setup:Add_listeners()
end

return Setup