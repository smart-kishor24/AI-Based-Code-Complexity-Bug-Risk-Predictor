# NASA PROMISE Defect Prediction Dataset Repository

This directory contains legitimate software defect prediction datasets sourced from the NASA Metrics Data Program (MDP) / PROMISE Software Engineering Repository.

## Datasets

### 1. KC1 (`kc1.csv`)
- **Origin:** NASA Metrics Data Program (MDP)
- **Domain:** Ground control software written in C/C++ for a satellite reception ground station.
- **Instances:** 2,109 raw subroutine records (1,212 unique instances after deduplication).
- **Target Variable:** `defects` (Boolean: `true` / `false`, mapped to `1` / `0`).
- **Defect Distribution:** 315 Defective records (26.0%), 897 Clean records (74.0%).
- **Imbalance Ratio:** ~2.85:1 (Clean to Defective).

### 2. Feature Schema (21 Software Engineering Metrics)
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

## Granularity and Methodological Notice
The NASA PROMISE datasets describe function- and subroutine-level modules extracted from historical C/C++ aerospace systems. While these metrics correspond structurally to Python function AST features, defect probabilities reflect statistical correlations with historical defect patterns rather than executable guarantees of a bug.
