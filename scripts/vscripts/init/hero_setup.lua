Utilities = require "utilities.utilities"

local HeroSetup = {}

local selected_heroes = {}

function HeroSetup:Pick_radiant_team_heroes()
    print("Selecting radiant heroes after delay")
    for player_id = 0, 4 do
        PlayerResource:SetCustomTeamAssignment(player_id, DOTA_TEAM_GOODGUYS)
        PlayerResource:GetPlayer(player_id):SetSelectedHero(HeroSetup:Get_random_hero())
        if player_id ~= 0 then
            SendToServerConsole("kickid " .. tostring(player_id + 1))
        end
    end
end

function HeroSetup:Select_radiant_heroes()
    print("Selecting radiant heroes")
    Timers:CreateTimer(HeroSetup.Pick_radiant_team_heroes)
end

function HeroSetup:Set_dire_team_bots()
    local lanes = {"mid", "top", "bot", "top", "bot"}
    for i = 1, 5 do
        Tutorial:AddBot(HeroSetup:Get_random_hero(), lanes[i], "easy", false)
    end
end

function HeroSetup:Select_dire_heroes()
    print("Selecting dire heroes")

    Timers:CreateTimer(
        function()
            if not Game_states:Is_game_in_progress_state() then
                return 1.0
            end
            HeroSetup:Set_dire_team_bots()
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