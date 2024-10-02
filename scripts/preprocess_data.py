import os
import json
import pandas as pd
from datetime import datetime
from azureml.core import Workspace, Dataset, Datastore

# Connect to Azure ML Workspace
ws = Workspace.from_config('../config/config.json')

# Access the default datastore (Azure Blob Storage)
datastore = Datastore.get(ws, datastore_name='workspaceblobstore')

# Load the dataset from Azure Blob Storage
dataset = Dataset.File.from_files(path=(datastore, 'aqi_data/'))

# Download the files from Azure Blob Storage to local folder
download_dir = './data/raw/'  # Define local directory to store downloaded files
os.makedirs(download_dir, exist_ok=True)  # Create directory if it doesn't exist
dataset.download(target_path=download_dir, overwrite=True)

# Combine the data from downloaded files into a pandas DataFrame
all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.json')]

# Process each JSON file and combine them into a DataFrame
all_data = []
for file in all_files:
    with open(file, 'r') as f:
        data = json.load(f)
        for entry in data['list']:
            # Convert timestamp to a readable date format
            timestamp = entry['dt']
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            # Extract AQI and pollutant concentrations
            record = {
                'date': date,
                'aqi': entry['main']['aqi'],
                'pm2_5': entry['components']['pm2_5'],
                'pm10': entry['components']['pm10'],
                'co': entry['components']['co'],
                'no': entry['components']['no'],
                'no2': entry['components']['no2'],
                'o3': entry['components']['o3'],
                'so2': entry['components']['so2'],
                'nh3': entry['components']['nh3']
            }
            all_data.append(record)

# Convert the list of records into a pandas DataFrame
df = pd.DataFrame(all_data)

# Save processed data locally and upload it back to Azure Blob Storage
output_file_path = './data/processed/combined_aqi_data_pune.csv'
df.to_csv(output_file_path, index=False)

# Upload the processed data to Azure Blob Storage
datastore.upload_files([output_file_path], target_path='processed_aqi_data/', overwrite=True)
print(f"Processed data uploaded to Azure Blob Storage as {output_file_path}")
