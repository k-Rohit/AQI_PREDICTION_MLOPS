import os
from azureml.core import Workspace, Dataset, Datastore

# Connect to the Azure ML Workspace using config.json
ws = Workspace.from_config('/Users/kumarrohit/Desktop/AQI_Prediction_MLOPS/config/config.json')

# Access the default datastore (Azure Blob Storage)
datastore = Datastore.get(ws, datastore_name='workspaceblobstore')

# Local directory containing the raw data (ensure this path is correct)
src_dir = '/Users/kumarrohit/Desktop/AQI_Prediction_MLOPS/data/raw'  # Relative path to your data directory

# Check if the directory exists and is valid
if not os.path.isdir(src_dir):
    raise Exception(f"Directory not found: {src_dir}")

# Use the new upload method to upload the directory and create a FileDataset
dataset = Dataset.File.upload_directory(
    src_dir=src_dir,  # Local directory
    target=(datastore, 'aqi_data/'),  # Target path in Azure Blob Storage
    overwrite=True
)

# Register the dataset in Azure ML workspace
dataset = dataset.register(workspace=ws, name='aqi_data', description='AQI Raw Data')
print("Data uploaded and dataset registered successfully.")
