-- Settings_setup
local Settings_setup = {}

function Settings_setup:Get_and_set_settings()
    ---@type table
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/settings")
    request:Send(
        ---@param settings_json table
        function(settings_json)
            ---@type table
            local settings_data = package.loaded["game/dkjson"].decode(settings_json["Body"])
            for key, value in pairs(settings_data) do
                Settings[key:upper()] = value
            end
        end
    )
end

return Settings_setup