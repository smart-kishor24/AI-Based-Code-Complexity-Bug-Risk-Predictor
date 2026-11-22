"""
Feature Extraction Engine module.
Extracts software complexity metrics and AST numerical features from parsed functions,
including Cyclomatic Complexity, Halstead Metrics, and structural measurements.
"""

import ast
import math
from typing import List, Dict, Any, Optional
import pandas as pd

from modules.code_parser import FunctionNodeInfo, ParseResult

# Try importing Radon for standard industry calculations
try:
    from radon.complexity import cc_visit
    import radon.metrics as radon_metrics
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False


def calculate_ast_cyclomatic_complexity(func_code: str) -> int:
    """
    Computes McCabe's Cyclomatic Complexity strictly from Python AST.
    Formula: CC = 1 + Decision Points
    Decision points include: If, For, While, AsyncFor, ExceptHandler,
    Boolean Ops (And/Or adds len - 1), comprehension ifs, and assert.
    """
    try:
        tree = ast.parse(func_code)
    except Exception:
        return 1

    complexity = 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While)):
            complexity += 1
        elif isinstance(node, ast.ExceptHandler):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            # Each additional operand in 'and'/'or' adds a branch
            complexity += max(0, len(node.values) - 1)
        elif isinstance(node, ast.comprehension):
            complexity += len(node.ifs)
        elif isinstance(node, ast.Assert):
            complexity += 1

    return complexity


def calculate_ast_halstead(func_code: str) -> Dict[str, float]:
    """
    Computes Halstead software metrics via AST token walking as a fallback or complement.
    n1: distinct operators
    n2: distinct operands
    N1: total operators
    N2: total operands
    """
    operators = []
    operands = []

    try:
        tree = ast.parse(func_code)
    except Exception:
        return {
            "h_length": 0.0,
            "h_vocabulary": 0.0,
            "h_volume": 0.0,
            "h_difficulty": 0.0,
            "h_effort": 0.0,
            "h_time": 0.0,
            "h_bugs": 0.0,
        }

    for node in ast.walk(tree):
        # Operators
        if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)):
            operators.append(node.__class__.__name__)
        elif isinstance(node, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn)):
            operators.append(node.__class__.__name__)
        elif isinstance(node, (ast.And, ast.Or, ast.Not, ast.BitOr, ast.BitAnd, ast.BitXor, ast.Invert)):
            operators.append(node.__class__.__name__)
        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.Return, ast.Call)):
            operators.append(node.__class__.__name__)

        # Operands
        elif isinstance(node, ast.Name):
            operands.append(node.id)
        elif isinstance(node, ast.Constant):
            operands.append(repr(node.value))

    n1 = len(set(operators))
    n2 = len(set(operands))
    N1 = len(operators)
    N2 = len(operands)

    N = N1 + N2
    n = n1 + n2

    if n > 0:
        volume = N * math.log2(n)
    else:
        volume = 0.0

    if n2 > 0 and n1 > 0:
        difficulty = (n1 / 2.0) * (N2 / float(n2))
    else:
        difficulty = 0.0

    effort = difficulty * volume
    time = effort / 18.0 if effort > 0 else 0.0
    bugs = volume / 3000.0 if volume > 0 else 0.0

    return {
        "h_length": float(N),
        "h_vocabulary": float(n),
        "h_volume": round(volume, 2),
        "h_difficulty": round(difficulty, 2),
        "h_effort": round(effort, 2),
        "h_time": round(time, 2),
        "h_bugs": round(bugs, 4),
        "uniq_op": float(n1),
        "uniq_opnd": float(n2),
        "total_op": float(N1),
        "total_opnd": float(N2),
    }


class FeatureExtractor:
    """Extracts function-level numerical features and metrics for ML models."""

    CORE_FEATURE_COLUMNS = [
        "loc",
        "cyclomatic_complexity",
        "max_nesting_depth",
        "param_count",
        "return_count",
        "loop_count",
        "condition_count",
        "call_count",
        "exception_count",
        "class_method_count",
    ]

    HALSTEAD_FEATURE_COLUMNS = [
        "h_volume",
        "h_difficulty",
        "h_effort",
        "h_length",
        "h_vocabulary",
        "uniq_op",
        "uniq_opnd",
        "total_op",
        "total_opnd",
    ]

    @classmethod
    def get_cyclomatic_complexity(cls, func: FunctionNodeInfo) -> int:
        """Determines cyclomatic complexity via Radon if available, falling back to AST."""
        if RADON_AVAILABLE and func.raw_code:
            try:
                results = cc_visit(func.raw_code)
                for item in results:
                    if item.name == func.name:
                        return int(item.complexity)
                if results:
                    return int(results[0].complexity)
            except Exception:
                pass
        return calculate_ast_cyclomatic_complexity(func.raw_code)

    @classmethod
    def extract_function_metrics(
        cls,
        func: FunctionNodeInfo,
        class_method_count_map: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        """Extracts complete metric record for one function."""
        cc = cls.get_cyclomatic_complexity(func)
        class_method_cnt = 0
        if func.class_name and class_method_count_map:
            class_method_cnt = class_method_count_map.get(func.class_name, 1)

        halstead = calculate_ast_halstead(func.raw_code)

        data = {
            "function_name": func.name,
            "class_name": func.class_name or "(Global)",
            "start_line": func.start_line,
            "end_line": func.end_line,
            "is_method": func.is_method,
            "is_nested": func.is_nested,
            # Core Features
            "loc": int(func.loc),
            "cyclomatic_complexity": int(cc),
            "max_nesting_depth": int(func.max_nesting_depth),
            "param_count": int(func.param_count),
            "return_count": int(func.return_count),
            "loop_count": int(func.loop_count),
            "condition_count": int(func.condition_count),
            "call_count": int(func.call_count),
            "exception_count": int(func.exception_count),
            "class_method_count": int(class_method_cnt),
            # Halstead metrics
            **halstead,
        }
        return data

    @classmethod
    def extract_all_features(cls, parse_result: ParseResult) -> pd.DataFrame:
        """
        Converts all functions from a ParseResult into a structured DataFrame
        with validation for missing or invalid values.
        """
        if not parse_result.functions:
            columns = [
                "function_name",
                "class_name",
                "start_line",
                "end_line",
                "is_method",
                "is_nested",
            ] + cls.CORE_FEATURE_COLUMNS + cls.HALSTEAD_FEATURE_COLUMNS
            return pd.DataFrame(columns=columns)

        # Count methods per class
        class_method_count_map: Dict[str, int] = {}
        for func in parse_result.functions:
            if func.class_name:
                class_method_count_map[func.class_name] = (
                    class_method_count_map.get(func.class_name, 0) + 1
                )

        rows = []
        for func in parse_result.functions:
            metrics = cls.extract_function_metrics(func, class_method_count_map)
            rows.append(metrics)

        df = pd.DataFrame(rows)

        # Fill potential NaNs and validate numeric types
        numeric_cols = cls.CORE_FEATURE_COLUMNS + cls.HALSTEAD_FEATURE_COLUMNS
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        return df
