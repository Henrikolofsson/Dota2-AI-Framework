local Event_listeners = require "listeners.event_listeners"

local Match_setup = {}

function Match_setup:SetBotThinkingEnabled()
    local GameMode = GameRules:GetGameModeEntity()
    GameMode:SetBotThinkingEnabled(true)
end

function Match_setup:Remove_all_game_rule_starting_delays()
    GameRules:SetShowcaseTime(1)
    GameRules:SetStrategyTime(1)
    GameRules:SetHeroSelectionTime(1)
    GameRules:SetCustomGameSetupTimeout(1)
    GameRules:SetPreGameTime(5)
    --Game.SetRemainingSetupTime(4);
end

function Match_setup:Grant_global_vision()
    SendToServerConsole("dota_all_vision 1")
end

function Match_setup:Auto_launch_custom_game()
    Timers:CreateTimer({
        endTime = 1,
        callback = function()
            GameRules:FinishCustomGameSetup()
        end
    })
end

function Match_setup:Add_listeners()
    Event_listeners:Add_on_game_rules_state_change(self)
end

function Match_setup:Populate_game()
    SendToServerConsole("dota_create_fake_clients")
end

function Match_setup:Run()
    Match_setup:Auto_launch_custom_game()
    Match_setup:SetBotThinkingEnabled()
    Match_setup:Remove_all_game_rule_starting_delays()
    Match_setup:Grant_global_vision()
    Match_setup:Add_listeners()
end

return Match_setup