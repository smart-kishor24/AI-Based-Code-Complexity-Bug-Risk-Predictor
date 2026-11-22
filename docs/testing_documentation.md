# Testing Documentation & Verification Suite

## 1. Overview
Quality assurance was conducted using `pytest` covering syntax boundaries, AST visitors, feature scaling, model inference, XAI drivers, PDF report generation, and SQLite database lifecycles.

## 2. Test Suite Execution Summary

Command executed:
```powershell
python -m pytest tests/ -v
```

Execution Result:
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\nalam\OneDrive\Desktop\mini project
collected 18 items

tests/test_feature_extractor.py::test_cyclomatic_complexity_ast PASSED   [  5%]
tests/test_feature_extractor.py::test_halstead_metrics_extraction PASSED [ 11%]
tests/test_feature_extractor.py::test_feature_extractor_dataframe PASSED [ 16%]
tests/test_feature_extractor.py::test_static_analyzer_catches_anti_patterns PASSED [ 22%]
tests/test_parser.py::test_valid_python_file PASSED                      [ 27%]
tests/test_parser.py::test_empty_python_file PASSED                      [ 33%]
tests/test_parser.py::test_invalid_syntax PASSED                         [ 38%]
tests/test_parser.py::test_nested_functions PASSED                       [ 44%]
tests/test_parser.py::test_class_methods PASSED                          [ 50%]
tests/test_parser.py::test_deeply_nested_conditions PASSED               [ 55%]
tests/test_parser.py::test_large_source_file PASSED                      [ 61%]
tests/test_prediction.py::test_missing_dataset_handling PASSED           [ 66%]
tests/test_prediction.py::test_predictor_handles_empty_dataframe PASSED  [ 72%]
tests/test_prediction.py::test_trained_model_prediction PASSED           [ 77%]
tests/test_prediction.py::test_explainability_local_and_global PASSED    [ 83%]
tests/test_reports.py::test_csv_export PASSED                            [ 88%]
tests/test_reports.py::test_pdf_generation PASSED                        [ 94%]
tests/test_reports.py::test_sqlite_history_lifecycle PASSED              [100%]

======================= 18 passed, 3 warnings in 7.90s ========================
```

---

## 3. Specific Test Case Breakdown

| ID | Module Under Test | Test Description | Input Condition | Expected Result | Status |
|:---|:---|:---|:---|:---|:---|
| TC-01 | `code_parser` | Valid Python File | Standard function with docstring | `is_valid == True`, 1 function extracted | **PASSED** |
| TC-02 | `code_parser` | Empty Input | `""` empty string | `is_valid == False`, error message set | **PASSED** |
| TC-03 | `code_parser` | Syntax Error | Missing parentheses `def foo(:` | Catches `SyntaxError`, logs line number | **PASSED** |
| TC-04 | `code_parser` | Nested Functions | Function defining inner helper | Extracts both, marks `is_nested=True` on inner | **PASSED** |
| TC-05 | `code_parser` | Class Methods | Class with 2 member functions | Marks `is_method=True`, sets `class_name` | **PASSED** |
| TC-06 | `code_parser` | Deep Nesting | 4 nested `if` statements | `max_nesting_depth == 4` | **PASSED** |
| TC-07 | `code_parser` | Large File | 50 programmatic functions | Parses all 50 functions reliably | **PASSED** |
| TC-08 | `feature_extractor` | AST McCabe CC | Function with `if`, `and`, `for`, `elif` | Computes correct CC ($=5$) | **PASSED** |
| TC-09 | `feature_extractor` | Halstead Calculation | Arithmetic token sequence | Returns valid Volume, Difficulty, Effort | **PASSED** |
| TC-10 | `feature_extractor` | DataFrame Pipeline | Multi-function AST ParseResult | Generates structured DataFrame | **PASSED** |
| TC-11 | `static_analyzer` | Anti-Pattern Detection | Mutable default, bare except, `== None` | Flags W0102, W0702, E711 | **PASSED** |
| TC-12 | `data_loader` | Missing Dataset | Non-existent filepath | Raises informative `FileNotFoundError` | **PASSED** |
| TC-13 | `defect_predictor` | Empty Data Input | Empty DataFrame | Returns empty list without throwing | **PASSED** |
| TC-14 | `defect_predictor` | Inference Vector | Low & high complexity function rows | Produces valid defect probabilities $[0, 1]$ | **PASSED** |
| TC-15 | `explainability` | SHAP Global/Local | Trained model + feature row | Produces feature attributions and narrative | **PASSED** |
| TC-16 | `report_generator` | CSV Export | Metrics DataFrame + predictions | Generates valid formatted CSV string | **PASSED** |
| TC-17 | `report_generator` | PDF Generation | Analysis payload | Builds byte stream beginning with `%PDF` | **PASSED** |
| TC-18 | `history_db` | SQLite Lifecycle | Insert, query, summary, clear | Persists records and clears on demand | **PASSED** |
