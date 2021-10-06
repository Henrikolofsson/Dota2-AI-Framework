local Utilities = {}

---@param table_to_search table
---@param value_to_find any
---@return boolean
function Utilities:Table_includes_value(table_to_search, value_to_find) -- unused
    for _index, value in ipairs(table_to_search) do
        if value == value_to_find then
            return true
        end
    end

    return false
end

---@param table_to_count table
---@return integer
function Utilities:Get_table_length(table_to_count)
    local count = 0
    for _ in pairs(table_to_count) do
        count = count + 1
    end
    return count
end

return Utilities