import csv
import os

from datetime import datetime
from typing import Iterable


class Statistics:
    def __init__(self, number_of_games: int):
        if not os.path.exists("statistics"):
            os.makedirs("statistics")

        # Each data point is stored on a single row. The data starts with general statistics
        # that are not tied to a particular hero. Each hero specific column is prefixed with 0-9.
        #
        # game_time = Number of seconds elapsed since map start (doesn't count up when the game is paused) (float).
        # x_id      = The hero's in-game player id (int)
        # x_team    = The team the hero is on. Radiant is 2, Dire is 3 (int).
        # x_name    = The hero's name, e.g. "npc_dota_hero_puck" (str).
        # x_gold    = The hero's current gold value (int).
        self.field_names = (
            'game_time',
            '0_id', '0_team', '0_name', '0_gold',
            '1_id', '1_team', '1_name', '1_gold',
            '2_id', '2_team', '2_name', '2_gold',
            '3_id', '3_team', '3_name', '3_gold',
            '4_id', '4_team', '4_name', '4_gold',
            '5_id', '5_team', '5_name', '5_gold',
            '6_id', '6_team', '6_name', '6_gold',
            '7_id', '7_team', '7_name', '7_gold',
            '8_id', '8_team', '8_name', '8_gold',
            '9_id', '9_team', '9_name', '9_gold',
        )

        # In the settings file there's a setting for the number of games that can be played
        # without restarting Dota. Each game gets its own statistics file with the _x suffix
        # starting at 0 for the first game.
        self.number_of_games = number_of_games

        t = datetime.today()
        timestamp = f"{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"

        # Maps from i -> "statistics/2021_11_18_14_23_14_game_stats_i.csv"
        self.filenames = {i: f"statistics/{timestamp}_game_stats_{i}.csv"
                          for i in range(self.number_of_games)}

        for filename in self.filenames.values():
            with open(filename, "a", encoding="utf8", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(self.field_names)

    def save(self, game_statistics: dict) -> bool:
        game_number = game_statistics['game_number']
        filename = self.filenames[game_number]
        stats = self.to_csv(game_statistics)

        # newline="" is important to ensure that the csv is written properly.
        # see: https://docs.python.org/3/library/csv.html#id3
        with open(filename, "a", encoding="utf8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(stats)

        return True

    def to_csv(self, game_statistics: dict) -> Iterable[str]:
        return [game_statistics['fields'][field_name] for field_name in self.field_names]
