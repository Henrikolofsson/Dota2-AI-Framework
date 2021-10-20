local item_shop_availability = require "python_AI.item_shop_availability"
local shoptype_model_names = require "python_AI.shoptype_model_names"
local Utilities = require "utilities.utilities"

local Command_controller = {}



-- A little help function that returns the shoptype for a given model name
-- Explanation: the defualt dota map models shops as entities of the class trigger_shop
-- that class has an attribute shoptype that's exactly what we need here
-- Unfortunately, that attribute does not seem to be exposed to the LUA API
-- Lucky for us, the trigger all have uniquely named model names, even though they don't appear on the map
-- we can use that to hard code the shoptypes ourselves
--
-- This may obviously break in between patches. It may not even work on themed maps
--
-- Note: Shops seem to have multiple triggers, with the exception of the radiant home shop
-- @returns the type for a given modelname: 0 for home and 1 for secret shop. -1 in the case of an error
function GetShopType(model_name)
    if not shoptype_model_names[model_name] then
        Warning("Unknown shop " .. model_name)
        return -1
    end

    return shoptype_model_names[model_name]
end

-- This function is generated from the game's item.txt
-- It returns true if a given item name can be bought in a certain shop type
-- 0 = home, 1 = secret shop
function IsAvailableInShop(item_name, shoptype)
    if not item_shop_availability[item_name] then
        Warning(item_name .. " is unknown")
        return false
    end

    return item_shop_availability[item_name] == shoptype
end


function PingNearestShop(eHero)
    --ping nearest shop
    local nearest = nil
    local nearestDistance = 21200 --15000 is the edge size of the map, so the longest distance is the hypotenuse = 21200
    eShop = Entities:FindByClassname(nil, "trigger_shop")
    while eShop ~= nil do
        local d = CalcDistanceBetweenEntityOBB(eHero, eShop)
        if nearestDistance > d then
            nearestDistance = d
            nearest = eShop:GetOrigin()
        end
        eShop = Entities:FindByClassname(eShop, "trigger_shop")
    end
    MinimapEvent(eHero:GetTeam(), eHero, nearest.x, nearest.y, DOTA_MINIMAP_EVENT_HINT_LOCATION, 1)
end




-- Main entry function --
function Command_controller:ParseHeroCommand(eHero, result)
    -- local result = package.loaded["game/dkjson"].decode(reply)
    local command = result.command

    --TODO deal with abilities that the hero can interrupt
    local eAbility = eHero:GetCurrentActiveAbility()
    if eAbility then
        self:Noop(eHero, result)
        Warning("active not null")
        return
    end
    -- print(result)
    if command == "MOVE" then
        self:MoveTo(eHero, result)
    elseif command == "LEVELUP" then
        self:LevelUp(eHero, result)
    elseif command == "ATTACK" then
        self:Attack(eHero, result)
    elseif command == "CAST" then
        self:Cast(eHero, result)
    elseif command == "BUY" then
        self:Buy(eHero, result)
    elseif command == "SELL" then
        self:Sell(eHero, result)
    elseif command == "USE_ITEM" then
        self:UseItem(eHero, result)
    elseif command == "NOOP" then
        self:Noop(eHero, result)
    elseif command == "CAST_ABILITY_TOGGLE" then
        self:CastAbilityToggle(eHero, result)
    elseif command == "CAST_ABILITY_NO_TARGET" then
        self:CastAbilityNoTarget(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_POINT" then
        self:CastAbilityTargetPoint(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_AREA" then
        self:CastAbilityTargetArea(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT" then
        self:CastAbilityTargetUnit(eHero, result)
    elseif command == "CAST_ABILITY_VECTOR_TARGETING" then
        self:CastAbilityVectorTargeting(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_UNIT_AOE" then
        self:CastAbilityTargetUnitAOE(eHero, result)
    elseif command == "CAST_ABILITY_TARGET_COMBO_TARGET_POINT_UNIT" then
        self:CastAbilityComboTargetPointUnit(eHero, result)
    else
        self.Error = true
        Warning(eHero:GetName() .. " sent invalid command " .. reply)
    end
end


-- Buying items --
function Command_controller:Buy(eHero, result)
    local itemName = result.item
    local itemCost = GetItemCost(itemName)

    if eHero:GetGold() < itemCost then
        Warning(eHero:GetName() .. " tried to buy " .. itemName .. " but couldn't afford it")
        return
    end

    local targetSlot = -1
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_6, 1 do
        if not eHero:GetItemInSlot(i) then
            targetSlot = i
            break
        end
    end

    --TODO item availability is missing

    if targetSlot < 0 then
        Warning(eHero:GetName() .. " tried to buy " .. itemName .. " but has no space left")
        --TODO buy into stash
        return
    end

    local eShop = Entities:FindByClassnameWithin(nil, "trigger_shop", eHero:GetOrigin(), 0.01)
    if eShop then
        local shopType = GetShopType(eShop:GetModelName())

        if IsAvailableInShop(itemName, shopType) then
            local eItem = CreateItem(itemName, eHero, eHero)
            EmitSoundOn("General.Buy", eHero)
            eHero:AddItem(eItem)
            eHero:SpendGold(itemCost, DOTA_ModifyGold_PurchaseItem) --should the reason take DOTA_ModifyGold_PurchaseConsumable into account?
        else
            --TODO ping actually the right shop
            PingNearestShop(eHero)
            Warning("Shop is of type " .. shopType)
            return
        end
    else
        PingNearestShop(eHero)
        return
    end

    -- Say(nil, eHero:GetName() .. " bought " .. itemName, false)
end

function Command_controller:Sell(eHero, result)
    local slot = result.slot

    if eHero:CanSellItems() then
        local eItem = eHero:GetItemInSlot(slot)
        if eItem then
            --TODO GetCost does not return the value altered, i.e. halved
            EmitSoundOn("General.Sell", eHero)
            eHero:ModifyGold(eItem:GetCost(), true, DOTA_ModifyGold_SellItem) -- Claims sell-operation gives reliable gold. (Second param = true)
            eHero:RemoveItem(eItem)
        else
            Warning("No item in slot " .. slot)
        end
    else
        PingNearestShop(eHero)
        Warning("Bot tried to sell item outside shop")
    end
end

function Command_controller:Noop(eHero, result)
    --Noop
end

function Command_controller:MoveTo(eHero, result)
    eHero:MoveToPosition(Vector(result.x, result.y, result.z))
    -- Say(nil, eHero:GetName() .. " moving to " .. result.x .. ", " .. result.y .. ", " .. result.z, false)
end

function Command_controller:LevelUp(eHero, result)
    local abilityPoints = eHero:GetAbilityPoints()
    if abilityPoints <= 0 then
        Warning(eHero:GetName() .. " has no ability points. Why am I levelling up?")
        return
    end

    local abilityIndex = result.abilityIndex

    local ability = eHero:GetAbilityByIndex(abilityIndex)
    if ability:GetLevel() == ability:GetMaxLevel() then
        Warning(eHero:GetName() .. ": " .. ability:GetName() .. " is maxed out")
        return
    end
    ability:UpgradeAbility(false)
    eHero:SetAbilityPoints(abilityPoints - 1) --UpgradeAbility doesn't decrease the ability points
    -- Say(nil, eHero:GetName() .. " levelled up ability " .. abilityIndex, false)
end

function Command_controller:Attack(eHero, result)
    --Might want to check attack range
    --eHero:PerformAttack(EntIndexToHScript(result.target), true, true, false, true)
    eHero:MoveToTargetToAttack(EntIndexToHScript(result.target))
    -- Say(nil, eHero:GetName() .. " attacking " .. result.target, false)
end

function Command_controller:Cast(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)

    if eAbility and eAbility ~= nil then
        self:UseAbility(eHero, eAbility)
    end
end

function Command_controller:UseItem(eHero, result)
    local slot = result.slot
    local eItem = eHero:GetItemInSlot(slot)
    Warning("Hero" .. eHero:GetName() .. "is attempting to use item " .. eItem:GetName())
    if eItem then
        self:UseAbility(eHero, eItem)
    else
        Warning("Bot tried to use item in empty slot")
    end
end

function Command_controller:CastAbilityToggle(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        -- eAbility:OnToggle()
        eHero:CastAbilityToggle(eAbility, player)
    end
end

function Command_controller:CastAbilityNoTarget(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityNoTarget(eAbility, player)
    end
end

function Command_controller:CastAbilityTargetPoint(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
    end
end

function Command_controller:CastAbilityTargetArea(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
    end
end

function Command_controller:CastAbilityTargetUnit(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        local target = EntIndexToHScript(result.target)
        eHero:CastAbilityOnTarget(target, eAbility, player)
    end
end

function Command_controller:CastAbilityVectorTargeting(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
    end
end

function Command_controller:CastAbilityTargetUnitAOE(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local player = eHero:GetPlayerOwnerID()
        local target = EntIndexToHScript(result.target)
        eHero:CastAbilityOnTarget(target, eAbility, player)
    end
end

function Command_controller:CastAbilityComboTargetPointUnit(eHero, result)
    local eAbility = eHero:GetAbilityByIndex(result.ability)
    if self:SetupAbility(eHero, eAbility) then
        local behavior = eAbility:GetBehavior()
        local player = eHero:GetPlayerOwnerID()
        if (Utilities:Bitwise_AND(behaviour, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET)) then
            local target = EntIndexToHScript(result.target)
            eHero:CastAbilityOnTarget(target, eAbility, player)
        elseif (Utilities:Bitwise_AND(behaviour, DOTA_ABILITY_BEHAVIOR_POINT)) then
            eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
        end
    end
end

function Command_controller:SetupAbility(eHero, eAbility)
    local level = eAbility:GetLevel()
    local manaCost = eAbility:GetManaCost(level)
    if eHero:GetMana() < manaCost then
        Warning("Bot tried to use ability without mana")
        return false
    elseif eAbility:GetCooldownTimeRemaining() > 0 then
        Warning("Bot tried to use ability still on cooldown")
        return false
    end
    return true
end

function Command_controller:UseAbility(eHero, eAbility)
    local level = eAbility:GetLevel()
    local manaCost = eAbility:GetManaCost(level)
    local player = eHero:GetPlayerOwnerID()
    local behavior = eAbility:GetBehavior()

    if level == 0 then
        Warning("Bot tried to use ability without level")
        return
    end

    if eHero:GetMana() < manaCost then
        Warning("Bot tried to use ability without mana")
    elseif eAbility:GetCooldownTimeRemaining() > 0 then
        Warning("Bot tried to use ability still on cooldown")
    else
        if not eAbility:IsItem() then
            eAbility:StartCooldown(eAbility:GetCooldown(level))
            eAbility:PayManaCost()
            eAbility:OnSpellStart()
        end

        --There is some logic missing here to check for range and make the hero face the right direction
        if (Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_NO_TARGET)) then
            -- Say(nil, eHero:GetName() .. " casting " .. eAbility:GetName(), false)
            eHero:CastAbilityNoTarget(eAbility, player)
        elseif (Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_UNIT_TARGET)) then
            local target = EntIndexToHScript(result.target)
            if target:IsAlive() then
                Say(nil, eHero:GetName() .. " casting " .. eAbility:GetName() .. " on unit " .. target:GetName(), false)
                eHero:CastAbilityOnTarget(target, eAbility, player)
            end
        elseif (Utilities:Bitwise_AND(behavior, DOTA_ABILITY_BEHAVIOR_POINT)) then
            -- Say(
            --     nil,
            --     eHero:GetName() ..
            --         " casting " .. eAbility:GetName() .. " on " .. result.x .. ", " .. result.y .. ", " .. result.z,
            --     false
            -- )
            eHero:CastAbilityOnPosition(Vector(result.x, result.y, result.z), eAbility, player)
        else
            Warning(eHero:GetName() .. " sent invalid cast command " .. behavior)
            self._Error = true
        end
    end
end


return Command_controller