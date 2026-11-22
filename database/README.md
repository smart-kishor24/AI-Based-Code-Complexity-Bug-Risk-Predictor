# SQLite Analysis History Database

This directory hosts the SQLite database (`analysis_history.db`) for tracking past codebase inspections.

## Schema
Table: `analysis_history`
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `filename` (TEXT)
- `timestamp` (TEXT)
- `function_count` (INTEGER)
- `low_risk_count` (INTEGER)
- `medium_risk_count` (INTEGER)
- `high_risk_count` (INTEGER)
- `avg_cyclomatic_complexity` (REAL)
- `total_loc` (INTEGER)
- `static_issues_count` (INTEGER)
- `summary` (TEXT)

## Privacy & Data Retention
User-submitted source code is parsed in memory and is **never** permanently stored in the database. Only metadata, metric aggregations, and summaries are preserved.
A "Clear Analysis History" button is provided directly in the Reports tab.
