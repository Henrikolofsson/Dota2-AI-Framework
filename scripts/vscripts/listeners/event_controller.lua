-- imports
local Game_state_controller = require "game_states.game_state_controller"



-- locals
local hero_selection_game_state_callbacks = {}
local pre_game_state_callbacks = {}
local in_progress_game_state_callbacks = {}

---@param callbacks table
local function Run_callbacks(callbacks)
    for _index, callback in ipairs(callbacks) do
        callback()
    end
end



-- Event_controller
local Event_controller = {}



function Event_controller:Initialize_listeners()
    ListenToGameEvent("game_rules_state_change", Dynamic_Wrap( Event_controller, "On_game_state_change" ), self)
end



function Event_controller:On_game_state_change()
    if Game_state_controller:Is_hero_selection_state() then
        Run_callbacks(hero_selection_game_state_callbacks)

    elseif Game_state_controller:Is_pre_game_state() then
        Run_callbacks(pre_game_state_callbacks)

    elseif Game_state_controller:Is_game_in_progress_state() then
        Run_callbacks(in_progress_game_state_callbacks)

    end
end



---@param callback function
function Event_controller:Add_on_hero_selection_game_state_listener(callback)
    table.insert(hero_selection_game_state_callbacks, callback)
end

---@param callback function
function Event_controller:Add_on_pre_game_state_listener(callback)
    table.insert(pre_game_state_callbacks, callback)
end

---@param callback function
function Event_controller:Add_on_in_progress_game_state_listener(callback)
    table.insert(in_progress_game_state_callbacks, callback)
end



return Event_controller