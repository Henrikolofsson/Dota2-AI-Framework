-- imports
local Settings_setup = require "init.settings_setup"
local Event_controller = require "listeners.event_controller"
local Match_setup_controller = require "init.match_setup.match_setup_controller"
local Hero_setup_controller = require "init.hero_setup.hero_setup_controller"
local Python_AI_controller = require "python_AI.python_AI_controller"
local Match_end_controller = require "match_end.match_end_controller"



-- constants
local ONE_SECOND_DELAY = 1.0
local ADMIN_PLAYER_ID = 0
local SPECTATOR_TEAM = 1



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

function Main_controller.Select_heroes_after_populate_game()
    Hero_setup_controller:Select_heroes()
    Timers:CreateTimer(Main_controller.Initialize_bot_thinking)
end

function Main_controller.On_hero_selection_game_state()
    Match_setup_controller:Populate_game()
    Timers:CreateTimer({
        endTime = 1.0,
        callback = Main_controller.Select_heroes_after_populate_game
    })
end

function Main_controller.On_pre_game_state()
    if not Settings.should_have_pre_game_delay then
        Match_setup_controller:Force_game_start()
    end
end

function Main_controller.On_post_game_state()
    Match_end_controller:Handle_match_end()
end

function Main_controller.On_player_chat(chat_text)
    if chat_text == "end" then
        Match_end_controller:Handle_match_end()
    elseif chat_text == "restart" then
        Match_end_controller:Handle_restart_game()
    elseif chat_text == "exit" then
        Match_end_controller:Handle_exit()
    end
end

function Main_controller:Put_admin_on_spectator_team()
    PlayerResource:GetPlayer(ADMIN_PLAYER_ID):SetTeam(SPECTATOR_TEAM)
end

function Main_controller.Run_after_settings()
    if Settings.spectator_mode then
        Main_controller:Put_admin_on_spectator_team()
    end
    Event_controller:Initialize_listeners()
    Match_setup_controller:Initialize_match_setup()
    Event_controller:Add_on_hero_selection_game_state_listener(Main_controller.On_hero_selection_game_state)
    Event_controller:Add_on_pre_game_state_listener(Main_controller.On_pre_game_state)
    Event_controller:Add_on_in_progress_game_state_listener(Main_controller.in_progress_game_state_callbacks)
    Event_controller:Add_on_post_game_state_listener(Main_controller.On_post_game_state)
    Event_controller:Add_on_player_chat_listener(Main_controller.On_player_chat)
end

function Main_controller.Run()
    Settings_setup:Get_and_set_settings()
    Timers:CreateTimer({
        endTime = 1.0,
        callback = Main_controller.Run_after_settings
    })
end