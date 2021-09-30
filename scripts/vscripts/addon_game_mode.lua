if SimpleAI == nil then
    _G.SimpleAI = class({})
end



-- imports
require "libraries.timers"
require "settings.settings"
local Setup = require "init.setup"



-- Addon entry point
function Activate()
    GameRules.SimpleAI = SimpleAI()
    GameRules.SimpleAI:Init_game_mode()
end

function SimpleAI:Init_game_mode()
    Setup:Run()
end