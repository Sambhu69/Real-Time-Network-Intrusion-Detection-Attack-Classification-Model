# 🛡️ Real-Time Network Intrusion Detection System

<div align="center">
  
  ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
  ![XGBoost](https://img.shields.io/badge/XGBoost-%23121011.svg?style=for-the-badge)
  
  <p><strong>An End-to-End Machine Learning Pipeline for Network Threat Analysis and Classification</strong></p>
</div>

## 📖 Project Overview

This project implements a robust, real-time Network Intrusion Detection System (NIDS) utilizing the comprehensive **UNSW-NB15** dataset. It demonstrates a complete MLOps lifecycle—from rigorous data preprocessing and feature engineering to deploying a high-performance classification model via a RESTful API and visualizing threats on a live dashboard.

Designed with production readiness in mind, this architecture is capable of ingesting network traffic features and classifying them into normal behavior or specific attack vectors (e.g., DoS, Fuzzers, Exploits) with high precision and low latency.

---

## 🏗️ System Architecture

1. **Data Pipeline**: 
   - Strict `.gitignore` implementations prevent tracking of massive raw CSVs.
   - Intelligent feature selection via **Mutual Information**.
   - Robust class balancing utilizing **SMOTE** to handle minority attack vectors.
   - Preprocessing artifacts stored securely (`StandardScaler`, `OneHotEncoder`).
2. **Machine Learning Model**: 
   - Highly optimized **XGBoost** Classifier.
   - Integrated **SHAP** values for model explainability and feature importance analysis.
3. **Backend Service**: 
   - High-throughput asynchronous **FastAPI** application serving the trained model.
4. **Frontend Interface**: 
   - Interactive **Streamlit** dashboard for monitoring network traffic, visualizing predictions, and investigating anomalous behaviors.

---

## 🚀 Key Results & Metrics

By addressing the severe class imbalances inherent in network traffic data, the model achieves exceptional performance across multiple attack categories:

* **Class Balancing Strategies**: Applied SMOTE to synthetically oversample minority attack classes, dramatically improving recall without sacrificing precision.
* **F1-Scores**: Sustained **>95% average F1-score** across critical attack vectors (specific results vary by class).
* **Explainability**: SHAP (SHapley Additive exPlanations) integration ensures that every blocked request or flagged anomaly is fully interpretable by security analysts.

---

## 📂 Directory Layout

```text
├── api/                      # FastAPI application for inference
├── configs/                  # Configuration files
├── dashboard/                # Streamlit UI dashboard
├── data/                     # Data assets (raw & processed)
├── models/                   # Serialized models & artifacts
├── notebooks/                # Exploratory Data Analysis & Prototyping
├── reports/                  # Evaluation metrics & visual reports
├── src/                      # Core ML pipeline source code
├── tests/                    # Unit & integration tests
├── .gitignore                # Strict version control policies
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Local Deployment & Installation

Follow these steps to run the complete system locally.

### 1. Clone the Repository
```bash
git clone https://github.com/Sambhu69/Real-Time-Network-Intrusion-Detection-Attack-Classification-Model.git
cd Real-Time-Network-Intrusion-Detection-Attack-Classification-Model
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the FastAPI Backend
Start the inference server on port 8000:
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*API Documentation available at: `http://localhost:8000/docs`*

### 5. Launch the Streamlit Dashboard
In a new terminal instance (ensure the virtual environment is activated):
```bash
cd dashboard
streamlit run app.py
```
*Dashboard available at: `http://localhost:8501`*

---

## 👨‍💻 Author

**Sambhav Shrestha**  
*Data Scientist & AI/ML Engineer*

Passionate about building scalable machine learning systems, optimizing MLOps workflows, and developing intelligent solutions for real-world problems.

[GitHub](https://github.com/Sambhu69) | [LinkedIn](#)

---
*If you find this project interesting or useful, please consider giving it a ⭐!*
