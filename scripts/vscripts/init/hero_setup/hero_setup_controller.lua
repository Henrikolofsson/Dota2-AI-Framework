-- imports
local Hero_selector = require "init.hero_setup.hero_selector"
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

function Hero_setup_controller:Select_radiant_heroes()
    local from_player_id, to_player_id = 1, 5

    Hero_selector:Pick_heroes(
        Settings.radiant_party_names,
        DOTA_TEAM_GOODGUYS,
        from_player_id,
        to_player_id
    )
end

function Hero_setup_controller:Select_dire_heroes()
    local from_player_id, to_player_id = 6, 10

    Hero_selector:Pick_heroes(
        Settings.dire_party_names,
        DOTA_TEAM_BADGUYS,
        from_player_id,
        to_player_id
    )
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