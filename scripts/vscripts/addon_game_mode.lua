if Main_controller == nil then
    _G.Main_controller = class({})
end



-- imports
require "libraries.timers"
require "settings.settings"
require "main_controller"



-- Addon entry point.
function Activate()
    GameRules.Main_controller = Main_controller()
    Timers:CreateTimer({
        endTime = 1.0,
        callback = GameRules.Main_controller.Run
    })
end