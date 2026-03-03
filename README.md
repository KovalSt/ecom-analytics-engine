# 🛒 E-Commerce Data Engine: Analytics & ML Prediction

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![CatBoost](https://img.shields.io/badge/CatBoost-Machine%20Learning-yellow.svg)

## 📌 Project Overview
This project is an end-to-end Data Science and Analytics solution built on the **Olist Brazilian E-Commerce Dataset** (100,000+ real orders). It features a fully automated ETL pipeline, a relational SQL database, an interactive BI dashboard, and a Machine Learning model that predicts delivery delays.

## 🚀 Key Features
* **Automated ETL Pipeline**: Uses the Kaggle API to programmatically download and ingest raw CSV data into a local SQLite database.
* **Advanced SQL Analytics**: Utilizes complex SQL queries (JOINs, aggregations) to calculate business KPIs such as Revenue, Total Orders, and Average Order Value (AOV).
* **Interactive BI Dashboard**: A dynamic web application built with **Streamlit** and **Plotly**, featuring real-time filtering by date, geography, and category.
* **Machine Learning Prediction**: Integrated **CatBoost** classifier trained to predict the risk of delivery delays with **92%+ accuracy**, based on order details, state, and freight value.

## 🛠️ Tech Stack
* **Language:** Python
* **Database:** SQLite
* **Data Processing & Analytics:** Pandas, SQL
* **Machine Learning:** CatBoost, Scikit-Learn
* **Data Visualization:** Plotly Express
* **Web Framework:** Streamlit

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/KovalSt/ecom-analytics-engine.git](https://github.com/KovalSt/ecom-analytics-engine.git)
   cd ecom-analytics-engine
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## 📊 Dataset
The data was provided by [Olist](https://olist.com/), the largest department store in Brazilian marketplaces. It encompasses over 100k anonymized orders made between 2016 and 2018 at multiple marketplaces in Brazil.

## 👨‍💻 Author
**Stanislav Kovalchuk**
* **GitHub:** https://github.com/KovalSt