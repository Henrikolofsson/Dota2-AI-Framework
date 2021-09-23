local Setup = {}

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

function Setup:Developer_setups()
    Setup:Remove_all_game_rule_starting_delays()
    Setup:Grant_global_vision()
end

return Setup