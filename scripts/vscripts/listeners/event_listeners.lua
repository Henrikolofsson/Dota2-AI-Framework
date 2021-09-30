-- imports
local Game_states = require "game_states.game_states"
local Hero_setup_controller = require "init.hero_setup.hero_setup_controller"
local Python_AI_setup = require "init.python_AI_setup"



-- Event_listeners
local Event_listeners = {}
Event_listeners.match_setup = nil

---@param match_setup table
function Event_listeners:Add_on_game_rules_state_change(match_setup)
    Event_listeners.match_setup = match_setup
    ListenToGameEvent("game_rules_state_change", Dynamic_Wrap( Event_listeners, "On_game_rules_state_change" ), self)
end

function Event_listeners:On_game_rules_state_change()
    if Game_states:Is_hero_selection_state() then
        self.match_setup:Populate_game()
        Hero_setup_controller:Select_heroes()
        Python_AI_setup:Initialize_bot_thinking(Hero_setup_controller)

    elseif Game_states:Is_pre_game_state() then
        self.match_setup:Force_game_start()

    elseif Game_states:Is_game_in_progress_state() then
    end
end

return Event_listeners