-- imports
local Utilities = require "utilities.utilities"



-- World_data_builder
local World_data_builder = {}
World_data_builder.entities = nil
World_data_builder.all_units = nil
World_data_builder.requesting_hero = nil
---@type integer
World_data_builder.requesting_team = nil


---@param unit_data table
---@param unit_entity table
function World_data_builder:Insert_base_unit_data(unit_data, unit_entity)
    local attackTarget = unit_entity:GetAttackTarget()
    if attackTarget then
        unit_data.attackTarget = attackTarget:entindex()
    else
        unit_data.attackTarget = nil
    end
    unit_data.level = unit_entity:GetLevel()
    unit_data.origin = Utilities:Vector_to_array(unit_entity:GetOrigin())
    unit_data.health = unit_entity:GetHealth()
    unit_data.maxHealth = unit_entity:GetMaxHealth()
    unit_data.mana = unit_entity:GetMana()
    unit_data.maxMana = unit_entity:GetMaxMana()
    unit_data.alive = unit_entity:IsAlive()
    unit_data.blind = unit_entity:IsBlind()
    unit_data.dominated = unit_entity:IsDominated()
    unit_data.deniable = unit_entity:Script_IsDeniable()
    unit_data.disarmed = unit_entity:IsDisarmed()
    unit_data.rooted = unit_entity:IsRooted()
    unit_data.name = unit_entity:GetName()
    unit_data.team = unit_entity:GetTeamNumber()
    unit_data.attackRange = unit_entity:Script_GetAttackRange()
    unit_data.forwardVector = Utilities:Vector_to_array(unit_entity:GetForwardVector())
    unit_data.isAttacking = unit_entity:IsAttacking()
end

---@param hero_entity table
---@return table items
function World_data_builder:Get_items_data(hero_entity)
    local items = {}
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_6, 1 do
        local item = hero_entity:GetItemInSlot(i)
        items[i] = {}
        if item then
            items[i].name = item:GetName()
            items[i].slot = item:GetItemSlot()
            items[i].charges = item:GetCurrentCharges()
            items[i].castRange = item:GetCastRange()
        end
    end
    return items
end

---@param hero_entity table
---@return boolean
function World_data_builder:Has_tower_aggro(hero_entity)
    for _index, unit in ipairs(self.all_units) do
        if unit:IsTower() then
            ---@type table
            local aggro_target = unit:GetAggroTarget()
            if aggro_target == hero_entity then
                return true
            end
        end
    end
    return false
end

---@param hero_entity table
---@return integer
function World_data_builder:Get_hero_ability_count(hero_entity)
    return hero_entity:GetAbilityCount() - 1 --minus 1 because lua for loops are upper boundary inclusive
end

---@param hero_entity table
---@return table abilities
function World_data_builder:Get_hero_abilities(hero_entity)
    local abilities = {}
    local ability_count = self:Get_hero_ability_count(hero_entity)

    for index = 0, ability_count, 1 do
        local ability_entity = hero_entity:GetAbilityByIndex(index)
        -- abilityCount returned 16 for me even though the hero had only 5 slots (maybe it's actually max slots?). We fix that by checking for null pointer
        if ability_entity then
            abilities[index] = {}
            abilities[index].type = "Ability"
            abilities[index].name = ability_entity:GetAbilityName()
            abilities[index].targetFlags = ability_entity:GetAbilityTargetFlags()
            abilities[index].targetTeam = ability_entity:GetAbilityTargetTeam()
            abilities[index].targetType = ability_entity:GetAbilityTargetType()
            abilities[index].abilityType = ability_entity:GetAbilityType()
            abilities[index].abilityIndex = ability_entity:GetAbilityIndex()
            abilities[index].level = ability_entity:GetLevel()
            abilities[index].maxLevel = ability_entity:GetMaxLevel()
            abilities[index].abilityDamage = ability_entity:GetAbilityDamage()
            abilities[index].abilityDamageType = ability_entity:GetAbilityDamage()
            abilities[index].cooldownTime = ability_entity:GetCooldownTime()
            abilities[index].cooldownTimeRemaining = ability_entity:GetCooldownTimeRemaining()
            abilities[index].behavior = ability_entity:GetBehavior()
            abilities[index].toggleState = ability_entity:GetToggleState()
        end
    end

    return abilities
end

---@param hero_data table
---@param hero_entity table
function World_data_builder:Insert_base_hero_data(hero_data, hero_entity)
    hero_data.type = "Hero"
    hero_data.hasTowerAggro = self:Has_tower_aggro(hero_entity)
    hero_data.deaths = hero_entity:GetDeaths()
    hero_data.items = self:Get_items_data(hero_entity)

    -- should not be seen by enemy team BEGIN
    hero_data.denies = hero_entity:GetDenies()
    hero_data.xp = hero_entity:GetCurrentXP()
    hero_data.gold = hero_entity:GetGold()
    hero_data.abilityPoints = hero_entity:GetAbilityPoints()

    hero_data.abilities = self:Get_hero_abilities(hero_entity)
    -- should not be seen by enemy team END
end

---@param unit_entity table
---@return table unit_data
function World_data_builder:Get_unit_data(unit_entity)
    local unit_data = {}
    self:Insert_base_unit_data(unit_data, unit_entity)

    if unit_entity:IsHero() then
        self:Insert_base_hero_data(unit_data, unit_entity)

    elseif unit_entity:IsBuilding() then
        if unit_entity:IsTower() then
            unit_data.type = "Tower"
        else
            unit_data.type = "Building"
        end
    else
        unit_data.type = "BaseNPC"
    end

    return unit_data
end

---@param tree_entity table
---@return table tree_data
function World_data_builder:Get_tree_data(tree_entity)
    local tree_data = {}
    tree_data.origin = Utilities:Vector_to_array(tree_entity:GetOrigin())
    tree_data.type = "Tree"
    return tree_data
end

function World_data_builder:Insert_trees()
    local tree_entity = Entities:FindByClassname(nil, "ent_dota_tree")
    while tree_entity ~= nil do
        if IsLocationVisible(self.requesting_hero:GetTeam(), tree_entity:GetOrigin()) and tree_entity:IsStanding() then
            self.entities[tree_entity:entindex()] = self:Get_tree_data(tree_entity)
        end
        tree_entity = Entities:FindByClassname(tree_entity, "ent_dota_tree")
    end
end

---@param flags table should_get_invulnerable: ```boolean```
---@return table all_units
function World_data_builder:Get_all_units(flags)
    local invulnerable_flag = 0

    if flags.should_get_invulnerable then
        invulnerable_flag = DOTA_UNIT_TARGET_FLAG_INVULNERABLE
    end

    return FindUnitsInRadius(
        self.requesting_hero:GetTeamNumber(),
        self.requesting_hero:GetOrigin(),
        nil,
        FIND_UNITS_EVERYWHERE,
        DOTA_UNIT_TARGET_TEAM_BOTH,
        DOTA_UNIT_TARGET_ALL,
        DOTA_UNIT_TARGET_FLAG_FOW_VISIBLE +
        invulnerable_flag,
        FIND_ANY_ORDER,
        true
    )
end

function World_data_builder:Insert_all_units()
    self.all_units = self:Get_all_units( { should_get_invulnerable = false } )
    Utilities:Insert_range(self.all_units, self:Get_all_units( { should_get_invulnerable = true } ))

    for _index, unit in ipairs(self.all_units) do
        self.entities[unit:entindex()] = self:Get_unit_data(unit)
    end
end

---@param hero_entity table
---@return table entities
function World_data_builder:Get_all_entities(hero_entity)
    self.requesting_hero = hero_entity
    self.requesting_team = hero_entity:GetTeam()
    self.entities = {}
    self.all_units = {}

    self:Insert_trees()
    self:Insert_all_units()

    return self.entities
end

return World_data_builder