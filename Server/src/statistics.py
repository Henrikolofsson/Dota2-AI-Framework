import csv
import os

from datetime import datetime
from typing import Iterable


class Statistics:
    def __init__(self):
        if not os.path.exists("statistics"):
            os.makedirs("statistics")

        t = datetime.today()
        timestamp = f"{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"
        self.filename = f"statistics/{timestamp}_game_stats.csv"

    def save(self, game_statistics: dict) -> bool:
        stats = self.to_csv(game_statistics)

        # newline="" is important to ensure that the csv is written properly.
        # see: https://docs.python.org/3/library/csv.html#id3
        with open(self.filename, "a", encoding="utf8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(stats)

        return True

    def to_csv(self, game_statistics: dict) -> Iterable[str]:
        return str(game_statistics).split(" ")  # placeholder
