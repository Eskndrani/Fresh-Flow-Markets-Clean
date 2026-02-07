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
        # Paths - use relative paths from project root
        # model.py is in New_ML_Models/Guide_to_use/, so go up 2 levels to get project root
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        self.model_dir = os.path.join(base_dir, "New_ML_Models", "stock_forecaster", "models", "lstm_models") + os.sep
        self.scaler_dir = os.path.join(base_dir, "New_ML_Models", "stock_forecaster", "models", "scalers") + os.sep
        
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
            
        path = os.path.join(base_dir, "New_ML_Models", "stock_forecaster", "MSE.json")
        with open(path, 'r', encoding='utf-8') as f:
            self.errors = json.load(f)
        self.base_dir = base_dir  # Store for reference  

    def get_mean_absolute_error(self, category_name):        
        return self.errors[category_name]

    def predict(self, category_name, month, last_qty,number_of_days=1):
        if category_name not in self.model:
            raise ValueError(f"Category '{category_name}' not found.")

        model = self.model[category_name]
        scaler = self.scaler[category_name]
        prediction = last_qty
        for i in range(number_of_days):
        # 1. Scale the input
            last_qty = prediction
            qty_scaled = float(scaler.transform([[last_qty]])[0][0])

            # 2. Prepare features (LSTM expects 3D input [samples, time_steps, features])
            features = np.array([[month, qty_scaled]]) 
            features = np.reshape(features, (1, 1, features.shape[1]))

            # 3. Predict
            prediction_scaled = model.predict(features, verbose=0)
            
            # 4. Inverse Transform to get actual quantity
            prediction = float(scaler.inverse_transform(prediction_scaled)[0][0])
        
        return max(0, prediction)
    def stock_reorder_recommendation(self, category_name, month,last_qty,number_of_days,current_stock,multipler):
        prediction = self.predict(category_name, month, last_qty, number_of_days)
        reorder_qty = max(0, prediction - current_stock)
        reorder_qty = reorder_qty * multipler
        if reorder_qty > current_stock:
            return reorder_qty-current_stock
        else:
            return 0
class Customer_Churn_Detection: 
    def __init__(self):
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        file_path = os.path.join(base_dir, "New_ML_Models", "customer_churn", "model_bundle.joblib")
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
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        model_dir = os.path.join(base_dir, "New_ML_Models", "Campaign_ROI_Predictor", "models")
        self.regressor = joblib.load(os.path.join(model_dir, 'campaign_redemption_regressor.pkl'))
        self.classifier = joblib.load(os.path.join(model_dir, 'campaign_success_classifier.pkl'))
        self.scaler = joblib.load(os.path.join(model_dir, 'campaign_scaler.pkl'))
        self.feature_columns = joblib.load(os.path.join(model_dir, 'campaign_features.pkl'))
    def predict_redemption(self,  duration_days, discount, max_redemptions, redemptions_per_duration):
        x = [[duration_days, discount, max_redemptions, redemptions_per_duration]]
        # Scale features before prediction
        x_scaled = self.scaler.transform(x)
        y = self.regressor.predict(x_scaled)
        return round(y[0])
    def predict_success_probability(self, duration_days, discount, max_redemptions, redemptions_per_duration):
        x = [[duration_days, discount, max_redemptions, redemptions_per_duration]]
        # Scale features before prediction
        x_scaled = self.scaler.transform(x)
        y = self.classifier.predict_proba(x_scaled)
        return y[0][1]

class Operational_risk_predictor:
    def __init__(self):
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        model_dir = os.path.join(base_dir, "New_ML_Models", "Operational_risk_predictors", "models")
        self.model = joblib.load(os.path.join(model_dir, 'random_forest_model(preferred).pkl'))
        self.scaler = joblib.load(os.path.join(model_dir, 'feature_scaler.pkl'))
        self.feature_columns = joblib.load(os.path.join(model_dir, 'feature_columns.pkl'))
    def predict_risk_percentage(self,balance_discrepancy_pct_mean,balance_discrepancy_pct_max,transaction_total_count,closing_balance_mean,total_amount_mean,cash_amount_mean,balance_discrepancy_risk,balance_variance_risk):
        x = [[balance_discrepancy_pct_mean,balance_discrepancy_pct_max,transaction_total_count,closing_balance_mean,total_amount_mean,cash_amount_mean,balance_discrepancy_risk,balance_variance_risk]]
        # Scale features before prediction
        x_scaled = self.scaler.transform(x)
        y = self.model.predict_proba(x_scaled)
        return y[0][1]

class RevenuePredictor:
    def __init__(self):
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        self.model_path = os.path.join(base_dir, "New_ML_Models", "revenue_predictor", "revenue_predictor_xgb.pkl")
        self.model = joblib.load(self.model_path)
        self.metadata_path = os.path.join(base_dir, "New_ML_Models", "revenue_predictor", "revenue_predictor_metadata.json")
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = None
    def predict(self, is_weekend, is_holiday, lagged_revenue):
        features = np.array([[is_weekend, is_holiday, lagged_revenue]])
        prediction = float(self.model.predict(features)[0])
        return max(0, prediction)

# Execution block removed - models should be initialized by the calling application
