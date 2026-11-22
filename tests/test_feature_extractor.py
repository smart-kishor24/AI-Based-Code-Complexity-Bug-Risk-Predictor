"""
Unit tests for Feature Extractor and Static Analyzer modules.
"""

import pytest
import pandas as pd
from modules.code_parser import ASTCodeAnalyzer
from modules.feature_extractor import FeatureExtractor, calculate_ast_cyclomatic_complexity, calculate_ast_halstead
from modules.static_analyzer import StaticCodeAnalyzer, BuiltInASTLinter


def test_cyclomatic_complexity_ast():
    func_code = """
def sample_branches(a, b):
    if a > 0 and b > 0:
        for i in range(5):
            print(i)
    elif a < 0:
        return -1
    return 0
"""
    # 1 base + if (1) + and (1) + for (1) + elif (1) = 5
    cc = calculate_ast_cyclomatic_complexity(func_code)
    assert cc == 5


def test_halstead_metrics_extraction():
    func_code = "def calc(x, y):\n    return (x + y) * 2\n"
    h = calculate_ast_halstead(func_code)
    assert "h_volume" in h
    assert "h_difficulty" in h
    assert "h_effort" in h
    assert h["h_volume"] > 0
    assert h["h_length"] > 0


def test_feature_extractor_dataframe():
    code = """
class DataService:
    def fetch_data(self, endpoint, timeout):
        try:
            return endpoint + "?t=" + str(timeout)
        except Exception:
            return ""

def standalone(x):
    return x * 2
"""
    analyzer = ASTCodeAnalyzer(code)
    parse_result = analyzer.parse()
    df = FeatureExtractor.extract_all_features(parse_result)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "loc" in df.columns
    assert "cyclomatic_complexity" in df.columns
    assert "max_nesting_depth" in df.columns
    assert "param_count" in df.columns


def test_static_analyzer_catches_anti_patterns():
    code = """
import unused_module

def risky_function(cache=[]):
    try:
        x = 10
    except:
        pass
    if x == None:
        return None
"""
    issues = StaticCodeAnalyzer.analyze_code(code)
    rule_ids = [issue["rule_id"] for issue in issues]

    # Should detect mutable default (W0102), bare except (W0702), and comparison to None (E711)
    assert any("0102" in r for r in rule_ids)  # mutable default
    assert any("0702" in r for r in rule_ids)  # bare except
    assert any("711" in r for r in rule_ids)   # == None
