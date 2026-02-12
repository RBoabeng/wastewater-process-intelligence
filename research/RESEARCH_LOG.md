#  Research & Implementation Log

This log documents the academic and technical research driving the development of the **Wastewater Process Intelligence** system. Each entry connects theoretical insights to specific project features.

---

## 11th February 2026 | Paper: Apllication of ML Models in Optimizing WWTPs (Zamfir et al., 2025)

**Source:** DOI: 10.3390/app15158360

**Focus:** Model Selection for Limited Data

###  Summary

* **Key Finding:** For datasets with limited training samples (like UCI), **SVMs** outperform Deep Learning for predicting COD/BOD.
* **Operational Insight:** **Random Forest** is recommended for "Operator Decision Support" because it provides interpretable rules (e.g., for chemical dosing) rather than being a "Black Box".

###  Action Plan
* **Hybrid Strategy:** I will build two specific models:
    1. **The "Virtual Sensor" (SVM):** Optimized for pure accuracy to predict BOD levels.
    2. **The "Operator Assistant" (Random Forest):** Used to extract "Feature Importance"  to tell operators *which* sensor (pH vs. Flow) is driving the changes.

---

## 11th February 2026 | Data Exploration: Time Horizon Analysis

**Observation:** The dataset spans 22 months (Jan 1990 - Oct 1991).
**Implication:**

* **Seasonality:** Captures two full biological cycles (warm/cold seasons), allowing the model to learn temperature-dependent bacterial activity.
* **Split Strategy:** Sufficient length to perform "Walk-Forward Validation" rather than random K-Fold cross-validation, ensuring no data leakage from future to past.

---

## 12th February 2026 | Feasibility Study: Correlation Analysis

**Observation:**

* Input COD and Input BOD show a moderate positive correlation (Pearson r = 0.51).
* Input Flow shows a negative correlation (-0.33) with pollutant concentration, confirming the "dilution effect" during storm events.

**Decision:**

* **Feasibility Confirmed:** The 0.51 correlation is strong enough to use COD as a primary predictor.
* **Model Justification:** The relationship is not perfectly linear, necessitating non-linear models like XGBoost/RF rather than simple regression.
* **Feature Selection:** Will include Flow, pH, Conductivity, and COD as the "Input Vector" to predict BOD.

---

## 12th February 2026 | EDA: Seasonality Analysis

**Observation:**

* Significant seasonal variance identified. Input BOD drops to ~125 mg/L in August (Month 8) and rises to ~250 mg/L in December (Month 12).
* The variance (interquartile range) is also higher in winter months.

**Decision:**

* **Feature Engineering:** Must include `Month` as a categorical or cyclical feature.
* **Model Strategy:** A single "Global Average" baseline would fail; the model requires temporal features to handle the 2x swing in pollutant load between Summer and Winter.

---

## 12th February 2026 | Lag Analysis: Hydraulic Retention Time (HRT)

**Observation:**

* Cross-Correlation Function (CCF) shows peak correlation at **Lag 0**.
* Visual inspection of Input vs. Output COD peaks shows alignment within the same 24-hour window.

**Conclusion:**

* The plant's HRT is < 24 hours.
* **Model Strategy:** I will proceed with a non-lagged feature set, focusing on same-day sensor fusion (pH, Cond, Flow, COD) to predict BOD. This aligns with the "Operator Decision Support" goals for real-time dosing adjustments.

---
