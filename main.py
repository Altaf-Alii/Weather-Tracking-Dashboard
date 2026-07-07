"""
main.py
-------
Entry point of the Weather Tracking Dashboard.
Provides a simple CLI menu:
1. Get Weather
2. View History
3. Analyze Data
4. Save Data (export info)
5. Exit
"""

import os
import sys

from dotenv import load_dotenv

from weather_api import WeatherAPI, WeatherAPIError
from storage import WeatherStorage
from analyzer import WeatherAnalyzer

load_dotenv()


def print_header(title: str):
    print("\n" + "=" * 42)
    print(title.center(42))
    print("=" * 42)


def display_weather(data: dict):
    print_header(f"Weather in {data['city']}, {data['country']}")
    print(f"Condition   : {data['condition']} ({data['description']})")
    print(f"Temperature : {data['temperature']} °C")
    print(f"Feels Like  : {data['feels_like']} °C")
    print(f"Humidity    : {data['humidity']}%")
    print(f"Wind Speed  : {data['wind_speed']} m/s")


def get_weather_flow(api: WeatherAPI, storage: WeatherStorage):
    city = input("Enter city name: ").strip()
    if not city:
        print("City name cannot be empty.")
        return

    try:
        data = api.get_weather(city)  # case-insensitive - API handles it
    except WeatherAPIError as e:
        print(f"Error: {e}")
        return

    display_weather(data)

    save = input("\nSave this record to history? (y/n): ").strip().lower()
    if save == "y":
        storage.save_record(data)
        print("Saved to history.")

    refresh = input("Refresh this city's weather again? (y/n): ").strip().lower()
    if refresh == "y":
        get_weather_flow(api, storage)


def view_history(storage: WeatherStorage):
    history = storage.load_json_history()
    if not history:
        print("\nNo history found yet. Fetch some weather first!")
        return

    print_header("Weather History (last 20 records)")
    print(f"{'Timestamp':<20} | {'City':<15} | {'Temp':<7} | Condition")
    print("-" * 60)
    for r in history[-20:]:
        print(f"{r['timestamp']:<20} | {r['city']:<15} | {r['temperature']:<6}°C | {r['condition']}")


def analyze_data(storage: WeatherStorage):
    history = storage.load_json_history()
    if not history:
        print("\nNo data available to analyze yet.")
        return

    analyzer = WeatherAnalyzer(history)

    print_header("Analyze Data")
    print("1. Average temperature (by city)")
    print("2. Temperature trend (by city) + graph")
    print("3. Most common weather condition")
    print("4. Filter records by date")
    choice = input("Choose option (1-4): ").strip()

    if choice == "1":
        city = input("Enter city: ").strip()
        avg = analyzer.average_temperature(city)
        if avg is None:
            print(f"No records found for '{city}'.")
        else:
            print(f"Average temperature in {city}: {avg:.1f} °C")

    elif choice == "2":
        city = input("Enter city: ").strip()
        trend = analyzer.temperature_trend(city)
        if not trend:
            print(f"No records found for '{city}'.")
            return
        for t, temp in trend:
            print(f"{t} -> {temp} °C")
        plot = input("\nPlot this trend as a graph? (y/n): ").strip().lower()
        if plot == "y":
            from graphs import plot_temperature_trend
            plot_temperature_trend(trend, city)

    elif choice == "3":
        city = input("Enter city (leave blank for all cities): ").strip() or None
        result = analyzer.most_common_condition(city)
        if result is None:
            print("No data found.")
        else:
            condition, count = result
            print(f"Most common condition: {condition} ({count} times)")

    elif choice == "4":
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        records = analyzer.filter_by_date(date_str)
        if not records:
            print(f"No records found on {date_str}.")
            return
        for r in records:
            print(f"{r['timestamp']} | {r['city']} | {r['temperature']}°C | {r['condition']}")

    else:
        print("Invalid option.")


def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("ERROR: OPENWEATHER_API_KEY not found.")
        print("Create a '.env' file in this folder with:")
        print("  OPENWEATHER_API_KEY=your_api_key_here")
        sys.exit(1)

    api = WeatherAPI(api_key)
    storage = WeatherStorage()

    while True:
        print_header("Weather Tracking Dashboard")
        print("1. Get Weather")
        print("2. View History")
        print("3. Analyze Data")
        print("4. Save Data (export info)")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            get_weather_flow(api, storage)
        elif choice == "2":
            view_history(storage)
        elif choice == "3":
            analyze_data(storage)
        elif choice == "4":
            print("\nData is auto-saved at:")
            print("  data/weather_history.json")
            print("  data/weather_history.csv")
        elif choice == "5":
            print("\nGoodbye! Stay weather-aware.")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
