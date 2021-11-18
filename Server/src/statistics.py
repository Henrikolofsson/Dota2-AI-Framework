import os

from datetime import datetime


class Statistics:
    def __init__(self):
        if not os.path.exists("statistics"):
            os.makedirs("statistics")

        t = datetime.today()
        timestamp = f"{t.year}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}"
        self.filename = f"statistics/{timestamp}_game_stats.csv"

    def save(self, game_statistics: dict) -> bool:
        stats = self.to_csv(game_statistics)

        # Opens the file in append mode, meaning that new data will be written to
        # the end of the file if the file already exists, otherwise a new file will
        # be created.
        with open(self.filename, "a", encoding="utf") as f:
            f.write(str(stats))
            f.write("\n")

        return True

    def to_csv(self, game_statistics: dict):
        # Not implemented.
        return game_statistics
