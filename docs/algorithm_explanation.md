# Algorithm Explanations & Theoretical Foundation

## 1. Software Engineering Complexity Metrics

### A. McCabe Cyclomatic Complexity
Formulated by Thomas J. McCabe in 1976, Cyclomatic Complexity ($v(G)$) measures the number of linearly independent paths through a program's source code. Represented as a directed control flow graph $G = (V, E)$ where $V$ represents basic blocks and $E$ represents control transfers:
$$v(G) = E - V + 2P$$
For a single connected component ($P=1$):
$$v(G) = 1 + \Pi$$
where $\Pi$ denotes the count of binary decision points (`if`, `while`, `for`, `assert`, `except`, `and`, `or`).

### B. Halstead Software Science Metrics
Introduced by Maurice Halstead in 1977, these metrics model cognitive programming effort based on primitive token counts:
- $\eta_1$: Number of distinct operators
- $\eta_2$: Number of distinct operands
- $N_1$: Total number of operators
- $N_2$: Total number of operands

Derived metrics:
- **Program Vocabulary:** $\eta = \eta_1 + \eta_2$
- **Program Length:** $N = N_1 + N_2$
- **Volume:** $V = N \times \log_2(\eta)$
- **Difficulty:** $D = \frac{\eta_1}{2} \times \frac{N_2}{\eta_2}$
- **Effort:** $E = D \times V$
- **Time Required to Code:** $T = \frac{E}{18} \text{ seconds}$
- **Estimated Number of Bugs:** $B = \frac{V}{3000}$

---

## 2. Supervised Classification Algorithms

### A. Logistic Regression (Baseline)
Models the log-odds of a defect as a linear combination of normalized software features:
$$\ln\left(\frac{p}{1-p}\right) = \beta_0 + \sum_{j=1}^{d} \beta_j X_j$$
- Optimization: $L_2$-regularized log-loss.
- Class Imbalance Handling: Balanced class weighting inversely proportional to class frequencies.

### B. Decision Tree Classifier
Non-parametric recursive partitioning algorithm splitting the feature space to minimize Gini Impurity:
$$I_G(t) = 1 - \sum_{i=0}^{1} p_i^2$$
- Constrained with `max_depth=6` and `min_samples_split=10` to mitigate empirical overfitting on defect datasets.

### C. Random Forest Classifier (Primary Model)
An ensemble of $B=120$ bootstrap-aggregated (bagged) de-correlated decision trees:
$$\hat{f}_{\text{rf}}(x) = \frac{1}{B} \sum_{b=1}^{B} f_b(x)$$
- At each split, a random subset of metrics $\sqrt{p}$ is considered.
- Resilient to multicollinearity inherent among software complexity metrics (e.g., strong correlation between LOC, Halstead Volume, and Cyclomatic Complexity).

### D. Extreme Gradient Boosting (XGBoost)
Sequential ensemble minimizing a regularized objective function via second-order Taylor expansion:
$$\mathcal{L}^{(t)} = \sum_{i=1}^{n} \left[ g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)$$
where $g_i$ and $h_i$ are the first and second gradients of the loss function, and $\Omega(f_t) = \gamma T + \frac{1}{2} \lambda \|w\|^2$.

---

## 3. Explainable AI: SHAP (SHapley Additive exPlanations)
Based on cooperative game theory (Lloyd Shapley, 1953), SHAP attributes the deviation of a model prediction from the base expected value to individual metric features:
$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$
- Properties:
  1. **Local Accuracy (Additivity):** $\sum_{i=0}^{M} \phi_i(x) = f(x)$
  2. **Missingness:** Features with zero presence have zero impact.
  3. **Consistency:** If a feature's marginal contribution increases, its Shapley value cannot decrease.
