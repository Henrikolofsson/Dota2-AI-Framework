if SimpleAI == nil then
    _G.SimpleAI = class({})
end

require "libraries.timers"
local Setup = require "init.setup"

function Activate()
    GameRules.SimpleAI = SimpleAI()
    GameRules.SimpleAI:Init_game_mode()
end

function SimpleAI:Init_game_mode()
    Setup:Run()
end