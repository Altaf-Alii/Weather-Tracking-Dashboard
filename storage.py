"""
storage.py
----------
Handles saving and loading weather history records.
Stores data in BOTH JSON (easy to parse/analyze in Python)
and CSV (easy to open in Excel) for flexibility.
"""

import json
import csv
import os
from datetime import datetime


class WeatherStorage:
    def __init__(self, json_path="data/weather_history.json",
                 csv_path="data/weather_history.csv"):
        self.json_path = json_path
        self.csv_path = csv_path

        folder = os.path.dirname(json_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(json_path):
            with open(json_path, "w") as f:
                json.dump([], f)

    def save_record(self, weather_data: dict) -> dict:
        """Append one weather record to both JSON and CSV history files."""
        record = {
            "city": weather_data["city"],
            "country": weather_data.get("country", ""),
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "condition": weather_data["condition"],
            "wind_speed": weather_data["wind_speed"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        history = self.load_json_history()
        history.append(record)
        with open(self.json_path, "w") as f:
            json.dump(history, f, indent=2)

        self._append_csv(record)
        return record

    def _append_csv(self, record: dict):
        file_exists = os.path.exists(self.csv_path)
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)

    def load_json_history(self) -> list:
        """Load all saved weather records."""
        try:
            with open(self.json_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
