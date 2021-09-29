local Utilities = {}

---@param tableToSearch table
---@param valueToFind any
---@return boolean
function Utilities:Table_includes_value(tableToSearch, valueToFind) -- unused
    for _index, value in ipairs(tableToSearch) do
        if value == valueToFind then
            return true
        end
    end

    return false
end

function Utilities:Get_table_length(table_to_count)
    local count = 0
    for _ in pairs(table_to_count) do
        count = count + 1
    end
    return count
end

return Utilities