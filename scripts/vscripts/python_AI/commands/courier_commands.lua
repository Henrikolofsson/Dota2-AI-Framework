local Courier_commands = {}

local courier_origin_pos = {}
local stash_use_range = 700
local max_transfer_range = 500
local stash_position_radiant = Vector(-6554.667480, -6723.997559, 384.000000)
local stash_position_dire = Vector(7413.382324, 6215.563965, 384.000000)

function Courier_commands:Move_to_hero(hero_entity)
    --[[
        GetPreferredCourierForPlayer always returns the courier that's associated
        with a particular hero. This matches what you would expect in a real game
        of Dota where you can only use your own courier.

        The MoveToNPC command continues to be applied on subsequent game ticks, i.e.
        you only have issue it once and the NPC in question (courier in this case)
        will continue close the distance to the target NPC. It still continues to do
        this even if it is standing right next to the target. In other words, you
        have to issue a stop command for it to stop following the hero.
    ]]
    local player_id = hero_entity:GetPlayerOwnerID()
    local courier_entity = PlayerResource:GetPreferredCourierForPlayer(player_id)

    Courier_commands:Save_courier_origin(courier_entity)
    courier_entity:MoveToNPC(hero_entity)
end

function Courier_commands:Hold(hero_entity)
    --[[
        Stops the courier at its current position. Because COURIER_MOVE_TO_HERO never
        stops the courier from following the hero, a stop command is necessary if the
        AI changes its mind and wants to leave the courier at its current position.

        todo: currently has the unintended side effect of putting the courier in a
        permanent hold position where it doesn't move when told to retrieve items.
    ]]
    local player_id = hero_entity:GetPlayerOwnerID()
    local courier = PlayerResource:GetPreferredCourierForPlayer(player_id)
    courier:Hold()
end

function Courier_commands:Move_to_base(courier)
    --[[
        Moves a courier to its origin position.
        The origin position is the vector where a particular courier spawned at
        the start of the game.
    ]]
    courier:MoveToPosition(courier_origin_pos[courier])
end

function Courier_commands:Retrieve(hero_entity)
    --[[
        1. Courier moves to within range of the stash.
            - Range is defined by @stash_use_range.
        2. Courier picks up the items from the stash.
        3. Courier moves towards the hero.
        4. Courier delivers items when it's within the range.
            - Range is defined by @max_transfer_range.
        5. Courier moves back to its origin position.

        Currently ignores all edge cases like full inventories, courier deaths, and other
        things that might come up later.
    ]]
    local player_id = hero_entity:GetPlayerOwnerID()
    local courier_entity = PlayerResource:GetPreferredCourierForPlayer(player_id)
    local team = hero_entity:GetTeam()
    local stash_position = team == DOTA_TEAM_GOODGUYS and stash_position_radiant or stash_position_dire

    Courier_commands:Save_courier_origin(courier_entity)
    courier_entity:MoveToPosition(stash_position)

    Timers:CreateTimer(function()
        if courier_entity:IsPositionInRange(stash_position, stash_use_range) then
            Courier_commands:Get_stashed_items(hero_entity, courier_entity)
            courier_entity:MoveToNPC(hero_entity)

            Timers:CreateTimer(function()
                local range_to_hero = courier_entity:GetRangeToUnit(hero_entity)
                if range_to_hero <= max_transfer_range then
                    Courier_commands:Transfer_to_hero(hero_entity, courier_entity)
                    Courier_commands:Move_to_base(courier_entity)
                    return nil
                end
                return 1.0
              end
            )

            return nil
        end
        return 1.0
      end
    )
end

function Courier_commands:Transfer_to_hero(hero_entity, courier_entity)
    for i = DOTA_ITEM_SLOT_1, DOTA_ITEM_SLOT_9 do
        local maybe_item = courier_entity:GetItemInSlot(i)
        if maybe_item then
            local item = courier_entity:TakeItem(maybe_item)
            hero_entity:AddItem(item)
        end
    end
end

function Courier_commands:Get_stashed_items(hero_entity, courier_entity)
    for i = DOTA_STASH_SLOT_1, DOTA_STASH_SLOT_6 do
        local stashed_item = hero_entity:GetItemInSlot(i)
        if stashed_item then
            local item = hero_entity:TakeItem(stashed_item)
            courier_entity:AddItem(item)
        end
    end
end

function Courier_commands:Save_courier_origin(courier_entity)
    if not courier_origin_pos[courier_entity] then
        courier_origin_pos[courier_entity] = courier_entity:GetOrigin()
    end
end

return Courier_commands