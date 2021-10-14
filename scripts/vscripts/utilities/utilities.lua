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

---@param vector table
---@return table
function Utilities:Vector_to_array(vector)
    return {vector.x, vector.y, vector.z}
end

---@param original_table table
---@param table_to_insert table
function Utilities:Insert_range(original_table, table_to_insert)
    for _index, value in ipairs(table_to_insert) do
        table.insert(original_table, value)
    end
end

return Utilities