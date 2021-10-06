local Party_collector = {}

---@param picked_hero_names_data table
---@return table
function Party_collector:Decode_hero_names_response(picked_hero_names_data)
    return package.loaded["game/dkjson"].decode(picked_hero_names_data["Body"])
end

---@param request table
---@param response_callback function
function Party_collector:Send_request(request, response_callback)
    request:Send(
        function(picked_hero_names_data)
            local picked_hero_names = Party_collector:Decode_hero_names_response(picked_hero_names_data)
            response_callback(picked_hero_names)
        end
    )
end

---@param response_callback function
function Party_collector:Request_radiant_party(response_callback)
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/party")
    Party_collector:Send_request(request, response_callback)
end

---@param response_callback function
function Party_collector:Request_dire_party(response_callback)
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/enemy_party")
    Party_collector:Send_request(request, response_callback)
end

return Party_collector