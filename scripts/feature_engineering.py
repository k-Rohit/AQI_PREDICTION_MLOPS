import os
import pandas as pd
from azureml.core import Workspace, Dataset, Datastore

# Connect to Azure ML Workspace
ws = Workspace.from_config('config/config.json')

# Access the default datastore
datastore = Datastore.get(ws, datastore_name='workspaceblobstore')

# Load the dataset from Azure Blob Storage
dataset = Dataset.File.from_files(path=(datastore, 'processed_aqi_data/'))

# Download the files from Azure Blob Storage to local folder
download_dir = './data/processed/'  # Define local directory to store downloaded files
os.makedirs(download_dir, exist_ok=True)  # Create directory if it doesn't exist
dataset.download(target_path=download_dir, overwrite=True)

# Combine the data from downloaded CSV files into a pandas DataFrame
all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.csv')]

# Assuming there's only one CSV file in the processed data directory
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

def create_time_based_features(df):
    """Extracts useful time-based features from the date column."""
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = df['date'].dt.hour
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df = df.drop(columns=['date'])
    return df

def create_lag_features(df, lag_hours=1):
    """Creates lag features for AQI and other pollutants."""
    for feature in ['aqi', 'pm2_5', 'pm10', 'co', 'no', 'no2', 'o3', 'so2', 'nh3']:
        df[f'{feature}_lag_{lag_hours}h'] = df[feature].shift(lag_hours)
    df = df.dropna()
    return df

if __name__ == "__main__":
    # Step 1: Create time-based features
    df = create_time_based_features(df)
    
    # Step 2: Create lag features
    df = create_lag_features(df, lag_hours=1)

    # Step 3: Save feature-engineered data locally and to Azure
    output_path = './data/feature_engineered/engineered_aqi_data_pune.csv'  # Save in the feature-engineered folder
    df.to_csv(output_path, index=False)
    print(f"Feature engineering completed. Data saved locally to {output_path}.")

    # Upload the processed data to Azure Blob Storage
    datastore.upload_files([output_path], target_path='feature_engineered_aqi_data/', overwrite=True)
    print("Feature-engineered data uploaded to Azure Blob Storage.")

