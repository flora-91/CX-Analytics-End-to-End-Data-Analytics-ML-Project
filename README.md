# 📊 Customer Experience Analytics

### End-to-End Data Analytics & Machine Learning Project

An end-to-end Customer Experience Analytics solution that transforms customer feedback into actionable business insights.

The project integrates Customer Experience metrics (NPS & CSAT), operational data, Natural Language Processing (NLP), Machine Learning, and interactive Power BI dashboards to support data-driven decision-making.

---

## 🚀 Project Overview

Organizations collect thousands of customer surveys every day, but most of that information is never transformed into actionable insights.

This project demonstrates how a complete analytics pipeline can integrate structured and unstructured data, automate analysis, predict customer dissatisfaction, and visualize business insights in an interactive dashboard.

---

# 🎯 Business Problem

Many organizations measure Customer Experience through:

- NPS
- CSAT
- Customer surveys
- Open-ended comments

However, these datasets are often analyzed separately, making it difficult to understand customer behavior and identify the factors driving dissatisfaction.

This project addresses that challenge by integrating operational data with Customer Experience metrics into a single analytical solution.

---

# 💡 Solution

The proposed solution includes:

- ETL Pipeline developed in Python
- Operational Database (PostgreSQL)
- Data Warehouse implemented in Snowflake
- Dimensional Modeling
- Exploratory Data Analysis (EDA)
- Natural Language Processing (Sentiment Analysis)
- Machine Learning for detractor prediction
- Interactive dashboards in Power BI

---

# 🏗 Solution Architecture

```text
                Customer Surveys
                        │
                        │
 Operational Database (PostgreSQL)
                        │
                        ▼
            ETL Pipeline (Python)
                        │
                        ▼
        Snowflake Data Warehouse
                        │
                        ▼
         Exploratory Data Analysis
                        │
                        ▼
      Natural Language Processing
                        │
                        ▼
          Machine Learning Models
                        │
                        ▼
         Interactive Power BI Dashboard
```

---

# 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Database | PostgreSQL |
| Data Warehouse | Snowflake |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-Learn, XGBoost |
| NLP | NLTK, Pysentimiento |
| Visualization | Power BI |
| SQL | PostgreSQL / Snowflake SQL |
| Version Control | Git & GitHub |
| Project Management | Notion |

---

# 📂 Repository Structure

```text
CX-Analytics-End-to-End-Data-Analytics-ML-Project
│
├── 📁 Documentation
│   ├── PI2026C1 - Final Project Report.pdf
│   ├── PI2026C1 - Project Presentation.pdf
│   └── VitaHealth_ER_Diagram.png
│
├── 📁 Scripts
│   │
│   ├── 📁 01_data_generation
│   │   ├── 01_FL_02_data_generation.py
│   │   ├── 01_FL_VitaHealth_schema.sql
│   │   ├── business_rules.md
│   │   ├── encuestas_cx.csv
│   │   └── README.md
│   │
│   ├── 📁 02_sql_queries
│   │   ├── 02_FL_12Queries_vitahealth.sql
│   │   └── README.md
│   │
│   ├── 📁 03_dimensional_model
│   │   ├── 03_FL_dimensional_model.sql
│   │   └── README.md
│   │
│   ├── 📁 04_etl_pipeline
│   │   └── VitaHealth_dw
│   │       ├── 📁 config
│   │       ├── 📁 src
│   │       ├── requirements.txt
│   │       └── README.md
│   │
│   ├── 📁 05_machine_learning
│   │   ├── FL_EDA.ipynb
│   │   ├── FL_NLP.ipynb
│   │   ├── FL_modelado_ml.ipynb
│   │   ├── importancia_variables.csv
│   │   └── metricas_modelo.csv
│   │
│   └── 📁 06_powerbi
│       └── Power BI Dashboard (.pbix)
│
├── .gitignore
└── README.md
```

---

# ⚙ Project Workflow

## 1️⃣ Data Generation

- Synthetic operational healthcare database
- PostgreSQL implementation

---

## 2️⃣ SQL

- Relational model
- SQL queries
- Data validation

---

## 3️⃣ Dimensional Modeling

- Star Schema
- Fact table
- Dimension tables

---

## 4️⃣ ETL Pipeline

- Data extraction
- Cleaning
- Transformation
- Integration
- Loading into Snowflake

---

## 5️⃣ Machine Learning

The analytical pipeline includes:

- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- NLP
- Sentiment Analysis
- Topic Detection
- Customer Detractor Prediction

Algorithms evaluated:

- Logistic Regression
- Random Forest
- XGBoost

---

## 6️⃣ Power BI Dashboard

Interactive dashboard including:

- Customer Experience KPIs
- NPS
- CSAT
- Sentiment Analysis
- Topic Analysis
- Customer Risk Prediction
- Executive Insights

---

# ✨ Key Features

✔ ETL Pipeline

✔ PostgreSQL Operational Database

✔ Snowflake Data Warehouse

✔ Dimensional Modeling

✔ NLP Sentiment Analysis

✔ Topic Detection

✔ Machine Learning

✔ Predictive Analytics

✔ Power BI Dashboard

✔ Business Insights

---

# 📈 Machine Learning

The predictive model estimates the probability that a customer becomes a detractor based on:

- Customer Experience metrics
- Operational variables
- Survey responses
- NLP features

Model performance was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

# 📊 Dashboard Preview

> Dashboard screenshots will be added here.

---

# 🔮 Future Improvements

Future versions may include:

- Automated ETL scheduling
- Cloud deployment
- CRM integration
- API integration
- Real-time dashboards
- Advanced NLP models
- Generative AI for automatic insight generation

---

# 📚 Documentation

The complete technical documentation is available in the **Documentation** folder.

It includes:

- Business Problem
- Solution Design
- Architecture
- Technologies
- Machine Learning
- Agile Methodology
- Financial Analysis
- Conclusions

---

# 👩‍💻 Author

**Florencia Lombardi**

Data Analyst | Business Intelligence | Customer Experience Analytics

GitHub: https://github.com/flora-91

