import plotly.express as px
from business_trends_content import business_trends_sections
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import date
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import tensorflow as tf
# API Configuration
API_BASE = "http://localhost:5000"
import sys
sys.path.append('D:/Deloitte/New_ML_Models/Guide_to_use')
from guide import *
stock_forecaster = StockForecaster()
customer_churn_detector = Customer_Churn_Detection()
campaign_detector = Campaign_Detector()
opr_risk_predictor = Operational_risk_predictor()
revenue_predictor = RevenuePredictor()

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=60)
        if response.status_code == 200:
            return response.json() # Return the whole dictionary immediately
        return None
    except Exception as e:
        st.error(f"Connection Error: {e}") # Show the actual error in the UI
        return None

def safe_columns(df, required_cols):
    available_cols = [col for col in required_cols if col in df.columns]
    return df[available_cols] if available_cols else df


def get_category_from_item(item_name):
    """Derive category from item name using keyword matching."""
    if not item_name or not isinstance(item_name, str):
        return "Other/Uncategorized"
    item_lower = item_name.strip().lower()
    if any(k in item_lower for k in ["soda", "cola", "vin", "beer", "øl", "juice", "coffee", "kaffe", "tea", "the", "latte", "drink", "water", "vand", "lassi", "shake"]):
        return "Beverages"
    elif any(k in item_lower for k in ["sushi", "maki", "nigiri", "gyoza", "tempura", "sashimi", "edamame", "hosomaki"]):
        return "Sushi & Asian"
    elif any(k in item_lower for k in ["sandwich", "wrap", "burger", "pita", "durum", "rulle"]):
        return "Handhelds"
    elif any(k in item_lower for k in ["pizza", "pasta", "steak", "chicken", "meal", "kylling", "kebab", "curry", "bolognese", "lasagna"]):
        return "Main Courses"
    elif any(k in item_lower for k in ["cake", "kage", "dessert", "mousse", "sweet", "oreo", "cookie", "is", "gelato", "cheesecake"]):
        return "Desserts & Sweets"
    elif any(k in item_lower for k in ["brunch", "breakfast", "morning", "morgen", "egg", "bowl", "yogurt", "pancake"]):
        return "Breakfast & Brunch"
    elif any(k in item_lower for k in ["salat", "salad", "greens", "asparges"]):
        return "Salads & Greens"
    elif any(k in item_lower for k in ["fries", "fritter", "pommes", "snacks", "dip", "oliven", "mandler", "nuggets", "samosa"]):
        return "Sides & Snacks"
    elif any(k in item_lower for k in ["klip", "powerbank", "pose", "lighter", "levering", "personale", "deposit"]):
        return "Misc/Services"
    else:
        return "Other/Uncategorized"


def category_to_model_key(category_display):
    """Map display category (e.g. 'Main Courses') to guide model key (e.g. 'Main_Courses')."""
    if not category_display or category_display == "—":
        return None
    m = {
        "Beverages": "Beverages",
        "Sushi & Asian": "Sushi_&_Asian",
        "Handhelds": "Handhelds",
        "Main Courses": "Main_Courses",
        "Desserts & Sweets": "Desserts_&_Sweets",
        "Breakfast & Brunch": "Breakfast_&_Brunch",
        "Salads & Greens": "Salads_&_Greens",
        "Sides & Snacks": "Sides_&_Snacks",
        "Misc/Services": "Misc_Services",
        "Other/Uncategorized": "Other_Uncategorized",
    }
    return m.get(category_display)


# Page configuration
st.set_page_config(
    page_title="Fresh Flow Markets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Initialize session state for page routing if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = "Main Statistics"

# Create clickable text links using columns


_, nav_col_home, nav_col_trends, nav_col1, nav_col2, nav_col3, logo_col = st.columns([1, 2, 2, 2, 2, 2, 2])

with nav_col_home:
    if st.button("Home"):
        st.session_state.page = "Home"
        st.rerun()
with nav_col_trends:
    if st.button("Business Trends"):
        st.session_state.page = "Business Trends"
        st.rerun()
with nav_col1:
    if st.button("Main Statistics"):
        st.session_state.page = "Main Statistics"
        st.rerun()
with nav_col2:
    if st.button("Inventory Management"):
        st.session_state.page = "Inventory Management"
        st.rerun()
with nav_col3:
    if st.button("Forecasting Suggestions"):
        st.session_state.page = "Forecasting Suggestions"
        st.rerun()
with logo_col:
    st.image("logo.png.jpeg", width=80)

# Update the 'page' variable used for routing in the rest of your script
page = st.session_state.page

st.markdown("---")

# --- CONDITIONAL SIDEBAR ---
# Features only appear when Inventory Management is selected
if page == "Inventory Management":
    with st.sidebar:
        st.title("Fresh Flow Markets")
        st.markdown("---")
        st.header("⚙️ Filters")
        per_page = st.selectbox("Items per page", [10, 20, 50], index=1)
        search_term = st.text_input("🔍 Search Items", placeholder="Enter item name or barcode")
        page_num = st.number_input("Page", min_value=1, value=1)
        st.markdown("---")
        st.caption("Deloitte x AUC Hackathon")
else:
    # This hides the sidebar on other pages by forcing it collapsed 
    # or simply leaving it empty as per Streamlit's behavior.
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_dashboard():
    """Main Statistics Dashboard"""
    st.title("📊 Fresh Flow Markets - Sales Dashboard")
    
    col_date1, col_date2 = st.columns([2, 1])
    with col_date1:
        days = st.selectbox(
            "📅 Select Time Period",
            options=[30, 90, 180, 365, 730, 1095, 1825],
            index=5,
            format_func=lambda x: f"Last {x} days ({x//365} years)" if x >= 365 else f"Last {x} days"
        )
    with col_date2:
        st.metric("Data Range", f"{days} days")

    with st.spinner("Fetching latest data..."):
        analytics = fetch_data("/api/analytics/dashboard", params={"days": days})
        orders_meta = fetch_data("/api/orders", params={"per_page": 1})

    total_orders = 0
    total_revenue = 0.0
    aov = 0.0
    
    if orders_meta and orders_meta.get('success'):
        total_orders = orders_meta.get('pagination', {}).get('total', 399810)
    elif analytics and 'data' in analytics and 'summary' in analytics['data']:
        total_orders = analytics['data']['summary'].get('total_orders', 0)
    
    if analytics and 'data' in analytics and 'summary' in analytics['data']:
        summary = analytics['data']['summary']
        total_revenue = float(summary.get('total_revenue') or 0.0)
        aov = float(summary.get('avg_order_value') or 0.0)
    
    if total_revenue > 0 and total_orders > 0:
        aov = total_revenue / total_orders

    st.subheader("🎯 Key Business Metrics")
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Total Transactions", f"{total_orders:,}")
    with m2: 
        rev_str = f"${total_revenue:,.2f}" if total_revenue < 1000000 else f"${total_revenue/1000000:.2f}M"
        st.metric("Total Revenue", rev_str)
    with m3: st.metric("Average Order Value", f"${aov:.2f}")

    st.divider()

    st.subheader("📦 Order Counts by Status")
    status_data = []
    if analytics and 'data' in analytics:
        status_data = analytics['data'].get('by_status', [])
    
    if status_data and len(status_data) > 0:
        df_status = pd.DataFrame(status_data)
        cols = st.columns(min(4, len(df_status)))
        for idx, status_row in enumerate(df_status.itertuples()):
            with cols[idx % len(cols)]:
                count = status_row.count
                if status_row.status is None or pd.isna(status_row.status):
                    status_name = "Unknown"
                else:
                    status_name = str(status_row.status).replace('_', ' ').title()
                st.metric(status_name, f"{count:,}")
    else:
        st.info("📊 No order status data available for the selected period")
    
    st.divider()

    st.subheader("📊 Order Status Distribution")
    if status_data and len(status_data) > 0:
        df_status = pd.DataFrame(status_data)
        col_pie, col_stat_table = st.columns([2, 1])
        with col_pie:
            fig_pie = px.pie(df_status, values='count', names='status', hole=0.4)
            st.plotly_chart(fig_pie, width="stretch")
        with col_stat_table:
            st.dataframe(df_status, width="stretch", hide_index=True)
    else:
        st.info("📊 No status distribution data available")

    st.divider()

    st.subheader("🏆 Top Selling Items")
    top_items_raw = analytics['data'].get('top_items', []) if analytics and 'data' in analytics else []

    if top_items_raw and len(top_items_raw) > 0:
        df_top = pd.DataFrame(top_items_raw)
        mapping = {'title': 'Item Name', 'order_count': 'Orders', 'total_quantity': 'Units Sold', 'revenue': 'Revenue'}
        df_top = df_top.rename(columns=mapping)
        item_col = 'Item Name'
        val_col = 'Orders'

        col_chart, col_table = st.columns([2, 1])
        with col_chart:
            fig = px.bar(df_top.head(5), x=val_col, y=item_col, orientation='h', color=val_col)
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, width="stretch")
        with col_table:
            st.dataframe(df_top, width="stretch", hide_index=True)
    else:
        st.info("📊 No top selling items data available")

    if st.button("🔄 Refresh Dashboard", type="primary"):
        st.rerun()

def show_inventory():
    """Inventory Management Page"""
    st.title("📦 Inventory Management")
    st.markdown("**Monitor and manage your inventory items**")
    
    with st.expander("ℹ️ How to Use the Inventory Dashboard", expanded=False): 
     st.markdown("""
    ### **Inventory Management Dashboard**
    
    This dashboard provides centralized control over your inventory. Use the tools below to maintain optimal stock levels, track item details, and ensure efficient operations.
    
    **Key Functionalities:**
    * **Search & Filter:** Locate specific items instantly using the search bar in the sidebar.
    * **Item Details:** View comprehensive information for each product by selecting it from the list.
    * **Low Stock Monitoring:** Items below their defined threshold are automatically highlighted for review.
    * **View Customization:** Adjust the number of items displayed per page using the selector in the sidebar.
    
    **Pro Tip:** Regularly check the "Low Stock" list to prevent inventory shortages.
    """)

    # Use variables from the conditional sidebar defined at top
    params = {
        'page': page_num,
        'per_page': per_page
    }
    if search_term:
        params['search'] = search_term
        params['page'] = 1

    data = fetch_data('/api/inventory/items', params)
    
    if data and data.get('data'):
        items = data['data']
        pagination = data.get('pagination', {})
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        df = pd.DataFrame(items)
        tab1, tab2, tab3 = st.tabs(["📋 All Items", "📊 Item Details", "🚨 Low Stock"])
        
        with tab1:
            st.subheader("All Inventory Items")
            display_cols = ['title', 'barcode', 'price', 'vat', 'status']
            available_cols = [col for col in display_cols if col in df.columns]
            
            if available_cols:
                display_df = df[available_cols].copy()
                if 'price' in display_df.columns:
                    display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
                if 'vat' in display_df.columns:
                    display_df['vat'] = display_df['vat'].apply(lambda x: f"{x}%" if pd.notna(x) else "N/A")
                st.dataframe(display_df, width="stretch", hide_index=True)
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
             st.info(f"📊 Showing {len(items)} items | Page {pagination.get('page', 1)} of {pagination.get('pages', 1)} | Total: {pagination.get('total', 0)}")
        
        
        with tab2:
            st.subheader("Item Details")
            if len(items) > 0:
                selected_item = st.selectbox(
                    "Select an item to view details:",
                    options=range(len(items)),
                    format_func=lambda i: items[i].get('title', f'Item {i+1}')
                )
                item = items[selected_item]
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Basic Info")
                    st.write(f"**ID:** {item.get('id', 'N/A')}")
                    st.write(f"**Title:** {item.get('title', 'N/A')}")
                    st.write(f"**Barcode:** {item.get('barcode', 'N/A')}")
                    st.write(f"**Price:** ${item.get('price', 0):.2f}")
                    st.write(f"**VAT:** {item.get('vat', 0)}%")
                    st.write(f"**Status:** {item.get('status', 'N/A')}")
                with col2:
                    st.markdown("### Availability")
                    st.write(f"**Display for Customers:** {'Yes' if item.get('display_for_customers') else 'No'}")
                    st.write(f"**Delivery:** {'Yes' if item.get('delivery') else 'No'}")
                    st.write(f"**Eat In:** {'Yes' if item.get('eat_in') else 'No'}")
                    st.write(f"**Takeaway:** {'Yes' if item.get('takeaway') else 'No'}")
        
       
        
        with tab3:
            st.subheader("🚨 Low Stock Alerts")
            low_stock_response = fetch_data('/api/inventory/low-stock')
            
            if low_stock_response and low_stock_response.get('data'):
                ls_df = pd.DataFrame(low_stock_response['data'])
                # Only show the ID and Name (Title) as requested
                cols = [c for c in ['title','id', 'current_stock'] if c in ls_df.columns]
                st.dataframe(ls_df[cols], width="stretch", hide_index=True)
            else:
                st.info("No low stock items found.")
    else:
        st.warning("⚠️ No inventory data available. Please check API connection.")

    
    if st.button("🔄 Refresh Inventory", type="primary"):
        st.rerun()

def show_forecasting():
    """Forecasting Suggestions Page"""
    st.title("🔮 Demand Forecasting & Reorder Suggestions")
    st.markdown("**AI-powered predictions to optimize your inventory**")
    
    ml_health = fetch_data('/api/ml/health')
    if ml_health and ml_health.get('status') == 'healthy':
        st.success("✅ ML Service is operational")
        with st.expander("📊 Available ML Models"):
            models = ml_health.get('available_models', {})
            for model_name, available in models.items():
                status = "✅ Ready" if available else "❌ Not Available"
                st.write(f"**{model_name.replace('_', ' ').title()}:** {status}")
    else:
        st.warning("⚠️ ML Service may not be fully operational")
    
    st.markdown("---")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Demand Forecast", 
        "📦 Reorder Recommendations", 
        "🔄 Bulk Forecast",
        "🎯 Campaign ROI",
        "👥 Customer Churn",
        "🏪 Cashier Integrity and Operational Risk",
        "💰 Revenue"

    ])
    with tab1:
        st.subheader("Predict Item Demand")
        item_name = st.text_input("Item name", placeholder="e.g. Chicken Burger, Cola, Sushi Maki...", key="forecast_item_name")
        category = get_category_from_item(item_name) if item_name else "—"
        st.write("**Category:**", category)
        month = st.selectbox("Month", options=list(range(1, 13)), format_func=lambda x: str(x), key="forecast_month")
        forecast_days = st.slider("Forecast Period (days)", min_value=1, max_value=30, value=7, key="forecast_days")
        if st.button("🔮 Generate Forecast", type="primary", key="forecast_btn"):
            # Placeholder: 12 dummy numbers — replace with your logic
            value=0
            for i in range(forecast_days):
                value += stock_forecaster.predict(category, month, i)
            st.subheader(f"Forecast Result after forecast_days")
            st.write("Category:", category, "| Month:", month, "| Forecasting days:", forecast_days)
            st.write("**Number of orders in the next forecast_days:**", value)
            

    with tab2:
        st.subheader("Stock Reorder Recommendations")
        reorder_item_name = st.text_input("Item name", placeholder="e.g. Chicken Burger, Cola...", key="reorder_item_name")
        category_reorder = get_category_from_item(reorder_item_name) if reorder_item_name else "—"
        st.write("**Category:**", category_reorder)
        col1, col2 = st.columns(2)
        with col1:
            month_reorder = st.selectbox("Month", options=list(range(1, 13)), format_func=lambda x: str(x), key="reorder_month")
            last_qty = st.number_input("Last quantity (recent demand)", min_value=0.0, value=50.0, step=1.0, key="reorder_last_qty")
            forecast_days_reorder = st.number_input("Forecast period (days)", min_value=1, value=7, key="reorder_forecast_days")
        with col2:
            current_stock = st.number_input("Current Stock Level", min_value=0.0, value=100.0, step=1.0, key="reorder_current_stock")
            safety_multiplier = st.slider("Safety Stock Multiplier", min_value=1.0, max_value=2.0, value=1.2, step=0.1, key="reorder_safety")
        if st.button("📦 Get Reorder Recommendation", type="primary", key="reorder_btn"):
            model_key = category_to_model_key(category_reorder)
            if not reorder_item_name or not model_key:
                st.warning("Enter an item name so we can derive the category.")
            else:
                try:
                    reorder_qty = stock_forecaster.stock_reorder_recommendation(
                        model_key, month_reorder, last_qty, forecast_days_reorder, current_stock, safety_multiplier
                    )
                    pred = stock_forecaster.predict(model_key, month_reorder, last_qty, forecast_days_reorder)
                    st.metric("Category", category_reorder)
                    st.metric("Predicted demand (over period)", f"{pred:.1f}")
                    st.metric("Recommended reorder quantity", f"{reorder_qty:.0f}")
                    if reorder_qty > 0:
                        st.warning("⚠️ Reorder recommended.")
                    else:
                        st.success("✅ Stock levels adequate.")
                except Exception as e:
                    st.error(f"Failed: {str(e)}")

    with tab3:
        st.subheader("Bulk Item Forecast")
        item_names_input = st.text_area("Item names (comma-separated)", value="Chicken Burger, Cola, Sushi Maki", key="bulk_item_names")
        month_bulk = st.selectbox("Month", options=list(range(1, 13)), format_func=lambda x: str(x), key="bulk_month")
        bulk_forecast_days = st.slider("Forecast Days", min_value=1, max_value=30, value=7, key="bulk_days")
        last_qty_bulk = st.number_input("Last quantity (used for each item)", min_value=0.0, value=50.0, step=1.0, key="bulk_last_qty")
        if st.button("🔄 Generate Bulk Forecast", type="primary", key="bulk_btn"):
            names = [x.strip() for x in item_names_input.split(',') if x.strip()]
            if not names:
                st.warning("Enter at least one item name.")
            else:
                summary_data = []
                for item_name in names:
                    cat = get_category_from_item(item_name)
                    model_key = category_to_model_key(cat)
                    if not model_key:
                        summary_data.append({"Item name": item_name, "Category": cat, "Predicted demand": "N/A", "Status": "❌ Unknown category"})
                        continue
                    try:
                        pred = stock_forecaster.predict(model_key, month_bulk, last_qty_bulk, bulk_forecast_days)
                        summary_data.append({"Item name": item_name, "Category": cat, "Predicted demand": f"{pred:.1f}", "Status": "✅ Success"})
                    except Exception as e:
                        summary_data.append({"Item name": item_name, "Category": cat, "Predicted demand": "N/A", "Status": f"❌ {str(e)}"})
                st.dataframe(pd.DataFrame(summary_data), width="stretch", hide_index=True)
    with tab4:
        st.subheader("🎯 Campaign Strategy & Optimization")
        st.markdown("Use local ML models to predict campaign performance and compare scenarios.")
        
        st.write("### 1. Performance Predictor")
        st.caption("Model uses: duration_days, discount (%), max_redemptions, redemptions_per_duration.")
        with st.form("campaign_predictor_form"):
            col1, col2 = st.columns(2)
            with col1:
                duration = st.number_input("Campaign Duration (Days)", min_value=1, value=7, key="camp_dur")
                discount = st.slider("Discount (%)", min_value=0, max_value=100, value=20, key="camp_disc")
            with col2:
                max_redemptions = st.number_input("Max Redemptions", min_value=1, value=100, key="camp_max_red")
                redemptions_per_duration = st.number_input("Redemptions per Duration", min_value=0.0, value=50.0, step=5.0, key="camp_red_per")
            submit_campaign = st.form_submit_button("🚀 Predict Performance", type="primary")
        if submit_campaign:
            try:
                prob = campaign_detector.predict_success_probability(duration, discount, max_redemptions, redemptions_per_duration)
                expected = campaign_detector.predict_redemption(duration, discount, max_redemptions, redemptions_per_duration)
                st.success("Analysis Complete!")
                m1, m2 = st.columns(2)
                m1.metric("Success Probability", f"{prob * 100:.1f}%")
                m2.metric("Expected Redemptions", f"{expected}")
                st.progress(min(prob, 1.0))
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")

        st.markdown("---")
        st.write("### 2. Goal Optimizer")
        st.caption("Try a few duration/discount combinations to find a good success probability.")
        with st.form("campaign_optimizer_form"):
            o_col1, o_col2 = st.columns(2)
            with o_col1:
                target_redemptions = st.number_input("Target Redemptions", min_value=1, value=50, key="opt_target")
                max_red_opt = st.number_input("Max Redemptions (cap)", min_value=1, value=200, key="opt_max_red")
            with o_col2:
                max_discount = st.slider("Max Allowed Discount (%)", 5, 50, 25, key="opt_max_disc")
            optimize_submit = st.form_submit_button("✨ Find Best Among Samples", type="primary")
        if optimize_submit:
            try:
                best_prob, best_dur, best_disc = 0.0, 7, 10
                for d in [7, 14, 21]:
                    for disc in range(10, min(max_discount + 1, 51), 5):
                        p = campaign_detector.predict_success_probability(d, disc, max_red_opt, float(target_redemptions))
                        if p > best_prob:
                            best_prob, best_dur, best_disc = p, d, disc
                st.success("Best sampled configuration found.")
                st.write("**Recommended:**", best_dur, "days,", best_disc, "% discount → Success probability:", f"{best_prob * 100:.1f}%")
                st.metric("Expected Redemptions (approx)", campaign_detector.predict_redemption(best_dur, best_disc, max_red_opt, float(target_redemptions)))
            except Exception as e:
                st.error(f"Optimization failed: {str(e)}")
        st.markdown("---")
        st.write("### 3. Campaign Comparison")
        with st.form("campaign_comparison_form"):
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.markdown("#### 🅰️ Scenario A")
                a_duration = st.number_input("Duration (A)", min_value=1, value=7, key="dur_a")
                a_discount = st.slider("Discount % (A)", 0, 100, 10, key="disc_a")
                a_max_red = st.number_input("Max Redemptions (A)", min_value=1, value=100, key="max_red_a")
                a_red_per = st.number_input("Redemptions per Duration (A)", min_value=0.0, value=30.0, key="red_per_a")
            with comp_col2:
                st.markdown("#### 🅱️ Scenario B")
                b_duration = st.number_input("Duration (B)", min_value=1, value=14, key="dur_b")
                b_discount = st.slider("Discount % (B)", 0, 100, 20, key="disc_b")
                b_max_red = st.number_input("Max Redemptions (B)", min_value=1, value=100, key="max_red_b")
                b_red_per = st.number_input("Redemptions per Duration (B)", min_value=0.0, value=50.0, key="red_per_b")
            compare_submit = st.form_submit_button("⚖️ Compare Scenarios", type="primary")
        if compare_submit:
            try:
                prob_a = campaign_detector.predict_success_probability(a_duration, a_discount, a_max_red, a_red_per)
                prob_b = campaign_detector.predict_success_probability(b_duration, b_discount, b_max_red, b_red_per)
                exp_a = campaign_detector.predict_redemption(a_duration, a_discount, a_max_red, a_red_per)
                exp_b = campaign_detector.predict_redemption(b_duration, b_discount, b_max_red, b_red_per)
                best_idx = 0 if prob_a >= prob_b else 1
                st.success(f"**Scenario {'A' if best_idx == 0 else 'B'}** has higher success probability.")
                res_a, res_b = st.columns(2)
                with res_a:
                    st.metric("Scenario A Success", f"{prob_a * 100:.1f}%", delta="Winner" if best_idx == 0 else None)
                    st.write("Expected Redemptions:", exp_a)
                with res_b:
                    st.metric("Scenario B Success", f"{prob_b * 100:.1f}%", delta="Winner" if best_idx == 1 else None)
                    st.write("Expected Redemptions:", exp_b)
                comp_df = pd.DataFrame({"Scenario": ["Scenario A", "Scenario B"], "Success Probability": [prob_a * 100, prob_b * 100]})
                st.plotly_chart(px.bar(comp_df, x="Scenario", y="Success Probability", color="Scenario", title="Success Probability Comparison"), use_container_width=True)
            except Exception as e:
                st.error(f"Comparison failed: {str(e)}")
    with tab5:
        st.subheader("Customer Churn and Loyalty Prediction")
        st.info("Predict churn using local model (4 features: discount amount, points earned, avg price, waiting time).")

        with st.expander("🔍 Analyze Single Customer", expanded=True):
            with st.form("churn_form"):
                col1, col2 = st.columns(2)
                with col1:
                    cust_id = st.number_input("Customer ID", min_value=1, value=123, key="churn_cust_id")
                    discount_amount = st.number_input("Total Discount Amount ($)", min_value=0.0, value=25.0, step=10.0, key="churn_disc")
                    points_earned = st.number_input("Points Earned", min_value=0.0, value=500.0, step=100.0, key="churn_pts")
                with col2:
                    price = st.number_input("Avg Order Price ($)", min_value=0.0, value=75.50, step=10.0, key="churn_price")
                    waiting_time = st.number_input("Avg Waiting Time (min)", min_value=0.0, value=25.5, step=0.5, key="churn_wait")
                submit = st.form_submit_button("🔮 Predict Churn Risk", type="primary")
            if submit:
                try:
                    will_churn = customer_churn_detector.predict(discount_amount, points_earned, price, waiting_time)
                    st.success("Analysis Complete!")
                    m1, m2 = st.columns(2)
                    m1.metric("Customer ID", cust_id)
                    m2.metric("Will Churn", "Yes" if will_churn else "No")
                    st.info("Model returns class (0 = no churn, 1 = churn). Use retention actions for flagged customers.")
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")

        st.markdown("---")
        st.subheader("📋 Batch Churn (same 4 features per row)")
        batch_disc = st.number_input("Discount ($)", min_value=0.0, value=25.0, key="batch_disc")
        batch_pts = st.number_input("Points Earned", min_value=0.0, value=500.0, key="batch_pts")
        batch_price = st.number_input("Avg Price ($)", min_value=0.0, value=75.0, key="batch_price")
        batch_wait = st.number_input("Waiting Time (min)", min_value=0.0, value=25.0, key="batch_wait")
        if st.button("Predict Churn for This Profile", key="batch_churn_btn"):
            try:
                will_churn = customer_churn_detector.predict(batch_disc, batch_pts, batch_price, batch_wait)
                st.metric("Will Churn", "Yes" if will_churn else "No")
            except Exception as e:
                st.error(f"Batch prediction failed: {str(e)}")

    with tab6:
        st.subheader("🏪 Cashier Integrity & Operational Risk Monitor")
        st.markdown("Detect anomalies in cashier performance using pre-calculated risk assessments.")
        
        # Quick Lookup from Pre-calculated Data
        st.markdown("### 🔍 Quick Risk Lookup")
        st.info("Enter Cashier ID to get pre-calculated risk assessment from historical analysis")
        
        with st.form("cashier_lookup_form"):
            col1, col2 = st.columns([2, 1])
            with col1:
                cashier_id_lookup = st.number_input("Cashier ID", min_value=1, value=22354, key="lookup_cashier", 
                                                   help="Try 22354 for a known high-risk example")
            with col2:
                st.write("")  # Spacing
                
            submit_lookup = st.form_submit_button("🔍 Get Risk Assessment", type="primary")
        
        if submit_lookup:
            with st.spinner(f"Looking up cashier {cashier_id_lookup}..."):
                try:
                    response = requests.get(f"{API_BASE}/api/ml/operations/cashier-risk-lookup/{cashier_id_lookup}", timeout=10)
                    
                    if response.status_code == 200:
                        res = response.json()
                        if res.get('success'):
                            result = res.get('data', {})
                            
                            st.success("✅ Cashier Found!")
                            
                            # Display risk info
                            col1, col2, col3, col4 = st.columns(4)
                            risk_prob = result.get('risk_probability', 0) * 100
                            col1.metric("Risk Probability", f"{risk_prob:.1f}%")
                            col2.metric("Risk Category", result.get('risk_category', 'N/A'))
                            col3.metric("Total Transactions", f"{result.get('num_transactions_sum', 0):,.0f}")
                            col4.metric("Amount of Transaction Total", f"${result.get('transaction_total_sum', 0):,.2f}")
                            
                            # Risk Level Indicator
                            if result.get('risk_category') == 'CRITICAL':
                                st.error(f"🚨 **CRITICAL RISK** - Immediate attention required!")
                            elif result.get('risk_category') == 'HIGH':
                                st.warning(f"⚠️ **HIGH RISK** - Review required")
                            elif result.get('risk_category') == 'MEDIUM':
                                st.info(f"🔵 **MEDIUM RISK** - Monitor closely")
                            else:
                                st.success("✅ **LOW RISK** - Normal operations")
                            
                            # Financial Details
                            st.markdown("#### 💰 Key Metrics")
                            f_col1, f_col2 = st.columns(2)
                            with f_col1:
                                st.metric("Max Discrepancy %", f"{result.get('balance_discrepancy_pct_max', 0):,.1f}%")
                                st.metric("Balance Difference", f"${result.get('balance_diff_sum', 0):,.2f}")
                            with f_col2:
                                st.metric("VAT Component", f"${result.get('vat_component_sum', 0):,.2f}")
                                st.metric("Anomaly Score", f"{result.get('anomaly_score', 0):.3f}")
                        else:
                            st.error(f"❌ {res.get('error', 'Unknown error')}")
                    elif response.status_code == 404:
                        st.warning(f"⚠️ Cashier {cashier_id_lookup} not found in pre-calculated assessments")
                        st.info("💡 Try the Manual Entry option below to analyze this cashier")
                    else:
                        st.error(f"API Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # st.markdown("---")
        
        # Advanced Manual Entry (Collapsible)
        with st.expander("Advanced: Manual Feature Entry for new data", expanded=False):
            st.warning("Use this section **only if the cashier is not available in Quick Lookup**. "
        "Enter **summary statistics for one cashier during a single shift or time period**. "
        "If exact values are unknown, use **reasonable estimates**. "
        "Higher discrepancies, unusually large percentages, or high variability may indicate elevated risk." )
            
        
            col1, col2 = st.columns(2)
            with col1:
                cashier_id = st.number_input("Cashier ID", min_value=1, value=22354, help="Unique cashier identifier")
            with col2:
                shift_date = st.date_input("Shift Date", value=date.today())
            
            # st.warning("🚨 **Example:** Cashier 22354 - CONFIRMED 100% risk in training data (27,100% max discrepancy!)")
            
            st.markdown("#### 📊 Balance Difference Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                balance_diff_sum = st.number_input("Balance Diff Sum ($)", value=101066.0, step=100.0, help="Total balance discrepancies")
                balance_diff_mean = st.number_input("Balance Diff Mean ($)", value=66.0, step=1.0, help="Average discrepancy per transaction")
            with col2:
                balance_diff_std = st.number_input("Balance Diff Std Dev ($)", value=150.0, step=1.0, help="Variation in discrepancies (high = suspicious)")
                balance_diff_min = st.number_input("Balance Diff Min ($)", value=-200.0, step=10.0, help="Largest shortage")
            with col3:
                balance_diff_max = st.number_input("Balance Diff Max ($)", value=500.0, step=10.0, help="Largest overage")
                balance_disc_pct_mean = st.number_input("Discrepancy % Mean", value=150.0, step=0.1, help="Average discrepancy percentage")
            
            st.markdown("#### 💰 Transaction Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                balance_disc_pct_max = st.number_input("Discrepancy % Max 🚨", value=27100.0, step=100.0, help="CRITICAL: Maximum discrepancy percentage (model key feature!)")
                trans_total_sum = st.number_input("Transaction Total Sum ($)", value=213647.75, step=100.0, help="Total transaction value")
            with col2:
                trans_total_count = st.number_input("Transaction Count", min_value=1, value=1531, help="Number of transactions")
                trans_total_mean = st.number_input("Transaction Mean ($)", value=139.5, step=1.0, help="Average transaction value")
            with col3:
                vat_sum = st.number_input("VAT Sum ($)", value=32047.16, step=10.0, help="Total VAT collected")
                num_trans_sum = st.number_input("Num Transactions Sum", min_value=1, value=1531, help="Transaction count")
            
            st.markdown("#### 🏦 Balance & Amount Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                opening_bal_mean = st.number_input("Opening Balance Mean ($)", value=1000.0, step=100.0, help="Average shift opening balance")
                closing_bal_mean = st.number_input("Closing Balance Mean ($)", value=50000.0, step=100.0, help="Average shift closing balance")
            with col2:
                id_count = st.number_input("ID Count", min_value=1, value=1, help="Number of unique cashier IDs")
                total_amt_sum = st.number_input("Total Amount Sum ($)", value=213647.75, step=100.0, help="Total amount processed")
            with col3:
                total_amt_mean = st.number_input("Total Amount Mean ($)", value=139.5, step=1.0, help="Average amount per transaction")
                total_amt_std = st.number_input("Total Amount Std Dev ($)", value=85.0, step=1.0, help="Transaction amount variation")
            
            st.markdown("#### 💵 Cash Statistics")
            col1, col2 = st.columns(2)
            with col1:
                cash_amt_sum = st.number_input("Cash Amount Sum ($)", value=150000.0, step=100.0, help="Total cash handled")
            with col2:
                cash_amt_mean = st.number_input("Cash Amount Mean ($)", value=98.0, step=1.0, help="Average cash per transaction")
            st.markdown("#### 📊 Model Risk Inputs (2 extra features)")
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                balance_discrepancy_risk = st.number_input("Balance Discrepancy Risk", value=0.0, step=0.1, help="Risk score 0–1")
            with col_r2:
                balance_variance_risk = st.number_input("Balance Variance Risk", value=0.0, step=0.1, help="Risk score 0–1")
            
            if st.button("🔍 Analyze Cashier Risk", type="primary"):
                with st.spinner("Analyzing cashier data..."):
                    try:
                        risk_pct = opr_risk_predictor.predict_risk_percentage(
                            balance_disc_pct_mean, balance_disc_pct_max, trans_total_count,
                            closing_bal_mean, total_amt_mean, cash_amt_mean,
                            balance_discrepancy_risk, balance_variance_risk
                        )
                        risk_score = risk_pct * 100
                        if risk_score >= 70:
                            risk_level = "CRITICAL"
                        elif risk_score >= 50:
                            risk_level = "HIGH"
                        elif risk_score >= 25:
                            risk_level = "MEDIUM"
                        else:
                            risk_level = "LOW"
                        st.success("✅ Analysis Complete!")
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Risk Score", f"{risk_score:.1f}%")
                        m2.metric("Risk Level", risk_level)
                        m3.metric("Action Required", "⚠️ Yes" if risk_score >= 50 else "✅ No")
                        st.progress(min(risk_pct, 1.0))
                        if risk_level == "CRITICAL":
                            st.error("🚨 **CRITICAL RISK** - Immediate action required")
                        elif risk_level == "HIGH":
                            st.warning("⚠️ **HIGH RISK** - Review required")
                        elif risk_level == "MEDIUM":
                            st.info("🔵 **MEDIUM RISK** - Monitor closely")
                        else:
                            st.success("✅ **LOW RISK** - Normal operations")
                    except Exception as e:
                        st.error(f"Could not run risk model: {str(e)}")
            
        st.markdown("---")
        
        

    with tab7:
        st.subheader("💰 Revenue Forecasting")
        st.markdown("Predict future daily revenue based on historical trends and calendar events.")
        
        # UI Layout for inputs
        col1, col2 = st.columns(2)
        
        with col1:
            lagged_revenue = st.number_input(
                "Yesterday's Revenue ($)", 
                min_value=0.0, 
                value=5000.0, 
                step=100.0,
                help="The revenue recorded on the previous business day."
            )
        
        with col2:
            is_holiday = st.toggle("Is Holiday?", value=False)
            is_weekend = st.toggle("Is Weekend?", value=False)

        if st.button("🔮 Predict Revenue", type="primary"):
            with st.spinner("Calculating projected revenue..."):
                try:
                    pred_revenue = revenue_predictor.predict(int(is_weekend), int(is_holiday), lagged_revenue)
                    st.divider()
                    m1, m2 = st.columns(2)
                    m1.metric("Predicted Revenue", f"${pred_revenue:,.2f}")
                    diff = pred_revenue - lagged_revenue
                    pct_change = (diff / lagged_revenue) * 100 if lagged_revenue != 0 else 0
                    m2.metric("Projected Growth", f"{pct_change:+.2f}%", delta=f"${diff:,.2f}")
                    plot_data = pd.DataFrame({
                        "Day": ["Yesterday", "Forecast"],
                        "Revenue": [lagged_revenue, pred_revenue]
                    })
                    fig = px.bar(plot_data, x="Day", y="Revenue", color="Day", title="Revenue Comparison", text_auto='.2s')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to run Revenue Prediction: {str(e)}")

    

    
    st.markdown("---")
# Page routing
if page == "Home":
    # 1. Logo Section (Centered)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        try:
            # Note: Ensure 'logo.png.jpeg' is in the same folder as dashboard.py
            st.image('logo.png.jpeg', width=120)
        except Exception:
            st.info("💎 Fresh Flow Logo") 

    # 2. Hero Section
    st.markdown("<h1 style='text-align: center;'>Fuller Shelves, Less Waste</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Empowering Retailers with AI-Driven Inventory Management")
    
    # Fixed indentation for the description block
    st.markdown("""
    Fresh Flow Markets leverages advanced AI to optimize inventory, reduce waste, and 
    maximize profits for fresh produce departments. Our platform is designed to 
    simplify ordering, forecasting, and supplier management for retailers of all sizes.
    """)
    
    st.markdown("---")

    # 3. Why Choose Fresh Flow (Organized into Columns)
    st.markdown("### 🚀 Why Choose Fresh Flow?")
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("- **Reduce stock-outs** and waste")
        st.markdown("- **Boost revenue** and margins")
        st.markdown("- **Effortless** inventory management")
    
    with feat_col2:
        st.markdown("- **Actionable** team insights")
        st.markdown("- **Seamless** system integration")
        st.markdown("- **Designed** for fresh retail")

    st.markdown("---")

    # 4. Testimonials
    st.markdown("### 💬 What Our Customers Say")
    st.info("\"Fresh Flow Markets helped us decrease shrink and increase revenue. The outcome couldn't have been better!\"\n\n**— Retail Store Owner**")
    st.info("\"With Fresh Flow's AI, we reduced waste and improved customer satisfaction.\"\n\n**— Grocery Manager**")
    
    st.markdown("---")

    # 5. Our Solution List
    st.markdown("### 🛠️ Our Solution")
    st.markdown("""
    * **AI-powered** demand forecasting
    * **Intuitive** inventory tracking
    * **Easy** supplier management
    * **Effortless** IT integration
    * **Specialized** for fresh produce environments
    """)

    st.markdown("---")

    # 6. Call to Action & Footer
    st.markdown("### Ready to try AI that really works for fresh produce?")
    st.markdown("[🎯 Book a Demo](https://calendly.com/mael-freshflow) | [📧 Contact Us](mailto:support@freshflow.com)")
    
    st.caption("Deloitte x AUC Hackathon Project | v1.0.4-stable")
elif page == "Business Trends":
    st.title("📊 Business Trends")
    st.info("Explore key business trends, visualize patterns, and gain actionable insights from your data.")
    st.markdown("---")
    tabs = st.tabs([section['title'] for section in business_trends_sections])

    for idx, section in enumerate(business_trends_sections):
        with tabs[idx]:
            st.subheader(section['title'])
            st.markdown(section['description'])
            st.markdown("---")
            for img in section['images']:
                try:
                    st.image(img['file'], caption=img['caption'], use_column_width=True)
                    st.markdown(f"*{img.get('desc', '')}*")
                except Exception as e:
                    st.warning(f"Image not found or cannot be displayed: {img['file']} ({e})")
            st.markdown("---")
elif page == "Main Statistics":
    show_dashboard()
elif page == "Inventory Management":
    show_inventory()
elif page == "Forecasting Suggestions":
    show_forecasting()

    # --- UNIVERSAL FOOTER ---
st.markdown("---") # Visual separator
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("### 📞 Contact Us")
    st.caption("Fresh Flow Markets HQ")
    st.caption("Email: support@freshflow.com")
    st.caption("Phone: +1 (555) 012-3456")

with footer_col2:
    st.markdown("### 🛠️ Technical Support")
    st.caption("System Status: Online")
    st.caption("Documentation: [Click Here](#)")
    st.caption("Bug Report: [Open Ticket](#)")

with footer_col3:
    st.markdown("### 🏢 About")
    st.caption("Deloitte x AUC Hackathon Project")
    st.caption("© 2026 Fresh Flow Markets")
    st.caption("v1.0.4-stable")