import csv
import os

from datetime import datetime
from typing import Iterable


class Statistics:
    def __init__(self):
        # Each data point is stored on a single row.
        # The data starts with general statistics that are not tied to a particular hero.
        # Each hero specific column is prefixed with [0-9].
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

        if not os.path.exists("statistics"):
            os.makedirs("statistics")

        t = datetime.today()
        timestamp = f"{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"
        self.filename = f"statistics/{timestamp}_game_stats.csv"

        with open(self.filename, "a", encoding="utf8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.field_names)

    def save(self, game_statistics: dict) -> bool:
        stats = self.to_csv(game_statistics)

        # newline="" is important to ensure that the csv is written properly.
        # see: https://docs.python.org/3/library/csv.html#id3
        with open(self.filename, "a", encoding="utf8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(stats)

        return True

    def to_csv(self, game_statistics: dict) -> Iterable[str]:
        return [game_statistics[field_name] for field_name in self.field_names]
