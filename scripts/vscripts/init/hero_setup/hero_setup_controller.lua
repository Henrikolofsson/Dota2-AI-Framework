-- imports
local Hero_selector = require "init.hero_setup.hero_selector"
local Party_collector = require "init.hero_setup.party_collector"
local Native_bot_setup = require "init.hero_setup.native_bot_setup"
local Utilities = require "utilities.utilities"



-- constants
local ONE_SECOND_DELAY = 1.



-- Hero_setup_controller
local Hero_setup_controller = {}
Hero_setup_controller.radiant_heroes = nil
Hero_setup_controller.dire_heroes = nil

---@return table
function Hero_setup_controller:Get_radiant_heroes()
    return self.radiant_heroes
end

---@return table
function Hero_setup_controller:Get_dire_heroes()
    return self.dire_heroes
end

---@return boolean
function Hero_setup_controller:All_players_have_chosen_hero()
    return Utilities:To_bool(self.radiant_heroes)
end

---@param picked_hero_names table
function Hero_setup_controller.Handle_radiant_party_response(picked_hero_names)
    local FROM_PLAYER_ID, TO_PLAYER_ID = 0, 4

    Hero_selector:Pick_heroes(
        picked_hero_names,
        DOTA_TEAM_GOODGUYS,
        FROM_PLAYER_ID,
        TO_PLAYER_ID
    )
end

---@param picked_hero_names table
function Hero_setup_controller.Handle_dire_party_response(picked_hero_names)
    if Settings.SHOULD_DIRE_BE_NATIVE_BOTS then
        Native_bot_setup:Create_bots(picked_hero_names)
        return
    end

    local FROM_PLAYER_ID, TO_PLAYER_ID = 5, 9

    Hero_selector:Pick_heroes(
        picked_hero_names,
        DOTA_TEAM_BADGUYS,
        FROM_PLAYER_ID,
        TO_PLAYER_ID
    )
end

function Hero_setup_controller:Select_radiant_heroes()
    Party_collector:Request_radiant_party(self.Handle_radiant_party_response)
end

function Hero_setup_controller:Select_dire_heroes()
    Party_collector:Request_dire_party(self.Handle_dire_party_response)
end

function Hero_setup_controller:Acquire_selected_heroes()
    Timers:CreateTimer(
        ---@return number
        function()
            if not Hero_selector:All_players_have_chosen_hero() then
                return ONE_SECOND_DELAY
            end
            self.radiant_heroes = Hero_selector.radiant_heroes
            self.dire_heroes = Hero_selector.dire_heroes
        end
    )
end

function Hero_setup_controller:Select_heroes()
    self:Select_radiant_heroes()
    self:Select_dire_heroes()
    self:Acquire_selected_heroes()
end

return Hero_setup_controller