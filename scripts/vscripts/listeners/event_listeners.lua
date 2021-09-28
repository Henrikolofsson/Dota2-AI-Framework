local Game_states = require "game_states.game_states"
local Hero_setup = require "init.hero_setup"

local Event_listeners = {}

function Event_listeners:Add_on_game_rules_state_change(Match_setup)
    Event_listeners.Match_setup = Match_setup
    ListenToGameEvent("game_rules_state_change", Dynamic_Wrap( Event_listeners, "On_game_rules_state_change" ), self)
end

function Event_listeners:On_game_rules_state_change()
    if Game_states:Is_hero_selection_state() then
        self.Match_setup:Populate_game()
        Hero_setup:Select_heroes()

    elseif Game_states:Is_pre_game_state() then
        GameRules:ForceGameStart()

    elseif Game_states:Is_game_in_progress_state() then
    end
end

return Event_listeners