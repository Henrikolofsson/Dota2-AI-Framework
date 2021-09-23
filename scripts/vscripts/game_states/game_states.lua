Setup = require "init/setup"

Game_states = {}

function Game_states:Is_hero_selection_state()
    return GameRules:State_Get() == DOTA_GAMERULES_STATE_HERO_SELECTION
end

function Game_states:Is_pre_game_state()
    return GameRules:State_Get() == DOTA_GAMERULES_STATE_PRE_GAME
end

function Game_states:Is_game_in_progress_state()
    return GameRules:State_Get() == DOTA_GAMERULES_STATE_GAME_IN_PROGRESS
end

function Game_states:On_game_rules_state_change()

    if Game_states:Is_hero_selection_state() then
        print("Entered game selection state")
        Setup:Select_heroes()

    elseif Game_states:Is_pre_game_state() then
        print("Entered pre game state")
        GameRules:ForceGameStart()

    elseif Game_states:Is_game_in_progress_state() then
        print("Entered game in progress state")
    end

end

return Game_states