# Future Scope & Research Extensions

## 1. Multi-Language AST Parsing
- Current implementation natively supports Python source code via the `ast` module.
- Future versions can integrate Tree-Sitter or ANTLR4 parsers to extend function-level metric extraction to C/C++, Java, JavaScript, TypeScript, and Rust.

## 2. Advanced Graph Neural Networks (Code-GNN)
- While tabular complexity metrics capture macro-level cognitive and architectural strain, Program Dependence Graphs (PDG) and Control Flow Graphs (CFG) capture exact data flow semantics.
- Future work involves fusing Graph Convolutional Networks (GCN) or Tree-LSTMs over AST nodes alongside McCabe and Halstead features.

## 3. Automated Refactoring & LLM Repair Integration
- Currently, the recommendation engine delivers rule-based refactoring guidance.
- Future extensions could integrate local code generation models (e.g., StarCoder, CodeGemma) to draft automated pull requests demonstrating how to decompose high-risk functions with guard clauses and helper abstractions.

## 4. Continuous Integration / Continuous Deployment (CI/CD) Tooling
- Packaging the analysis engine into a standalone GitHub Action or GitLab CI pipeline runner that blocks merges if a commit introduces functions exceeding critical risk thresholds ($P(\text{Defect}) > 0.80$ and $CC > 15$).

## 5. Longitudinal Defect Tracking Across Git Commits
- Integration with Git commit histories (using PyDriller) to compute process and churn metrics (number of past revisions, author counts, code churn lines) to augment static code complexity metrics with developer velocity signals.
