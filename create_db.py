import os
import pandas as pd
import sqlite3

DATA_DIR = 'data/raw'
DB_NAME = 'ecommerce.db'

conn = sqlite3.connect(DB_NAME)

print("Починаємо завантаження даних у SQL...")

for file in os.listdir(DATA_DIR):
    if file.endswith('.csv'):
        file_path = os.path.join(DATA_DIR, file)

        df = pd.read_csv(file_path)
        table_name = file.replace('olist_', '').replace('_dataset', '').replace('.csv', '')
        
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"✅ Таблиця '{table_name}' успішно створена! Завантажено {len(df)} рядків.")

conn.close()
print(f"🎉 Готово! База даних '{DB_NAME}' успішно створена та готова до роботи.")
