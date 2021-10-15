-- Settings_setup
local Settings_setup = {}

function Settings_setup:Get_and_set_settings()
    ---@type table
    local request = CreateHTTPRequestScriptVM("GET", "http://localhost:8080/api/settings")
    request:Send(
        ---@param settings_json table
        function(settings_json)
            ---@type table
            if settings_json["StatusCode"] == 406 then
                print("Request settings was Not Acceptable!")
                return
            end
            local settings_data = package.loaded["game/dkjson"].decode(settings_json["Body"])
            DeepPrintTable(settings_data)
            for key, value in pairs(settings_data) do
                Settings[key] = value
            end
            DeepPrintTable(Settings)
        end
    )
end

return Settings_setup