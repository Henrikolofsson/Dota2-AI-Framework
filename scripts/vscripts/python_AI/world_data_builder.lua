-- World_data_builder
local World_data_builder = {}

function World_data_builder:Insert_base_unit_data(unit_data, unit_entity)
    unit_data.level = unit_entity:GetLevel()
    unit_data.origin = VectorToArray(unit_entity:GetOrigin())
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
    unit_data.forwardVector = VectorToArray(unit_entity:GetForwardVector())
    unit_data.isAttacking = unit_entity:IsAttacking()
end

function World_data_builder:Insert_base_hero_data(hero_data, hero_entity)
    hero_data.hasTowerAggro = self:HasTowerAggro(hero_entity)
    hero_data.abilityPoints = hero_entity:GetAbilityPoints()
    hero_data.gold = hero_entity:GetGold()
    hero_data.type = "Hero"
    hero_data.xp = hero_entity:GetCurrentXP()
    hero_data.deaths = hero_entity:GetDeaths()
    hero_data.denies = hero_entity:GetDenies()
    hero_data.items = self:JSONitems(hero_entity)

    hero_data.abilities = {}
    local abilityCount = hero_entity:GetAbilityCount() - 1 --minus 1 because lua for loops are upper boundary inclusive

    for index = 0, abilityCount, 1 do
        local eAbility = hero_entity:GetAbilityByIndex(index)
        -- abilityCount returned 16 for me even though the hero had only 5 slots (maybe it's actually max slots?). We fix that by checking for null pointer
        if eAbility then
            hero_data.abilities[index] = {}
            hero_data.abilities[index].type = "Ability"
            hero_data.abilities[index].name = eAbility:GetAbilityName()
            hero_data.abilities[index].targetFlags = eAbility:GetAbilityTargetFlags()
            hero_data.abilities[index].targetTeam = eAbility:GetAbilityTargetTeam()
            hero_data.abilities[index].targetType = eAbility:GetAbilityTargetType()
            hero_data.abilities[index].abilityType = eAbility:GetAbilityType()
            hero_data.abilities[index].abilityIndex = eAbility:GetAbilityIndex()
            hero_data.abilities[index].level = eAbility:GetLevel()
            hero_data.abilities[index].maxLevel = eAbility:GetMaxLevel()
            hero_data.abilities[index].abilityDamage = eAbility:GetAbilityDamage()
            hero_data.abilities[index].abilityDamageType = eAbility:GetAbilityDamage()
            hero_data.abilities[index].cooldownTime = eAbility:GetCooldownTime()
            hero_data.abilities[index].cooldownTimeRemaining = eAbility:GetCooldownTimeRemaining()
            hero_data.abilities[index].behavior = eAbility:GetBehavior()
            hero_data.abilities[index].toggleState = eAbility:GetToggleState()
        end
    end
end

function World_data_builder:Get_unit_data(unit_entity)
    local unit_data = {}
    World_data_builder:Insert_base_unit_data(unit_data, unit_entity)

    if unit_entity:IsHero() then
        World_data_builder:Insert_base_hero_data(unit_data, unit_entity)

    elseif unit_entity:IsBuilding() then
        if unit_entity:IsTower() then
            unit_data.type = "Tower"
        else
            unit_data.type = "Building"
        end
    else
        unit_data.type = "BaseNPC"
    end

    local attackTarget = unit_entity:GetAttackTarget()
    if attackTarget then
        unit_data.attackTarget = attackTarget:entindex()
    end

    return unit_data
end






function World_data_builder:Get_tree_data(tree_entity)
    local tree_data = {}
    tree_data.origin = VectorToArray(tree_entity:GetOrigin())
    tree_data.type = "Tree"
    return tree_data
end

function World_data_builder:Insert_trees(entities, hero)
    local tree_entity = Entities:FindByClassname(nil, "ent_dota_tree")
    while tree_entity ~= nil do
        if hero:CanEntityBeSeenByMyTeam(tree_entity) and not tree_entity:IsStanding() then
            entities[tree_entity:entindex()] = World_data_builder:Get_tree_data(tree_entity)
        end
        tree_entity = Entities:FindByClassname(tree_entity, "ent_dota_tree")
    end
end

---@param hero table
---@param should_get_invulnerable boolean
---@return table
function World_data_builder:Get_all_units(hero, should_get_invulnerable)
    local invulnerable_flag = 0

    if should_get_invulnerable then
        invulnerable_flag = DOTA_UNIT_TARGET_FLAG_INVULNERABLE
    end

    return FindUnitsInRadius(
        hero:GetTeamNumber(),
        hero:GetOrigin(),
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

function World_data_builder:Insert_all_units(entities, hero, should_insert_invulnerable)
    local all_units = World_data_builder:Get_all_units(hero, should_insert_invulnerable)
    local bot_team = hero:GetTeam()

    for _index, unit in ipairs(all_units) do
        entities[unit:entindex()] = World_data_builder:Get_unit_data(unit)
    end
end

---@param hero table
---@return table
function World_data_builder:Get_all_entities(hero)
    local entities = {}

    World_data_builder:Insert_trees(entities, hero)

    World_data_builder:Insert_all_units(entities, hero, false)

    World_data_builder:Insert_all_units(entities, hero, true)

    return entities
end

return World_data_builder