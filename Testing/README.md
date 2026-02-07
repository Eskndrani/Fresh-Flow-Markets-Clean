# Model Testing Documentation

This directory contains testing notebooks and test data for evaluating ML models from `New_ML_Models`.

## 📁 Directory Structure

```
Testing/
├── README.md                          # This file
├── main_tests.ipynb                   # Main testing notebook (4 models)
├── operational_risk_test.ipynb        # Operational risk testing notebook
├── Stock_Forecasting_Test.csv         # Test data for stock forecaster
├── revenue_prediction_test.csv         # Test data for revenue predictor
├── customer_churn_test.csv            # Test data for customer churn predictor
├── campaign_success_test.csv          # Test data for campaign predictor
├── cashiers_risk_test.csv             # Test data for operational risk predictor
└── Results/
    └── exports/                       # Exported test results (CSV files)
        ├── stock_forecaster_results.csv
        ├── revenue_predictor_results.csv
        ├── customer_churn_predictor_results.csv
        ├── campaign_success_predictor_results.csv
        └── operational_risk_predictor_results.csv
```

## 🧪 Testing Notebooks

### 1. Main Tests Notebook (`main_tests.ipynb`)

Tests 4 ML models on their respective test datasets:

1. **Stock Forecaster (LSTM)** - Time series forecasting
   - Model: LSTM neural network
   - Test Data: `Stock_Forecasting_Test.csv`
   - Features: `month`, `lagged_qt`
   - Output: Predicted stock quantities

2. **Revenue Predictor (XGBoost)** - Time series regression
   - Model: XGBoost regressor
   - Test Data: `revenue_prediction_test.csv`
   - Features: `is_weekend`, `is_holiday`, `lagged_revenue`
   - Output: Predicted revenue values
   - Metrics: MSE, MAE, R²

3. **Customer Churn Predictor (Random Forest)** - Classification
   - Model: Random Forest classifier
   - Test Data: `customer_churn_test.csv`
   - Features: `discount_amount`, `points_earned`, `price`, `waiting_time`
   - Output: Churn prediction (0/1) and probability
   - Metrics: Accuracy, Classification Report

4. **Campaign Success Predictor (Random Forest Classifier)** - Classification
   - Model: Random Forest classifier
   - Test Data: `campaign_success_test.csv`
   - Features: `duration_days`, `discount`, `redemptions`, `redemptions_per_duration`
   - Output: Success prediction (0/1) and probability
   - Metrics: Accuracy, Classification Report

### 2. Operational Risk Test Notebook (`operational_risk_test.ipynb`)

Tests the operational risk predictor separately:

- **Operational Risk Predictor (Random Forest)** - Classification
  - Model: Random Forest classifier
  - Test Data: `cashiers_risk_test.csv`
  - Features: Multiple cashier metrics (balance discrepancies, transaction counts, etc.)
  - Output: Risk level prediction (0/1) and probability
  - Metrics: Accuracy, Classification Report

## 🚀 How to Use

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- Jupyter Notebook or JupyterLab
- Required Python packages (see `requirements.txt` in project root)

### Running the Tests

1. **Open Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Run Main Tests:**
   - Open `main_tests.ipynb`
   - Execute all cells sequentially (Cell → Run All)
   - Results will be exported to `Results/exports/`

3. **Run Operational Risk Tests:**
   - Open `operational_risk_test.ipynb`
   - Execute all cells sequentially
   - Results will be exported to `Results/exports/operational_risk_predictor_results.csv`

### Expected Output

After running the notebooks, you should see:

1. **Console Output:**
   - Model loading confirmations
   - Test execution progress
   - Performance metrics (accuracy, MSE, MAE, R²)
   - Classification reports (for classification models)

2. **CSV Files in `Results/exports/`:**
   - `stock_forecaster_results.csv` - Stock predictions
   - `revenue_predictor_results.csv` - Revenue predictions with actual vs predicted
   - `customer_churn_predictor_results.csv` - Churn predictions with probabilities
   - `campaign_success_predictor_results.csv` - Campaign success predictions
   - `operational_risk_predictor_results.csv` - Risk predictions for cashiers

## 📊 Test Data Format

### Stock Forecasting Test Data
- **File:** `Stock_Forecasting_Test.csv`
- **Columns:** `month`, `total_qt`, `lagged_qt`

### Revenue Prediction Test Data
- **File:** `revenue_prediction_test.csv`
- **Columns:** `is_weekend`, `is_holiday`, `lagged_revenue`, `val` (actual revenue)

### Customer Churn Test Data
- **File:** `customer_churn_test.csv`
- **Columns:** `user_id`, `discount_amount`, `points_earned`, `price`, `waiting_time`, `vip_threshold`, `rating`, `is_churned`

### Campaign Success Test Data
- **File:** `campaign_success_test.csv`
- **Columns:** `duration_days`, `discount`, `redemptions`, `redemptions_per_duration`, `val` (success label)

### Operational Risk Test Data
- **File:** `cashiers_risk_test.csv`
- **Columns:** `cashier_id`, `risk_level`, `balance_discrepancy_pct_max`, `balance_diff_sum`, `num_transactions_sum`, `transaction_total_sum`, `vat_component_sum`, etc.

## 📈 Understanding Results

### Regression Models (Stock Forecaster, Revenue Predictor)
- **MSE (Mean Squared Error):** Lower is better
- **MAE (Mean Absolute Error):** Lower is better
- **R² (R-squared):** Closer to 1.0 is better (1.0 = perfect predictions)

### Classification Models (Churn, Campaign, Operational Risk)
- **Accuracy:** Percentage of correct predictions (higher is better)
- **Classification Report:** Includes precision, recall, and F1-score for each class
- **Probability:** Confidence score for the prediction (0.0 to 1.0)

## 🔧 Troubleshooting

### Common Issues

1. **Model Not Found:**
   - Ensure models are in `New_ML_Models/` directory
   - Check model file paths in the notebook

2. **Import Errors:**
   - Install missing packages: `pip install -r requirements.txt`
   - Ensure TensorFlow is installed for LSTM models: `pip install tensorflow`

3. **Data Loading Errors:**
   - Verify test CSV files are in the `Testing/` directory
   - Check file names match exactly (case-sensitive)

4. **Memory Issues:**
   - For large test datasets, consider testing on a subset
   - Close other applications to free up memory

## 📝 Notes

- The operational risk test is in a separate notebook due to its complexity and different feature requirements
- All results are automatically exported to CSV files for further analysis
- The notebooks include error handling for missing data or model failures
- Test data should match the format expected by each model

## 🔗 Related Files

- Model definitions: `New_ML_Models/`
- Model usage guide: `New_ML_Models/Guide_to_use/model.py`
- Project README: `../README.md`
- ML Models README: `../New_ML_Models/README.md`

## 📧 Support

For issues or questions about the testing notebooks, please refer to:
- Project documentation in `../docs/`
- Model-specific README files in `../New_ML_Models/`

---

**Last Updated:** 2026-02-07

