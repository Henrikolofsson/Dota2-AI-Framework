Utilities = require "utilities.utilities"

local HeroSetup = {}

local selected_heroes = {}

local good_guys_heroes = {}

function HeroSetup:Pick_radiant_team_heroes(picked_hero_names_data, team, from_player_id, to_player_id)
    print("Selecting radiant heroes after delay")
    local picked_hero_names = package.loaded["game/dkjson"].decode(picked_hero_names_data["Body"])
    for player_id = from_player_id, to_player_id do
        local hero_name_index = player_id + 1
        PlayerResource:SetCustomTeamAssignment(player_id, team)
        table.insert(selected_heroes, picked_hero_names[hero_name_index])
        PlayerResource:GetPlayer(player_id):SetSelectedHero(picked_hero_names[hero_name_index])

        if team == DOTA_TEAM_GOODGUYS then
            Timers:CreateTimer(
                function()
                    if not PlayerResource:GetSelectedHeroEntity(player_id) then
                        print("PlayerResource:GetSelectedHeroEntity(player_id) was nil")
                        return 1.0
                    end
                    table.insert(good_guys_heroes, PlayerResource:GetSelectedHeroEntity(player_id))
                end
            )
        end

        if player_id ~= 0 then
            SendToServerConsole("kickid " .. tostring(player_id + 1))
        end
    end

    Timers:CreateTimer(
        function()
            for i = 1, 5 do
                if not good_guys_heroes[i] then
                    return 1.0
                end
            end
            HeroSetup:Destroy_towers()
            HeroSetup:MoveToTower(HeroSetup:GetTowerByName("npc_dota_badguys_tower4"))
        end
    )
end

function HeroSetup:GetTowerByName(to_find)
    local allTowers = Entities:FindAllByClassname("npc_dota_tower")

    for _index, tower in pairs(allTowers) do
        if tower:GetUnitName() == to_find then
            return tower
        end
    end
end

function HeroSetup:Destroy_towers()
    HeroSetup:GetTowerByName("npc_dota_badguys_tower1_mid"):ForceKill(false)
    HeroSetup:GetTowerByName("npc_dota_badguys_tower2_mid"):ForceKill(false)
    HeroSetup:GetTowerByName("npc_dota_badguys_tower3_mid"):ForceKill(false)
    HeroSetup:GetTowerByName("npc_dota_badguys_tower4"):ForceKill(false)
end

function HeroSetup:MoveToTower(tower)
    for i = 1, 5 do
        good_guys_heroes[i]:MoveToNPC(tower)
    end
end

function HeroSetup:AttackToTower(tower)
    for i = 1, 5 do
        good_guys_heroes[i]:MoveToNPC(tower)
    end
end

function HeroSetup:Select_radiant_heroes()
    print("Selecting radiant heroes")
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/party")
    request:Send(
        function(picked_hero_names_data)
            HeroSetup:Pick_radiant_team_heroes(picked_hero_names_data, DOTA_TEAM_GOODGUYS, 0, 4)
        end
    )
end

function HeroSetup.Set_dire_team_bots(picked_hero_names_data)
    local picked_hero_names = package.loaded["game/dkjson"].decode(picked_hero_names_data["Body"])
    local lanes = {"mid", "top", "bot", "top", "bot"}
    for i = 1, 5 do
        Tutorial:AddBot(picked_hero_names[i], lanes[i], "easy", false)
    end
end

function HeroSetup:Select_dire_heroes()
    print("Selecting dire heroes")

    Timers:CreateTimer(
        function()
            if not Game_states:Is_game_in_progress_state() then
                return 1.0
            end
            local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/enemy_party")
            request:Send(HeroSetup.Set_dire_team_bots)
        end
    )
end

function HeroSetup:Populate_game()
    SendToServerConsole("dota_create_fake_clients")
end

function HeroSetup:Select_heroes()
    HeroSetup:Populate_game()
    print("Entered Select_heroes")
    HeroSetup:Select_radiant_heroes()
    HeroSetup:Select_dire_heroes()
end

---@return string
function HeroSetup:Get_random_hero()
    local hero

    repeat
        hero = Hero_ids[math.random(#Hero_ids)]
    until not Utilities:Table_includes_value(selected_heroes, hero)

    table.insert(selected_heroes, hero)

    return hero
end

return HeroSetup