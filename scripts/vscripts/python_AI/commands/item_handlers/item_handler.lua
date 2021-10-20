local item_shop_availability = require "python_AI.commands.item_handlers.item_shop_availability"
local shoptype_model_names = require "python_AI.commands.item_handlers.shoptype_model_names"
local Item_handler = {}

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
function Item_handler:Get_shop_type(shop_entity)
    local model_name = shop_entity:GetModelName()

    if model_name == "maps/dota/entities/unnamed_11.vmdl" then --radiant home
        return 0
    elseif model_name == "maps/dota/entities/unnamed_12.vmdl" then --dire home
        return 0
    elseif model_name == "maps/dota/entities/unnamed_18.vmdl" then --radiant secret
        return 1
    elseif model_name == "maps/dota/entities/unnamed_19.vmdl" then --dire secret
        return 1
    elseif model_name == "maps/dota/entities/unnamed_23.vmdl" then --dire home
        return 0
    elseif model_name == "maps/dota/entities/unnamed_33.vmdl" then --radiant side
        return 1
    elseif model_name == "maps/dota/entities/unnamed_34.vmdl" then --dire secret
        return 1
    else
        Warning("Unknown shop " .. model_name)
        return -1
    end

    -- if not shoptype_model_names[model_name] then
    --     print("attempt buy: unknown shop")
    --     Warning("Unknown shop " .. model_name)
    --     return -1
    -- end

    -- return shoptype_model_names[model_name]
end

-- This function is generated from the game's item.txt
-- It returns true if a given item name can be bought in a certain shop type
-- 0 = home, 1 = secret shop
function Item_handler:Is_available_in_shop(item_name, shoptype)
    if not item_shop_availability[item_name] then
        print("attempt buy: not available")
        Warning(item_name .. " is unknown")
        return false
    end

    return item_shop_availability[item_name] == shoptype
end


function Item_handler:Ping_nearest_shop(eHero)
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

return Item_handler