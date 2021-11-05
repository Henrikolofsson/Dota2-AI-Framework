local Match_end_controller = {}

local function Restart()
    SendToServerConsole("dota_launch_custom_game Dota2-AI-Framework dota")
end

local function Exit()
    SendToServerConsole("kickid 1")
end

function Match_end_controller:Handle_match_end()
    ---@type table
    local request = CreateHTTPRequestScriptVM("POST", "http://localhost:8080/api/game_ended")
    request:Send(
        ---@param response_json table
        function(response_json)
            ---@type table
            local response = package.loaded["game/dkjson"].decode(response_json["Body"])
            if response.status == "restart" then
                Restart()
            elseif response.status == "done" then
                Exit()
            end
        end
    )
end

function Match_end_controller:Handle_restart_game()
    ---@type table
    local request = CreateHTTPRequestScriptVM("POST", "http://localhost:8080/api/restart_game")
    request:Send(
        ---@param response_json table
        function(response_json)
            Restart()
        end
    )
end

function Match_end_controller:Handle_exit()
    ---@type table
    Exit()
end

return Match_end_controller