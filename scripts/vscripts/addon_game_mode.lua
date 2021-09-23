if SimpleAI == nil then
    _G.SimpleAI = class({})
end

require "libraries/timers"
Game_states = require "game_states/game_states"
Hero_ids = require "init/config/hero_id"
Setup = require "init/setup"

function Activate()
    GameRules.SimpleAI = SimpleAI()
    GameRules.SimpleAI:Init_game_mode()
end

function SimpleAI:Init_game_mode()
    print( "Template addon is loaded." )

    Setup:Developer_setups()

    ListenToGameEvent("game_rules_state_change", Dynamic_Wrap( SimpleAI, "On_game_rules_state_change" ), self)

end

function SimpleAI:On_game_rules_state_change()
    Game_states:On_game_rules_state_change()
end