"""
graphs.py
---------
Bonus feature: plots temperature trend graphs using matplotlib.
"""

import matplotlib.pyplot as plt


def plot_temperature_trend(trend_data: list, city: str):
    """trend_data: list of (timestamp, temperature) tuples."""
    if not trend_data:
        print("No data available to plot.")
        return

    timestamps = [t[0] for t in trend_data]
    temps = [t[1] for t in trend_data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temps, marker="o", color="#2b7de9")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Temperature Trend - {city.title()}")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature (°C)")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    filename = f"{city.lower().replace(' ', '_')}_temperature_trend.png"
    plt.savefig(filename)
    print(f"Graph saved as: {filename}")
    plt.show()
