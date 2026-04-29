"""Tests for the Sprout semantic analyzer."""

import pytest
from sprout.lexer import Lexer
from sprout.parser import Parser
from sprout.semantic import SemanticAnalyzer, SemanticError


def analyze(src):
    tokens = Lexer(src).tokenize()
    ast = Parser(tokens).parse()
    SemanticAnalyzer().analyze(ast)


def analyze_err(src):
    with pytest.raises(SemanticError):
        analyze(src)


class TestUndefinedVariables:
    def test_defined_variable(self):
        analyze("let x = 1; println(x)")

    def test_undefined_variable(self):
        analyze_err("println(undefined_var)")

    def test_forward_reference_to_function(self):
        # Top-level functions are collected in first pass
        analyze("println(add(1, 2)); fn add(a, b) { return a + b }")

    def test_param_in_body(self):
        analyze("fn f(x) { return x + 1 }")

    def test_closure_captures_outer(self):
        analyze("let n = 5; fn f() { return n }")


class TestReturnPlacement:
    def test_return_in_function(self):
        analyze("fn f() { return 42 }")

    def test_return_outside_function(self):
        analyze_err("return 42")


class TestBreakContinuePlacement:
    def test_break_in_loop(self):
        analyze("while true { break }")

    def test_break_outside_loop(self):
        analyze_err("break")

    def test_continue_in_loop(self):
        analyze("while true { continue }")

    def test_continue_outside_loop(self):
        analyze_err("continue")

    def test_break_in_nested_loop(self):
        analyze("while true { while true { break } }")


class TestScoping:
    def test_nested_scope(self):
        analyze("""
            let x = 1
            if true {
                let y = 2
            }
        """)

    def test_for_loop_variable(self):
        analyze("""
            for i in range(10) {
                println(i)
            }
        """)
