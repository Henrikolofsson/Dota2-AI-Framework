local Courier_commands = {}

local ABILITY_RETRIEVE = 0
local ABILITY_GO_TO_SECRET_SHOP = 1
local ABILITY_RETURN_ITEMS_TO_STASH = 2
local ABILITY_SPEED_BURST = 3
local ABILITY_TRANSFER_ITEMS = 4
local ABILITY_SHIELD = 5

function Courier_commands:Move_to_position(hero_entity, result)
    local courier_entity = Courier_commands:Get_courier(hero_entity)
    local destination = Vector(result.x, result.y, result.z)
    courier_entity:MoveToPosition(destination)
end

function Courier_commands:Stop(hero_entity)
    local courier_entity = Courier_commands:Get_courier(hero_entity)
    courier_entity:Stop()
end

function Courier_commands:Retrieve(hero_entity)
    Courier_commands:Use_ability(hero_entity, ABILITY_RETRIEVE)
end

function Courier_commands:Go_to_secret_shop(hero_entity)
    Courier_commands:Use_ability(hero_entity, ABILITY_GO_TO_SECRET_SHOP)
end

function Courier_commands:Return_items_to_stash(hero_entity)
    Courier_commands:Use_ability(hero_entity, ABILITY_RETURN_ITEMS_TO_STASH)
end

function Courier_commands:Speed_burst(hero_entity)
    Courier_commands:Use_ability_restricted(hero_entity, 10, ABILITY_SPEED_BURST)
end

function Courier_commands:Transfer_items(hero_entity)
    Courier_commands:Use_ability(hero_entity, ABILITY_TRANSFER_ITEMS)
end

function Courier_commands:Shield(hero_entity)
    Courier_commands:Use_ability_restricted(hero_entity, 20, ABILITY_SHIELD)
end

function Courier_commands:Use_ability_restricted(hero_entity, level, ability_index)
    local courier_entity = Courier_commands:Get_courier(hero_entity)
    local courier_level = courier_entity:GetLevel()

    if courier_level >= level then
        local ability = courier_entity:GetAbilityByIndex(ability_index)
        local cooldown_ready = ability:IsCooldownReady()
        if cooldown_ready then
            courier_entity:CastAbilityNoTarget(ability, courier_entity:GetPlayerOwnerID())
        end
    end 
end

function Courier_commands:Use_ability(hero_entity, ability_index)
    local courier_entity = Courier_commands:Get_courier(hero_entity)
    local ability = courier_entity:GetAbilityByIndex(ability_index)
    courier_entity:CastAbilityNoTarget(ability, courier_entity:GetPlayerOwnerID())
end

function Courier_commands:Get_courier(hero_entity)
    local player_id = hero_entity:GetPlayerOwnerID()
    local courier_entity = PlayerResource:GetPreferredCourierForPlayer(player_id)
    return courier_entity
end

return Courier_commands