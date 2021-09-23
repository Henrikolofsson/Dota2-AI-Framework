if CAddonTemplateGameMode == nil then
    CAddonTemplateGameMode = class({})
end

function Activate()
    GameRules.AddonTemplate = CAddonTemplateGameMode()
    GameRules.AddonTemplate:InitGameMode()
end

function CAddonTemplateGameMode:InitGameMode()
    print( "Template addon is loaded." )

    ListenToGameEvent( "dota_player_gained_level", Dynamic_Wrap( CustomGameMode, "OnLevelUp" ), self )

    GameRules:GetGameModeEntity():SetThink( "OnThink", self, "GlobalThink", 2 )
end



