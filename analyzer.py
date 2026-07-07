"""
analyzer.py
-----------
Analyzes stored weather history: averages, trends,
most common conditions, and filtering by city/date.
"""

from collections import defaultdict


class WeatherAnalyzer:
    def __init__(self, history: list):
        self.history = history

    def filter_by_city(self, city: str) -> list:
        city = city.strip().lower()
        return [r for r in self.history if r["city"].strip().lower() == city]

    def filter_by_date(self, date_str: str) -> list:
        """date_str format: YYYY-MM-DD"""
        return [r for r in self.history if r["timestamp"].startswith(date_str)]

    def average_temperature(self, city: str = None):
        records = self.filter_by_city(city) if city else self.history
        if not records:
            return None
        temps = [r["temperature"] for r in records]
        return sum(temps) / len(temps)

    def temperature_trend(self, city: str) -> list:
        """Returns list of (timestamp, temperature) tuples, sorted by time."""
        records = sorted(self.filter_by_city(city), key=lambda r: r["timestamp"])
        return [(r["timestamp"], r["temperature"]) for r in records]

    def most_common_condition(self, city: str = None):
        records = self.filter_by_city(city) if city else self.history
        counts = defaultdict(int)
        for r in records:
            counts[r["condition"]] += 1
        if not counts:
            return None
        return max(counts.items(), key=lambda x: x[1])
