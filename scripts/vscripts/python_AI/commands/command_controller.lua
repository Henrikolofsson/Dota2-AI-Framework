local item_shop_availability = require "python_AI.commands.item_handlers.item_shop_availability"
local item_disassemblable = require "python_AI.commands.item_handlers.item_disassemblable"
local Utilities = require "utilities.utilities"
local Courier_commands = require "python_AI.commands.courier_commands"

local Command_controller = {}

function Command_controller:Hero_has_active_ability(hero_entity)
    return Utilities:To_bool(hero_entity:GetCurrentActiveAbility())
end

-- Main entry function --
function Command_controller:Parse_hero_command(hero_entity, result)
    local command = result.command

    --TODO deal with abilities that the hero can interrupt
    if self:Hero_has_active_ability(hero_entity) then
        self:Noop(hero_entity, result)
        Warning("active not null")
        return
    end

    if     command == "MOVE"                                        then self:Move_to(hero_entity, result)
    elseif command == "STOP"                                        then self:Stop(hero_entity)
    elseif command == "LEVEL_UP"                                    then self:Level_up(hero_entity, result)
    elseif command == "ATTACK"                                      then self:Attack(hero_entity, result)
    elseif command == "CAST"                                        then self:Cast(hero_entity, result)
    elseif command == "BUY"                                         then self:Buy(hero_entity, result)
    elseif command == "SELL"                                        then self:Sell(hero_entity, result)
    elseif command == "USE_ITEM"                                    then self:Use_item(hero_entity, result)
    elseif command == "DISASSEMBLE"                                 then self:Disassemble_item(hero_entity, result)
    elseif command == "UNLOCK_ITEM"                                 then self:Check_and_unlock_item(hero_entity, result)
    elseif command == "LOCK_ITEM"                                   then self:Check_and_lock_item(hero_entity, result)
    elseif command == "TOGGLE_ITEM"                                 then self:Toggle_item(hero_entity, result)
    elseif command == "PICK_UP_RUNE"                                then self:Pick_up_rune(hero_entity, result)
    elseif command == "NOOP"                                        then self:Noop(hero_entity, result)
    elseif command == "GLYPH"                                       then self:Cast_glyph_of_fortification(hero_entity)
    elseif command == "TP_SCROLL"                                   then self:Use_tp_scroll(hero_entity, result)
    elseif command == "BUYBACK"                                     then self:Buyback(hero_entity)
    elseif command == "CAST_ABILITY_TOGGLE"                         then self:Cast_ability_toggle(hero_entity, result)
    elseif command == "CAST_ABILITY_NO_TARGET"                      then self:Cast_ability_no_target(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_POINT"                   then self:Cast_ability_target_point(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_AREA"                    then self:Cast_ability_target_area(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT"                    then self:Cast_ability_target_unit(hero_entity, result)
    elseif command == "CAST_ABILITY_VECTOR_TARGETING"               then self:Cast_ability_vector_targeting(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT_AOE"                then self:Cast_ability_target_unit_AOE(hero_entity, result)
    elseif command == "CAST_ABILITY_TARGET_COMBO_TARGET_POINT_UNIT" then self:Cast_ability_combo_target_point_unit(hero_entity, result)
    elseif command == "COURIER_RETRIEVE"                            then Courier_commands:Retrieve(hero_entity)
    elseif command == "COURIER_SECRET_SHOP"                         then Courier_commands:Go_to_secret_shop(hero_entity)
    elseif command == "COURIER_RETURN_ITEMS"                        then Courier_commands:Return_items_to_stash(hero_entity)
    elseif command == "COURIER_SPEED_BURST"                         then Courier_commands:Speed_burst(hero_entity)
    elseif command == "COURIER_TRANSFER_ITEMS"                      then Courier_commands:Transfer_items(hero_entity)
    elseif command == "COURIER_SHIELD"                              then Courier_commands:Shield(hero_entity)
    elseif command == "COURIER_STOP"                                then Courier_commands:Stop(hero_entity)
    elseif command == "COURIER_MOVE_TO_POSITION"                    then Courier_commands:Move_to_position(hero_entity, result)
    elseif command == "COURIER_SELL"                                then Courier_commands:Sell(hero_entity, result)
    else
        Warning(hero_entity:GetName() .. " sent invalid command " .. command)
    end
end


function Command_controller:Hero_can_afford_item(hero_entity, item_name)
    return GetItemCost(item_name) <= hero_entity:GetGold()
end

function Command_controller:Unit_has_free_item_slot(unit_entity)
    local item_in_slot
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_9, 1 do
        item_in_slot = unit_entity:GetItemInSlot(i)
        if not item_in_slot then
            return true
        end
    end
    return false
end

function Command_controller:Unit_can_stack_item_of_name(unit_entity, item_name)
    local item_in_slot
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_9, 1 do
        item_in_slot = unit_entity:GetItemInSlot(i)
        if (item_in_slot) and item_in_slot:IsStackable() and item_in_slot:GetName() == item_name then -- should check special cases where item has max-stack!
            return true
        end
    end
    return false
end

function Command_controller:Buy_item_for_unit(unit_entity, hero_entity, name_of_item_to_buy)
    EmitSoundOn("General.Buy", unit_entity)
    unit_entity:AddItem(CreateItem(name_of_item_to_buy, unit_entity, unit_entity))
    hero_entity:SpendGold(GetItemCost(name_of_item_to_buy), DOTA_ModifyGold_PurchaseItem) --should the reason take DOTA_ModifyGold_PurchaseConsumable into account?
end

function Command_controller:Unit_can_buy_item(unit_entity, item_name)
    return unit_entity:IsInRangeOfShop(item_shop_availability[item_name], true)
    and (self:Unit_has_free_item_slot(unit_entity) or self:Unit_can_stack_item_of_name(unit_entity, item_name))
end

function Command_controller:Get_courier_of_hero(hero_entity)
    return PlayerResource:GetPreferredCourierForPlayer(hero_entity:GetPlayerID())
end

function Command_controller:Buy(hero_entity, result)
    local item_name = result.item

    if not self:Hero_can_afford_item(hero_entity, item_name) then
        Warning(hero_entity:GetName() .. " tried to buy " .. item_name .. " but couldn't afford it")
        return
    end

    if self:Unit_can_buy_item(hero_entity, item_name) then
        self:Buy_item_for_unit(hero_entity, hero_entity, item_name)
    else
        local courier_entity = self:Get_courier_of_hero(hero_entity)
        if self:Unit_can_buy_item(courier_entity, item_name) then
            self:Buy_item_for_unit(courier_entity, hero_entity, item_name)
        else
            Warning(hero_entity:GetName() .. " tried to buy " .. item_name .. " but neither hero nor courier was not in range!")
        end
    end
end

function Command_controller:Sell(unit_entity, result)
    local slot = result.slot

    if unit_entity:CanSellItems() then
        local item_entity = unit_entity:GetItemInSlot(slot)
        if item_entity then
            if item_entity:IsSellable() then
                unit_entity:SellItem(item_entity)
                EmitSoundOn("General.Sell", unit_entity)
            else
                Warning("Item in slot " .. slot .. " is not sellable.")
            end
        else
            Warning("No item in slot " .. slot)
        end
    else
        Warning("Bot tried to sell item outside shop")
    end
end

function Command_controller:Noop(hero_entity, result)
    --Noop
end

function Command_controller:Move_to(hero_entity, result)
    hero_entity:MoveToPosition(Vector(result.x, result.y, result.z))
end

function Command_controller:Stop(hero_entity)
    hero_entity:Stop()
end

function Command_controller:Level_up(hero_entity, result)
    local ability_points = hero_entity:GetAbilityPoints()
    if ability_points <= 0 then
        Warning(hero_entity:GetName() .. " has no ability points. Why am I levelling up?")
        return
    end

    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)

    if ability_entity:GetLevel() == ability_entity:GetMaxLevel() then
        Warning(hero_entity:GetName() .. ": " .. ability_entity:GetName() .. " is maxed out")
        return
    end

    local required_level = ability_entity:GetHeroLevelRequiredToUpgrade()
    local hero_level = hero_entity:GetLevel()
    if hero_level < required_level then
        Warning(hero_entity:GetName() .. "(level " .. hero_level .. ") tried to level up ability " .. ability_entity:GetName() .. " which requries level " .. required_level)
        return
    end

    ability_entity:UpgradeAbility(false)
    hero_entity:SetAbilityPoints(ability_points - 1)
end

function Command_controller:Attack(hero_entity, result)
    hero_entity:MoveToTargetToAttack(EntIndexToHScript(result.target))
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
        self:Use_ability(hero_entity, item_entity, result)
    else
        Warning("Bot tried to use item in empty slot")
    end
end

function Command_controller:Disassemble_item(hero_entity, result)
    local slot = result.slot
    local item_entity = hero_entity:GetItemInSlot(slot)

    if item_entity and self:Hero_can_disassemble_item(item_entity) then
        hero_entity:DisassembleItem(item_entity)
    else
        Warning("Hero" .. hero_entity:GetName() .. "tried to disassemble Item" .. item_entity:GetName())
    end
end

function Command_controller:Hero_can_disassemble_item(item_entity)
    for _index, value in ipairs(item_disassemblable) do
        if item_entity:GetName() == value then
            return true
        end
    end
    return false
end


function Command_controller:Check_and_unlock_item(hero_entity, result)
    local slot = result.slot
    local item_entity = hero_entity:GetItemInSlot(slot)

    if item_entity then
        if item_entity:IsCombineLocked() then
            item_entity:SetCombineLocked(false)
        end
    else
        Warning("No item in slot " .. slot)
    end
end

function Command_controller:Check_and_lock_item(hero_entity, result)
    local slot = result.slot
    local item_entity = hero_entity:GetItemInSlot(slot)

    if item_entity then
        if not item_entity:IsCombineLocked() then
            item_entity:SetCombineLocked(true)
        end
    else
        Warning("No item in slot " .. slot)
    end
end

function Command_controller:Toggle_item(hero_entity, result)
    local slot = result.slot
    local item_entity = hero_entity:GetItemInSlot(slot)

    if item_entity then
        item_entity:OnToggle()
    else
        Warning("No item in slot " .. slot)
    end
end

function Command_controller:Buyback(hero_entity)
    hero_entity:Buyback()
end

function Command_controller:Cast_glyph_of_fortification(hero_entity)
    ExecuteOrderFromTable({
        UnitIndex = hero_entity:entindex(),
        OrderType = DOTA_UNIT_ORDER_GLYPH,
    })
end

function Command_controller:Use_tp_scroll(hero_entity, result)
    local tp_scroll_entity = hero_entity:GetItemInSlot(DOTA_ITEM_TP_SCROLL)

    if tp_scroll_entity then
        if tp_scroll_entity:IsCooldownReady() then
            self:Use_ability(hero_entity, tp_scroll_entity, result)
        else
            Warning("Bot tried to use town portal scrolls while on cooldown.")
        end
    else
        Warning("Bot has no town portal scrolls available.")
    end
end

function Command_controller:Scan(hero_entity, result) -- unused
    ExecuteOrderFromTable({
        UnitIndex = hero_entity:entindex(),
        OrderType = DOTA_UNIT_ORDER_RADAR,
        Position = Vector(result.x, result.y, result.z),
    })
end

function Command_controller:Pick_up_rune(hero_entity, result)
    hero_entity:PickupRune(EntIndexToHScript(result.target))
end

function Command_controller:Cast_ability_toggle(hero_entity, result)
    local ability_entity = hero_entity:GetAbilityByIndex(result.ability)
    if self:SetupAbility(hero_entity, ability_entity) then
        local player_id = hero_entity:GetPlayerOwnerID()
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
        if bit.band(behavior, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET) ~= 0 then
            local target_entity = EntIndexToHScript(result.target)
            hero_entity:CastAbilityOnTarget(target_entity, ability_entity, player_id)
        elseif bit.band(behavior, DOTA_ABILITY_BEHAVIOR_POINT) ~= 0 then
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

    if not self:Hero_can_afford_to_cast_ability(hero_entity, ability_entity) then
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
        if bit.band(behavior, DOTA_ABILITY_BEHAVIOR_NO_TARGET) ~= 0 then
            hero_entity:CastAbilityNoTarget(ability_entity, player_id)

        elseif bit.band(behavior, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET) ~= 0 then
            local target_entity = EntIndexToHScript(result.target)
            if target_entity:IsAlive() then
                hero_entity:CastAbilityOnTarget(target_entity, ability_entity, player_id)
            end

        elseif bit.band(behavior, DOTA_ABILITY_BEHAVIOR_POINT) ~= 0 then
            hero_entity:CastAbilityOnPosition(Vector(result.x, result.y, result.z), ability_entity, player_id)

        else
            Warning(hero_entity:GetName() .. " sent invalid cast command " .. behavior)
        end
    end
end


return Command_controller