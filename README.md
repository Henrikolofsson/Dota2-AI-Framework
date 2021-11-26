# Dota2AddonV1

## User Manual

### Settings

### Creating bots

### Chat commands

The framework uses in-game chat commands for some functionality. 
To use a chat command, press enter followed by tab. You should now be in the "all" chat channel. In that channel, type your command and press enter. 


| command | description |
|---------|-------------|
| restart | Restarts the current game. Does not decrease the counter for the number of games in this session which means that you can run this command an unlimited number of times without restarting Dota.
| end     | Ends the current game and decreases the number of remaining games. For example, if number_of_games in settings.json is 2, using the end command once will start a new game and put the number of remaining games to 1. Using end again will end the session.  |
| exit    | Immediately ends the session without taking number_of_games into account.|

### Statistics

The framework collects statistics from the game as it is running. The statistics are saved to timestamped csv files in the Server/src/statistics folder. 

It's possible to run multiple consecutive games without restarting Dota (defined in settings.json). To account for that possibility, each csv file has a suffix indicating which game it belongs to for that particular instance of Dota.

#### Statistics: defining the collection interval

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

#### Statistics: defining what statistics to collect

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

#### Statistics: hero order

Heroes are ordered within a particular game but not between games. 

Example: 
- 'npc_dota_hero_queenofpain' is in position 1 of the hero list in the Dota addon. Statistics related to this hero will be collected first and be placed in the first position for all statistics collected during that particular game.
- In the next game (either through a complete restart of the Dota client or via the restart chat command), 'npc_dota_hero_queenofpain' could be in a different position in the hero list.
- This means that you cannot rely on hero order when analyzing statistics from multiple games.

#### Statistics: restarting the game with the chat command

The framework supports restarting the current game with the "restart" chat command (sent to the "all" chat channel in-game). If this chat command is used, the statistics for the new game will be appended to the same file as the previous game. If this happens, and you still want to save the resulting data, the csv file must be manually processed and split based on the game time timestamps. Moving to the next game with the "end" command will however save the statistics to the next numbered file. 

