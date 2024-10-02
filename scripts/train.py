import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
from azureml.core import Workspace, Dataset, Datastore

# Connect to Azure ML Workspace
ws = Workspace.from_config('config/config.json')

# Access the default datastore (Azure Blob Storage)
datastore = Datastore.get(ws, datastore_name='workspaceblobstore')

# Load the feature-engineered dataset from Azure Blob Storage
dataset = Dataset.File.from_files(path=(datastore, 'feature_engineered_aqi_data/'))

# Download the files from Azure Blob Storage to local folder
download_dir = './data/feature_engineered/'  # Feature-engineered data folder
os.makedirs(download_dir, exist_ok=True)
dataset.download(target_path=download_dir, overwrite=True)

# Load the feature-engineered data into a pandas DataFrame
all_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.csv')]
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)


# Step 1: Define features (X) and target (y)
X = df.drop(columns=['aqi'])
y = df['aqi']

# Step 2: Apply Min-Max Scaling
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 4: Train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Make predictions and evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"R² Score: {r2}")

# Step 6: Save the trained model and the scaler locally
joblib.dump(model, 'models/aqi_random_forest_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

# Step 7: Upload the model and scaler to Azure Blob Storage
datastore.upload_files(['models/aqi_random_forest_model.pkl', 'models/scaler.pkl'], target_path='models/', overwrite=True)
print("Model and scaler uploaded to Azure Blob Storage.")
