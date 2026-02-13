# 🪪 Model Card: Wastewater BOD Soft Sensor

**Model Date:** February 2026
**Model Version:** 1.1.0
**Model Type:** Random Forest Regressor (Log-Transformed Target)
**License:** MIT

## 1. Intended Use

* **Primary Use:** Real-time estimation of Biological Oxygen Demand (BOD) in municipal wastewater treatment plants.
* **Intended Users:** Plant operators, Process engineers.
* **Out-of-Scope Use:** This model should **not** be used for regulatory compliance reporting (e.g., government fines). It is an operational tool for *process control only*. Lab samples remain the legal standard.

## 2. Model Description

The model predicts BOD (mg/L) using surrogate physical-chemical sensors available in real-time. It employs a **Random Forest** architecture trained on log-transformed targets to handle high-variance biological shock loads.

* **Inputs:**
  * Flow Rate ($Q_E$)
  * pH ($PH_E$)
  * Conductivity ($COND_E$) - *Primary proxy for dilution/industrial load*
  * Chemical Oxygen Demand ($COD_E$) - *Primary proxy for organic load*
  * Seasonality (Sine/Cosine of Month) - *Cyclical time encoding*

## 3. Performance Metrics

* **RMSE:** 44.95 mg/L
* **R² Score:** 0.28 (Validation Set)
* **Error Analysis:** The model is most accurate in the 100-300 mg/L range. It tends to underestimate extreme shock loads (>500 mg/L) but successfully flags them as "Warning" events.

## 4. Training Data

* **Source:** UCI Machine Learning Repository (Water Treatment Plant Data).
* **Time Period:** 1990 (Training) vs. 1991 (Testing) to validate temporal generalization.
* **Preprocessing:**
  * COD outliers capped at 99th percentile.
  * Target variable log-transformed (`np.log1p`) to normalize distribution.

## 5. Limitations & Bias (EU AI Act Transparency)

* **Seasonal Drift:** The model performance varies by season due to temperature-dependent bacterial activity. The `sin_month` feature mitigates but does not eliminate this.
* **Sensor Failure:** The model assumes valid sensor inputs. If the Conductivity probe fails (reads 0), the model will predict incorrectly.
* **Concept Drift:** The model was trained on historical data. Significant changes in the catchment area (e.g., a new factory opening) will require retraining.
  * *Mitigation:* The `/monitoring/stats` endpoint tracks input drift in real-time.

## 6. Ethical Considerations

* **Safety:** Over-reliance on the model could lead to under-treatment of sewage if the model predicts "Low BOD" falsely.
* **Mitigation:** The system includes a hard-coded "Shock Load Warning" when predictions exceed 400 mg/L, prompting manual operator review.
