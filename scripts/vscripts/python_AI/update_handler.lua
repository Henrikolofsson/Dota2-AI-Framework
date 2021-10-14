-- Constants
local RADIANT_UPDATE_ROUTE = "radiant_update"
local DIRE_UPDATE_ROUTE = "dire_update"



-- Update_handler
local Update_handler = {}

---@param heroes table
---@return string
function Update_handler:Get_route(heroes)
    if heroes[1]:GetTeam() == DOTA_TEAM_GOODGUYS then
        return RADIANT_UPDATE_ROUTE
    elseif heroes[1]:GetTeam() == DOTA_TEAM_BADGUYS then
        return DIRE_UPDATE_ROUTE
    end
end

---@param entities table
---@param heroes table
---@param on_update_callback function
function Update_handler:Update(entities, heroes, on_update_callback)
    ---@type table
    local body = package.loaded["game/dkjson"].encode({["entities"] = entities})

    local route = self:Get_route(heroes)

    ---@type table
    local request = CreateHTTPRequestScriptVM("POST", "http://localhost:8080/api/" .. route)
    request:SetHTTPRequestHeaderValue("Accept", "application/json")
    request:SetHTTPRequestHeaderValue("X-Jersey-Tracing-Threshold", "VERBOSE")
    request:SetHTTPRequestRawPostBody("application/json", body)
    request:Send(
        ---@param result table
        function(result)
            ---@type table
            local commands = package.loaded["game/dkjson"].decode(result["Body"])
            on_update_callback(heroes, commands)
        end
    )
end

return Update_handler