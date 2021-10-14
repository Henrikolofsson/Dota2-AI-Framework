-- Update_handler
local Update_handler = {}

---@param entities table
---@param heroes table
function Update_handler:Update(entities, heroes, on_update_callback)
    local body = package.loaded["game/dkjson"].encode({["entities"] = entities})

    local route
    if heroes[1]:GetTeam() == DOTA_TEAM_GOODGUYS then
        route = "radiant_update"
    elseif heroes[1]:GetTeam() == DOTA_TEAM_BADGUYS then
        route = "dire_update"
    end

    local request = CreateHTTPRequestScriptVM("POST", "http://localhost:8080/api/" .. route)
    request:SetHTTPRequestHeaderValue("Accept", "application/json")
    request:SetHTTPRequestHeaderValue("X-Jersey-Tracing-Threshold", "VERBOSE")
    request:SetHTTPRequestRawPostBody("application/json", body)
    request:Send(
        function(result)
            local commands = package.loaded["game/dkjson"].decode(result["Body"])
            on_update_callback(heroes, commands)
        end
    )
end

return Update_handler