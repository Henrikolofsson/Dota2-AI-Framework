local Item_handler = require "python_AI.commands.item_handlers.item_handler"
local Utilities = require "utilities.utilities"

local Command_controller = {}

function Command_controller:Hero_has_active_ability(hero_entity)
    return Utilities:To_bool(hero_entity:GetCurrentActiveAbility())
end

-- Main entry function --
function Command_controller:ParseHeroCommand(hero_entity, result)
    local command = result.command

    --TODO deal with abilities that the hero can interrupt
    if self:Hero_has_active_ability(hero_entity) then
        self:Noop(hero_entity, result)
        Warning("active not null")
        return
    end

    if     command == "MOVE"                                        then self:Move_to(hero_entity, result)
    elseif command == "LEVELUP"                                     then self:Level_up(hero_entity, result)
    elseif command == "ATTACK"                                      then self:Attack(hero_entity, result)
    elseif command == "CAST"                                        then self:Cast(hero_entity, result)
    elseif command == "BUY"                                         then self:Buy(hero_entity, result)
    elseif command == "SELL"                                        then self:Sell(hero_entity, result)
    elseif command == "USE_ITEM"                                    then self:Use_item(hero_entity, result)
    elseif command == "NOOP"                                        then self:Noop(hero_entity, result)
    elseif command == "CAST_ABILITY_TOGGLE"                         then self:Cast_ability_toggle(hero_entity, result)
    elseif command == "CAST_ABILITY_NO_TARGET"                      then self:Cast_ability_no_target(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_POINT"                   then self:Cast_ability_target_point(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_AREA"                    then self:Cast_ability_target_area(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT"                    then self:Cast_ability_target_unit(hero_entity, result)
    elseif command == "CAST_ABILITY_VECTOR_TARGETING"               then self:Cast_ability_vector_targeting(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT_AOE"                then self:Cast_ability_target_unit_AOE(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_COMBO_TARGET_POINT_UNIT" then self:Cast_ability_combo_target_point_unit(hero_entity, result)
    else
        self.Error = true
        Warning(hero_entity:GetName() .. " sent invalid command " .. command)
    end
end


function Command_controller:Hero_can_afford_item(hero_entity, item_name)
    return GetItemCost(item_name) <= hero_entity:GetGold()
end

-- Buying items --
function Command_controller:Buy(hero_entity, result)
    print("attempt buy")
    local item_name = result.item
    local item_cost = GetItemCost(item_name)

    if not self:Hero_can_afford_item(hero_entity, item_name) then
        Warning(hero_entity:GetName() .. " tried to buy " .. item_name .. " but couldn't afford it")
        return
    end

    local target_slot = -1
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_6, 1 do
        if not hero_entity:GetItemInSlot(i) then
            target_slot = i
            break
        end
    end

    --TODO item availability is missing

    if target_slot < 0 then
        print("attempt buy: no slot")
        Warning(hero_entity:GetName() .. " tried to buy " .. item_name .. " but has no space left")
        --TODO buy into stash
        return
    end

    local closest_shop_entity = Entities:FindByClassnameWithin(nil, "trigger_shop", hero_entity:GetOrigin(), 0.01)
    if closest_shop_entity then
        local shop_type = Item_handler:Get_shop_type(closest_shop_entity)

        if Item_handler:Is_available_in_shop(item_name, shop_type) then
            local item_entity = CreateItem(item_name, hero_entity, hero_entity)
            EmitSoundOn("General.Buy", hero_entity)
            hero_entity:AddItem(item_entity)
            hero_entity:SpendGold(item_cost, DOTA_ModifyGold_PurchaseItem) --should the reason take DOTA_ModifyGold_PurchaseConsumable into account?
        else
            --TODO ping actually the right shop
            Item_handler:Ping_nearest_shop(hero_entity)
            Warning("Shop is of type " .. shop_type)
            return
        end
    else
        print("attempt buy: no shop")
        Item_handler:Ping_nearest_shop(hero_entity)
        return
    end

    -- Say(nil, hero_entity:GetName() .. " bought " .. itemName, false)
end

function Command_controller:Sell(hero_entity, result)
    local slot = result.slot

    if hero_entity:CanSellItems() then
        local item_entity = hero_entity:GetItemInSlot(slot)
        if item_entity then
            --TODO GetCost does not return the value altered, i.e. halved
            EmitSoundOn("General.Sell", hero_entity)
            hero_entity:ModifyGold(item_entity:GetCost(), true, DOTA_ModifyGold_SellItem) -- Claims sell-operation gives reliable gold. (Second param = true)
            hero_entity:RemoveItem(item_entity)
        else
            Warning("No item in slot " .. slot)
        end
    else
        Item_handler:Ping_nearest_shop(hero_entity)
        Warning("Bot tried to sell item outside shop")
    end
end

function Command_controller:Noop(hero_entity, result)
    --Noop
end

function Command_controller:Move_to(hero_entity, result)
    hero_entity:MoveToPosition(Vector(result.x, result.y, result.z))
    -- Say(nil, hero_entity:GetName() .. " moving to " .. result.x .. ", " .. result.y .. ", " .. result.z, false)
end

function Command_controller:Level_up(hero_entity, result)
    local ability_points = hero_entity:GetAbilityPoints()
    if ability_points <= 0 then
        Warning(hero_entity:GetName() .. " has no ability points. Why am I levelling up?")
        return
    end

    local ability_index = result.abilityIndex

    local ability_entity = hero_entity:GetAbilityByIndex(ability_index)
    if ability_entity:GetLevel() == ability_entity:GetMaxLevel() then
        Warning(hero_entity:GetName() .. ": " .. ability_entity:GetName() .. " is maxed out")
        return
    end
    ability_entity:UpgradeAbility(false)
    hero_entity:SetAbilityPoints(ability_points - 1) --UpgradeAbility doesn't decrease the ability points
    -- Say(nil, hero_entity:GetName() .. " levelled up ability " .. ability_index, false)
end

function Command_controller:Attack(hero_entity, result)
    --Might want to check attack range
    --hero_entity:PerformAttack(EntIndexToHScript(result.target), true, true, false, true)
    hero_entity:MoveToTargetToAttack(EntIndexToHScript(result.target))
    -- Say(nil, hero_entity:GetName() .. " attacking " .. result.target, false)
end

function Command_controller:Cast(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)

    if ability_entity and ability_entity ~= nil then
        self:Use_ability(hero_entity, ability_entity, result)
    end
end

function Command_controller:Use_item(hero_entity, result)
    local slot = result.slot
    local item_entity = hero_entity:GetItemInSlot(slot)
    Warning("Hero" .. hero_entity:GetName() .. "is attempting to use item " .. item_entity:GetName())
    if item_entity then
        self:Use_ability(hero_entity, item_entity)
    else
        Warning("Bot tried to use item in empty slot")
    end
end

function Command_controller:Cast_ability_toggle(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        -- ability_entity:OnToggle()
        hero_entity:CastAbilityToggle(ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_no_target(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        hero_entity:CastAbilityNoTarget(ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_target_point(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        hero_entity:CastAbilityOnPosition(Vector(result.x, result.y, result.z), ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_target_area(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        hero_entity:CastAbilityOnPosition(Vector(result.x, result.y, result.z), ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_target_unit(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        local target_entity = EntIndexToHScript(result.target)
        hero_entity:CastAbilityOnTarget(target_entity, ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_vector_targeting(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        hero_entity:CastAbilityOnPosition(Vector(result.x, result.y, result.z), ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_target_unit_AOE(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
        local target_entity = EntIndexToHScript(result.target)
        hero_entity:CastAbilityOnTarget(target_entity, ability_entity, player_id)
    end
end

function Command_controller:Cast_ability_combo_target_point_unit(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local behavior = ability_entity:GetBehavior()
        local player_id = hero_entity:GetPlayerOwnerID()
        if Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET) then
            local target_entity = EntIndexToHScript(result.target)
            hero_entity:CastAbilityOnTarget(target_entity, ability_entity, player_id)
        elseif Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_POINT) then
            hero_entity:CastAbilityOnPosition(Vector(result.x, result.y, result.z), ability_entity, player_id)
        end
    end
end

function Command_controller:Hero_can_afford_to_cast_ability(hero_entity, ability_entity)
    return ability_entity:GetManaCost(ability_entity:GetLevel()) <= hero_entity:GetMana()
end

function Command_controller:SetupAbility(hero_entity, ability_entity)
    if not self:Hero_can_afford_to_cast_ability(hero_entity, ability_entity) then
        Warning("Bot tried to use ability without mana")
        return false
    elseif ability_entity:GetCooldownTimeRemaining() > 0 then
        Warning("Bot tried to use ability still on cooldown")
        return false
    end
    return true
end

function Command_controller:Use_ability(hero_entity, ability_entity, result)
    local level = ability_entity:GetLevel()
    local player_id = hero_entity:GetPlayerOwnerID()
    local behavior = ability_entity:GetBehavior()

    if level == 0 then
        Warning("Bot tried to use ability without level")
        return
    end

    if self:Hero_can_afford_to_cast_ability(hero_entity, ability_entity) then
        Warning("Bot tried to use ability without mana")
    elseif ability_entity:GetCooldownTimeRemaining() > 0 then
        Warning("Bot tried to use ability still on cooldown")
    else
        if not ability_entity:IsItem() then
            ability_entity:StartCooldown(ability_entity:GetCooldown(level))
            ability_entity:PayManaCost()
            ability_entity:OnSpellStart()
        end

        --There is some logic missing here to check for range and make the hero face the right direction
        if Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_NO_TARGET) then
            -- Say(nil, hero_entity:GetName() .. " casting " .. ability_entity:GetName(), false)
            hero_entity:CastAbilityNoTarget(ability_entity, player_id)
        elseif Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET) then
            local target_entity = EntIndexToHScript(result.target)
            if target_entity:IsAlive() then
                -- Say(nil, hero_entity:GetName() .. " casting " .. ability_entity:GetName() .. " on unit " .. target_entity:GetName(), false)
                hero_entity:CastAbilityOnTarget(target_entity, ability_entity, player_id)
            end
        elseif Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_POINT) then
            -- Say(
            --     nil,
            --     hero_entity:GetName() ..
            --         " casting " .. ability_entity:GetName() .. " on " .. result.x .. ", " .. result.y .. ", " .. result.z,
            --     false
            -- )
            hero_entity:CastAbilityOnPosition(Vector(result.x, result.y, result.z), ability_entity, player_id)
        else
            Warning(hero_entity:GetName() .. " sent invalid cast command " .. behavior)
            self._Error = true
        end
    end
end


return Command_controller