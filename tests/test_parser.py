"""
Unit tests for AST Code Parser module (modules/code_parser.py).
Tests:
1. Valid Python file
2. Empty Python file
3. Invalid syntax
4. Nested functions
5. Class methods
6. Deeply nested conditions
7. Large source file
"""

import pytest
from modules.code_parser import ASTCodeAnalyzer, ParseResult, FunctionNodeInfo


def test_valid_python_file():
    code = """
def add(a, b):
    \"\"\"Add two numbers.\"\"\"
    return a + b
"""
    analyzer = ASTCodeAnalyzer(code)
    res = analyzer.parse()
    assert res.is_valid is True
    assert res.error_message is None
    assert len(res.functions) == 1
    func = res.functions[0]
    assert func.name == "add"
    assert func.param_count == 2
    assert func.return_count == 1
    assert func.loc >= 3


def test_empty_python_file():
    analyzer = ASTCodeAnalyzer("")
    res = analyzer.parse()
    assert res.is_valid is False
    assert "empty" in res.error_message.lower()
    assert len(res.functions) == 0


def test_invalid_syntax():
    code = "def broken_func(:\n    return 42"
    analyzer = ASTCodeAnalyzer(code)
    res = analyzer.parse()
    assert res.is_valid is False
    assert res.error_line is not None
    assert "syntax error" in res.error_message.lower()


def test_nested_functions():
    code = """
def outer_func(x):
    def inner_func(y):
        if y > 0:
            return y * 2
        return y
    return inner_func(x) + 1
"""
    analyzer = ASTCodeAnalyzer(code)
    res = analyzer.parse()
    assert res.is_valid is True
    assert len(res.functions) == 2
    names = [f.name for f in res.functions]
    assert "outer_func" in names
    assert "inner_func" in names
    inner = next(f for f in res.functions if f.name == "inner_func")
    assert inner.is_nested is True


def test_class_methods():
    code = """
class Calculator:
    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Zero division")
        return a / b
"""
    analyzer = ASTCodeAnalyzer(code)
    res = analyzer.parse()
    assert res.is_valid is True
    assert len(res.class_names) == 1
    assert res.class_names[0] == "Calculator"
    assert len(res.functions) == 2
    for f in res.functions:
        assert f.is_method is True
        assert f.class_name == "Calculator"


def test_deeply_nested_conditions():
    code = """
def evaluate_nested(a, b, c, d):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    return 1
    return 0
"""
    analyzer = ASTCodeAnalyzer(code)
    res = analyzer.parse()
    assert res.is_valid is True
    func = res.functions[0]
    assert func.max_nesting_depth == 4
    assert func.condition_count == 4


def test_large_source_file():
    # Generate 50 functions in a large file
    lines = []
    for i in range(50):
        lines.append(f"def generated_func_{i}(x):\n    if x > {i}:\n        return x * {i}\n    return 0\n")
    large_code = "\n".join(lines)
    analyzer = ASTCodeAnalyzer(large_code)
    res = analyzer.parse()
    assert res.is_valid is True
    assert len(res.functions) == 50
