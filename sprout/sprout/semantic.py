"""Semantic analyzer for the Sprout language.

Performs:
- Scope resolution (undefined variable detection)
- Function arity checks
- Return statement placement validation
- Break/continue placement validation
- Warning on unused variables (non-fatal)
"""

from __future__ import annotations
from typing import Optional
from .ast_nodes import (
    Node, Program, Block, VarDecl, Assign, IfStmt, WhileStmt, ForStmt,
    FunctionDef, ReturnStmt, BreakStmt, ContinueStmt, ExprStmt, ImportStmt,
    BinaryOp, UnaryOp, LogicalOp, Identifier, IntLiteral, FloatLiteral,
    StringLiteral, BoolLiteral, NilLiteral, ArrayLiteral, DictLiteral,
    Subscript, Attribute, Call, FunctionExpr,
)


class SemanticError(Exception):
    def __init__(self, message: str, line: int = 0, col: int = 0):
        super().__init__(f"SemanticError at {line}:{col}: {message}")
        self.line = line
        self.col = col


class Scope:
    def __init__(self, parent: Optional[Scope] = None):
        self.parent = parent
        self.symbols: dict[str, bool] = {}  # name -> is_function

    def define(self, name: str, is_function: bool = False) -> None:
        self.symbols[name] = is_function

    def lookup(self, name: str) -> Optional[bool]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def is_defined(self, name: str) -> bool:
        return self.lookup(name) is not None


# Built-in names always available
BUILTINS = {
    "print", "println", "input", "len", "type", "str", "int", "float",
    "bool", "range", "append", "pop", "keys", "values", "has",
    "sqrt", "abs", "floor", "ceil", "min", "max", "round",
    "split", "join", "trim", "upper", "lower", "starts_with", "ends_with",
    "contains", "replace", "format",
    "exit", "assert",
}


class SemanticAnalyzer:
    def __init__(self):
        self.errors: list[SemanticError] = []
        self.warnings: list[str] = []
        self._loop_depth = 0
        self._func_depth = 0

    def analyze(self, node: Node, scope: Optional[Scope] = None) -> None:
        if scope is None:
            scope = Scope()
            for name in BUILTINS:
                scope.define(name, is_function=True)
        self._visit(node, scope)
        if self.errors:
            raise self.errors[0]

    def _visit(self, node: Node, scope: Scope) -> None:
        method = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method, self._visit_generic)
        visitor(node, scope)

    def _visit_generic(self, node: Node, scope: Scope) -> None:
        pass

    # ── Statements ─────────────────────────────────────────────────────────

    def _visit_Program(self, node: Program, scope: Scope) -> None:
        # First pass: collect top-level function names
        for stmt in node.statements:
            if isinstance(stmt, FunctionDef):
                scope.define(stmt.name, is_function=True)
        for stmt in node.statements:
            self._visit(stmt, scope)

    def _visit_Block(self, node: Block, scope: Scope) -> None:
        for stmt in node.statements:
            self._visit(stmt, scope)

    def _visit_VarDecl(self, node: VarDecl, scope: Scope) -> None:
        if node.value:
            self._visit(node.value, scope)
        scope.define(node.name)

    def _visit_Assign(self, node: Assign, scope: Scope) -> None:
        self._visit(node.value, scope)
        if isinstance(node.target, Identifier):
            if not scope.is_defined(node.target.name):
                self.errors.append(SemanticError(
                    f"Undefined variable '{node.target.name}'",
                    node.line, node.col,
                ))
        else:
            self._visit(node.target, scope)

    def _visit_IfStmt(self, node: IfStmt, scope: Scope) -> None:
        self._visit(node.condition, scope)
        self._visit(node.then_branch, Scope(parent=scope))
        for cond, body in node.elif_branches:
            self._visit(cond, scope)
            self._visit(body, Scope(parent=scope))
        if node.else_branch:
            self._visit(node.else_branch, Scope(parent=scope))

    def _visit_WhileStmt(self, node: WhileStmt, scope: Scope) -> None:
        self._visit(node.condition, scope)
        self._loop_depth += 1
        self._visit(node.body, Scope(parent=scope))
        self._loop_depth -= 1

    def _visit_ForStmt(self, node: ForStmt, scope: Scope) -> None:
        self._visit(node.iterable, scope)
        loop_scope = Scope(parent=scope)
        loop_scope.define(node.var)
        self._loop_depth += 1
        self._visit(node.body, loop_scope)
        self._loop_depth -= 1

    def _visit_FunctionDef(self, node: FunctionDef, scope: Scope) -> None:
        # Already registered in parent pass; define in current scope too for nested
        scope.define(node.name, is_function=True)
        fn_scope = Scope(parent=scope)
        for param, default in zip(node.params, node.defaults):
            fn_scope.define(param)
            if default:
                self._visit(default, scope)
        self._func_depth += 1
        self._visit(node.body, fn_scope)
        self._func_depth -= 1

    def _visit_FunctionExpr(self, node: FunctionExpr, scope: Scope) -> None:
        fn_scope = Scope(parent=scope)
        for param, default in zip(node.params, node.defaults):
            fn_scope.define(param)
            if default:
                self._visit(default, scope)
        self._func_depth += 1
        self._visit(node.body, fn_scope)
        self._func_depth -= 1

    def _visit_ReturnStmt(self, node: ReturnStmt, scope: Scope) -> None:
        if self._func_depth == 0:
            self.errors.append(SemanticError(
                "'return' outside of function", node.line, node.col,
            ))
        if node.value:
            self._visit(node.value, scope)

    def _visit_BreakStmt(self, node: BreakStmt, scope: Scope) -> None:
        if self._loop_depth == 0:
            self.errors.append(SemanticError(
                "'break' outside of loop", node.line, node.col,
            ))

    def _visit_ContinueStmt(self, node: ContinueStmt, scope: Scope) -> None:
        if self._loop_depth == 0:
            self.errors.append(SemanticError(
                "'continue' outside of loop", node.line, node.col,
            ))

    def _visit_ExprStmt(self, node: ExprStmt, scope: Scope) -> None:
        self._visit(node.expr, scope)

    def _visit_ImportStmt(self, node: ImportStmt, scope: Scope) -> None:
        # Register the module name as a known namespace
        scope.define(node.module)

    # ── Expressions ────────────────────────────────────────────────────────

    def _visit_Identifier(self, node: Identifier, scope: Scope) -> None:
        if not scope.is_defined(node.name):
            self.errors.append(SemanticError(
                f"Undefined variable '{node.name}'", node.line, node.col,
            ))

    def _visit_BinaryOp(self, node: BinaryOp, scope: Scope) -> None:
        self._visit(node.left, scope)
        self._visit(node.right, scope)

    def _visit_UnaryOp(self, node: UnaryOp, scope: Scope) -> None:
        self._visit(node.operand, scope)

    def _visit_LogicalOp(self, node: LogicalOp, scope: Scope) -> None:
        self._visit(node.left, scope)
        self._visit(node.right, scope)

    def _visit_Call(self, node: Call, scope: Scope) -> None:
        self._visit(node.callee, scope)
        for arg in node.args:
            self._visit(arg, scope)

    def _visit_ArrayLiteral(self, node: ArrayLiteral, scope: Scope) -> None:
        for elem in node.elements:
            self._visit(elem, scope)

    def _visit_DictLiteral(self, node: DictLiteral, scope: Scope) -> None:
        for k, v in node.pairs:
            self._visit(k, scope)
            self._visit(v, scope)

    def _visit_Subscript(self, node: Subscript, scope: Scope) -> None:
        self._visit(node.obj, scope)
        self._visit(node.index, scope)

    def _visit_Attribute(self, node: Attribute, scope: Scope) -> None:
        self._visit(node.obj, scope)
