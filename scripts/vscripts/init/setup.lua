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
            
            -- local bot_id = 5
            -- while bot_id < 10 do
            --     PlayerResource:SetCustomTeamAssignment(bot_id, DOTA_TEAM_DIRE)
            --     local bot = PlayerResource:GetPlayer(bot_id)
            --     bot:MakeRandomHeroSelection()
            -- end

            local currentState = GameRules:State_Get()
            if currentState ~= DOTA_GAMERULES_STATE_GAME_IN_PROGRESS then
                return 1.0
            end
            for i = 1, 5 do
                local lane = nil
                print("Index: " .. i)
                if i == 1 then
                    lane = "mid"
                elseif i == 2 or i == 4 then
                    lane = "top"
                else
                    lane = "bot"
                end

                Tutorial:AddBot(setup:Get_random_hero(), lane, "easy", false)
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

function setup:Get_random_hero()
    local hero = Hero_ids[math.random(#Hero_ids)]
    if Table_includes_value(selected_heroes, hero) then
        return setup:Get_random_hero()
    else
        table.insert(selected_heroes, hero)
        return hero
    end
end

print(Hero_ids)

return setup