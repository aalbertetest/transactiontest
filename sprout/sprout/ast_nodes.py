"""AST node definitions for the Sprout language."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    line: int
    col: int


# ─── Statements ──────────────────────────────────────────────────────────────

@dataclass
class Program(Node):
    statements: list


@dataclass
class VarDecl(Node):
    name: str
    value: Optional[Any]  # Optional[Node]


@dataclass
class Assign(Node):
    target: Any   # Node
    op: str       # "=", "+=", "-=", "*=", "/="
    value: Any    # Node


@dataclass
class Block(Node):
    statements: list


@dataclass
class IfStmt(Node):
    condition: Any
    then_branch: Any
    elif_branches: list
    else_branch: Optional[Any]


@dataclass
class WhileStmt(Node):
    condition: Any
    body: Any


@dataclass
class ForStmt(Node):
    var: str
    iterable: Any
    body: Any


@dataclass
class FunctionDef(Node):
    name: str
    params: list
    defaults: list
    body: Any


@dataclass
class ReturnStmt(Node):
    value: Optional[Any]


@dataclass
class BreakStmt(Node):
    pass


@dataclass
class ContinueStmt(Node):
    pass


@dataclass
class ExprStmt(Node):
    expr: Any


@dataclass
class ImportStmt(Node):
    module: str


# ─── Expressions ─────────────────────────────────────────────────────────────

@dataclass
class BinaryOp(Node):
    op: str
    left: Any
    right: Any


@dataclass
class UnaryOp(Node):
    op: str
    operand: Any


@dataclass
class LogicalOp(Node):
    op: str   # "and" | "or"
    left: Any
    right: Any


@dataclass
class Identifier(Node):
    name: str


@dataclass
class IntLiteral(Node):
    value: int


@dataclass
class FloatLiteral(Node):
    value: float


@dataclass
class StringLiteral(Node):
    value: str


@dataclass
class BoolLiteral(Node):
    value: bool


@dataclass
class NilLiteral(Node):
    pass


@dataclass
class ArrayLiteral(Node):
    elements: list


@dataclass
class DictLiteral(Node):
    pairs: list


@dataclass
class Subscript(Node):
    obj: Any
    index: Any


@dataclass
class Attribute(Node):
    obj: Any
    name: str


@dataclass
class Call(Node):
    callee: Any
    args: list


@dataclass
class FunctionExpr(Node):
    """Anonymous lambda-style function."""
    params: list
    defaults: list
    body: Any
