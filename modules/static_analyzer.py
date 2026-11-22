"""
Static Code Analysis Engine module.
Integrates static analysis (Ruff CLI and built-in AST inspection) to detect code smells,
style violations, unused variables, undefined names, and hazardous patterns without executing code.
"""

import ast
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class StaticIssue:
    line: int
    column: int
    rule_id: str
    severity: str  # "Error", "Warning", "Convention", "Refactor"
    message: str
    suggestion: str


class BuiltInASTLinter(ast.NodeVisitor):
    """
    Built-in AST-based static rule analyzer.
    Detects critical code smells and issues without external dependencies.
    """

    PYTHON_BUILTINS = set(dir(__builtins__)) | {
        "self", "cls", "__name__", "__doc__", "__file__", "__package__"
    }

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.issues: List[StaticIssue] = []
        self.imported_names: Dict[str, Tuple[int, int]] = {}
        self.used_names: set = set()
        self.defined_functions: set = set()

    def analyze(self) -> List[StaticIssue]:
        try:
            tree = ast.parse(self.source_code)
        except SyntaxError as exc:
            return [
                StaticIssue(
                    line=exc.lineno or 1,
                    column=exc.offset or 1,
                    rule_id="E999",
                    severity="Error",
                    message=f"Syntax Error: {exc.msg}",
                    suggestion="Fix the syntax error to enable complete static analysis.",
                )
            ]

        # Check module docstring
        if not ast.get_docstring(tree):
            self.issues.append(
                StaticIssue(
                    line=1,
                    column=1,
                    rule_id="C0114",
                    severity="Convention",
                    message="Missing module docstring.",
                    suggestion="Add a top-level docstring explaining the purpose of this module.",
                )
            )

        self.visit(tree)
        self._check_unused_imports()

        # Sort issues by line number
        self.issues.sort(key=lambda x: (x.line, x.column))
        return self.issues

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            self.imported_names[name] = (node.lineno, node.col_offset + 1)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            self.imported_names[name] = (node.lineno, node.col_offset + 1)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.defined_functions.add(node.name)
        # Check function docstring
        if not ast.get_docstring(node):
            self.issues.append(
                StaticIssue(
                    line=node.lineno,
                    column=node.col_offset + 1,
                    rule_id="C0116",
                    severity="Convention",
                    message=f"Missing docstring in function '{node.name}'.",
                    suggestion="Document function parameters, return values, and behavior using a docstring.",
                )
            )

        # Check function length
        end_lineno = getattr(node, "end_lineno", node.lineno)
        func_len = end_lineno - node.lineno + 1
        if func_len > 50:
            self.issues.append(
                StaticIssue(
                    line=node.lineno,
                    column=node.col_offset + 1,
                    rule_id="R0915",
                    severity="Refactor",
                    message=f"Function '{node.name}' is too long ({func_len} lines > 50).",
                    suggestion="Split the function into smaller helper sub-functions with focused responsibilities.",
                )
            )

        # Check parameter count
        param_count = len(node.args.args)
        if param_count > 6:
            self.issues.append(
                StaticIssue(
                    line=node.lineno,
                    column=node.col_offset + 1,
                    rule_id="R0913",
                    severity="Refactor",
                    message=f"Function '{node.name}' has too many arguments ({param_count} > 6).",
                    suggestion="Bundle related arguments into a dataclass, dictionary, or configuration object.",
                )
            )

        # Check mutable default arguments
        for default in node.args.defaults + node.args.kw_defaults:
            if default and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append(
                    StaticIssue(
                        line=default.lineno,
                        column=default.col_offset + 1,
                        rule_id="W0102",
                        severity="Warning",
                        message=f"Dangerous mutable default argument in function '{node.name}'.",
                        suggestion="Use 'None' as default value and initialize the mutable object inside the function body.",
                    )
                )

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)  # type: ignore

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self.issues.append(
                StaticIssue(
                    line=node.lineno,
                    column=node.col_offset + 1,
                    rule_id="W0702",
                    severity="Warning",
                    message="Bare 'except:' clause used.",
                    suggestion="Catch specific exception classes (e.g. 'except ValueError:') rather than catching all exceptions.",
                )
            )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        # Check comparison with None using == or !=
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Eq, ast.NotEq)):
                if (isinstance(comparator, ast.Constant) and comparator.value is None) or \
                   (isinstance(node.left, ast.Constant) and node.left.value is None):
                    self.issues.append(
                        StaticIssue(
                            line=node.lineno,
                            column=node.col_offset + 1,
                            rule_id="E711",
                            severity="Warning",
                            message="Comparison to None should use 'is' or 'is not' rather than '==' or '!='.",
                            suggestion="Replace 'x == None' with 'x is None' or 'x != None' with 'x is not None'.",
                        )
                    )
        self.generic_visit(node)

    def _check_unused_imports(self) -> None:
        for name, (line, col) in self.imported_names.items():
            if name not in self.used_names:
                self.issues.append(
                    StaticIssue(
                        line=line,
                        column=col,
                        rule_id="W0611",
                        severity="Warning",
                        message=f"Unused import '{name}'.",
                        suggestion=f"Remove the unused import '{name}' to clean up module dependencies.",
                    )
                )


class StaticCodeAnalyzer:
    """Orchestrates static analysis using Ruff when available, with AST fallback."""

    @classmethod
    def analyze_code(cls, source_code: str) -> List[Dict[str, Any]]:
        """
        Runs static analysis on source code without modifying it.
        Returns a structured list of issue dictionaries.
        """
        if not source_code.strip():
            return []

        # Attempt Ruff if installed and accessible
        ruff_path = shutil.which("ruff")
        if ruff_path:
            try:
                ruff_issues = cls._run_ruff(source_code, ruff_path)
                if ruff_issues is not None:
                    return [asdict(issue) for issue in ruff_issues]
            except Exception:
                pass  # Fall back to built-in AST linter

        # Fallback to Built-in AST Linter
        linter = BuiltInASTLinter(source_code)
        issues = linter.analyze()
        return [asdict(issue) for issue in issues]

    @classmethod
    def _run_ruff(cls, source_code: str, ruff_executable: str) -> Optional[List[StaticIssue]]:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
            temp_path = temp_file.name
            temp_file.write(source_code)

        try:
            cmd = [
                ruff_executable,
                "check",
                "--output-format=json",
                "--isolated",
                temp_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.stdout:
                raw_data = json.loads(result.stdout)
                issues: List[StaticIssue] = []
                for item in raw_data:
                    code = item.get("code", "RUFF")
                    # Map Ruff codes to severities
                    severity = "Warning"
                    if code.startswith("E") or code.startswith("F"):
                        severity = "Error"
                    elif code.startswith("C") or code.startswith("I"):
                        severity = "Convention"
                    elif code.startswith("R"):
                        severity = "Refactor"

                    suggestion = "Review and correct the identified style or safety issue."
                    fix = item.get("fix")
                    if fix and fix.get("message"):
                        suggestion = fix["message"]

                    issues.append(
                        StaticIssue(
                            line=item.get("location", {}).get("row", 1),
                            column=item.get("location", {}).get("column", 1),
                            rule_id=code,
                            severity=severity,
                            message=item.get("message", "Lint warning"),
                            suggestion=suggestion,
                        )
                    )
                return issues
        except Exception:
            return None
        finally:
            try:
                Path(temp_path).unlink(missing_ok=True)
            except Exception:
                pass
        return None
