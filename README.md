# Dota2AddonV1

## User Manual

### 1. Collecting Statistics

The framework collects statistics from the game as it is running. The statistics are saved to timestamped csv files in the Server/src/statistics folder. 

It's possible to run multiple consecutive games without restarting Dota (defined in settings.json). To account for that possibility, each csv file has a suffix indicating which game it belongs to for that particular instance of Dota.

#### 1.1 Defining collection interval

You can adjust how often statistics are collected by setting the collection_interval variable in the function Python_AI_setup:Set_statistics_collection.

```lua
function Python_AI_setup:Set_statistics_collection(radiant_heroes, dire_heroes)
    --[[
        Creates a timer that runs the Python_AI_thinking:Collect_and_send_statistics
        function once every @collection_interval seconds.
    ]]
    local collection_interval = 5
end
```

#### 1.2 Defining what statistics to collect

To collect statistics that are not currently collected you must do the following:
1. (Re)define the column names for the csv file in Statistics.py.
2. Collect the appropriate statistics and add them to the stats table in the Collect_statistics function in the Lua addon.

```lua
function Python_AI_thinking:Collect_statistics(radiant_heroes, dire_heroes, game_number)
    local heroes = Utilities:Concat_lists(radiant_heroes, dire_heroes)
    local stats = {}
    local fields = {}
    ...
    return stats
end
```
3. The statistics are sent as a JSON document to the Python server. You must ensure that the to_csv method in Statistics.py correctly translates the statistics that you've gathered into csv that matches the columns that you have defined. 

#### 1.3 Caveats

##### 1.3.1 Hero order

Heroes are ordered within a particular game but not between games. 

Example: 
- 'npc_dota_hero_queenofpain' is in position 1 of the hero list in the Dota addon. Statistics related to this hero will be collected first and be placed in the first position for all statistics collected during that particular game.
- In the next game (either through a complete restart of the Dota client or via the restart chat command), 'npc_dota_hero_queenofpain' could be in a different position in the hero list.
- This means that you cannot rely on hero order when analyzing statistics from multiple games.

##### 1.3.2 Restarting the game with the chat command

The framework supports restarting the current game with the "restart" chat command (sent to the "all" chat channel in-game). If this chat command is used, the statistics for the new game will be appended to the same file as the previous game. If this happens, and you still want to save the resulting data, the csv file must be manually processed and split based on the game time timestamps.

