# AI-Based Code Complexity & Bug Risk Predictor

[![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E.svg)](https://scikit-learn.org/)
[![Explainable AI](https://img.shields.io/badge/SHAP-TreeExplainer-brightgreen.svg)](https://shap.readthedocs.io/)
[![Tests](https://img.shields.io/badge/pytest-18%20passed-success.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-Academic%20Evaluation-lightgrey.svg)]()

> An intelligent, hybrid software engineering decision-support system that unifies **AST Structural Decomposition**, **Quantitative Code Metrics (McCabe & Halstead)**, **Static Anti-Pattern Linting**, **Supervised Defect Prediction (NASA PROMISE)**, and **Explainable AI (SHAP)** into an interactive, publication-grade web dashboard and PDF report generator.

---

## 📑 Table of Contents
1. [Project Overview & Abstract](#project-overview--abstract)
2. [Problem Statement & Motivation](#problem-statement--motivation)
3. [Existing vs. Proposed System](#existing-vs-proposed-system)
4. [System Architecture](#system-architecture)
5. [Technology Stack](#technology-stack)
6. [Project Folder Structure](#project-folder-structure)
7. [Dataset Source & Methodology](#dataset-source--methodology)
8. [Machine Learning Pipeline & Empirical Results](#machine-learning-pipeline--empirical-results)
9. [Explainable AI (SHAP) Interpretation](#explainable-ai-shap-interpretation)
10. [Streamlit Multi-Page UI Walkthrough](#streamlit-multi-page-ui-walkthrough)
11. [Installation & Windows 11 Execution](#installation--windows-11-execution)
12. [Automated Testing & QA Verification](#automated-testing--qa-verification)
13. [Limitations & Ethical Software Engineering Notice](#limitations--ethical-software-engineering-notice)
14. [Future Scope](#future-scope)

---

## 1. Project Overview & Abstract

### Abstract
Modern software engineering organizations operate within continuously expanding source codebases characterized by complex function hierarchies, non-trivial control-flow logic, deeply nested branching, and extensive dependencies. Traditional static analysis linters identify predefined stylistic and syntactic issues, but they lack the empirical capability to evaluate software defect susceptibility based on historical defect patterns.

This project delivers an end-to-end, production-style academic mini-project designed to assist software engineers, QA teams, and code reviewers. The system safely ingests Python source code, extracts granular control flow and Halstead software science metrics using Python's native Abstract Syntax Tree (`ast`), integrates static code smell detection, and applies supervised machine learning algorithms trained on verified **NASA PROMISE** historical defect records to estimate function-level defect probability. Furthermore, local and global predictions are explained via **SHAP (SHapley Additive exPlanations)** to ensure transparency and developer trust.

---

## 2. Problem Statement & Motivation

1. **Cognitive Overload in Manual Review:** Developers cannot maintain a complete mental model of functions with high cyclomatic complexity ($CC > 10$) and deep nesting ($depth > 4$), resulting in overlooked defects.
2. **Deficit in Static Linters:** Conventional linters (Pylint, Flake8) lack probabilistic defect models; formatting warnings are presented with the same gravity as high-risk structural anomalies.
3. **Black-Box AI Skepticism:** Uninterpretable machine learning predictions are rejected by developers who require actionable remediation rationale.

---

## 3. Existing vs. Proposed System

| Dimension | Existing Linters (Pylint, Flake8) | Black-Box Deep Learning | **Proposed System (Code Risk Predictor)** |
|:---|:---|:---|:---|
| **Underlying Approach** | Deterministic syntax rules | Opaque token/graph embeddings | **Hybrid: AST + Metrics + ML + XAI** |
| **Defect Probability** | ❌ None (binary rule triggers) | Uncalibrated classification | **✅ Calibrated posterior probability $[0.0, 1.0]$** |
| **Historical Data** | ❌ None | Ad-hoc web scrapes | **✅ Legitimate NASA PROMISE repository** |
| **Explainability** | Line-based warning | ❌ Uninterpretable attention weights | **✅ SHAP local & global attribution + narrative** |
| **Remediation Guidance** | Style-only fixes | ❌ None | **✅ Metric-specific refactoring advice** |
| **Deliverables** | Terminal output | CLI log | **✅ Interactive UI + Downloadable PDF / CSV** |

---

## 4. System Architecture

```text
USER (Browser / Developer)
        │
        ▼
STREAMLIT WEB APPLICATION
        │
        ▼
SOURCE CODE INPUT (File Upload / Paste)
        │
        ▼
CODE VALIDATION & AST PARSING (ast.parse)
        │
        ├─────────────────────────────────────────────────┐
        ▼                                                 ▼
AST FEATURE EXTRACTION                            STATIC CODE ANALYSIS
(LOC, McCabe CC, Halstead, Nesting, Params)       (Ruff CLI & AST Anti-Pattern Linter)
        │                                                 │
        ▼                                                 ▼
FEATURE PREPROCESSING & STANDARD SCALING          STATIC CODE WARNINGS
        │                                                 │
        ▼                                                 │
TRAINED ML ENSEMBLE (Random Forest / XGBoost)             │
        │                                                 │
        ├───────────────────────┐                         │
        ▼                       ▼                         │
DEFECT PROBABILITY         SHAP TREE EXPLAINER            │
P(Defect | X)              (Local / Global Attributions)  │
        │                       │                         │
        └───────────┬───────────┘                         │
                    ▼                                     │
         RISK BAND CLASSIFICATION                         │
         (Low / Medium / High Risk)                       │
                    │                                     │
                    ▼                                     │
         RULE-BASED RECOMMENDATION ENGINE ◄───────────────┘
                    │
                    ├─────────────────────────────────────┐
                    ▼                                     ▼
         INTERACTIVE STREAMLIT DASHBOARD        REPORTS & PERSISTENCE
         (Charts, Tables, Inspections)          (PDF, CSV, SQLite History)
```

---

## 5. Technology Stack

- **Core Runtime:** Python 3.11.9
- **Parsing Engine:** Python `ast` module (safe non-executing compilation), `radon` (cyclomatic complexity)
- **Static Analysis:** `ruff` (isolated check mode) & built-in AST anti-pattern visitor
- **Machine Learning & Preprocessing:** `scikit-learn`, `xgboost`, `pandas`, `numpy`, `joblib`
- **Explainable AI:** `shap` (TreeExplainer & additive feature attributions)
- **Frontend Dashboard:** `streamlit`, `plotly` (interactive web graphics), custom CSS
- **Report Generation:** `reportlab` (Platypus flowable PDF compilation), `csv`
- **Database:** `sqlite3` (metadata & analysis history)
- **Quality Assurance:** `pytest` (comprehensive automated test suite)

---

## 6. Project Folder Structure

```text
mini project/
│
├── app.py                      # Main Streamlit application entry point & router
├── requirements.txt            # Locked project dependencies
├── README.md                   # Comprehensive academic and technical documentation
├── .gitignore                  # Git tracking exclusion specifications
├── download_and_train.py       # Standalone pipeline to download NASA data & train models
│
├── config/
│   └── settings.py             # System paths, risk thresholds, and metric heuristic constants
│
├── modules/
│   ├── __init__.py
│   ├── code_parser.py          # AST parser, function visitor, and nesting depth calculator
│   ├── feature_extractor.py    # LOC, McCabe CC, Halstead metrics, and structural metrics
│   ├── static_analyzer.py      # Ruff CLI wrapper & built-in AST code smell linter
│   ├── data_loader.py          # NASA PROMISE dataset loader, cleaner, and preprocessor
│   ├── model_trainer.py        # ML pipeline (LR, Decision Tree, Random Forest, XGBoost)
│   ├── model_evaluator.py      # Accuracy, Precision, Recall, F1, ROC-AUC, CM & curves
│   ├── defect_predictor.py     # Probability inference, feature mapping, and risk tiering
│   ├── explainability.py       # SHAP global importance, local attributions & narratives
│   ├── recommendation_engine.py# Actionable refactoring guidance generator
│   ├── report_generator.py     # Publication-grade PDF compilation & CSV export
│   └── history_db.py           # SQLite analysis session tracking & metadata storage
│
├── pages/
│   ├── 1_Home.py               # Executive KPIs, summary metrics, and historical logs
│   ├── 2_Code_Upload.py        # File uploader, direct text editor, and analysis trigger
│   ├── 3_Complexity_Analysis.py# Function-wise metrics table, Halstead metrics, Plotly charts
│   ├── 4_Static_Analysis.py    # Linting issues, severity filters, and suggestions
│   ├── 5_Risk_Prediction.py    # Defect probabilities, risk bands, and high-risk alerts
│   ├── 6_Explainable_AI.py     # Global SHAP importance & local waterfall risk drivers
│   ├── 7_Model_Performance.py # Empirical model benchmarks, confusion matrix, ROC curves
│   └── 8_Reports.py            # PDF/CSV downloads, refactoring guidance, SQLite viewer
│
├── dataset/
│   ├── README.md               # NASA PROMISE schema, source documentation & granularity
│   └── kc1.csv                 # Legitimate NASA KC1 dataset (2,109 raw / 1,212 deduplicated)
│
├── models/
│   ├── README.md               # Model persistence documentation
│   ├── defect_predictor_rf.joblib     # Serialized Random Forest model
│   ├── feature_scaler.joblib          # Fitted StandardScaler
│   ├── feature_columns.joblib         # Serialized training feature schema
│   └── model_evaluation_metrics.json  # Stored benchmark metrics & confusion matrices
│
├── database/
│   ├── README.md               # SQLite schema & privacy policy
│   └── analysis_history.db     # SQLite analysis history database
│
├── sample_code/
│   ├── simple_example.py       # Low complexity, clean PEP-8 sample
│   ├── complex_example.py      # High CC, long parameters, multiple branches sample
│   └── nested_conditions.py    # Deeply nested control flow & anti-pattern sample
│
├── tests/
│   ├── test_parser.py          # AST parser unit tests
│   ├── test_feature_extractor.py # Complexity & static analysis unit tests
│   ├── test_prediction.py      # Predictor, missing data, and SHAP tests
│   └── test_reports.py         # PDF, CSV, and SQLite lifecycle tests
│
├── docs/
│   ├── project_abstract.md     # Formal academic abstract
│   ├── problem_statement.md    # Problem motivation & research objectives
│   ├── methodology.md          # Architectural pipeline & step-by-step methodology
│   ├── architecture.md         # Dataflow diagrams & component interactions
│   ├── algorithm_explanation.md# McCabe, Halstead, Random Forest, XGBoost, and SHAP math
│   ├── testing_documentation.md# Complete test matrix and pytest execution logs
│   └── future_scope.md         # Planned research extensions
│
└── output/
    └── reports/                # Local cache directory for generated PDF reports
```

---

## 7. Dataset Source & Methodology

- **Repository:** NASA Metrics Data Program (MDP) / PROMISE Repository.
- **Dataset:** **NASA KC1** (`kc1.csv`).
- **Domain:** Production ground control software written in C/C++ for a satellite reception ground station.
- **Instances:** 2,109 raw subroutine records (1,212 unique instances after deduplication).
- **Target Variable:** `defects` (Binary: `0 = Clean`, `1 = Defective`).
- **Defect Distribution:** 315 Defective records (26.0%), 897 Clean records (74.0%).
- **Class Imbalance Ratio:** ~2.85:1 (Clean to Defective).
- **Data Splitting Protocol:** Stratified 80/20 train/test holdout split and 5-Fold Stratified Cross-Validation on the training partition. The `StandardScaler` was fitted strictly on `X_train` to eliminate test data leakage.

---

## 8. Machine Learning Pipeline & Empirical Results

The pipeline evaluates four algorithms under balanced class weighting:
1. **Logistic Regression (Baseline):** $L_2$-regularized linear log-odds classifier.
2. **Decision Tree:** Constrained depth ($max\_depth=6$) recursive partitioning.
3. **Random Forest (Primary):** $120$ de-correlated bagged decision trees with balanced subsampling.
4. **XGBoost:** Gradient-boosted decision trees optimizing binary logloss.

### Actual Benchmark Results (Holdout Test Partition)
> *Note: All metrics reported below are genuine empirical test outputs computed by the evaluation engine.*

| Model Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | 5-Fold CV F1 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Logistic Regression (Baseline)** | 60.91% | 32.61% | 47.62% | 38.71% | 0.6079 | 49.38% |
| **Decision Tree** | 58.44% | 27.38% | 36.51% | 31.29% | 0.5135 | 42.35% |
| **Random Forest (Primary Model)** | **67.90%** | **40.26%** | **49.21%** | **44.29%** | **0.6288** | **48.33%** |
| **XGBoost Classifier** | 67.08% | 36.92% | 38.10% | 37.50% | 0.6106 | 46.62% |

### Primary Model Confusion Matrix (Random Forest)
- **True Negatives (TN):** 134
- **False Positives (FP):** 46
- **False Negatives (FN):** 32
- **True Positives (TP):** 31

### Top 5 Predictive Features (Gini Importance)
1. `h_difficulty`: $0.0854$ (Halstead Difficulty)
2. `h_intelligence`: $0.0783$ (Halstead Intelligence)
3. `h_volume`: $0.0757$ (Halstead Volume)
4. `h_effort`: $0.0670$ (Halstead Effort)
5. `h_length`: $0.0659$ (Halstead Program Length)

---

## 9. Explainable AI (SHAP) Interpretation

To eliminate the "black-box" dilemma in software defect prediction, the platform implements **SHAP (SHapley Additive exPlanations)** via `TreeExplainer`:

1. **Global Importance:** Ranks the relative weight of each metric across the entire dataset.
2. **Local Function Attribution:** Deconstructs an individual function's predicted probability into:
   - **Base Value:** $E[f(x)] \approx 0.50$ (the dataset expectation).
   - **Positive Drivers (+):** Metrics pushing predicted risk upward (e.g., elevated cyclomatic complexity, deeply nested conditions, high Halstead effort).
   - **Negative Drivers (-):** Metrics moderating predicted risk downward (e.g., minimal arguments, low LOC).
3. **Natural Language Narrative:** Synthesizes an interpretable explanation (e.g., *"Function 'process_complex_transactions' has an estimated defect probability of 82.4%. Elevated risk is primarily driven by cyclomatic_complexity (24, contribution +0.31) and max_nesting_depth (5, contribution +0.18)."*).

---

## 10. Streamlit Multi-Page UI Walkthrough

The application features 8 specialized navigation pages:
1. **🏠 Page 1: Home Dashboard:** Executive metric cards, active session snapshot, defect distribution donut chart, and recent analysis history table.
2. **📤 Page 2: Code Upload:** Ingestion interface supporting `.py` file uploads, direct multi-line pasting, and one-click benchmark script loaders (`simple_example.py`, `complex_example.py`, `nested_conditions.py`).
3. **⚙️ Page 3: Complexity Analysis:** Function-level metrics table, interactive Plotly bar charts of McCabe CC with warning/critical threshold lines, LOC vs. CC scatter plots, Halstead software science metrics, and an individual function code inspector.
4. **🔍 Page 4: Static Analysis:** Static linting table categorizing issues into Errors, Warnings, Refactors, and Conventions with exact line/column locations and recommended fixes.
5. **🎯 Page 5: Risk Prediction:** ML defect risk classification into Low ($< 30\%$), Medium ($30\% - 70\%$), and High ($> 70\%$) tiers with configurable thresholds, risk distribution charts, and high-risk function callout banners.
6. **💡 Page 6: Explainable AI:** Global SHAP feature importance plot and local waterfall contribution charts with natural language risk narratives.
7. **📈 Page 7: Model Performance:** Training dataset metadata (NASA KC1), multi-model benchmark table, interactive Confusion Matrix heatmap, and multi-model ROC comparison curves.
8. **📑 Page 8: Reports:** One-click **Download PDF Technical Report** (ReportLab compiled), **Download Raw CSV Dataset**, prioritized refactoring guidance list, and SQLite database history management.

---

## 11. Installation & Windows 11 Execution

### Prerequisites
- Windows 11 (or compatible OS)
- Python 3.11.x installed and added to system `PATH`
- Git (optional, for version control)

### Step 1: Clone or Navigate to Project Directory
```powershell
cd "c:\Users\nalam\OneDrive\Desktop\mini project"
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Verify or Re-Train ML Model Artifacts (Optional)
The verified dataset (`dataset/kc1.csv`) and pre-trained model artifacts (`models/`) are already bundled. To re-train or download fresh NASA data:
```powershell
python download_and_train.py
```

### Step 5: Launch the Streamlit Dashboard
```powershell
streamlit run app.py
```
The application will launch in your default web browser at `http://localhost:8501`.

---

## 12. Automated Testing & QA Verification

The project includes an automated test suite executed via `pytest`:
```powershell
python -m pytest tests/ -v
```

### Test Coverage Highlights
- `test_parser.py`: Validates AST parsing, syntax errors, nested functions, class methods, deep nesting, and large files.
- `test_feature_extractor.py`: Verifies McCabe CC calculation, Halstead calculations, DataFrame transformations, and static anti-pattern detection (mutable defaults, bare `except:`, `== None`).
- `test_prediction.py`: Checks dataset error handling, empty input handling, model inference, probability calibration, and SHAP explainability.
- `test_reports.py`: Tests CSV export formatting, ReportLab PDF byte compilation, and SQLite database insert/query/clear lifecycles.

**Result:** `18 passed in 7.90s` (100% passing rate).

---

## 13. Limitations & Ethical Software Engineering Notice

> ⚠️ **Important Methodological Notice:**
> - **Complexity $\ne$ Bug:** A function with elevated cyclomatic complexity ($CC > 15$) is cognitively demanding and harder to test, but does **not** automatically contain an executable bug.
> - **Statistical Association:** Defect probabilities reflect statistical patterns learned from historical NASA aerospace software and serve as an **advisory decision-support tool**, not a proof of correctness.
> - **Language Scope:** The current AST parser targets Python source code; metrics from C/C++ datasets (NASA KC1) serve as an established transfer benchmark for control flow complexity.

---

## 14. Future Scope

1. **Multi-Language Support:** Integrating Tree-Sitter parsers for C/C++, Java, JavaScript, and TypeScript.
2. **Code Graph Neural Networks:** Incorporating Control Flow Graphs (CFG) and Program Dependence Graphs (PDG) with Graph Convolutional Networks (GCN).
3. **Automated LLM Refactoring:** Integrating local code models to draft automated pull requests containing guard-clause refactorings.
4. **CI/CD Integration:** Packaging into a GitHub Action / GitLab CI pipeline runner to enforce pull-request risk gates.

---

## 📜 Academic Attribution
- **Dataset:** NASA Metrics Data Program (MDP) / PROMISE Software Engineering Repository.
- **Complexity Theory:** Thomas J. McCabe (1976), Maurice H. Halstead (1977).
- **Explainability:** Scott M. Lundberg & Su-In Lee, *A Unified Approach to Interpreting Model Predictions* (NeurIPS 2017).
