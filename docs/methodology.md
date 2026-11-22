# System Architecture & Implementation Methodology

## 1. Architectural Philosophy
The application adheres to clean separation of concerns, decoupling user interface presentation from core parsing, metric calculation, machine learning inference, and report compilation.

```
+─────────────────────────────────────────────────────────────────────────+
|                           STREAMLIT WEB DASHBOARD                       |
|   (Home, Code Upload, Complexity, Static, ML Risk, XAI, Benchmarks, PDF)  |
+─────────────────────────────────────────────────────────────────────────+
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        ▼                                                       ▼
+───────────────────────────────+               +───────────────────────────────+
|     modules/code_parser.py    |               |   modules/static_analyzer.py  |
|  - ast.parse() Introspection  |               |  - Ruff Integration (CLI/JSON)|
|  - Function Node Isolation    |               |  - AST Anti-Pattern Linter    |
|  - Nesting Depth Visitor      |               |  - Mutable Defaults & Bare Try|
+───────────────────────────────+               +───────────────────────────────+
        │                                                       │
        ▼                                                       │
+───────────────────────────────+                               │
|  modules/feature_extractor.py |                               │
|  - McCabe CC (Radon / AST)    |                               │
|  - Halstead Software Science  |                               │
|  - LOC, Params, Returns, Calls|                               │
+───────────────────────────────+                               │
        │                                                       │
        ▼                                                       │
+───────────────────────────────+                               │
|   modules/defect_predictor.py |                               │
|  - Aligned Feature Mapping    |                               │
|  - StandardScaler Inference   |                               │
|  - Calibrated Probability P(Y)|                               │
|  - Risk Band Categorization   |                               │
+───────────────────────────────+                               │
        │                       │                               │
        ▼                       ▼                               │
+─────────────────────+ +─────────────────────────+             │
| modules/            | | modules/                |             │
| explainability.py   | | recommendation_engine.py| ◄───────────┘
| - SHAP TreeExplainer| | - Prioritized Refactoring|
| - Local Attribution | | - Severity Sorting     |
+─────────────────────+ +─────────────────────────+
        │                               │
        └───────────────┬───────────────┘
                        ▼
+─────────────────────────────────────────────────────────────────────────+
|                       modules/report_generator.py                       |
|   - Multi-Page PDF Document Compilation via ReportLab Platypus Engine   |
|   - Structured Raw CSV Data Generation                                  |
|   - SQLite Historical Run Persister (modules/history_db.py)             |
+─────────────────────────────────────────────────────────────────────────+
```

## 2. Methodology Step-by-Step

### Phase 1: Ingestion & Safe Parsing
- Source code is supplied via `.py` file upload or multi-line text input.
- File sizes are strictly bounded ($\le 2$ MB).
- Syntax parsing is performed exclusively via Python's native `ast.parse()`. No user-submitted code is ever executed via `eval()`, `exec()`, or subprocess shells.
- Syntax errors are caught gracefully, returning precise line numbers, columns, and compiler messages.

### Phase 2: AST Metric Extraction
- An AST visitor isolates individual function boundaries (`FunctionDef`, `AsyncFunctionDef`).
- Inner/nested functions are parsed into their own discrete analytical entities, preventing double-counting within the enclosing parent.
- Enclosing class context and method classifications (`is_method`) are recorded.
- McCabe Cyclomatic Complexity is computed both via Radon and an AST branch decision visitor:
  $$CC = 1 + \sum \text{Decision Nodes}$$
- Halstead metrics are computed by tokenizing operators and operands.

### Phase 3: Static Analysis & Anti-Pattern Detection
- The codebase executes Ruff CLI with JSON output when present, backed by an autonomous AST visitor.
- Detects unused imports, mutable default arguments, bare `except:` clauses, non-idiomatic `== None` checks, missing docstrings, and long function warnings.

### Phase 4: Machine Learning Inference
- Pre-trained models (fitted strictly with standard scaling) transform extracted metrics into probabilistic defect estimates:
  $$\hat{P}(\text{Defect} \mid X) \in [0.0, 1.0]$$
- Configurable risk thresholds assign functions to Low Risk ($< 30\%$), Medium Risk ($30\% - 70\%$), or High Risk ($> 70\%$).

### Phase 5: Explainable AI (SHAP)
- A TreeExplainer computes exact additive Shapley values for tree ensembles:
  $$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i$$
- Identifies the top positive contributors (increasing risk) and top negative contributors (moderating risk).
- Formulates a natural language narrative explaining why the model assigned a particular risk score.

### Phase 6: Reporting and Persistence
- Results are compiled into a formatted PDF using ReportLab Platypus flowables.
- Run summaries are stored in SQLite (`database/analysis_history.db`) without storing source code permanently.
