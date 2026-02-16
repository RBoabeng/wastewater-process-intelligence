## Executive Summary

**Real-Time Wastewater Process Intelligence: An MLOps Approach to BOD Estimation**

**Date:** February 2026
**Author:** Richard Boabeng

#### 1.Introduction & Problem Statement

Municipal wastewater treatment relies on Biological Oxygen Demand ($BOD_5$) to measure organic pollution. However, the standard laboratory test requires 5 days of incubation. This delay prevents plant operators from reacting to "shock loads" (sudden pollution spikes) in real-time, risking environmental non-compliance.


**Objective:** To develop a "Soft Sensor"—a Machine Learning model that estimates current BOD levels instantly using surrogate sensors (pH, Conductivity, COD, Flow) available in real-time.


#### 2.System Architecture & Methodology

The project transitioned from feasibility studies (Jupyter Notebooks) to a production-grade MLOps Platform:

* **Data Pipeline:** A modular ETL process (`src/data_loader.py`) cleans raw sensor data and removes outliers (99th percentile cap).

* **Feature Engineering:** To capture biological seasonality without mathematical discontinuities, we implemented Cyclical Time Encoding (Sine/Cosine transformation of months).

* **Model Selection:** A Random Forest Regressor was selected over SVM for its superior handling of non-linear interactions and robustness to noise ($RMSE \approx 45$ mg/L).

* **Deployment:** The model is served via a **FastAPI** microservice, container-ready for Kubernetes.


#### 3. Monitoriing & Observability

To satisfy operational requirements, the system includes a custom monitoring middleware:

* **Performance:** Tracks API latency (inference time < 20ms).

* **Drift Detection:** Continuously monitors input **Conductivity** and **COD**. If the rolling average exceeds safe baselines (indicating industrial dumping or sensor failure), the system flags a "Drift Warning."


#### 4. Regulatory Compliance (EU AI Act)

As a high-stakes operational tool, the system adheres to Article 13 (Transparency) of the EU AI Act. A comprehensive **Model Card** was generated to document:

* **Intended Use:** Process control guidance (not legal reporting).

* **Limitations:** Sensitivity to sensor calibration drift.

* **Ethical Risks:** Potential for automation bias leading to under-treatment.


#### 5. Conclusion

his project demonstrates that AI can bridge the gap between physical sensors and biological metrics. By integrating robust MLOps practices—automated pipelines, real-time monitoring, and regulatory documentation, we have transformed a theoretical model into a deployable, transparent safety tool for water infrastructure.
