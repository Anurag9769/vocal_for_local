import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load your dataset
data = pd.read_csv('soil_crop_data.csv')

# Preprocessing
# One-hot encode categorical columns
data_encoded = pd.get_dummies(data, columns=['Soil Texture', 'Crop Type'])

X = data_encoded.drop('target_crop_yield', axis=1)  # Features
y = data_encoded['target_crop_yield']                 # Target variable

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)
print(f'Predictions: {predictions}')

# Evaluation
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')
