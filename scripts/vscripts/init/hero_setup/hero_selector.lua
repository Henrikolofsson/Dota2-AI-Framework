-- imports
local Utilities = require "utilities.utilities"



-- constants
local FULL_TEAM_COUNT = 5
local PLAYER_ADMIN_ID = 0
local ONE_SECOND_DELAY = 1.



-- Hero_selector
local Hero_selector = {}
Hero_selector.radiant_heroes = {}
Hero_selector.dire_heroes = {}

---@return boolean
function Hero_selector:All_players_have_chosen_hero()
    if Settings.should_dire_be_native_bots then
        return Utilities:Get_table_length(self.radiant_heroes) == FULL_TEAM_COUNT
    end
    return Utilities:Get_table_length(self.radiant_heroes) == FULL_TEAM_COUNT and Utilities:Get_table_length(self.dire_heroes) == FULL_TEAM_COUNT
end

---@param player_id integer
---@param team integer
function Hero_selector:Put_player_on_team(player_id, team)
    if not self:Is_admin(player_id) then
        PlayerResource:SetCustomTeamAssignment(player_id, team)
    end
end

---@param player_id integer
---@param hero_name string
function Hero_selector:Select_hero_for_player(player_id, hero_name)
    PlayerResource:GetPlayer(player_id):SetSelectedHero(hero_name)
end

---@param player_id integer
---@return boolean
function Hero_selector:Player_has_not_selected_hero(player_id)
    return not PlayerResource:GetSelectedHeroEntity(player_id)
end

---@param team integer
---@return table
function Hero_selector:Get_table_to_append_to(team)
    if team == DOTA_TEAM_GOODGUYS then
        return self.radiant_heroes
    end
    return self.dire_heroes
end

---@param player_id integer
---@param team integer
function Hero_selector:Append_hero_to_team_table(player_id, team)
    Timers:CreateTimer(
        function()
            if self:Player_has_not_selected_hero(player_id) then
                return ONE_SECOND_DELAY
            end

            local table_to_append_to = self:Get_table_to_append_to(team)

            table.insert(
                table_to_append_to,
                PlayerResource:GetSelectedHeroEntity(player_id)
            )
        end
    )
end

---@param player_id integer
---@return boolean
function Hero_selector:Is_admin(player_id)
    return player_id == PLAYER_ADMIN_ID
end

---@param player_id integer
function Hero_selector:Kick_player(player_id)
    -- Player ids are 1-10 in Server Console, making it necessary
    -- to increase player_id by 1 before sending the kick command.
    if not Settings.spectator_mode and self:Is_admin(player_id) then
        return
    end
    SendToServerConsole("kickid " .. tostring(player_id + 1))
end

---@param picked_hero_names table
---@param team integer
---@param from_player_id integer
---@param to_player_id integer
function Hero_selector:Pick_heroes(picked_hero_names, team, from_player_id, to_player_id)
    ---@type integer
    for player_id = from_player_id, to_player_id do
        local hero_name_index = player_id + 1
        if player_id > 4 then
            hero_name_index = player_id - 4
        end

        self:Put_player_on_team(player_id, team)
        self:Select_hero_for_player(player_id, picked_hero_names[hero_name_index])
        self:Append_hero_to_team_table(player_id, team)
        self:Kick_player(player_id)
    end
end

return Hero_selector