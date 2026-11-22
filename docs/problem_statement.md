# Problem Statement & Research Motivation

## 1. Context and Problem Definition
In contemporary software development, codebases undergo rapid iterative changes under aggressive delivery schedules. Software complexity naturally compounds over time, culminating in:
- Excessively elongated routines (high Lines of Code / LOC).
- Entangled branching and conditional logic (elevated McCabe Cyclomatic Complexity).
- Deep control flow hierarchies (high nesting depths).
- Bloated parameter signatures and scattered return pathways.

These architectural symptoms severely degrade code readability, increase cognitive fatigue during code reviews, and statistically elevate the likelihood of defect injection.

## 2. Limitations of Existing Solutions

### A. Manual Code Review
- **Cognitive Bottleneck:** Reviewers struggle to maintain complete mental models of functions exceeding 50 lines or cyclomatic complexities above 10.
- **Inconsistency:** Review rigor fluctuates between engineers and is subject to fatigue.
- **Scalability Deficit:** Not feasible for massive legacy refactorings or high-velocity continuous integration pipelines.

### B. Traditional Static Linters (Pylint, Flake8, Ruff)
- **Heuristic-Bound:** Traditional linters check predefined syntactic conventions (PEP-8 compliance, whitespace, unused imports).
- **Absence of Historical Learning:** They do not incorporate historical empirical data regarding which metric combinations have historically correlated with delivered post-release defects.
- **False Equivalence:** A formatting warning is often presented alongside severe architectural smells without probabilistic risk differentiation.

### C. Black-Box Neural Approaches
- **Opaque Reasoning:** Deep learning models operating over raw tokens or graph representations often operate as uninterpretable black boxes.
- **Lack of Developer Trust:** Software engineers reject automated tooling that flags code as "risky" without actionable explanations or remediation guidance.

## 3. Project Objectives
The objective of this academic mini-project is to bridge the gap between static analysis and empirical software engineering by engineering an end-to-end system that:
1. Safely accepts and parses Python source code without ever executing untrusted user input.
2. Extracts comprehensive AST-derived control-flow and Halstead complexity metrics at function granularity.
3. Incorporates static code smells and anti-pattern warnings in parallel.
4. Trains and evaluates multiple supervised machine learning models on legitimate historical NASA PROMISE defect records.
5. Employs Explainable AI (SHAP) to attribute defect risk to specific metric contributors.
6. Categorizes analyzed functions into configurable risk bands (Low, Medium, High).
7. Synthesizes rule-based, actionable engineering recommendations.
8. Generates professional PDF technical reports and CSV data exports.
