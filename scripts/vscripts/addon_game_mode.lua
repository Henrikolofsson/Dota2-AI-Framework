if SimpleAI == nil then
    _G.SimpleAI = class({})
end



-- imports
require "libraries.timers"
require "settings.settings"
local Setup = require "init.setup"



-- constants
SHOULD_HAVE_PRE_GAME_DELAY = false



-- Addon entry point
function Activate()
    GameRules.SimpleAI = SimpleAI()
    GameRules.SimpleAI:Init_game_mode()
end

function SimpleAI:Init_game_mode()
    Setup:Run()
end