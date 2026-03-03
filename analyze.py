import sqlite3
import pandas as pd
import os

os.makedirs('data/processed', exist_ok=True)

conn = sqlite3.connect('ecommerce.db')


query = """
SELECT 
    t.product_category_name_english AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.product_id) AS total_products_sold,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(SUM(oi.price) / COUNT(DISTINCT oi.order_id), 2) AS average_order_value
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
WHERE p.product_category_name IS NOT NULL
GROUP BY t.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
"""

print("Виконуємо просунутий SQL-запит...\n")
df_datamart = pd.read_sql_query(query, conn)

print("🏆 ТОП-10 категорій (Англійською) з метриками:")
print(df_datamart.to_string(index=False))

output_path = 'data/processed/top_categories_metrics.csv'
df_datamart.to_csv(output_path, index=False)
print(f"\n✅ Дані успішно збережено у {output_path}")

conn.close()