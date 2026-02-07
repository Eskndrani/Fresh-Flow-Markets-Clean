import joblib
import os
import numpy as np
import pandas as pd
import json
from tensorflow.keras.models import load_model

def date_to_features(date):
    """
    Transforms a date to day_of_week, is_weekend, is_holiday, month.
    Args:
        date (str or pd.Timestamp): Date to transform.
    Returns:
        month (int): Month number
    """
    dt = pd.to_datetime(date)
    month = dt.month
    return month

class StockForecaster:
    """
    Forecasts next day's stock quantity for a given item using per-category LSTM models.
    """
    def __init__(self):
        # Paths
        self.model_dir = "D:/Deloitte/New_ML_Models/stock_forecaster/models/lstm_models/"
        self.scaler_dir = "D:/Deloitte/New_ML_Models/stock_forecaster/models/scalers/"
        
        self.model = {}
        self.scaler = {}

        # List of categories to ensure consistent naming
        categories = [
            "Beverages", "Breakfast_&_Brunch", "Desserts_&_Sweets", 
            "Handhelds", "Main_Courses", "Misc_Services", 
            "Other_Uncategorized", "Salads_&_Greens", 
            "Sides_&_Snacks", "Sushi_&_Asian"
        ]

        # THE FIX: compile=False skips searching for the 'mse' function during load
        for cat in categories:
            filename = cat
            model_path = f"{self.model_dir}{filename}_lstm.h5"
            self.model[cat] = load_model(model_path, compile=False)
            self.scaler[cat] = joblib.load(f"{self.scaler_dir}{cat}_scaler.joblib")
            
        path = "D:/Deloitte/New_ML_Models/stock_forecaster/MSE.json"
        with open(path, 'r', encoding='utf-8') as f:
            self.errors = json.load(f)  

    def get_mean_absolute_error(self, category_name):        
        return self.errors[category_name]

    def predict(self, category_name, month, last_qty):
        if category_name not in self.model:
            raise ValueError(f"Category '{category_name}' not found.")

        model = self.model[category_name]
        scaler = self.scaler[category_name]

        # 1. Scale the input
        qty_scaled = float(scaler.transform([[last_qty]])[0][0])

        # 2. Prepare features (LSTM expects 3D input [samples, time_steps, features])
        features = np.array([[month, qty_scaled]]) 
        features = np.reshape(features, (1, 1, features.shape[1]))

        # 3. Predict
        prediction_scaled = model.predict(features, verbose=0)
        
        # 4. Inverse Transform to get actual quantity
        prediction = float(scaler.inverse_transform(prediction_scaled)[0][0])
        
        return max(0, prediction)

class Customer_Churn_Detection: 
    def __init__(self):
        file_path = "D:/Deloitte/New_ML_Models/customer_churn/model_bundle.joblib"
        bundle = joblib.load(file_path)
        self.model = bundle["model"]
        self.scaler = bundle["scaler"]
    def predict(self, discount_amount, points_earned, price, waiting_time):
        x = [[discount_amount, points_earned, price, waiting_time]]
        x_s = self.scaler.transform(x)
        y = self.model.predict(x_s)
        return y[0]

class Campaign_Detector:
    def __init__(self):
        model_dir = "D:/Deloitte/New_ML_Models/Campaign_ROI_Predictor/models/"
        self.regressor = joblib.load(os.path.join(model_dir, 'campaign_redemption_regressor.pkl'))
        self.classifier = joblib.load(os.path.join(model_dir, 'campaign_success_classifier.pkl'))
        self.scaler = joblib.load(os.path.join(model_dir, 'campaign_scaler.pkl'))
        self.feature_columns = joblib.load(os.path.join(model_dir, 'campaign_features.pkl'))
    def predict_redemption(self,  duration_days, discount, max_redemptions, redemptions_per_duration):
        x = [[duration_days, discount, max_redemptions, redemptions_per_duration]]
        # Note: Regressor usually needs scaled data if trained that way
        y = self.regressor.predict(x)
        return round(y[0])
    def predict_success_probability(self, duration_days, discount, max_redemptions, redemptions_per_duration):
        x = [[duration_days, discount, max_redemptions, redemptions_per_duration]]
        y = self.classifier.predict_proba(x)
        return y[0][1]

class Operational_risk_predictor:
    def __init__(self):
        model_dir = "D:/Deloitte/New_ML_Models/Operational_risk_predictors/models/"
        self.model = joblib.load(os.path.join(model_dir, 'random_forest_model(preferred).pkl'))
        self.scaler = joblib.load(os.path.join(model_dir, 'feature_scaler.pkl'))
        self.feature_columns = joblib.load(os.path.join(model_dir, 'feature_columns.pkl'))
    def predict_risk_percentage(self,balance_discrepancy_pct_mean,balance_discrepancy_pct_max,transaction_total_count,closing_balance_mean,total_amount_mean,cash_amount_mean,balance_discrepancy_risk,balance_variance_risk):
        x = [[balance_discrepancy_pct_mean,balance_discrepancy_pct_max,transaction_total_count,closing_balance_mean,total_amount_mean,cash_amount_mean,balance_discrepancy_risk,balance_variance_risk]]
        y = self.model.predict_proba(x)
        return y[0][1]

class RevenuePredictor:
    def __init__(self):
        self.model_path = "D:/Deloitte/New_ML_Models/revenue_predictor/revenue_predictor_xgb.pkl"
        self.model = joblib.load(self.model_path)
        self.metadata_path = "D:/Deloitte/New_ML_Models/revenue_predictor/revenue_predictor_metadata.json"
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = None
    def predict(self, is_weekend, is_holiday, lagged_revenue):
        features = np.array([[is_weekend, is_holiday, lagged_revenue]])
        prediction = float(self.model.predict(features)[0])
        return max(0, prediction)

# Execution block from enhanced version
model = Campaign_Detector()
print(model.predict_redemption(0,0,0,0))
