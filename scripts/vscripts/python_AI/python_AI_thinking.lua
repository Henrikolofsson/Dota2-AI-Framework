local Python_AI_thinking = {}

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
    return 0.33
end

return Python_AI_thinking