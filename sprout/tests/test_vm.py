"""Tests for the Sprout VM and compiler."""

import pytest
from sprout.interpreter import run_string
from sprout.vm import SproutError
from sprout.lexer import LexerError
from sprout.parser import ParseError
from sprout.semantic import SemanticError


def run(src):
    """Run Sprout source and return captured stdout."""
    return run_string(src)


def run_val(src):
    """Run a single expression and return the output line."""
    return run(f"println({src})").strip()


class TestArithmetic:
    def test_addition(self):
        assert run_val("1 + 2") == "3"

    def test_subtraction(self):
        assert run_val("10 - 3") == "7"

    def test_multiplication(self):
        assert run_val("6 * 7") == "42"

    def test_integer_division(self):
        assert run_val("7 / 2") == "3"

    def test_float_division(self):
        assert run_val("7.0 / 2") == "3.5"

    def test_modulo(self):
        assert run_val("17 % 5") == "2"

    def test_power(self):
        assert run_val("2 ** 10") == "1024"

    def test_negation(self):
        assert run_val("-5") == "-5"

    def test_precedence(self):
        assert run_val("2 + 3 * 4") == "14"

    def test_parentheses(self):
        assert run_val("(2 + 3) * 4") == "20"

    def test_division_by_zero(self):
        with pytest.raises(SproutError):
            run("let x = 1 / 0")


class TestComparisons:
    def test_equal(self):
        assert run_val("1 == 1") == "true"
        assert run_val("1 == 2") == "false"

    def test_not_equal(self):
        assert run_val("1 != 2") == "true"

    def test_less_than(self):
        assert run_val("3 < 5") == "true"
        assert run_val("5 < 3") == "false"

    def test_greater_than(self):
        assert run_val("5 > 3") == "true"

    def test_less_equal(self):
        assert run_val("3 <= 3") == "true"
        assert run_val("4 <= 3") == "false"

    def test_greater_equal(self):
        assert run_val("3 >= 3") == "true"


class TestLogical:
    def test_and_true(self):
        assert run_val("true and true") == "true"

    def test_and_false(self):
        assert run_val("true and false") == "false"

    def test_or_true(self):
        assert run_val("false or true") == "true"

    def test_or_false(self):
        assert run_val("false or false") == "false"

    def test_not(self):
        assert run_val("not true") == "false"
        assert run_val("not false") == "true"

    def test_short_circuit_and(self):
        # 'and' should not evaluate right side if left is false
        out = run("let x = false and (1/0 > 0); println(x)")
        assert out.strip() == "false"

    def test_short_circuit_or(self):
        out = run("let x = true or (1/0 > 0); println(x)")
        assert out.strip() == "true"


class TestVariables:
    def test_declare_and_use(self):
        out = run("let x = 42; println(x)")
        assert out.strip() == "42"

    def test_reassign(self):
        out = run("let x = 1; x = 99; println(x)")
        assert out.strip() == "99"

    def test_compound_assign(self):
        out = run("let x = 10; x += 5; println(x)")
        assert out.strip() == "15"

    def test_multiple_vars(self):
        out = run("let a = 1; let b = 2; println(a + b)")
        assert out.strip() == "3"


class TestStrings:
    def test_concat(self):
        assert run_val('"hello" + " " + "world"') == "hello world"

    def test_repeat(self):
        assert run_val('"ab" * 3') == "ababab"

    def test_len(self):
        assert run_val('len("hello")') == "5"

    def test_upper(self):
        assert run_val('upper("hello")') == "HELLO"

    def test_lower(self):
        assert run_val('lower("WORLD")') == "world"

    def test_contains(self):
        assert run_val('contains("foobar", "foo")') == "true"

    def test_replace(self):
        assert run_val('replace("hello world", "world", "Sprout")') == "hello Sprout"

    def test_split(self):
        assert run_val('split("a,b,c", ",")') == "[a, b, c]"

    def test_join(self):
        assert run_val('join(["a", "b", "c"], "-")') == "a-b-c"

    def test_index(self):
        assert run_val('"hello"[1]') == "e"

    def test_trim(self):
        assert run_val('trim("  hi  ")') == "hi"


class TestArrays:
    def test_empty_array(self):
        assert run_val("[]") == "[]"

    def test_array_elements(self):
        assert run_val("[1, 2, 3]") == "[1, 2, 3]"

    def test_index(self):
        assert run_val("[10, 20, 30][1]") == "20"

    def test_len(self):
        assert run_val("len([1, 2, 3])") == "3"

    def test_append(self):
        out = run("let a = [1, 2]; append(a, 3); println(a)")
        assert out.strip() == "[1, 2, 3]"

    def test_pop(self):
        out = run("let a = [1, 2, 3]; let v = pop(a); println(v); println(a)")
        lines = out.strip().split("\n")
        assert lines[0] == "3"
        assert lines[1] == "[1, 2]"

    def test_mutation(self):
        out = run("let a = [1, 2, 3]; a[0] = 99; println(a)")
        assert out.strip() == "[99, 2, 3]"

    def test_concat(self):
        assert run_val("[1, 2] + [3, 4]") == "[1, 2, 3, 4]"

    def test_out_of_bounds(self):
        with pytest.raises(SproutError):
            run("let a = [1]; println(a[5])")


class TestDicts:
    def test_empty_dict(self):
        assert run_val("{}") == "{}"

    def test_dict_access(self):
        assert run_val('{"a": 1}["a"]') == "1"

    def test_dict_mutation(self):
        out = run('let d = {"x": 1}; d["x"] = 99; println(d["x"])')
        assert out.strip() == "99"

    def test_keys(self):
        out = run('let d = {"a": 1}; println(len(keys(d)))')
        assert out.strip() == "1"

    def test_has(self):
        assert run_val('has({"k": 1}, "k")') == "true"
        assert run_val('has({"k": 1}, "z")') == "false"

    def test_missing_key(self):
        with pytest.raises(SproutError):
            run('let d = {}; println(d["missing"])')


class TestIfElse:
    def test_if_true(self):
        out = run("if true { println(1) }")
        assert out.strip() == "1"

    def test_if_false(self):
        out = run("if false { println(1) } else { println(2) }")
        assert out.strip() == "2"

    def test_elif(self):
        out = run("""
            let x = 50
            if x > 90 { println("A") }
            else if x > 70 { println("B") }
            else if x > 50 { println("C") }
            else { println("D") }
        """)
        assert out.strip() == "D"

    def test_nested_if(self):
        out = run("""
            let x = 5
            let y = 10
            if x > 0 {
                if y > 0 {
                    println("both positive")
                }
            }
        """)
        assert out.strip() == "both positive"


class TestWhileLoop:
    def test_basic_while(self):
        out = run("""
            let i = 0
            while i < 3 {
                println(i)
                i += 1
            }
        """)
        assert out.strip() == "0\n1\n2"

    def test_while_break(self):
        out = run("""
            let i = 0
            while true {
                if i >= 3 { break }
                println(i)
                i += 1
            }
        """)
        assert out.strip() == "0\n1\n2"

    def test_while_continue(self):
        out = run("""
            let i = 0
            while i < 5 {
                i += 1
                if i % 2 == 0 { continue }
                println(i)
            }
        """)
        assert out.strip() == "1\n3\n5"


class TestForLoop:
    def test_for_range(self):
        out = run("""
            for i in range(3) {
                println(i)
            }
        """)
        assert out.strip() == "0\n1\n2"

    def test_for_range_start_stop(self):
        out = run("""
            for i in range(2, 5) {
                println(i)
            }
        """)
        assert out.strip() == "2\n3\n4"

    def test_for_over_array(self):
        out = run("""
            for x in [10, 20, 30] {
                println(x)
            }
        """)
        assert out.strip() == "10\n20\n30"

    def test_for_over_string(self):
        out = run("""
            for ch in "abc" {
                println(ch)
            }
        """)
        assert out.strip() == "a\nb\nc"

    def test_for_with_break(self):
        out = run("""
            for i in range(10) {
                if i == 3 { break }
                println(i)
            }
        """)
        assert out.strip() == "0\n1\n2"


class TestFunctions:
    def test_basic_function(self):
        out = run("""
            fn square(x) { return x * x }
            println(square(5))
        """)
        assert out.strip() == "25"

    def test_function_default_param(self):
        out = run("""
            fn greet(name, greeting = "Hello") {
                return greeting + ", " + name + "!"
            }
            println(greet("Alice"))
            println(greet("Bob", "Hi"))
        """)
        lines = out.strip().split("\n")
        assert lines[0] == "Hello, Alice!"
        assert lines[1] == "Hi, Bob!"

    def test_recursion(self):
        out = run("""
            fn fact(n) {
                if n <= 1 { return 1 }
                return n * fact(n - 1)
            }
            println(fact(6))
        """)
        assert out.strip() == "720"

    def test_first_class_function(self):
        out = run("""
            fn apply(f, x) { return f(x) }
            fn double(x) { return x * 2 }
            println(apply(double, 7))
        """)
        assert out.strip() == "14"

    def test_anonymous_function(self):
        out = run("""
            let triple = fn(x) { return x * 3 }
            println(triple(4))
        """)
        assert out.strip() == "12"

    def test_closure(self):
        out = run("""
            fn make_adder(n) {
                return fn(x) { return x + n }
            }
            let add10 = make_adder(10)
            println(add10(5))
            println(add10(20))
        """)
        lines = out.strip().split("\n")
        assert lines[0] == "15"
        assert lines[1] == "30"

    def test_too_few_args(self):
        with pytest.raises(SproutError):
            run("fn f(a, b) { } f(1)")

    def test_too_many_args(self):
        with pytest.raises(SproutError):
            run("fn f(a) { } f(1, 2, 3)")

    def test_implicit_nil_return(self):
        out = run("""
            fn f() { }
            let x = f()
            println(x)
        """)
        assert out.strip() == "nil"


class TestBuiltins:
    def test_println(self):
        out = run('println("hello")')
        assert out == "hello\n"

    def test_print_no_newline(self):
        out = run('print("hi")')
        assert out == "hi"

    def test_type(self):
        assert run_val("type(42)") == "int"
        assert run_val("type(3.14)") == "float"
        assert run_val('type("s")') == "string"
        assert run_val("type(true)") == "bool"
        assert run_val("type(nil)") == "nil"
        assert run_val("type([])") == "array"
        assert run_val("type({})") == "dict"

    def test_str(self):
        assert run_val("str(42)") == "42"
        assert run_val("str(true)") == "true"
        assert run_val("str(nil)") == "nil"

    def test_int_conversion(self):
        assert run_val('int("42")') == "42"
        assert run_val("int(3.9)") == "3"

    def test_float_conversion(self):
        assert run_val('float("3.14")') == "3.14"

    def test_range(self):
        out = run("for i in range(3) { println(i) }")
        assert out.strip() == "0\n1\n2"

    def test_len_array(self):
        assert run_val("len([1, 2, 3])") == "3"

    def test_len_string(self):
        assert run_val('len("hello")') == "5"

    def test_sqrt(self):
        assert run_val("sqrt(9.0)") == "3.0"

    def test_abs(self):
        assert run_val("abs(-7)") == "7"

    def test_min_max(self):
        assert run_val("min(3, 1, 2)") == "1"
        assert run_val("max(3, 1, 2)") == "3"

    def test_assert_pass(self):
        run("assert(true)")  # should not raise

    def test_assert_fail(self):
        with pytest.raises(SproutError):
            run("assert(false, \"custom msg\")")


class TestImport:
    def test_math_module(self):
        out = run("""
            import math
            println(math["pi"] > 3)
        """)
        assert out.strip() == "true"

    def test_unknown_module(self):
        with pytest.raises(SproutError):
            run("import nonexistent")


class TestTypeConversion:
    def test_int_plus_float(self):
        assert run_val("1 + 1.5") == "2.5"

    def test_string_non_concat(self):
        with pytest.raises(SproutError):
            run('let x = "a" + 1')


class TestErrorHandling:
    def test_call_non_function(self):
        with pytest.raises(SproutError):
            run("let x = 42; x()")

    def test_undefined_variable(self):
        with pytest.raises(SemanticError):
            run("println(undefined)")

    def test_subscript_non_subscriptable(self):
        with pytest.raises(SproutError):
            run("let x = 42; x[0]")
