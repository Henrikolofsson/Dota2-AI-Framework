Utilities = {}

---@param tableToSearch table
---@param valueToFind any
---@return boolean
function Utilities:Table_includes_value(tableToSearch, valueToFind)
    for _index, value in ipairs(tableToSearch) do
        if value == valueToFind then
            return true
        end
    end

    return false
end

return Utilities