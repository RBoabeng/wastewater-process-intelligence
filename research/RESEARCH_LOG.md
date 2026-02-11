# 🔬 Research & Implementation Log

This log documents the academic and technical research driving the development of the **Wastewater Process Intelligence** system. Each entry connects theoretical insights to specific project features.

---

## 11th February 2026 | Paper: Apllication of ML Models in Optimizing WWTPs (2025)

**Source:** DOI: 10.3390/app15158360
**Focus:** Model Selection for Limited Data

###  Summary

* **Key Finding:** For datasets with limited training samples (like UCI), **SVMs** outperform Deep Learning for predicting COD/BOD.
* **Operational Insight:** **Random Forest** is recommended for "Operator Decision Support" because it provides interpretable rules (e.g., for chemical dosing) rather than being a "Black Box".

###  Action Plan
* **Hybrid Strategy:** I will build two specific models:
    1. **The "Virtual Sensor" (SVM):** Optimized for pure accuracy to predict BOD levels.
    2. **The "Operator Assistant" (Random Forest):** Used to extract "Feature Importance"  to tell operators *which* sensor (pH vs. Flow) is driving the changes.