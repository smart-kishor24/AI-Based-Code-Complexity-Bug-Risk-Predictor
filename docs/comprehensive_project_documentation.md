# AI-Based Code Complexity & Bug Risk Predictor
## Comprehensive Technical & Academic Project Documentation
**An AI/ML-Powered Static Code Analysis, Complexity Engineering & Defect Prediction Platform**

---

### Project Metadata
- **Project Title:** AI-Based Code Complexity & Bug Risk Predictor
- **Category:** Artificial Intelligence, Machine Learning, Software Engineering, Explainable AI (XAI)
- **Domain:** Automated Software Quality Assurance & Defect Susceptibility Estimation
- **Academic Context:** B.Tech Computer Science & Engineering (Artificial Intelligence and Machine Learning)
- **Developer / Author:** nalam
- **Submission Date:** 22-11-2026
- **Operating Environment:** Windows 11 / Linux / macOS (Python 3.11.x)
- **Repository Status:** Fully Implemented, Benchmark Trained, 19/19 Unit Tests Passing

---

## Table of Contents
1. [Project Abstract](#1-project-abstract)
2. [Problem Statement & Research Motivation](#2-problem-statement--research-motivation)
3. [Project Objectives](#3-project-objectives)
4. [Existing System vs. Proposed System](#4-existing-system-vs-proposed-system)
5. [Proposed System Capabilities](#5-proposed-system-capabilities)
6. [System Architecture & Dataflow](#6-system-architecture--dataflow)
7. [Comprehensive Technology Stack](#7-comprehensive-technology-stack)
8. [Project Folder & Package Structure](#8-project-folder--package-structure)
9. [Dataset Information & Preprocessing (NASA PROMISE KC1)](#9-dataset-information--preprocessing-nasa-promise-kc1)
10. [Algorithm Explanations & Theoretical Foundation](#10-algorithm-explanations--theoretical-foundation)
11. [Machine Learning Pipeline & Empirical Benchmark Results](#11-machine-learning-pipeline--empirical-benchmark-results)
12. [Explainable AI (SHAP) Interpretation Engine](#12-explainable-ai-shap-interpretation-engine)
13. [Installation & Windows 11 Setup Instructions](#13-installation--windows-11-setup-instructions)
14. [Execution Commands & User Guide](#14-execution-commands--user-guide)
15. [Sample Python Benchmark Scripts](#15-sample-python-benchmark-scripts)
16. [Comprehensive Verification & Testing Suite](#16-comprehensive-verification--testing-suite)
17. [Known Limitations & Ethical Disclaimers](#17-known-limitations--ethical-disclaimers)
18. [Future Scope & Planned Research Extensions](#18-future-scope--planned-research-extensions)
19. [License & Academic Acknowledgments](#19-license--academic-acknowledgments)

---

## 1. Project Abstract

Modern software engineering organizations operate within continuously expanding source codebases characterized by complex function hierarchies, non-trivial control-flow logic, deeply nested branching, and extensive API dependencies. While traditional static analysis linters (e.g., Pylint, Flake8, Ruff) provide deterministic rule-based checks for stylistic infractions and syntax anomalies, they lack the empirical capability to evaluate software defect susceptibility based on historical defect patterns. Conversely, manual peer review remains cognitively intensive, error-prone, and bottlenecked by human bandwidth.

This project delivers the design, empirical development, and implementation of the **AI-Based Code Complexity & Bug Risk Predictor**, an intelligent, hybrid software engineering analysis system. The platform integrates:
1. **Abstract Syntax Tree (AST)** structural parsing using Python's native compilation module to perform safe, non-executing static code introspection.
2. **Quantitative Software Engineering Metrics Computation**, synthesizing McCabe's Cyclomatic Complexity, Maximum Nesting Depth, argument counts, return counts, and Halstead Software Science metrics (Volume, Difficulty, Effort, Programming Time, and Estimated Defects).
3. **Static Rule-Based Anti-Pattern Detection** identifying hazardous programming patterns such as mutable default arguments, bare exception handlers, and non-idiomatic singleton comparisons.
4. **Supervised Machine Learning Defect Prediction** trained, cross-validated, and benchmarked on verified historical defect records from the **NASA PROMISE KC1** repository. Four algorithms were evaluated: Logistic Regression (baseline), Decision Tree, Random Forest (primary model), and Extreme Gradient Boosting (XGBoost).
5. **Explainable Artificial Intelligence (XAI)** utilizing SHAP (SHapley Additive exPlanations) to decompose both global feature importances and local, function-specific predictive drivers into human-interpretable natural language narratives and visual attribution charts.
6. **Publication-Grade Reporting**, delivering automated PDF technical reports (via ReportLab) and raw CSV metric exports alongside an interactive, professional Streamlit web dashboard.

---

## 2. Problem Statement & Research Motivation

### 2.1 The Software Complexity Crisis
Software systems undergo continuous iteration under aggressive delivery schedules. Complexity compounds over time, resulting in:
- Excessively elongated routines (high Lines of Code / LOC).
- Entangled branching and conditional logic (elevated McCabe Cyclomatic Complexity).
- Deep control flow hierarchies (high nesting depths).
- Bloated parameter signatures and scattered return pathways.

These symptoms severely degrade code readability, increase cognitive fatigue during code reviews, and statistically elevate the likelihood of defect injection.

### 2.2 Challenges in Current Industry Practices
- **Time-Consuming Manual Review:** Reviewing large repositories line-by-line is infeasible and does not scale with modern continuous integration (CI) release frequencies.
- **Subjectivity & Fatigue:** Manual review thoroughness fluctuates heavily between individual engineers and team seniors.
- **Linter Limitations:** Traditional linters check syntactic conventions (PEP-8 compliance, whitespace, unused imports), but do not predict the likelihood of an active defect based on historical post-release defect data.
- **Lack of Quantitative Risk Assessment:** Developers lack empirical probability indicators showing which functions deserve prioritized unit testing.
- **Black-Box AI Skepticism:** Uninterpretable neural networks that classify code without explanation fail to earn developer trust.

---

## 3. Project Objectives

### 3.1 Primary Objectives
1. **Safe AST Code Parser:** Develop an AST-based parser that decomposes Python source code without ever executing untrusted user input.
2. **Multi-Faceted Metric Extractor:** Compute 10+ structural and Halstead complexity metrics per function (LOC, Cyclomatic Complexity, Nesting Depth, Parameter Count, Return Count, Loop Count, Conditional Count, Call Count, Exception Count, and Halstead Volume/Difficulty/Effort).
3. **Supervised ML Defect Pipeline:** Train, cross-validate, and benchmark models on legitimate NASA PROMISE historical defect datasets with proper class imbalance handling and leakage prevention.
4. **Explainable AI (SHAP):** Provide global feature importance and local, function-level feature attributions with natural language narratives.
5. **Interactive Dashboard:** Build a responsive Streamlit application featuring 8 analytical pages with modern dark developer aesthetics.
6. **Rule-Based Recommendations:** Generate prioritized, actionable refactoring guidance tied to observed metrics (guard clauses, SRP decomposition, parameter dataclasses).
7. **Publication-Grade Reports:** Implement PDF report generation (via ReportLab Platypus) and CSV data exports.

### 3.2 Secondary Objectives
1. **SQLite History Database:** Track historical analysis metadata, function counts, and risk distributions with user-managed history clearing.
2. **Configurable Risk Thresholds:** Provide adjustable probability bounds for Low ($< 30\%$), Medium ($30\% - 70\%$), and High ($> 70\%$) risk tiers.
3. **Graceful Error Handling:** Validate input syntax, file sizes ($\le 2$ MB), file lines ($\le 5,000$), and encodings without crashing.
4. **Comprehensive Test Suite:** Build automated `pytest` test cases covering all edge cases, visitors, ML inference, and PDF exports.

---

## 4. Existing System vs. Proposed System

| Dimension | Existing Linters (Pylint, Flake8) | Black-Box Deep Learning | **Proposed System (Code Risk Predictor)** |
|:---|:---|:---|:---|
| **Underlying Approach** | Deterministic syntax rules | Opaque token/graph embeddings | **Hybrid: AST + Metrics + ML + XAI** |
| **Defect Probability** | ❌ None (binary rule triggers) | Uncalibrated classification | **✅ Calibrated posterior probability $\hat{P} \in [0.0, 1.0]$** |
| **Historical Data** | ❌ None | Ad-hoc web scrapes | **✅ Legitimate NASA PROMISE KC1 repository** |
| **Explainability** | Line-based warning | ❌ Uninterpretable attention | **✅ SHAP local/global attribution + narratives** |
| **Remediation Guidance** | Style-only fixes | ❌ None | **✅ Metric-specific refactoring advice** |
| **Deliverables** | Terminal text output | CLI log | **✅ Interactive UI + Downloadable PDF / CSV** |
| **Code Execution Safety**| Non-executing | Non-executing | **✅ Strictly non-executing AST compilation** |

---

## 5. Proposed System Capabilities

1. **Automated AST Code Parsing (`modules/code_parser.py`):** Uses Python's native `ast.parse()` to inspect source code without execution. Isolates top-level functions, class methods, and nested functions with independent analytical contexts.
2. **Feature Extraction Engine (`modules/feature_extractor.py`):** Computes McCabe Cyclomatic Complexity ($v(G)$), Maximum Nesting Depth, Lines of Code, and complete Halstead Software Science metrics.
3. **Static Code Analyzer (`modules/static_analyzer.py`):** Integrates Ruff CLI and an autonomous AST linter detecting mutable default arguments (`W0102`), bare `except:` clauses (`W0702`), and non-idiomatic `== None` checks (`E711`).
4. **Machine Learning Predictor (`modules/defect_predictor.py`):** Maps extracted function metrics into trained feature spaces to estimate defect probabilities.
5. **Explainable AI Engine (`modules/explainability.py`):** Applies SHAP `TreeExplainer` to quantify positive risk drivers and negative moderating factors with automated natural language generation.
6. **Prioritized Recommendation Engine (`modules/recommendation_engine.py`):** Ranks refactoring advice by severity (*Critical, High, Warning, Medium, Low, Convention*).
7. **Report Generator (`modules/report_generator.py`):** Builds formatted multi-page PDF documents and raw CSV metric files.
8. **Analysis History Database (`modules/history_db.py`):** Persists session metadata to SQLite without permanently retaining sensitive source code.

---

## 6. System Architecture & Dataflow

```text
USER (Browser / Developer)
        │
        ▼
STREAMLIT WEB APPLICATION (8-Page Multi-Page Architecture)
        │
        ▼
SOURCE CODE INPUT (File Upload / Direct Code Editor / Benchmark Presets)
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

## 7. Comprehensive Technology Stack

| Layer | Component / Tool | Version / Specification | Role in System |
|:---|:---|:---|:---|
| **Core Runtime** | Python | 3.11.9 (64-bit) | Base programming language and execution environment |
| **AST Parsing** | Python `ast` module | Built-in | Safe, non-executing AST generation and syntax validation |
| **Complexity Metrics** | `radon` | 6.0.1 | Industry-standard Cyclomatic Complexity calculation |
| **Static Linter** | `ruff` | 0.17.6 | Isolated static code linting and code smell detection |
| **Machine Learning** | `scikit-learn` | 1.9.1 | Supervised classification, preprocessing, and model evaluation |
| **Gradient Boosting** | `xgboost` | 3.2.0 | Extreme Gradient Boosting benchmark model |
| **Explainable AI** | `shap` | 0.51.0 | SHapley Additive exPlanations (TreeExplainer) |
| **Data Processing** | `pandas` & `numpy` | Pandas 3.0.5, NumPy 2.4.6 | Tabular feature manipulation and vector math |
| **Model Persistence** | `joblib` | 1.6.0 | Serialization of trained models, scalers, and schemas |
| **Web Dashboard** | `streamlit` | 1.67.0 | Multi-page reactive web UI framework |
| **Data Graphics** | `plotly` | 7.1.0 | Interactive bar charts, scatter plots, donuts, and heatmaps |
| **PDF Reporting** | `reportlab` | 5.1.0 | Multi-page Platypus flowable PDF document generation |
| **Database** | `sqlite3` | Built-in | Local analysis history and metadata persistence |
| **Testing** | `pytest` | 9.2.0 | Automated unit and integration testing framework |

---

## 8. Project Folder & Package Structure

```text
mini project/
│
├── app.py                             # Main Streamlit dashboard entry point & routing
├── requirements.txt                   # Pinned project dependencies
├── README.md                          # Full technical & academic documentation
├── .gitignore                         # Git exclusion rules (caches, venv, temporary files)
├── download_and_train.py              # NASA dataset downloader & ML model trainer script
│
├── .streamlit/
│   └── config.toml                    # Streamlit dark developer theme configuration
│
├── config/
│   └── settings.py                    # System paths, threshold defaults, heuristic constants
│
├── modules/
│   ├── __init__.py
│   ├── code_parser.py                 # AST parser, function visitor, nesting depth visitor
│   ├── feature_extractor.py           # LOC, McCabe CC (Radon/AST), Halstead metrics
│   ├── static_analyzer.py             # Ruff CLI integration & built-in AST code smell linter
│   ├── data_loader.py                 # NASA PROMISE dataset loader & preprocessor
│   ├── model_trainer.py               # Model training (LR, Tree, Random Forest, XGBoost)
│   ├── model_evaluator.py             # Evaluation metrics, confusion matrix, ROC/PR curves
│   ├── defect_predictor.py            # Inference engine, feature alignment, risk banding
│   ├── explainability.py              # SHAP TreeExplainer, local/global attributions
│   ├── recommendation_engine.py       # Rule-based prioritized refactoring advice
│   ├── report_generator.py            # ReportLab PDF compilation & CSV exporter
│   ├── history_db.py                  # SQLite analysis history tracking
│   └── ui_theme.py                    # Unified dark UI CSS tokens, cards, and chart layouts
│
├── pages/
│   ├── 1_Home.py                      # Executive metrics, session overview, maintainability gauge
│   ├── 2_Code_Upload.py               # File upload, code editor, sample loaders, execution
│   ├── 3_Complexity_Analysis.py       # Function metrics table, Halstead metrics, Plotly charts
│   ├── 4_Static_Analysis.py           # Lint warnings, severity filters, code smell details
│   ├── 5_Risk_Prediction.py           # Defect probabilities, risk bands, high-risk callouts
│   ├── 6_Explainable_AI.py            # Global SHAP bar chart, local waterfall, narratives
│   ├── 7_Model_Performance.py         # Dataset metadata, model benchmarks, CM & ROC curves
│   └── 8_Reports.py                   # PDF/CSV downloads, recommendations, SQLite history
│
├── dataset/
│   ├── README.md                      # NASA PROMISE repository schema & documentation
│   └── kc1.csv                        # NASA KC1 verified dataset (1,212 deduplicated records)
│
├── models/
│   ├── README.md                      # Model persistence details
│   ├── defect_predictor_rf.joblib     # Persisted Random Forest classifier
│   ├── feature_scaler.joblib          # Persisted StandardScaler
│   ├── feature_columns.joblib         # Persisted feature column schema
│   └── model_evaluation_metrics.json  # Persisted empirical benchmark metrics
│
├── database/
│   ├── README.md                      # SQLite schema and privacy guidelines
│   └── analysis_history.db            # SQLite database file
│
├── sample_code/
│   ├── simple_example.py              # Low complexity sample (PEP-8 compliant)
│   ├── complex_example.py             # High cyclomatic complexity & parameter sample
│   └── nested_conditions.py           # Deep nesting & anti-pattern sample
│
├── tests/
│   ├── test_parser.py                 # AST parser unit tests (7 tests)
│   ├── test_feature_extractor.py      # Metrics & static analysis unit tests (4 tests)
│   ├── test_prediction.py             # Predictor, missing data, SHAP test suite (4 tests)
│   ├── test_reports.py                # PDF, CSV, SQLite test suite (3 tests)
│   └── test_e2e_pipeline.py           # Full end-to-end integration test (1 test)
│
├── docs/
│   ├── project_abstract.md            # Formal academic abstract
│   ├── problem_statement.md           # Problem statement & research motivation
│   ├── methodology.md                 # Architectural pipeline & step-by-step methodology
│   ├── algorithm_explanation.md       # Mathematical derivations (McCabe, Halstead, ML, SHAP)
│   ├── testing_documentation.md       # Test matrix & pytest verification outputs
│   ├── future_scope.md                # Planned future research directions
│   └── comprehensive_project_documentation.md # This unified master document
│
└── output/
    └── reports/                       # Local PDF report export directory
```

---

## 9. Dataset Information & Preprocessing (NASA PROMISE KC1)

### 9.1 Dataset Provenance & Characteristics
- **Dataset:** **NASA KC1** from the NASA Metrics Data Program (MDP) / PROMISE Repository (`dataset/kc1.csv`).
- **Domain:** Production ground control software written in C/C++ for a satellite reception ground station.
- **Raw Records:** 2,109 subroutine records.
- **Deduplicated Records:** 1,212 unique instances (duplicates removed to prevent validation leakage).
- **Target Variable:** `defects` (`0 = Clean`, `1 = Defective`).
- **Class Distribution:** 315 Defective records (26.0%), 897 Clean records (74.0%).
- **Class Imbalance Ratio:** ~2.85 : 1 (Clean to Defective).

### 9.2 The 21 Feature Attributes
1. `loc`: Lines of code (McCabe)
2. `v(g)`: Cyclomatic complexity (McCabe)
3. `ev(g)`: Essential complexity (McCabe)
4. `iv(g)`: Design complexity (McCabe)
5. `n`: Halstead total operators + operands
6. `v`: Halstead volume
7. `l`: Halstead program length
8. `d`: Halstead difficulty
9. `i`: Halstead intelligence
10. `e`: Halstead effort
11. `b`: Halstead error estimate
12. `t`: Halstead execution time estimator
13. `lOCode`: Count of code lines
14. `lOComment`: Count of comment lines
15. `lOBlank`: Count of blank lines
16. `locCodeAndComment`: Lines containing both code and comments
17. `uniq_Op`: Unique operators count
18. `uniq_Opnd`: Unique operands count
19. `total_Op`: Total operators count
20. `total_Opnd`: Total operands count
21. `branchCount`: Flow graph branch count

### 9.3 Data Preprocessing Protocol
1. **Column Normalization:** Strip whitespace and convert column headers to lowercase.
2. **Standardized Renaming:** Map varied dataset column names to standardized identifiers using `METRIC_RENAME_MAP`.
3. **Numeric Coercion:** Convert all metric columns to float, coercing any corrupt strings or question marks to NaN.
4. **Missing Value Imputation:** Impute missing values using column median values (or 0 if unobserved).
5. **Constant Feature Removal:** Drop columns where variance is zero ($nunique \le 1$).
6. **Deduplication:** Remove identical duplicate rows across $X$ and $y$ combined.
7. **Leakage-Free Splitting:** Perform an 80/20 stratified split. Fit `StandardScaler` strictly on $X_{\text{train}}$ and transform $X_{\text{test}}$.

---

## 10. Algorithm Explanations & Theoretical Foundation

### 10.1 McCabe Cyclomatic Complexity
Formulated by Thomas J. McCabe in 1976, Cyclomatic Complexity ($v(G)$) measures the number of linearly independent paths through a control-flow graph $G = (V, E)$:
$$v(G) = E - V + 2P$$
For a single function routine ($P=1$):
$$v(G) = 1 + \sum \text{Decision Nodes}$$
Where decision nodes include: `if`, `while`, `for`, `async for`, `assert`, `except`, and boolean operators (`and`, `or`).

### 10.2 Halstead Software Science
Maurice Halstead (1977) modeled cognitive programming effort using token frequencies:
- $\eta_1$: Distinct operators
- $\eta_2$: Distinct operands
- $N_1$: Total operators
- $N_2$: Total operands

Derived formulas:
- **Program Vocabulary:** $\eta = \eta_1 + \eta_2$
- **Program Length:** $N = N_1 + N_2$
- **Volume:** $V = N \times \log_2(\eta)$
- **Difficulty:** $D = \frac{\eta_1}{2} \times \frac{N_2}{\eta_2}$
- **Effort:** $E = D \times V$
- **Time to Implement:** $T = \frac{E}{18} \text{ seconds}$
- **Estimated Bugs:** $B = \frac{V}{3000}$

### 10.3 Maximum Control-Flow Nesting Depth
Computed by `CodeNestingVisitor.calculate_max_depth()`:
1. Traverses the function's AST hierarchy recursively.
2. Increments depth upon encountering control-flow nodes (`If`, `For`, `While`, `Try`, `With`).
3. Explicitly skips nested `FunctionDef` and `ClassDef` bodies to prevent double-counting.
4. Returns the maximum depth integer observed.

---

## 11. Machine Learning Pipeline & Empirical Benchmark Results

### 11.1 Benchmark Results (Evaluated on Holdout Test Partition)
All metrics reflect actual, reproducible test evaluation on 243 holdout instances:

| Model Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | 5-Fold Stratified CV F1 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Logistic Regression (Baseline)** | 60.91% | 32.61% | 47.62% | 38.71% | 0.6079 | 49.38% |
| **Decision Tree** | 58.44% | 27.38% | 36.51% | 31.29% | 0.5135 | 42.35% |
| **Random Forest (Primary Model)** | **67.90%** | **40.26%** | **49.21%** | **44.29%** | **0.6288** | **48.33%** |
| **XGBoost Classifier** | 67.08% | 36.92% | 38.10% | 37.50% | 0.6106 | 46.62% |

### 11.2 Primary Model Diagnostics (Random Forest)
- **True Negatives (TN):** 134 (Clean subroutines correctly identified)
- **False Positives (FP):** 46 (Clean subroutines flagged as defect-prone)
- **False Negatives (FN):** 32 (Defective subroutines missed)
- **True Positives (TP):** 31 (Defective subroutines correctly flagged)

### 11.3 Top 5 Predictive Features (Gini Importance)
1. `h_difficulty`: $0.0854$ (Halstead Difficulty)
2. `h_intelligence`: $0.0783$ (Halstead Intelligence)
3. `h_volume`: $0.0757$ (Halstead Volume)
4. `h_effort`: $0.0670$ (Halstead Effort)
5. `h_length`: $0.0659$ (Halstead Program Length)

---

## 12. Explainable AI (SHAP) Interpretation Engine

Based on cooperative game theory, SHAP decomposes model predictions into additive feature contributions:
$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i(x)$$
Where $\phi_0 = E[f(x)]$ is the base expectation and $\phi_i$ is the marginal contribution of metric feature $i$.

### Function-Level Attribution Output Example
For function `process_complex_transactions`:
- **Estimated Defect Probability:** $82.4\%$ (High Risk)
- **Base Expected Value:** $0.50$
- **Positive Drivers (Risk Elevators):**
  - `cyclomatic_complexity` ($CC=24$): $+0.31$
  - `max_nesting_depth` ($depth=5$): $+0.18$
  - `total_op` ($total=78$): $+0.12$
- **Negative Drivers (Risk Moderators):**
  - `param_count` ($params=9$): $+0.08$
- **Generated Narrative:**
  > *"Function 'process_complex_transactions' has an estimated defect probability of 82.4%. Elevated risk is primarily driven by cyclomatic_complexity (24, contribution +0.31) and max_nesting_depth (5, contribution +0.18)."*

---

## 13. Installation & Windows 11 Setup Instructions

```powershell
# 1. Navigate to project root directory
cd "c:\Users\nalam\OneDrive\Desktop\mini project"

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install locked dependencies
pip install -r requirements.txt
```

---

## 14. Execution Commands & User Guide

```powershell
# Launch the Streamlit Multi-Page Web Dashboard
streamlit run app.py

# Execute the Full 19-Test Automated Verification Suite
python -m pytest tests/ -v

# Re-Train Machine Learning Models on NASA Dataset (Optional)
python download_and_train.py
```

---

## 15. Sample Python Benchmark Scripts

The project includes three realistic benchmark scripts located in `sample_code/`:
1. **`simple_example.py`:** Clean arithmetic utilities with minimal branching, high cohesion, low CC ($CC \le 2$), demonstrating **Low Risk** evaluation.
2. **`complex_example.py`:** A 9-parameter financial transaction engine with multiple loops and condition branches ($CC = 24$), demonstrating **High Risk** evaluation.
3. **`nested_conditions.py`:** Deeply nested control flow ($depth = 5$) containing anti-patterns like mutable default arguments (`def f(cache=[])`) and bare `except:` clauses, demonstrating **Static Analysis & High Complexity** warnings.

---

## 16. Comprehensive Verification & Testing Suite

### 16.1 Test Suite Summary
Command executed:
```powershell
python -m pytest tests/ -v
```
Result: **19 passed in 8.61s (100% passing rate)**.

### 16.2 Full Test Matrix

| Test ID | Module | Test Function | Test Objective & Verification | Result |
|:---:|:---|:---|:---|:---:|
| TC-01 | `code_parser` | `test_valid_python_file` | Verifies clean AST parsing, line tracking, and function isolation | **PASSED** |
| TC-02 | `code_parser` | `test_empty_python_file` | Verifies graceful error handling for empty input strings | **PASSED** |
| TC-03 | `code_parser` | `test_invalid_syntax` | Verifies line/column reporting on malformed Python syntax | **PASSED** |
| TC-04 | `code_parser` | `test_nested_functions` | Verifies inner/outer function isolation without double counting | **PASSED** |
| TC-05 | `code_parser` | `test_class_methods` | Verifies method detection, class context, and `is_method` flag | **PASSED** |
| TC-06 | `code_parser` | `test_deeply_nested_conditions` | Verifies accurate control flow depth calculation ($depth \ge 4$) | **PASSED** |
| TC-07 | `code_parser` | `test_large_source_file` | Verifies parsing performance over 50 programmatic routines | **PASSED** |
| TC-08 | `feature_extractor` | `test_cyclomatic_complexity_ast` | Verifies AST McCabe CC decision-node calculations ($CC=5$) | **PASSED** |
| TC-09 | `feature_extractor` | `test_halstead_metrics_extraction` | Verifies Halstead Volume, Difficulty, and Effort calculations | **PASSED** |
| TC-10 | `feature_extractor` | `test_feature_extractor_dataframe` | Verifies conversion of AST ParseResult into Pandas DataFrame | **PASSED** |
| TC-11 | `static_analyzer` | `test_static_analyzer_catches_anti_patterns` | Detects mutable defaults (W0102), bare except (W0702), and `== None` (E711) | **PASSED** |
| TC-12 | `data_loader` | `test_missing_dataset_handling` | Verifies explicit `FileNotFoundError` when invalid path is specified | **PASSED** |
| TC-13 | `defect_predictor` | `test_predictor_handles_empty_dataframe` | Verifies predictor returns empty list without throwing exceptions | **PASSED** |
| TC-14 | `defect_predictor` | `test_trained_model_prediction` | Verifies calibrated probability generation and risk tiering $[0, 1]$ | **PASSED** |
| TC-15 | `explainability` | `test_explainability_local_and_global` | Verifies SHAP global ranking and local narrative generation | **PASSED** |
| TC-16 | `report_generator` | `test_csv_export` | Verifies CSV export string creation with merged predictions | **PASSED** |
| TC-17 | `report_generator` | `test_pdf_generation` | Verifies ReportLab Platypus compilation generating valid PDF bytes | **PASSED** |
| TC-18 | `history_db` | `test_sqlite_history_lifecycle` | Verifies SQLite insert, query, aggregate summary, and clear records | **PASSED** |
| TC-19 | `e2e_pipeline` | `test_full_pipeline_complex_example` | Verifies complete end-to-end integration: AST $\rightarrow$ Metrics $\rightarrow$ ML $\rightarrow$ XAI $\rightarrow$ PDF $\rightarrow$ DB | **PASSED** |

---

## 17. Known Limitations & Ethical Disclaimers

1. **Complexity $\ne$ Bug:** High Cyclomatic Complexity ($CC > 15$) indicates testability friction and cognitive load, but does **not** guarantee an active runtime defect.
2. **Statistical Association:** Defect probabilities reflect historical correlations learned from NASA aerospace subroutines and serve as an **advisory decision-support tool**, not a formal correctness proof.
3. **Cross-Language Transfer:** The AST parser inspects Python code natively, while empirical defect weights originate from C/C++ aerospace modules (NASA KC1) serving as an established software engineering benchmark.
4. **Single-Routine Focus:** Metrics are computed per function; inter-procedural dataflow across multiple files is not currently modeled.

---

## 18. Future Scope & Planned Research Extensions

1. **Multi-Language Tree-Sitter Parsers:** Extend structural parsing beyond Python to Java, C/C++, Go, TypeScript, and Rust.
2. **Code Graph Neural Networks (Code-GNN):** Integrate Control Flow Graphs (CFG) and Program Dependence Graphs (PDG) with Graph Convolutional Networks (GCN) to complement tabular metrics with graph semantics.
3. **Automated LLM Refactoring:** Connect local open-weights code models (e.g., CodeGemma, StarCoder) to generate automated pull requests demonstrating guard-clause refactorings.
4. **CI/CD Quality Gates:** Package the engine into a GitHub Action / GitLab CI pipeline runner that blocks pull-request merges if a commit introduces functions with $P(\text{Defect}) > 0.80$ and $CC > 15$.
5. **Git Churn & Longitudinal Tracking:** Integrate PyDriller to analyze commit history churn (revisions, lines added/deleted, developer count) alongside static code metrics.

---

## 19. License & Academic Acknowledgments

### 19.1 Academic License
This project is released under the **MIT Academic License** for educational, academic research, and non-commercial evaluation purposes.

### 19.2 Acknowledgments
The author gratefully acknowledges:
- The **NASA Metrics Data Program (MDP)** and the **PROMISE Software Engineering Repository** for providing open historical defect benchmark data.
- The **Scikit-Learn**, **XGBoost**, and **SHAP** developer communities for providing machine learning and model explainability frameworks.
- The **Streamlit** and **Plotly** teams for reactive web application and interactive charting infrastructure.
- The **ReportLab** team for multi-page PDF compilation technology.
- Thomas J. McCabe and Maurice H. Halstead for foundational software complexity measurement theories.

---
*=== End of Comprehensive Technical & Academic Documentation ===*
