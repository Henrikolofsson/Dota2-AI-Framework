-- Python_AI_thinking
local Python_AI_thinking = {}

local printed = false

---@param hero table
---@return number
function Python_AI_thinking:OnThink(hero)
    -- pseudo
    -- local team_of_hero = hero:GetTeam()
    -- local allEntities = {}
    -- loopa igenom alla entiteter
        -- if entity == hero
        --     continue
        -- if entity:GetClassName() == "building" or entity:GetClassName() == "unit" or entity:GetClassName() == "hero" or entity:GetClassName() == "tree"
        --     if entity:IsVisible(team_of_hero)
        --         allEntities.push(entity)
        -- end
    -- anropa python api: "/update" med allEntities

    if not printed and hero:GetTeam() == DOTA_TEAM_BADGUYS then
        printed = true
        -- local towers = Entities:FindAllByClassname("npc_dota_tower")
        -- for _index, tower in ipairs(towers) do
        --     if tower:GetName()
        -- end
        Timers:CreateTimer({
            endTime = 40.0,
            callback = function()
                local all_units_vulnerable = FindUnitsInRadius(
                    hero:GetTeamNumber(),
                    hero:GetOrigin(),
                    nil,
                    FIND_UNITS_EVERYWHERE,
                    DOTA_UNIT_TARGET_TEAM_BOTH,
                    DOTA_UNIT_TARGET_ALL,
                    DOTA_UNIT_TARGET_FLAG_FOW_VISIBLE,
                    FIND_ANY_ORDER,
                    true
                )

                local all_units_invulnerable = FindUnitsInRadius(
                    hero:GetTeamNumber(),
                    hero:GetOrigin(),
                    nil,
                    FIND_UNITS_EVERYWHERE,
                    DOTA_UNIT_TARGET_TEAM_BOTH,
                    DOTA_UNIT_TARGET_ALL,
                    DOTA_UNIT_TARGET_FLAG_INVULNERABLE +
                    DOTA_UNIT_TARGET_FLAG_FOW_VISIBLE,
                    FIND_ANY_ORDER,
                    true
                )

                -- local visible_units = {}
                -- for _index, unit in ipairs(all_units) do
                --     if hero:CanEntityBeSeenByMyTeam(unit) then
                --         table.insert(visible_units, unit)
                --     end
                -- end

                print("Can be seen by" .. hero:GetName() .. ":")
                for _index, visible_unit in ipairs(all_units_vulnerable) do
                    print("--- " .. visible_unit:GetName())
                end
                for _index, visible_unit in ipairs(all_units_invulnerable) do
                    print("--- " .. visible_unit:GetName())
                end
            end
        })
    end

    return 0.33
end



return Python_AI_thinking