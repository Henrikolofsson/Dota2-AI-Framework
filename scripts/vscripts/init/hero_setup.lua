-- imports
local Game_states = require "game_states.game_states"



-- constants
local ONE_SECOND_DELAY = 1.0
local PLAYER_ADMIN_ID = 0



-- Hero_setup
local Hero_setup = {}
Hero_setup.good_guys_heroes = {}
-- List for future second team
Hero_setup.bad_guys_heroes = {}

---@param picked_hero_names_data table
---@return table
function Hero_setup:Decode_hero_names_response(picked_hero_names_data)
    return package.loaded["game/dkjson"].decode(picked_hero_names_data["Body"])
end

---@param player_id integer
---@param team integer
function Hero_setup:Put_player_on_team(player_id, team)
    PlayerResource:SetCustomTeamAssignment(player_id, team)
end

---@param player_id integer
---@param hero_name string
function Hero_setup:Select_hero_for_player(player_id, hero_name)
    PlayerResource:GetPlayer(player_id):SetSelectedHero(hero_name)
end

---@param player_id integer
---@return boolean
function Hero_setup:Player_has_not_selected_hero(player_id)
    return not PlayerResource:GetSelectedHeroEntity(player_id)
end

---@param player_id integer
---@param team integer
function Hero_setup:Append_hero_to_team_table(player_id, team)
    Timers:CreateTimer(
        function()
            if Hero_setup:Player_has_not_selected_hero(player_id) then
                return ONE_SECOND_DELAY
            end
            table.insert(
                (team == DOTA_TEAM_GOODGUYS and self.good_guys_heroes or self.bad_guys_heroes),
                PlayerResource:GetSelectedHeroEntity(player_id)
            )
        end
    )
end

---@param player_id integer
---@return boolean
function Hero_setup:Player_is_fake_client(player_id)
    return player_id ~= PLAYER_ADMIN_ID
end

---@param player_id integer
function Hero_setup:Kick_player(player_id)
    -- Player ids are 1-10 in Server Console, making it necessary
    -- to increase player_id by 1 before sending the kick command.
    SendToServerConsole("kickid " .. tostring(player_id + 1))
end

---@param player_id integer
function Hero_setup:Kick_player_if_fake_client(player_id)
    if Hero_setup:Player_is_fake_client(player_id) then
        Hero_setup:Kick_player(player_id)
    end
end

---@param picked_hero_names_data table
---@param team integer
---@param from_player_id integer
---@param to_player_id integer
function Hero_setup:Pick_heroes(picked_hero_names_data, team, from_player_id, to_player_id)
    local picked_hero_names = Hero_setup:Decode_hero_names_response(picked_hero_names_data)

    for player_id = from_player_id, to_player_id do
        local hero_name_index = player_id + 1

        Hero_setup:Put_player_on_team(player_id, team)
        Hero_setup:Select_hero_for_player(player_id, picked_hero_names[hero_name_index])
        Hero_setup:Append_hero_to_team_table(player_id, team)
        Hero_setup:Kick_player_if_fake_client(player_id)
    end
end

---@param picked_hero_names_data table
function Hero_setup:Handle_radiant_party_response(picked_hero_names_data)
    local FROM_PLAYER_ID, TO_PLAYER_ID = 0, 4

    Hero_setup:Pick_heroes(
        picked_hero_names_data,
        DOTA_TEAM_GOODGUYS,
        FROM_PLAYER_ID,
        TO_PLAYER_ID
    )
end

function Hero_setup:Request_radiant_party()
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/party")
    request:Send(Hero_setup.Handle_radiant_party_response)
end

function Hero_setup:Select_radiant_heroes()
    Hero_setup:Request_radient_party()
end

---@param picked_hero_names_data table
function Hero_setup.Handle_dire_party_response(picked_hero_names_data)
    local picked_hero_names = Hero_setup:Decode_hero_names_response(picked_hero_names_data)
    local lanes = {"mid", "top", "bot", "top", "bot"}
    for i = 1, 5 do
        Tutorial:AddBot(picked_hero_names[i], lanes[i], "easy", false)
    end
end

function Hero_setup:Request_dire_party()
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/enemy_party")
    request:Send(Hero_setup.Handle_dire_party_response)
end

function Hero_setup:Select_dire_heroes()
    Timers:CreateTimer(
        function()
            if not Game_states:Is_game_in_progress_state() then
                return ONE_SECOND_DELAY
            end
            Hero_setup:Request_dire_party()
        end
    )
end

function Hero_setup:Select_heroes()
    Hero_setup:Select_radiant_heroes()
    Hero_setup:Select_dire_heroes()
end

return Hero_setup