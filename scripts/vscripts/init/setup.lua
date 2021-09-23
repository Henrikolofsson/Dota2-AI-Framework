local setup = {}

local selected_heroes = {}

function setup:Remove_all_game_rule_starting_delays()
    GameRules:SetShowcaseTime(1)
    GameRules:SetStrategyTime(1)
    GameRules:SetHeroSelectionTime(1)
    GameRules:SetCustomGameSetupTimeout(1)
    GameRules:SetPreGameTime(5)
    SendToServerConsole("dota_all_vision 1")
    --Game.SetRemainingSetupTime(4);
end

function setup:Select_radiant_heroes()
    print("Selecting radiant heroes")
    Timers:CreateTimer(
        function()
            print("Selecting radiant heroes after delay")
            local player_id = 0
            while player_id < 5 do
                PlayerResource:SetCustomTeamAssignment(player_id, DOTA_TEAM_GOODGUYS)
                local player = PlayerResource:GetPlayer(player_id)
                player:MakeRandomHeroSelection()
                if player_id ~= 0 then
                    SendToServerConsole("kickid " .. tostring(player_id + 1))
                end
                player_id = player_id + 1
            end
        end
    )
end

function setup:Select_dire_heroes()
    print("Selecting dire heroes")

    Timers:CreateTimer(
        function()
            local current_state = GameRules:State_Get()

            if current_state ~= DOTA_GAMERULES_STATE_GAME_IN_PROGRESS then
                return 1.0
            end

            local lanes = {"mid", "top", "bot", "top", "bot"}
            for i = 1, 5 do
                Tutorial:AddBot(setup:Get_random_hero(), lanes[i], "easy", false)
            end
        end
    )
end

function setup:Populate_game()
    SendToServerConsole("dota_create_fake_clients")
end

function setup:Select_heroes()
    setup:Populate_game()
    print("Entered Select_heroes")
    setup:Select_radiant_heroes()
    setup:Select_dire_heroes()
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
function setup:Get_random_hero()
    local hero

    repeat
        hero = Hero_ids[math.random(#Hero_ids)]
    until not Table_includes_value(selected_heroes, hero)

    table.insert(selected_heroes, hero)

    return hero
end

return setup