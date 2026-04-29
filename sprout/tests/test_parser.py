"""Tests for the Sprout recursive descent parser."""

import pytest
from sprout.lexer import Lexer
from sprout.parser import Parser, ParseError
from sprout.ast_nodes import (
    Program, VarDecl, Assign, IfStmt, WhileStmt, ForStmt,
    FunctionDef, ReturnStmt, BreakStmt, ContinueStmt, ExprStmt,
    BinaryOp, UnaryOp, LogicalOp, Identifier, IntLiteral, FloatLiteral,
    StringLiteral, BoolLiteral, NilLiteral, ArrayLiteral, DictLiteral,
    Subscript, Attribute, Call, FunctionExpr,
)


def parse(src):
    tokens = Lexer(src).tokenize()
    return Parser(tokens).parse()


def parse_expr(src):
    prog = parse(src)
    return prog.statements[0].expr


class TestLiterals:
    def test_int(self):
        node = parse_expr("42")
        assert isinstance(node, IntLiteral)
        assert node.value == 42

    def test_float(self):
        node = parse_expr("3.14")
        assert isinstance(node, FloatLiteral)
        assert abs(node.value - 3.14) < 1e-9

    def test_string(self):
        node = parse_expr('"hello"')
        assert isinstance(node, StringLiteral)
        assert node.value == "hello"

    def test_bool_true(self):
        node = parse_expr("true")
        assert isinstance(node, BoolLiteral)
        assert node.value is True

    def test_bool_false(self):
        node = parse_expr("false")
        assert isinstance(node, BoolLiteral)
        assert node.value is False

    def test_nil(self):
        node = parse_expr("nil")
        assert isinstance(node, NilLiteral)


class TestBinaryOps:
    def test_addition(self):
        node = parse_expr("1 + 2")
        assert isinstance(node, BinaryOp)
        assert node.op == "+"
        assert isinstance(node.left, IntLiteral)
        assert isinstance(node.right, IntLiteral)

    def test_precedence_mul_over_add(self):
        node = parse_expr("1 + 2 * 3")
        assert isinstance(node, BinaryOp)
        assert node.op == "+"
        assert isinstance(node.right, BinaryOp)
        assert node.right.op == "*"

    def test_power_right_associative(self):
        node = parse_expr("2 ** 3 ** 4")
        assert isinstance(node, BinaryOp)
        assert node.op == "**"
        assert isinstance(node.right, BinaryOp)  # 3**4 on right

    def test_unary_minus(self):
        node = parse_expr("-5")
        assert isinstance(node, UnaryOp)
        assert node.op == "-"

    def test_not(self):
        node = parse_expr("not true")
        assert isinstance(node, UnaryOp)
        assert node.op == "not"


class TestLogicalOps:
    def test_and(self):
        node = parse_expr("a and b")
        assert isinstance(node, LogicalOp)
        assert node.op == "and"

    def test_or(self):
        node = parse_expr("a or b")
        assert isinstance(node, LogicalOp)
        assert node.op == "or"


class TestCollections:
    def test_empty_array(self):
        node = parse_expr("[]")
        assert isinstance(node, ArrayLiteral)
        assert node.elements == []

    def test_array_with_elements(self):
        node = parse_expr("[1, 2, 3]")
        assert isinstance(node, ArrayLiteral)
        assert len(node.elements) == 3

    def test_nested_array(self):
        node = parse_expr("[[1, 2], [3, 4]]")
        assert isinstance(node, ArrayLiteral)
        assert isinstance(node.elements[0], ArrayLiteral)

    def test_dict_literal(self):
        node = parse_expr('{"key": "value"}')
        assert isinstance(node, DictLiteral)
        assert len(node.pairs) == 1

    def test_subscript(self):
        node = parse_expr("arr[0]")
        assert isinstance(node, Subscript)
        assert isinstance(node.obj, Identifier)
        assert isinstance(node.index, IntLiteral)

    def test_attribute(self):
        node = parse_expr("obj.field")
        assert isinstance(node, Attribute)
        assert node.name == "field"


class TestCalls:
    def test_simple_call(self):
        node = parse_expr("f()")
        assert isinstance(node, Call)
        assert isinstance(node.callee, Identifier)
        assert node.args == []

    def test_call_with_args(self):
        node = parse_expr("add(1, 2, 3)")
        assert isinstance(node, Call)
        assert len(node.args) == 3

    def test_chained_call(self):
        node = parse_expr("f()()")
        assert isinstance(node, Call)
        assert isinstance(node.callee, Call)

    def test_method_call(self):
        node = parse_expr("obj.method(x)")
        assert isinstance(node, Call)
        assert isinstance(node.callee, Attribute)


class TestStatements:
    def test_var_decl(self):
        prog = parse("let x = 42")
        stmt = prog.statements[0]
        assert isinstance(stmt, VarDecl)
        assert stmt.name == "x"
        assert isinstance(stmt.value, IntLiteral)

    def test_var_decl_no_init(self):
        prog = parse("let x")
        stmt = prog.statements[0]
        assert isinstance(stmt, VarDecl)
        assert stmt.value is None

    def test_assignment(self):
        prog = parse("x = 10")
        stmt = prog.statements[0]
        assert isinstance(stmt, ExprStmt)
        assert isinstance(stmt.expr, Assign)
        assert stmt.expr.op == "="

    def test_compound_assignment(self):
        prog = parse("x += 5")
        stmt = prog.statements[0]
        assert isinstance(stmt.expr, Assign)
        assert stmt.expr.op == "+="

    def test_if_stmt(self):
        prog = parse("if x > 0 { println(x) }")
        stmt = prog.statements[0]
        assert isinstance(stmt, IfStmt)
        assert stmt.else_branch is None
        assert stmt.elif_branches == []

    def test_if_else(self):
        prog = parse("if a { b() } else { c() }")
        stmt = prog.statements[0]
        assert isinstance(stmt, IfStmt)
        assert stmt.else_branch is not None

    def test_if_elif_else(self):
        prog = parse("if a { } else if b { } else { }")
        stmt = prog.statements[0]
        assert isinstance(stmt, IfStmt)
        assert len(stmt.elif_branches) == 1

    def test_while_stmt(self):
        prog = parse("while x > 0 { x -= 1 }")
        stmt = prog.statements[0]
        assert isinstance(stmt, WhileStmt)

    def test_for_stmt(self):
        prog = parse("for i in arr { println(i) }")
        stmt = prog.statements[0]
        assert isinstance(stmt, ForStmt)
        assert stmt.var == "i"

    def test_return_stmt(self):
        prog = parse("fn f() { return 42 }")
        fn = prog.statements[0]
        ret = fn.body.statements[0]
        assert isinstance(ret, ReturnStmt)
        assert isinstance(ret.value, IntLiteral)

    def test_return_no_value(self):
        prog = parse("fn f() { return }")
        fn = prog.statements[0]
        ret = fn.body.statements[0]
        assert isinstance(ret, ReturnStmt)
        assert ret.value is None

    def test_break_continue(self):
        prog = parse("fn f() { while true { break } }")
        fn = prog.statements[0]
        loop = fn.body.statements[0]
        stmt = loop.body.statements[0]
        assert isinstance(stmt, BreakStmt)


class TestFunctions:
    def test_function_def(self):
        prog = parse("fn add(a, b) { return a + b }")
        fn = prog.statements[0]
        assert isinstance(fn, FunctionDef)
        assert fn.name == "add"
        assert fn.params == ["a", "b"]

    def test_function_with_default(self):
        prog = parse("fn pow(b, e = 2) { }")
        fn = prog.statements[0]
        assert fn.params == ["b", "e"]
        assert fn.defaults[0] is None
        assert isinstance(fn.defaults[1], IntLiteral)

    def test_lambda(self):
        prog = parse("let f = fn(x) { return x * 2 }")
        decl = prog.statements[0]
        assert isinstance(decl.value, FunctionExpr)
        assert decl.value.params == ["x"]


class TestErrors:
    def test_missing_closing_brace(self):
        with pytest.raises(ParseError):
            parse("if true { println(1)")

    def test_invalid_assignment_target(self):
        with pytest.raises(ParseError):
            parse("1 = 2")

    def test_unclosed_paren(self):
        with pytest.raises(ParseError):
            parse("f(1, 2")
