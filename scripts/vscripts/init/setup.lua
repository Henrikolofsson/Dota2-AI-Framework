local Setup = {}

local selected_heroes = {}

function Setup:Remove_all_game_rule_starting_delays()
    GameRules:SetShowcaseTime(1)
    GameRules:SetStrategyTime(1)
    GameRules:SetHeroSelectionTime(1)
    GameRules:SetCustomGameSetupTimeout(1)
    GameRules:SetPreGameTime(5)
    --Game.SetRemainingSetupTime(4);
end

function Setup:Grant_global_vision()
    SendToServerConsole("dota_all_vision 1")
end

function Setup:Developer_setups()
    Setup:Remove_all_game_rule_starting_delays()
    Setup:Grant_global_vision()
end



function Setup:Select_radiant_heroes()
    print("Selecting radiant heroes")
    Timers:CreateTimer(
        function()
            print("Selecting radiant heroes after delay")
            for player_id = 0, 4 do
                PlayerResource:SetCustomTeamAssignment(player_id, DOTA_TEAM_GOODGUYS)
                PlayerResource:GetPlayer(player_id):SetSelectedHero(Setup:Get_random_hero())
                if player_id ~= 0 then
                    SendToServerConsole("kickid " .. tostring(player_id + 1))
                end
            end
        end
    )
end

function Setup:Select_dire_heroes()
    print("Selecting dire heroes")

    Timers:CreateTimer(
        function()
            local current_state = GameRules:State_Get()

            if current_state ~= DOTA_GAMERULES_STATE_GAME_IN_PROGRESS then
                return 1.0
            end

            local lanes = {"mid", "top", "bot", "top", "bot"}
            for i = 1, 5 do
                Tutorial:AddBot(Setup:Get_random_hero(), lanes[i], "easy", false)
            end
        end
    )
end

function Setup:Populate_game()
    SendToServerConsole("dota_create_fake_clients")
end

function Setup:Select_heroes()
    Setup:Populate_game()
    print("Entered Select_heroes")
    Setup:Select_radiant_heroes()
    Setup:Select_dire_heroes()
end

---@param tableToSearch table
---@param valueToFind any
---@return boolean
local function Table_includes_value(tableToSearch, valueToFind)
    for _index, value in ipairs(tableToSearch) do
        if value == valueToFind then
            return true
        end
    end

    return false
end

---@return string
function Setup:Get_random_hero()
    local hero

    repeat
        hero = Hero_ids[math.random(#Hero_ids)]
    until not Table_includes_value(selected_heroes, hero)

    table.insert(selected_heroes, hero)

    return hero
end

return Setup