-- Settings_setup
local Settings_setup = {}

function Settings_setup:Get_and_set_settings()
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/settings")
    request:Send(
        function(json_settings)
            local settings_data = package.loaded["game/dkjson"].decode(json_settings["Body"])
            for key, value in pairs(settings_data) do
                Settings[key:upper()] = value
            end
        end
    )
end

return Settings_setup