import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from catboost import CatBoostClassifier

st.set_page_config(page_title="Pro E-commerce Analytics", page_icon="🛍️", layout="wide")

# ================= DATA LOADING =================
@st.cache_data
def load_full_data():
    conn = sqlite3.connect('ecommerce.db')
    query = """
    SELECT 
        date(o.order_purchase_timestamp) as order_date,
        c.customer_state,
        COALESCE(t.product_category_name_english, 'Other') as category,
        oi.price,
        oi.freight_value
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
    WHERE o.order_status = 'delivered' AND o.order_purchase_timestamp IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month_year'] = df['order_date'].dt.to_period('M').astype(str)
    return df

try:
    df = load_full_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ================= SIDEBAR (FILTERS) =================
st.sidebar.header("🎛️ Filters")

# 1. Date Filter
min_date = df['order_date'].min().date()
max_date = df['order_date'].max().date()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# 2. State Filter
all_states = sorted(df['customer_state'].unique())
selected_states = st.sidebar.multiselect("Customer State", all_states, default=all_states[:5])

mask = (df['order_date'].dt.date >= start_date) & (df['order_date'].dt.date <= end_date)
if selected_states:
    mask = mask & (df['customer_state'].isin(selected_states))
    
filtered_df = df[mask]

# ================= MAIN SCREEN =================
st.title("🛍️ Interactive E-commerce Dashboard")

tab1, tab2 = st.tabs(["📈 Advanced Analytics", "🤖 AI Delivery Delay Prediction"])

with tab1:
    st.markdown("Data is automatically recalculated when you change the filters in the sidebar.")
    
    # --- Section 1: Dynamic KPIs ---
    total_revenue = filtered_df['price'].sum()
    total_orders = len(filtered_df)
    aov = total_revenue / total_orders if total_orders > 0 else 0
    avg_freight = filtered_df['freight_value'].mean() if total_orders > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("📦 Total Orders", f"{total_orders:,}")
    col3.metric("💳 Average Order Value (AOV)", f"${aov:,.2f}")
    col4.metric("🚚 Avg. Freight Value", f"${avg_freight:,.2f}")
    
    st.divider()
    
    # --- Section 2: Plotly Charts ---
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        sales_trend = filtered_df.groupby('month_year')['price'].sum().reset_index()
        fig_trend = px.line(sales_trend, x='month_year', y='price', markers=True, 
                            title="📈 Revenue Trend (Monthly)",
                            labels={'month_year': 'Month', 'price': 'Revenue ($)'})
        st.plotly_chart(fig_trend, use_container_width=True)

    with row1_col2:
        top_cats = filtered_df.groupby('category')['price'].sum().reset_index().sort_values('price', ascending=False).head(10)
        fig_cats = px.bar(top_cats, x='price', y='category', orientation='h',
                          title="🏆 Top 10 Product Categories by Revenue",
                          labels={'price': 'Revenue ($)', 'category': 'Category'},
                          color='price', color_continuous_scale='Blues')
        fig_cats.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cats, use_container_width=True)

    st.divider()
    
    state_sales = filtered_df.groupby('customer_state')['price'].sum().reset_index().sort_values('price', ascending=False)
    fig_map = px.bar(state_sales, x='customer_state', y='price',
                     title="🗺️ Revenue by State (Geography)",
                     labels={'customer_state': 'State', 'price': 'Revenue ($)'},
                     color='price', color_continuous_scale='Viridis')
    st.plotly_chart(fig_map, use_container_width=True)

# ================= TAB 2: ML PREDICTION =================
with tab2:
    st.subheader("🔮 Delivery Delay Prediction (CatBoost)")
    st.markdown("Enter the order details, and the ML model will evaluate the risk of delayed delivery.")
    
    @st.cache_resource
    def load_model():
        model = CatBoostClassifier()
        model.load_model('models/delivery_delay_model.cbm')
        return model
        
    try:
        model = load_model()
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Customer State", ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA'])
                category = st.selectbox("Product Category", ['health_beauty', 'watches_gifts', 'sports_leisure', 'computers_accessories'])
            with col2:
                price = st.number_input("Product Price ($)", min_value=1.0, value=50.0)
                freight = st.number_input("Freight Value ($)", min_value=0.0, value=15.0)
                days = st.slider("Promised Delivery Days", min_value=1, max_value=60, value=14)
            
            submitted = st.form_submit_button("🚀 Predict Delay Risk")

        if submitted:
            category_map = {
                'health_beauty': 'beleza_saude',
                'watches_gifts': 'relogios_presentes',
                'sports_leisure': 'esporte_lazer',
                'computers_accessories': 'informatica_acessorios'
            }
            model_category = category_map[category]
            
            input_data = pd.DataFrame({'customer_state': [state], 'product_category_name': [model_category], 'price': [price], 'freight_value': [freight], 'promised_delivery_days': [days]})
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100 
            
            st.divider()
            if prediction == 1:
                st.error(f"⚠️ **WARNING: High Risk of Delay!** Probability of logistic failure: **{probability:.1f}%**.")
            else:
                st.success(f"✅ **On Track!** The order is expected to arrive on time. Delay risk: **{probability:.1f}%**.")
    except Exception as e:
        st.error("❌ Model not found. Please ensure the model is trained and saved.")