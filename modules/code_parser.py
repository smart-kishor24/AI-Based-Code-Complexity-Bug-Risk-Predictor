"""
AST-based Python Code Parser module.
Parses Python source code and extracts structural features, function boundaries,
and AST node metrics without executing the source code.
"""

import ast
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class FunctionNodeInfo:
    name: str
    class_name: Optional[str]
    is_method: bool
    is_nested: bool
    start_line: int
    end_line: int
    loc: int
    param_count: int
    return_count: int
    condition_count: int
    loop_count: int
    max_nesting_depth: int
    call_count: int
    exception_count: int
    docstring: Optional[str]
    raw_code: str


@dataclass
class ParseResult:
    is_valid: bool
    error_message: Optional[str]
    error_line: Optional[int]
    error_column: Optional[int]
    total_lines: int
    total_classes: int
    total_functions: int
    functions: List[FunctionNodeInfo]
    class_names: List[str]


class CodeNestingVisitor:
    """Calculates maximum control flow nesting depth within an AST node."""

    CONTROL_FLOW_NODES = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncWith,
    )

    @classmethod
    def calculate_max_depth(cls, node: ast.AST) -> int:
        def _get_depth(current_node: ast.AST, current_depth: int) -> int:
            max_d = current_depth
            for child in ast.iter_child_nodes(current_node):
                # Do not recurse into nested function or class definitions
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue

                if isinstance(child, cls.CONTROL_FLOW_NODES):
                    child_depth = _get_depth(child, current_depth + 1)
                else:
                    child_depth = _get_depth(child, current_depth)
                if child_depth > max_d:
                    max_d = child_depth
            return max_d

        return _get_depth(node, 0)


class FunctionMetricsCollector(ast.NodeVisitor):
    """
    Collects metric counts for a single function AST node without
    descending into nested functions.
    """

    def __init__(self, root_function_node: ast.AST):
        self.root = root_function_node
        self.return_count = 0
        self.condition_count = 0
        self.loop_count = 0
        self.call_count = 0
        self.exception_count = 0

    def collect(self) -> None:
        for node in ast.walk(self.root):
            # Skip the root function node itself for type checks
            if node is self.root:
                continue

            # Skip nodes belonging to nested functions/classes
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue

            # Return statements
            if isinstance(node, ast.Return):
                self.return_count += 1

            # Conditionals: if statements and ternary expressions
            elif isinstance(node, (ast.If, ast.IfExp)):
                self.condition_count += 1

            # Loops: for, while, async for
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                self.loop_count += 1

            # Function calls
            elif isinstance(node, ast.Call):
                self.call_count += 1

            # Exception handling: try blocks and raise statements
            elif isinstance(node, (ast.Try, ast.Raise)):
                self.exception_count += 1

            # Comprehension conditionals (e.g., [x for x in list if cond])
            elif isinstance(node, ast.comprehension):
                self.condition_count += len(node.ifs)


class ASTCodeAnalyzer:
    """Main AST analyzer for Python codebases."""

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.total_lines = len(self.lines)

    def parse(self) -> ParseResult:
        if not self.source_code.strip():
            return ParseResult(
                is_valid=False,
                error_message="Source code is empty.",
                error_line=None,
                error_column=None,
                total_lines=0,
                total_classes=0,
                total_functions=0,
                functions=[],
                class_names=[],
            )

        try:
            tree = ast.parse(self.source_code)
        except SyntaxError as exc:
            return ParseResult(
                is_valid=False,
                error_message=f"Syntax Error: {exc.msg}",
                error_line=exc.lineno,
                error_column=exc.offset,
                total_lines=self.total_lines,
                total_classes=0,
                total_functions=0,
                functions=[],
                class_names=[],
            )
        except Exception as exc:
            return ParseResult(
                is_valid=False,
                error_message=f"Parsing Error: {str(exc)}",
                error_line=None,
                error_column=None,
                total_lines=self.total_lines,
                total_classes=0,
                total_functions=0,
                functions=[],
                class_names=[],
            )

        class_names: List[str] = []
        functions: List[FunctionNodeInfo] = []

        # Traverse tree and maintain class context
        self._traverse_tree(tree, current_class=None, is_nested=False, functions=functions, class_names=class_names)

        return ParseResult(
            is_valid=True,
            error_message=None,
            error_line=None,
            error_column=None,
            total_lines=self.total_lines,
            total_classes=len(class_names),
            total_functions=len(functions),
            functions=functions,
            class_names=class_names,
        )

    def _traverse_tree(
        self,
        node: ast.AST,
        current_class: Optional[str],
        is_nested: bool,
        functions: List[FunctionNodeInfo],
        class_names: List[str],
    ) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                class_names.append(child.name)
                # Traverse class body
                for class_child in ast.iter_child_nodes(child):
                    if isinstance(class_child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self._process_function(
                            func_node=class_child,
                            class_name=child.name,
                            is_nested=False,
                            functions=functions,
                            class_names=class_names,
                        )
                    elif isinstance(class_child, ast.ClassDef):
                        # Nested class
                        self._traverse_tree(
                            class_child,
                            current_class=f"{child.name}.{class_child.name}",
                            is_nested=True,
                            functions=functions,
                            class_names=class_names,
                        )

            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._process_function(
                    func_node=child,
                    class_name=current_class,
                    is_nested=is_nested,
                    functions=functions,
                    class_names=class_names,
                )

    def _process_function(
        self,
        func_node: ast.AST,
        class_name: Optional[str],
        is_nested: bool,
        functions: List[FunctionNodeInfo],
        class_names: List[str],
    ) -> None:
        # Parameter count
        args = func_node.args
        param_count = (
            len(args.args)
            + len(args.posonlyargs)
            + len(args.kwonlyargs)
            + (1 if args.vararg else 0)
            + (1 if args.kwarg else 0)
        )
        # If method in class and first arg is self/cls, adjust or keep track
        is_method = class_name is not None

        # Line boundaries
        start_line = getattr(func_node, "lineno", 1)
        end_line = getattr(func_node, "end_lineno", start_line)
        loc = max(1, end_line - start_line + 1)

        # Metrics collected inside function
        collector = FunctionMetricsCollector(func_node)
        collector.collect()

        # Nesting depth
        max_nesting_depth = CodeNestingVisitor.calculate_max_depth(func_node)

        # Docstring
        docstring = ast.get_docstring(func_node)

        # Slice raw code lines safely
        if self.lines and 1 <= start_line <= len(self.lines):
            raw_code = "\n".join(self.lines[start_line - 1 : end_line])
        else:
            raw_code = ""

        info = FunctionNodeInfo(
            name=func_node.name,
            class_name=class_name,
            is_method=is_method,
            is_nested=is_nested,
            start_line=start_line,
            end_line=end_line,
            loc=loc,
            param_count=param_count,
            return_count=collector.return_count,
            condition_count=collector.condition_count,
            loop_count=collector.loop_count,
            max_nesting_depth=max_nesting_depth,
            call_count=collector.call_count,
            exception_count=collector.exception_count,
            docstring=docstring,
            raw_code=raw_code,
        )
        functions.append(info)

        # Check for nested functions inside this function
        for inner_child in ast.iter_child_nodes(func_node):
            if isinstance(inner_child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._process_function(
                    func_node=inner_child,
                    class_name=class_name,
                    is_nested=True,
                    functions=functions,
                    class_names=class_names,
                )
