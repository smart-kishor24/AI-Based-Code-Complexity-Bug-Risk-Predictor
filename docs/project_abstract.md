# Project Abstract

## Project Title
**AI-Based Code Complexity & Bug Risk Predictor**

## Authors / Academic Context
Department of Computer Science & Engineering (Artificial Intelligence and Machine Learning)  
Academic Mini-Project (B.Tech CSE-AIML)

---

## Abstract
Modern software engineering organizations operate within continuously expanding source codebases characterized by complex function hierarchies, non-trivial control-flow logic, deeply nested branching, and extensive API dependencies. While traditional static analysis linters (e.g., Pylint, Flake8, Ruff) provide deterministic rule-based checks for stylistic infractions and syntax anomalies, they lack the empirical capability to evaluate software defect susceptibility based on historical defect patterns. Conversely, manual peer review remains cognitively intensive, error-prone, and bottlenecked by human bandwidth.

This mini-project presents the design, empirical development, and implementation of the **AI-Based Code Complexity & Bug Risk Predictor**, an intelligent, hybrid software engineering analysis system. The platform integrates:
1. **Abstract Syntax Tree (AST)** structural parsing using Python's native compilation module to perform safe, non-executing static code introspection.
2. **Quantitative Software Engineering Metrics Computation**, synthesizing McCabe's Cyclomatic Complexity, Maximum Nesting Depth, argument counts, return counts, and Halstead Software Science metrics (Volume, Difficulty, Effort, Programming Time, and Estimated Defects).
3. **Static Rule-Based Anti-Pattern Detection** identifying hazardous programming patterns such as mutable default arguments, bare exception handlers, and non-idiomatic singleton comparisons.
4. **Supervised Machine Learning Defect Prediction** trained, cross-validated, and benchmarked on verified historical defect records from the **NASA PROMISE KC1** repository. Four algorithms were evaluated: Logistic Regression (baseline), Decision Tree, Random Forest (primary model), and Extreme Gradient Boosting (XGBoost).
5. **Explainable Artificial Intelligence (XAI)** utilizing SHAP (SHapley Additive exPlanations) to decompose both global feature importances and local, function-specific predictive drivers into human-interpretable natural language narratives and visual attribution charts.
6. **Publication-Grade Reporting**, delivering automated PDF technical reports (via ReportLab) and raw CSV metric exports alongside an interactive, professional Streamlit web dashboard.

The empirical findings demonstrate that ensemble tree architectures (specifically Random Forest and XGBoost) achieve strong diagnostic utility on holdout test partitions (Random Forest: 67.90% Accuracy, 44.29% F1-score, 0.6288 ROC-AUC, 48.33% 5-Fold Stratified Cross-Validation F1). Crucially, the system enforces a strict methodological boundary: high complexity is recognized as an indicator of cognitive load and maintainability friction rather than an incontrovertible guarantee of an active runtime defect. The application serves as an advisory decision-support tool for engineering teams to prioritize code reviews and unit test allocations efficiently.
