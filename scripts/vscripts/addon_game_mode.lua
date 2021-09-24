if SimpleAI == nil then
    _G.SimpleAI = class({})
end

require "libraries/timers"
Hero_ids = require "init/config/hero_id"
Setup = require "init/setup"

function Activate()
    GameRules.SimpleAI = SimpleAI()
    GameRules.SimpleAI:Init_game_mode()
end

function SimpleAI:Init_game_mode()
    print( "Template addon is loaded." )
    Setup:Run()
end