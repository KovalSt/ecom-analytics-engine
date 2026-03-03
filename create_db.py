import os
import pandas as pd
import sqlite3

# Шлях до папки з CSV файлами та назва нашої майбутньої бази
DATA_DIR = 'data/raw'
DB_NAME = 'ecommerce.db'

# Створюємо підключення. Якщо файлу ecommerce.db немає, він створиться автоматично
conn = sqlite3.connect(DB_NAME)

print("Починаємо завантаження даних у SQL...")

# Перебираємо всі файли у папці data/raw
for file in os.listdir(DATA_DIR):
    if file.endswith('.csv'):
        file_path = os.path.join(DATA_DIR, file)
        
        # Читаємо CSV файл через Pandas
        df = pd.read_csv(file_path)
        
        # Робимо красиві та короткі назви таблиць для SQL:
        # наприклад, "olist_orders_dataset.csv" перетвориться на "orders"
        table_name = file.replace('olist_', '').replace('_dataset', '').replace('.csv', '')
        
        # Записуємо DataFrame у таблицю SQL
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ Таблиця '{table_name}' успішно створена! Завантажено {len(df)} рядків.")

# Закриваємо підключення
conn.close()
print(f"🎉 Готово! База даних '{DB_NAME}' успішно створена та готова до роботи.")