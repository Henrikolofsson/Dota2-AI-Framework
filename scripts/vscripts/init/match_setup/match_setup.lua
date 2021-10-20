-- Match_setup
local Match_setup = {}

function Match_setup:Set_bot_thinking_enabled()
    ---@type table
    local GameMode = GameRules:GetGameModeEntity()
    GameMode:SetBotThinkingEnabled(true)
end

function Match_setup:Remove_all_game_rule_starting_delays()
    GameRules:SetHeroSelectionTime(1.)
    GameRules:SetShowcaseTime(1.)
    GameRules:SetStrategyTime(1.)
    GameRules:SetCustomGameSetupTimeout(1.)
    if Settings.should_have_pre_game_delay then
        GameRules:SetPreGameTime(90.)
    end
end

function Match_setup:Grant_global_vision()
    if Settings.grant_global_vision then
        SendToServerConsole("dota_all_vision 1")
    else
        SendToServerConsole("dota_all_vision 0")
    end
end

function Match_setup:Auto_launch_custom_game()
    Timers:CreateTimer({
        endTime = 1.,
        callback = function()
            GameRules:FinishCustomGameSetup()
        end
    })
end

function Match_setup:Populate_game()
    SendToServerConsole("dota_create_fake_clients")
end

function Match_setup:Force_game_start()
    SendToServerConsole("dota_dev forcegamestart")
end

function Match_setup:Run()
    self:Auto_launch_custom_game()
    if Settings.should_dire_be_native_bots then
        self:Set_bot_thinking_enabled()
    end
    self:Remove_all_game_rule_starting_delays()
    self:Grant_global_vision()
end

return Match_setup