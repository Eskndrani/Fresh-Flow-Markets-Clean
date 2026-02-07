Images are in the directory
# Fresh Flow Markets - AI-Powered Inventory Management System

**Deloitte Innovation Hub x AUC Hackathon 2026**

A comprehensive inventory management platform that leverages machine learning to optimize stock levels, predict demand, reduce waste, and maximize profits for retail businesses, particularly in fresh produce departments.

------

## 🔗 Repository History & Bandwidth Notice
> **Note on Migration**: All project information and development history are preserved in our original repository. Due to bandwidth limits on the previous host, we have migrated to this current repository for active development and deployment.
> 
> **Old Repository Link**: [Fresh-Flow-Markets-Inventory-Management-DIH-X-AUC-Hackathon](https://github.com/kareemelramly/Fresh-Flow-Markets-Inventory-Management-DIH-X-AUC-Hackathon-.git)

---

## 📋 Project Description

Fresh Flow Markets is an intelligent inventory management system designed to solve critical challenges faced by retailers:

- **Stock-out Prevention**: Predict demand accurately to avoid lost sales
- **Waste Reduction**: Optimize inventory levels to minimize spoilage and waste
- **Revenue Maximization**: Data-driven decisions to boost profitability
- **Operational Efficiency**: Automated forecasting and recommendations
- **Risk Management**: Detect operational anomalies and customer churn risks

The platform combines a modern web dashboard with a robust REST API backend, powered by 5 production-ready machine learning models that provide actionable insights for inventory management, marketing campaigns, customer retention, and operational risk monitoring.

---

## ✨ Features

### 🏠 **Home Dashboard**
- Welcome page with project overview
- Customer testimonials and value propositions
- Quick navigation to all system features

![Home Dashboard](docs/screenshots/home_dashboard.png)
*Home page with project introduction and navigation*

### 📊 **Main Statistics Dashboard**
- **Real-time Analytics**: View total transactions, revenue, and average order value
- **Order Status Distribution**: Visual breakdown of order statuses with pie charts
- **Top Selling Items**: Identify best-performing products with interactive charts
- **Time Period Selection**: Analyze data for 30 days to 5 years
- **Dynamic Metrics**: Live updates from the database

![Main Statistics Dashboard](docs/screenshots/main_statistics.png)
*Real-time analytics dashboard with key business metrics*

### 📦 **Inventory Management**
- **Item Search & Filtering**: Find items by name or barcode
- **Pagination**: Navigate through large inventory catalogs efficiently
- **Item Details View**: Comprehensive product information including:
  - Basic info (ID, title, barcode, price, VAT, status)
  - Availability settings (delivery, eat-in, takeaway)
- **Low Stock Alerts**: Automatic identification of items below threshold
- **Real-time Inventory Status**: Monitor current stock levels

![Inventory Management](docs/screenshots/inventory_management.png)
*Inventory management interface with search and filtering capabilities*

### 🔮 **Forecasting & AI Predictions**

#### 1. **Demand Forecast (LSTM)**
- Predict future demand for individual items
- Multi-day forecasting (1-30 days)
- Category-based predictions using LSTM neural networks
- Visual forecast charts with daily breakdowns
- Total and average daily demand metrics

![Demand Forecast](docs/screenshots/demand_forecast.png)
*LSTM-based demand forecasting with interactive charts*

#### 2. **Reorder Recommendations**
- AI-powered reorder quantity suggestions
- Safety stock calculations with customizable multipliers
- Lead time considerations
- Urgency indicators for stock replenishment

![Reorder Recommendations](docs/screenshots/reorder_recommendations.png)
*AI-powered reorder suggestions with safety stock calculations*

#### 3. **Bulk Item Forecast**
- Forecast demand for multiple items simultaneously
- Batch processing for efficiency
- Summary table with category and demand metrics
- Error handling for items without sufficient data

![Bulk Forecast](docs/screenshots/bulk_forecast.png)
*Batch forecasting for multiple items*

#### 4. **Campaign ROI Predictor**
- **Performance Predictor**: Predict campaign success probability before launch
- **Goal Optimizer**: Find optimal campaign parameters to hit targets
- **Campaign Comparison**: Benchmark two campaign scenarios side-by-side
- Expected redemptions and success probability
- Data-driven recommendations (Launch/Consider/Revise)

![Campaign ROI Predictor](docs/screenshots/campaign_roi.png)
*Campaign performance prediction and optimization tools*

#### 5. **Customer Churn Detection**
- Individual customer churn risk assessment
- Probability-based risk levels (Low/Medium/High)
- Customer engagement insights
- Retention strategy recommendations
- Estimated retention costs

![Customer Churn Detection](docs/screenshots/customer_churn.png)
*Customer churn risk assessment with retention strategies*

#### 6. **Operational Risk Monitor**
- **Quick Risk Lookup**: Pre-calculated risk assessments for cashiers
- **Manual Risk Analysis**: Enter shift data for new cashiers
- **Batch Risk Analysis**: Process multiple shift records simultaneously
- Risk categorization (Low/Medium/High/Critical)
- Financial and operational metrics
- Actionable recommendations based on risk level

![Operational Risk Monitor](docs/screenshots/operational_risk.png)
*Cashier integrity and operational risk monitoring dashboard*

#### 7. **Revenue Forecasting**
- Daily revenue predictions based on historical trends
- Holiday and weekend impact analysis
- Growth projections with percentage changes
- Visual revenue comparison charts

![Revenue Forecasting](docs/screenshots/revenue_forecast.png)
*Daily revenue predictions with trend analysis*

### 📈 **Business Trends**
- Comprehensive business analytics visualizations
- Multiple trend analysis sections
- Data-driven insights for strategic decision-making

![Business Trends](docs/screenshots/business_trends.png)
*Comprehensive business analytics and trend visualizations*

---

## 🛠️ Technologies Used

### **Frontend & Dashboard**
- **Streamlit** (v1.25.0+): Interactive web dashboard framework
- **Plotly** (v5.14.0+): Interactive data visualizations and charts
- **HTML/CSS**: Custom styling and UI components

### **Backend & API**
- **Flask** (v2.3.0+): Lightweight web framework for REST API
- **Flask-CORS** (v4.0.0+): Cross-origin resource sharing support
- **SQLite**: Database engine (622 MB production database)
- **SQLAlchemy** (v2.0.0+): ORM and database toolkit

### **Machine Learning & Data Science**
- **TensorFlow/Keras**: LSTM neural networks for time series forecasting
- **scikit-learn** (v1.3.0+): Machine learning algorithms (Random Forest, Gradient Boosting)
- **XGBoost** (v2.0.0+): Gradient boosting for revenue prediction
- **pandas** (v2.0.0+): Data manipulation and analysis
- **numpy** (v1.24.0+): Numerical computations
- **joblib** (v1.3.0+): Model serialization and model persistence

### **Data Processing**
- **pandas**: CSV processing and data manipulation
- **numpy**: Numerical operations
- **scipy** (v1.11.0+): Statistical functions

### **Utilities**
- **requests** (v2.31.0+): HTTP library for API calls
- **python-dateutil** (v2.8.0+): Date/time utilities
- **python-dotenv** (v1.0.0+): Environment variable management

### **Development Tools**
- **Jupyter Notebook**: Data analysis and model development
- **pytest** (v7.4.0+): Testing framework

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Deloitte
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: For TensorFlow/Keras models, ensure you have sufficient system resources. If you encounter issues, you can install TensorFlow separately:
```bash
pip install tensorflow
```

### Step 4: Set Up Database
```bash
# The database should be located at: database/fresh_flow_markets.db
# If the database doesn't exist, run:
python setup_database.py
```

### Step 5: Verify Installation
```bash
# Check that all models are accessible
python -c "from New_ML_Models.Guide_to_use.model import StockForecaster; print('Models loaded successfully!')"
```

---

## 🚀 Usage

### Starting the Dashboard

1. **Launch the Streamlit Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```
   The dashboard will open in your default web browser at `http://localhost:8501`

2. **Navigate the Dashboard**:
   - Use the navigation buttons at the top to switch between pages
   - **Home**: Project overview and introduction
   - **Main Statistics**: View sales analytics and key metrics
   - **Inventory Management**: Browse and search inventory items
   - **Forecasting Suggestions**: Access all ML prediction features

### Starting the API Server

1. **Launch the Flask API Server**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **API Endpoints**:
   - Health Check: `GET http://localhost:5000/health`
   - ML Service Health: `GET http://localhost:5000/api/ml/health`
   - Inventory Items: `GET http://localhost:5000/api/inventory/items`
   - Analytics: `GET http://localhost:5000/api/analytics/dashboard`
   - See `docs/API_DOCUMENTATION.md` for complete API reference

### Using ML Models Directly

#### Example 1: Stock Demand Forecasting
```python
from New_ML_Models.Guide_to_use.model import StockForecaster

# Initialize the model
forecaster = StockForecaster()

# Predict demand for a beverage item
predicted_qty = forecaster.predict(
    category_name="Beverages",
    month=2,  # February
    last_qty=50.0,  # Last known quantity
    number_of_days=7  # Forecast for 7 days
)

print(f"Predicted quantity: {predicted_qty}")
```

#### Example 2: Revenue Prediction
```python
from New_ML_Models.Guide_to_use.model import RevenuePredictor

# Initialize the model
predictor = RevenuePredictor()

# Predict tomorrow's revenue
predicted_revenue = predictor.predict(
    is_weekend=0,  # Not a weekend
    is_holiday=0,  # Not a holiday
    lagged_revenue=5000.0  # Yesterday's revenue
)

print(f"Predicted revenue: ${predicted_revenue:.2f}")
```

#### Example 3: Customer Churn Detection
```python
from New_ML_Models.Guide_to_use.model import Customer_Churn_Detection

# Initialize the model
churn_detector = Customer_Churn_Detection()

# Predict churn risk
will_churn = churn_detector.predict(
    discount_amount=25.0,
    points_earned=500.0,
    price=75.50,
    waiting_time=25.5
)

print(f"Will churn: {bool(will_churn)}")
```

#### Example 4: Campaign Success Prediction
```python
from New_ML_Models.Guide_to_use.model import Campaign_Detector

# Initialize the model
campaign_detector = Campaign_Detector()

# Predict campaign success probability
success_prob = campaign_detector.predict_success_probability(
    duration_days=7,
    discount=20,
    max_redemptions=100,
    redemptions_per_duration=15
)

print(f"Success probability: {success_prob * 100:.1f}%")
```

#### Example 5: Operational Risk Assessment
```python
from New_ML_Models.Guide_to_use.model import Operational_risk_predictor

# Initialize the model
risk_predictor = Operational_risk_predictor()

# Predict risk percentage
risk_score = risk_predictor.predict_risk_percentage(
    balance_discrepancy_pct_mean=150.0,
    balance_discrepancy_pct_max=27100.0,
    transaction_total_count=1531,
    closing_balance_mean=50000.0,
    total_amount_mean=139.5,
    cash_amount_mean=98.0,
    balance_discrepancy_risk=1.0,
    balance_variance_risk=1.0
)

print(f"Risk probability: {risk_score * 100:.1f}%")
```

### Testing ML Models

Run the test notebooks to evaluate model performance:

```bash
# Navigate to Testing directory
cd Testing

# Open Jupyter Notebook
jupyter notebook

# Run main_tests.ipynb for 4 models
# Run operational_risk_test.ipynb for operational risk model
```

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Streamlit Dashboard (dashboard.py)                │   │
│  │     - Interactive UI                                  │   │
│  │     - Real-time visualizations                       │   │
│  │     - User input forms                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    API Layer                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Flask REST API (app.py)                         │   │
│  │     - /api/inventory/*                              │   │
│  │     - /api/analytics/*                              │   │
│  │     - /api/ml/*                                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Machine Learning Service Layer                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ML Prediction Service                               │   │
│  │  - StockForecaster (LSTM)                           │   │
│  │  - RevenuePredictor (XGBoost)                        │   │
│  │  - Customer_Churn_Detection (Random Forest)         │   │
│  │  - Campaign_Detector (Random Forest + Gradient Boost)│   │
│  │  - Operational_risk_predictor (Random Forest)        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     SQLite Database                                 │   │
│  │     - 18 tables (10 dimension + 8 fact tables)      │   │
│  │     - 2.7M+ rows                                    │   │
│  │     - Inventory, Orders, Users, Campaigns          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Model Files                                      │   │
│  │     - LSTM models (.h5)                             │   │
│  │     - Scikit-learn models (.pkl, .joblib)          │   │
│  │     - Scalers and feature mappings                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

1. **Frontend (Streamlit Dashboard)**
   - User interface for all features
   - Direct model integration 
   - Real-time data visualization
   - Interactive forms and inputs

2. **Backend API (Flask)**
   - RESTful endpoints for inventory and analytics
   - Database query interface
   - Data aggregation and processing
   - CORS-enabled for web integration

3. **ML Service Layer**
   - 5 production-ready machine learning models
   - Direct model loading and prediction
   - Feature preprocessing and scaling
   - Model caching for performance

4. **Data Layer**
   - SQLite database for transactional data
   - CSV files for historical data
   - Model artifacts (saved models, scalers, mappings)
   - Configuration files

### Data Flow

1. **User Input** → Dashboard receives user parameters
2. **Model Loading** → Models loaded from disk (cached)
3. **Feature Processing** → Input data transformed/scaled
4. **Prediction** → ML model generates prediction
5. **Result Display** → Results shown in dashboard with visualizations

### Model Architecture Details

- **Stock Forecaster**: LSTM neural networks (one per category) with StandardScaler
- **Revenue Predictor**: XGBoost regressor with 3 features
- **Customer Churn**: Random Forest classifier with 4 features
- **Campaign Predictor**: Random Forest classifier + Gradient Boosting regressor
- **Operational Risk**: Random Forest classifier with 8 features

---

## 📁 Project Structure

```
Deloitte/
├── dashboard.py                 # Main Streamlit dashboard
├── app.py                      # Flask API server entry point
├── requirements.txt            # Python dependencies
├── setup_database.py           # Database initialization script
│
├── src/                        # Backend source code
│   ├── api/                    # API routes and database
│   │   ├── routes.py           # Standard API endpoints
│   │   ├── ml_routes.py        # ML prediction endpoints
│   │   └── database.py         # Database utilities
│   ├── services/               # Business logic
│   │   ├── inventory_service.py
│   │   └── ml_prediction_service.py
│   └── models/                 # Data models
│
├── New_ML_Models/              # Production ML models
│   ├── Guide_to_use/
│   │   └── model.py            # Model classes and functions
│   ├── stock_forecaster/       # LSTM models and scalers
│   ├── revenue_predictor/      # XGBoost model
│   ├── customer_churn/         # Random Forest model
│   ├── Campaign_ROI_Predictor/ # Campaign models
│   └── Operational_risk_predictors/ # Risk models
│
├── database/                    # Database files and docs
│   ├── fresh_flow_markets.db   # SQLite database (622 MB)
│   ├── DATABASE_SCHEMA.md      # Schema documentation
│   └── ERD.md                  # Entity relationship diagrams
│
├── data/                        # Data files
│   └── Inventory Management/    # CSV data files
│
├── Testing/                     # Model testing
│   ├── main_tests.ipynb        # Main test notebook
│   ├── operational_risk_test.ipynb
│   └── Results/                # Test results
│
└── docs/                        # Documentation
    ├── API_DOCUMENTATION.md
    ├── ML_API_DOCUMENTATION.md
    └── GETTING_STARTED.md
```

---

## 📊 Model Performance

| Model | Type | Performance Metrics |
|-------|------|-------------------|
| **Stock Forecaster** | LSTM (Time Series) | Category-specific MSE tracking |
| **Revenue Predictor** | XGBoost (Regression) | High accuracy on daily revenue |
| **Customer Churn** | Random Forest (Classification) | Binary churn prediction |
| **Campaign ROI** | Random Forest + Gradient Boost | 96.67% R², 99.90% AUC |
| **Operational Risk** | Random Forest (Classification) | Risk probability scoring |

---

## 🔗 Additional Resources

- **API Documentation**: `docs/API_DOCUMENTATION.md`
- **ML API Guide**: `docs/ML_API_DOCUMENTATION.md`
- **Database Schema**: `database/DATABASE_SCHEMA.md`
- **Getting Started**: `docs/GETTING_STARTED.md`
- **Testing Guide**: `Testing/README.md`

---

## 📝 Notes

- The dashboard uses models directly (no API dependency for ML predictions)
- All models are loaded from `New_ML_Models/` directory
- Database path: `database/fresh_flow_markets.db`
- Default API port: `5000`
- Default Streamlit port: `8501`

---

## 🎯 Key Achievements

✅ **5 Production-Ready ML Models** - All models tested and integrated  
✅ **Interactive Dashboard** - User-friendly Streamlit interface  
✅ **REST API Backend** - Complete API for inventory and analytics  
✅ **Comprehensive Testing** - Test notebooks for all models  
✅ **Full Documentation** - API docs, schemas, and usage guides  

---

**Last Updated**: February 2026  
**Version**: 1.0.4-stable  
**Project**: Deloitte x AUC Hackathon 2026
