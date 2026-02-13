# Wastewater BOD Prediction System (MLOps & Compliance)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Deployment-green)](https://fastapi.tiangolo.com/)
[![EU AI Act](https://img.shields.io/badge/Compliance-EU_AI_Act-violet)](MODEL_CARD.md)
[![Status](https://img.shields.io/badge/Status-Production_Ready-success)]()

## Overview

This project implements an end-to-end **MLOps Platform** for real-time wastewater quality monitoring. It deploys a **Soft Sensor** (Machine Learning Model) to estimate **Biological Oxygen Demand (BOD)**, a critical metric that typically requires a 5-day laboratory test ($BOD_5$).

By correlating real-time physical sensors (pH, Conductivity, COD, Flow) with historical biological data, this system provides **instant feedback** to plant operators, enabling proactive process control.

### Key Objectives

1. **Production Engineering:** Modular, refactored code structure suitable for Docker/Kubernetes.
2. **Observability:** Real-time tracking of **Data Drift** (Salinity spikes) and **System Latency**.
3. **Regulatory Compliance:** Full transparency documentation (`MODEL_CARD.md`) aligned with the **EU AI Act**.

---

## Project Structure

```bash
wastewater_project/
├── api/                   # FastAPI Deployment & Monitoring Middleware
│   └── main.py            # Serves the model + /monitoring/stats endpoint
├── config.yaml            # Central configuration (Model types, Paths)
├── data/                  # Data storage (Raw & Processed)
├── docs/                  # Sphinx Documentation
├── models/                # Serialized Models (.joblib)
├── notebooks/             # R&D and Exploratory Data Analysis
├── src/                   # Production Source Code (Refactored)
│   ├── data_loader.py     # Robust data ingestion
│   ├── features.py        # Feature Engineering (Cyclical Time)
│   ├── model.py           # Model Factory (RandomForest/SVM)
│   └── main.py            # Automated Training Pipeline
├── MODEL_CARD.md          # ⚖️ Regulatory Transparency Document
├── reflection_essay.md    # 📝 Reflection on EU AI Act & Ethics
└── README.md              # You are here
```

## Getting Started

**1. Installation**

Clone the repository and install dependencies:

```pip install -r requirements.txt
```

*(Dependencies include: `fastapi`, `uvicorn`, `pandas`, `scikit-learn`, `pyyaml`, `mlflow`)*


**2. Train the Model (Automated Pipeline)**

Run the MLOps pipeline to process data, engineer features, and train the model. This reads settings from `config.yaml`.

```python src/main.py
```

* **Output:** Saves a trained model to `models/bod_predictor.joblib`.

* **Metrics:** RMSE ~45 mg/L (Logged to MLflow).

**3. Launch the API (Deployment)**

Start the FastAPI server to serve predictions and monitor health.

```uvicorn api.main:app --reload
```
* **API Docs:** <http://127.0.0.1:8000/docs>

* **Monitoring Dashboard:** <http://127.0.0.1:8000/monitoring/stats>

---

## Monitoring & Observability
The system includes custom Middleware to track production health. Access the `/monitoring/stats` endpoint to view:

* **Latency:** Average inference time (ms).

* **Drift Detection:** Monitors input Conductivity and COD.

* **Alerts:** Flags "Shock Load" events if predictions exceed 400 mg/L.

---

## Regulatory Compliance (EU AI Act)
This project adheres to Article 13 (Transparency) of the EU AI Act for High-Risk AI Systems.

---

## Feature Engineering Highlight
To handle the biological seasonality of wastewater without creating discontinuities at year-end, we implemented **Cyclical Time Encoding:**

```
# Converting linear "Month" into continuous coordinates
df['sin_month'] = np.sin(2 * np.pi * df['Month'] / 12)
df['cos_month'] = np.cos(2 * np.pi * df['Month'] / 12)
```

This ensures the model understands that December (12) and January (1) are neighbors.

---

## License
MIT License - Open for educational and operational use.
