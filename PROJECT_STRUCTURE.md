# Project structure

Quick reference for the main folders and where to find things.

```
Deloitte/
├── app.py                    # Flask API entry point
├── dashboard.py              # Streamlit dashboard (run: streamlit run dashboard.py)
├── requirements.txt         # Python dependencies
├── style.css                 # Dashboard styles
├── business_trends_content.py
├── config/                   # App configuration (optional)
├── data/                     # CSV/data files
├── database/                 # DB setup and scripts
├── docs/                     # API docs, guides, PDFs
├── New_ML_Models/            # ML models and guide (used by dashboard)
│   ├── Guide_to_use/
│   │   └── guide.py          # StockForecaster, Campaign, Churn, Ops Risk, Revenue
│   ├── stock_forecaster/     # XGBoost models, scalers
│   ├── Campaign_ROI_Predictor/
│   ├── customer_churn/
│   ├── Operational_risk_predictors/
│   └── revenue_predictor/
├── src/
│   ├── api/                  # Flask routes, database
│   ├── services/             # ML prediction, inventory
│   ├── models/               # Data loaders, cleaning
│   └── utils/
├── Testing/                  # Test notebooks and results
└── Inventory Management business analysis/  # Analysis notebooks and exports
```

**Run dashboard:** `streamlit run dashboard.py`  
**Run API:** `python app.py`
