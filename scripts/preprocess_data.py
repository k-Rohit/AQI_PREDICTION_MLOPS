import os
import json
import pandas as pd
from datetime import datetime

def load_all_aqi_json(data_dir):
    """Load and combine all AQI JSON files from the specified directory."""
    all_data = []
    
    # Iterate through all files in the directory
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                all_data.append(data)
    
    return all_data

def process_aqi_data(data_list):
    """Process the AQI data from multiple files and combine them."""
    processed_data = []
    
    # Iterate through each file's data
    for data in data_list:
        for entry in data['list']:
            # Convert timestamp to a readable date format
            timestamp = entry['dt']
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            # Extract AQI and pollutant concentrations
            aqi = entry['main']['aqi']
            components = entry['components']
            
            # Create a dictionary for each record
            record = {
                'date': date,
                'aqi': aqi,
                'pm2_5': components['pm2_5'],
                'pm10': components['pm10'],
                'co': components['co'],
                'no': components['no'],
                'no2': components['no2'],
                'o3': components['o3'],
                'so2': components['so2'],
                'nh3': components['nh3']
            }
            
            # Append the record to the list
            processed_data.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame(processed_data)
    return df

def save_processed_data(df, output_path):
    """Save the processed DataFrame to a CSV file."""
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # Directory containing multiple JSON files
    input_data_dir = 'data/raw'  # Update to your folder path
    output_file_path = 'data/processed/combined_aqi_data_pune.csv'
    
    # Load and combine all the raw AQI data from multiple files
    raw_data_list = load_all_aqi_json(input_data_dir)
    
    # Process the combined data
    df_processed = process_aqi_data(raw_data_list)
    
    # Save the processed data to a CSV file
    save_processed_data(df_processed, output_file_path)
