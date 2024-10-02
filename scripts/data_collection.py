import requests
import json
import os
from datetime import datetime, timedelta
import time
import yaml

# Load API key from config
def load_api_key(config_path):
    """Load the API key from config.yaml file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config['api_key']

# Historical data from OpenWeather API
def fetch_openweather_historical_data(lat, lon, start_date, end_date, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start_date}&end={end_date}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from OpenWeather API (historical): {response.status_code}")
        return None

# Save data to a folder
def save_data(data, filename, output_dir):
    if data:
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, filename), 'w') as f:
            json.dump(data, f)
        print(f"Data saved to {filename}")
    else:
        print(f"No data to save for {filename}")

if __name__ == "__main__":
    city = "Pune"
    
    # Load API key from config file
    config_path = 'config/config.yaml'
    weather_api_key = load_api_key(config_path)
    
    # Latitude and Longitude for Pune
    lat, lon = 18.5204, 73.8567
    
    # Define the date range (past 365 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    output_dir = './data/raw'  # Use a relative path to store the data

    # Fetch historical data day by day for the past year
    for single_date in (start_date + timedelta(n) for n in range(365)):
        start_timestamp = int(single_date.timestamp())
        end_timestamp = int((single_date + timedelta(days=1)).timestamp())
        
        # Fetch data for a single day
        weather_data = fetch_openweather_historical_data(lat, lon, start_timestamp, end_timestamp, weather_api_key)
        
        if weather_data:
            # Save data only if fetched successfully
            save_data(weather_data, f"weather_pune_{single_date.strftime('%Y-%m-%d')}.json", output_dir)
        else:
            print(f"Failed to fetch data for {single_date.strftime('%Y-%m-%d')}")

        # Wait between requests to avoid hitting rate limits
        time.sleep(1)
