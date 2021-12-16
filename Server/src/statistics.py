import csv
import json
import os

from datetime import datetime
from itertools import chain
from typing import Iterable


class Statistics:
    def __init__(self, number_of_games: int):
        if not os.path.exists("statistics"):
            os.makedirs("statistics")

        # Each data point is stored on a single row. The data starts with general statistics
        # that are not tied to a particular hero (e.g. game time). Each hero specific column
        # is prefixed with 0-9.

        # Hero specific fields:
        hero_fields = (
            'id', 'team', 'name', 'gold', 'level', 'dmg_dealt_hero', 'dmg_dealt_struct', 'dmg_dealt_creep',
            'total_dmg_dealt', 'dmg_received_hero', 'dmg_received_struct', 'dmg_received_creep',
            'total_dmg_received', 'last_hits', 'kills', 'deaths', 'assists', 'denies'
        )

        all_hero_fields = [[f"{i}_{field_name}" for field_name in hero_fields] for i in range(10)]

        # Flatten the hero fields from [[0_id, 0_team, ...], [1_id, 1_team, ...], ...]
        # to [0_id, 0_team, 1_id, 1_team, ...]
        flattened_hero_fields = chain.from_iterable(all_hero_fields)

        # building fields currently not implemented.
        building_names = (
            'bad_rax_melee_top',
            'bad_rax_melee_mid',
            'bad_rax_melee_bot',
            'bad_rax_range_top',
            'bad_rax_range_mid',
            'bad_rax_range_bot',
            'dota_badguys_tower1_top',
            'dota_badguys_tower1_mid',
            'dota_badguys_tower1_bot',
            'dota_badguys_tower2_top',
            'dota_badguys_tower2_mid'
            'dota_badguys_tower2_bot',
            'dota_badguys_tower3_top',
            'dota_badguys_tower3_mid',
            'dota_badguys_tower3_bot',
            'dota_badguys_tower4_top',
            'dota_badguys_tower4_bot',
            'dota_badguys_fort',
            'good_rax_melee_top',
            'good_rax_melee_mid',
            'good_rax_melee_bot',
            'good_rax_range_top',
            'good_rax_range_mid',
            'good_rax_range_bot',
            'dota_goodguys_tower1_top',
            'dota_goodguys_tower1_mid',
            'dota_goodguys_tower1_bot',
            'dota_goodguys_tower2_top',
            'dota_goodguys_tower2_mid',
            'dota_goodguys_tower2_bot',
            'dota_goodguys_tower3_top',
            'dota_goodguys_tower3_mid',
            'dota_goodguys_tower3_bot',
            'dota_goodguys_tower4_top',
            'dota_goodguys_tower4_bot',
            'dota_badguys_fort'
        )

        building_fields = ('dmg_dealt', 'dmg_received', 'team', 'destroyed_time')
        all_building_fields = [[f"{name}_{field}" for field in building_fields] for name in building_names]
        flattened_building_fields = chain.from_iterable(all_building_fields)

        self.field_names = (
            'game_time',
            *flattened_hero_fields,  # * expands the fields into field names.
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

        self.end_filenames = {i: f"statistics/{timestamp}_game_stats_{i}_end.json"
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

    def end_game_stats(self, end_stats: dict) -> bool:
        game_number = end_stats['game_number']
        filename = self.end_filenames[game_number]

        with open(filename, 'w', encoding='utf8') as fp:
            fp.write(json.dumps(end_stats['end_stats'], indent=4))

        return True
