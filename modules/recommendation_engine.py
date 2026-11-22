"""
Recommendation Engine module.
Generates actionable, rule-based software engineering recommendations
based on calculated complexity metrics, static analysis warnings, and predicted risk.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from config.settings import METRIC_THRESHOLDS


class RecommendationEngine:
    """Generates code quality and refactoring recommendations."""

    @classmethod
    def generate_function_recommendations(cls, function_metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Evaluates a single function's metrics and returns a list of prioritized recommendations.
        """
        recs = []
        name = function_metrics.get("function_name", "function")
        loc = function_metrics.get("loc", 0)
        cc = function_metrics.get("cyclomatic_complexity", 1)
        depth = function_metrics.get("max_nesting_depth", 0)
        params = function_metrics.get("param_count", 0)
        returns = function_metrics.get("return_count", 0)
        loops = function_metrics.get("loop_count", 0)
        conds = function_metrics.get("condition_count", 0)
        calls = function_metrics.get("call_count", 0)

        # 1. Cyclomatic Complexity
        if cc > METRIC_THRESHOLDS["cyclomatic_complexity"]["critical"]:
            recs.append({
                "severity": "Critical",
                "category": "Complexity",
                "target": f"Function '{name}'",
                "message": f"Critical cyclomatic complexity ({cc} > {METRIC_THRESHOLDS['cyclomatic_complexity']['critical']}).",
                "action": "Split the function into smaller logical units or apply the Strategy/Dispatch pattern to reduce independent execution paths.",
            })
        elif cc > METRIC_THRESHOLDS["cyclomatic_complexity"]["warning"]:
            recs.append({
                "severity": "Warning",
                "category": "Complexity",
                "target": f"Function '{name}'",
                "message": f"Elevated cyclomatic complexity ({cc}).",
                "action": "Consider extracting conditional branches into separate helper methods.",
            })

        # 2. Maximum Nesting Depth
        if depth > METRIC_THRESHOLDS["max_nesting_depth"]["critical"]:
            recs.append({
                "severity": "Critical",
                "category": "Nesting",
                "target": f"Function '{name}'",
                "message": f"Deeply nested control structures (depth {depth} > {METRIC_THRESHOLDS['max_nesting_depth']['critical']}).",
                "action": "Invert conditions and adopt guard clauses (early returns) to flatten deeply nested logic.",
            })
        elif depth > METRIC_THRESHOLDS["max_nesting_depth"]["warning"]:
            recs.append({
                "severity": "Warning",
                "category": "Nesting",
                "target": f"Function '{name}'",
                "message": f"Noticeable nesting depth ({depth}).",
                "action": "Use guard clauses to return or continue early.",
            })

        # 3. Function Length (LOC)
        if loc > METRIC_THRESHOLDS["loc"]["critical"]:
            recs.append({
                "severity": "High",
                "category": "Function Length",
                "target": f"Function '{name}'",
                "message": f"Lengthy function body ({loc} lines > {METRIC_THRESHOLDS['loc']['critical']}).",
                "action": "Separate responsibilities into smaller subroutines conforming to the Single Responsibility Principle (SRP).",
            })
        elif loc > METRIC_THRESHOLDS["loc"]["warning"]:
            recs.append({
                "severity": "Medium",
                "category": "Function Length",
                "target": f"Function '{name}'",
                "message": f"Moderate function length ({loc} lines).",
                "action": "Monitor function size and verify if all operations belong to the same level of abstraction.",
            })

        # 4. Parameter Count
        if params > METRIC_THRESHOLDS["param_count"]["critical"]:
            recs.append({
                "severity": "High",
                "category": "Parameters",
                "target": f"Function '{name}'",
                "message": f"Excessive parameter count ({params} parameters).",
                "action": "Group related parameters into a dataclass, pydantic model, or parameter object.",
            })
        elif params > METRIC_THRESHOLDS["param_count"]["warning"]:
            recs.append({
                "severity": "Medium",
                "category": "Parameters",
                "target": f"Function '{name}'",
                "message": f"High parameter count ({params} parameters).",
                "action": "Consider whether some parameters can be packaged together or configured via defaults.",
            })

        # 5. Return Statement Count
        if returns > METRIC_THRESHOLDS["return_count"]["critical"]:
            recs.append({
                "severity": "Medium",
                "category": "Control Flow",
                "target": f"Function '{name}'",
                "message": f"High number of return points ({returns}).",
                "action": "Ensure exit points are clear and consistent to prevent unexpected partial state mutations.",
            })

        # 6. Loops and Algorithmic Complexity
        if loops > METRIC_THRESHOLDS["loop_count"]["warning"]:
            recs.append({
                "severity": "Medium",
                "category": "Performance",
                "target": f"Function '{name}'",
                "message": f"Multiple loops ({loops}) detected.",
                "action": "Review algorithmic time complexity to avoid O(n^2) nested iterations. Utilize generator expressions or vectorized NumPy operations where possible.",
            })

        return recs

    @classmethod
    def generate_all_recommendations(
        cls,
        metrics_df: pd.DataFrame,
        static_warnings: List[Dict[str, Any]],
        predicted_risks: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, str]]:
        """
        Combines metric recommendations, static analysis recommendations,
        and ML risk insights into a unified actionable list.
        """
        all_recs: List[Dict[str, str]] = []

        # 1. Metric recommendations per function
        if not metrics_df.empty:
            for _, row in metrics_df.iterrows():
                func_dict = row.to_dict()
                func_recs = cls.generate_function_recommendations(func_dict)
                all_recs.extend(func_recs)

        # 2. High ML Risk recommendations
        if predicted_risks:
            for risk_item in predicted_risks:
                if risk_item.get("risk_category") == "High Risk":
                    prob = risk_item.get("defect_probability", 0.0)
                    func_name = risk_item.get("function_name", "Function")
                    all_recs.append({
                        "severity": "Critical",
                        "category": "ML Defect Risk",
                        "target": f"Function '{func_name}'",
                        "message": f"ML model estimates high historical defect probability ({prob*100:.1f}%).",
                        "action": "Prioritize rigorous unit test coverage, property-based testing, and peer code review for this function.",
                    })

        # 3. Static analysis warning recommendations
        if static_warnings:
            # Group or summarize static warnings
            by_severity = {}
            for w in static_warnings:
                sev = w.get("severity", "Warning")
                by_severity[sev] = by_severity.get(sev, 0) + 1

            if len(static_warnings) > 0:
                all_recs.append({
                    "severity": "Warning" if by_severity.get("Error", 0) == 0 else "Critical",
                    "category": "Static Analysis",
                    "target": "Global Source Code",
                    "message": f"{len(static_warnings)} static analysis issues identified ({by_severity.get('Error', 0)} errors, {by_severity.get('Warning', 0)} warnings).",
                    "action": "Address static analysis warnings directly, especially unused variables, mutable defaults, and bare except clauses.",
                })

        # Priority order for sorting
        severity_rank = {"Critical": 0, "High": 1, "Warning": 2, "Medium": 3, "Low": 4, "Convention": 5}
        all_recs.sort(key=lambda r: severity_rank.get(r.get("severity", "Medium"), 10))

        return all_recs
