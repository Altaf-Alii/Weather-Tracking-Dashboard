# 🌦 Weather Tracking Dashboard with History Storage

A CLI-based Python application that fetches real-time weather using the
OpenWeatherMap API, stores historical records (JSON + CSV), and lets you
analyze past weather trends (averages, most common condition, graphs).

## 📁 Project Structure

```
weather_dashboard/
├── main.py            # CLI menu / entry point
├── weather_api.py      # OpenWeatherMap API integration
├── storage.py          # Save/load history (JSON + CSV)
├── analyzer.py         # Trend analysis, filters, averages
├── graphs.py            # Bonus: matplotlib temperature graphs
├── requirements.txt
├── .env.example         # Template for your API key
├── data/
│   └── sample_weather_data.json   # Sample data for demo/testing
└── README.md
```

## 🔑 1. Get an OpenWeatherMap API Key

1. Go to https://openweathermap.org/api
2. Create a free account and sign in.
3. Go to "API Keys" tab in your profile.
4. Copy your default API key (new keys can take 10–60 minutes to activate).

## ⚙️ 2. Setup

```bash
# Clone or unzip the project, then go inside it
cd weather_dashboard

# (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root (copy from `.env.example`):

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

## ▶️ 3. Run the App

```bash
python main.py
```

You'll see a menu:

```
1. Get Weather
2. View History
3. Analyze Data
4. Save Data (export info)
5. Exit
```

- **Get Weather** – enter any city name (case-insensitive), see live weather,
  optionally save it to history.
- **View History** – shows last 20 saved records.
- **Analyze Data** – average temperature by city, temperature trend + graph,
  most common condition, filter by date.
- **Save Data** – shows where your data is stored on disk.
- **Exit** – quits the app.

## 💾 Data Storage

Every saved record is written to:
- `data/weather_history.json`
- `data/weather_history.csv`

Each record includes: city, country, temperature, humidity, condition,
wind speed, and timestamp.

## 🛡 Error Handling

- Invalid city name → friendly error, asks to re-check spelling.
- No internet connection → clear error message, no crash.
- Invalid/missing API key → tells you to check `.env`.

## 🌟 Bonus Features Included

- Temperature trend graphs using `matplotlib` (saved as PNG + shown on screen).
- Case-insensitive city search.
- Modular code (API, storage, analysis, graphs all separated).

## 🚀 Possible Extensions

- Streamlit/Tkinter GUI dashboard
- Multi-city auto-refresh tracking
- Rain/storm alert notifications

## 📄 License

Free to use for learning and educational purposes.
