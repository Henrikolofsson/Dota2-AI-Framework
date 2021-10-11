-- imports
local Settings_setup = require "init.settings_setup"
local Event_controller = require "listeners.event_controller"
local Match_setup_controller = require "init.match_setup.match_setup_controller"
local Hero_setup_controller = require "init.hero_setup.hero_setup_controller"
local Python_AI_controller = require "python_AI.python_AI_controller"



-- constants
local ONE_SECOND_DELAY = 1.0



-- Main_controller
function Main_controller.Initialize_bot_thinking()
    if not Hero_setup_controller:All_players_have_chosen_hero() then
        return ONE_SECOND_DELAY
    end

    Python_AI_controller:Initialize_bot_thinking(
        Hero_setup_controller:Get_radiant_heroes(),
        Hero_setup_controller:Get_dire_heroes()
    )
end

function Main_controller.On_hero_selection_game_state()
    Match_setup_controller:Populate_game()
    Hero_setup_controller:Select_heroes()
    Timers:CreateTimer(Main_controller.Initialize_bot_thinking)
end

function Main_controller.On_pre_game_state()
    if not Settings.SHOULD_HAVE_PRE_GAME_DELAY then
        Match_setup_controller:Force_game_start()
    end
end

function Main_controller.Run()
    Settings_setup:Get_and_set_settings()
    Event_controller:Initialize_listeners()
    Match_setup_controller:Initialize_match_setup()
    Event_controller:Add_on_hero_selection_game_state_listener(Main_controller.On_hero_selection_game_state)
    Event_controller:Add_on_pre_game_state_listener(Main_controller.On_pre_game_state)
end