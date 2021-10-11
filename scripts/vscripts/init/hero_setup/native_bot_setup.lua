local Native_bot_setup = {}

---@param picked_hero_names table
function Native_bot_setup:Create_bots(picked_hero_names)
    local lanes = {"mid", "top", "bot", "top", "bot"}
    for i = 1, 5 do
        Tutorial:AddBot(picked_hero_names[i], lanes[i], Settings.NATIVE_BOTS_DIFFICULTY, false)
    end
end

return Native_bot_setup