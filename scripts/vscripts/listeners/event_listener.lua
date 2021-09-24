Game_states = require "game_states/game_states"

local Event_listener = {}

function Event_listener:Add_on_game_rules_state_change()
    ListenToGameEvent("game_rules_state_change", Dynamic_Wrap( Event_listener, "On_game_rules_state_change" ), self)
end

function Event_listener:On_game_rules_state_change()
    Game_states:On_game_rules_state_change()
end

return Event_listener