import streamlit as st
import pandas as pd

# 1. Налаштування сторінки
st.set_page_config(page_title="E-commerce Analytics", page_icon="🛒", layout="wide")

st.title("🛒 Аналітика продажів (Olist E-commerce)")
st.markdown("Цей інтерактивний дашборд побудовано на основі SQL-запитів до бази даних `ecommerce.db`.")

# 2. Функція для завантаження нашої "вітрини даних"
# st.cache_data дозволяє не читати файл заново при кожному кліку, що прискорює роботу
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/top_categories_metrics.csv')

# 3. Основна логіка відображення
try:
    df = load_data()
    
    # Створюємо дві колонки для метрик (AOV та Загальний дохід найпопулярнішої категорії)
    top_category = df.iloc[0]['category']
    top_revenue = df.iloc[0]['total_revenue']
    top_aov = df.iloc[0]['average_order_value']
    
    col1, col2 = st.columns(2)
    col1.metric(label=f"🏆 Топ категорія: {top_category}", value=f"${top_revenue:,.0f}")
    col2.metric(label="💳 Середній чек (AOV) топ категорії", value=f"${top_aov}")

    st.divider() # Горизонтальна лінія

    # Створюємо дві колонки для графіка та таблиці
    col_chart, col_table = st.columns([3, 2]) # Графік буде трохи ширшим
    
    with col_chart:
        st.subheader("📈 Дохід за категоріями")
        # Streamlit має вбудовані прості графіки
        st.bar_chart(data=df.set_index('category')['total_revenue'])
        
    with col_table:
        st.subheader("📊 Детальні дані")
        # Виводимо таблицю
        st.dataframe(df[['category', 'total_orders', 'average_order_value']], use_container_width=True)

except FileNotFoundError:
    st.error("❌ Файл з даними не знайдено. Переконайся, що ти запустив `analyze_data.py`!")