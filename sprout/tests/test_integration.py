"""Integration tests: run full example programs and check expected output."""

import subprocess
import sys
import os
import pytest

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")
PYTHON = sys.executable


def run_example(filename):
    path = os.path.join(EXAMPLES_DIR, filename)
    result = subprocess.run(
        [PYTHON, "-m", "sprout", path],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    return result.returncode, result.stdout, result.stderr


class TestExamples:
    def test_01_hello_world(self):
        rc, out, _ = run_example("01_hello_world.sp")
        assert rc == 0
        assert "Hello, World!" in out

    def test_02_variables(self):
        rc, out, _ = run_example("02_variables.sp")
        assert rc == 0
        assert "Sprout" in out
        assert "3.14159" in out
        assert "true" in out
        assert "nil" in out

    def test_03_arithmetic(self):
        rc, out, _ = run_example("03_arithmetic.sp")
        assert rc == 0
        assert "a + b = 22" in out
        assert "a % b = 2" in out

    def test_04_strings(self):
        rc, out, _ = run_example("04_strings.sp")
        assert rc == 0
        assert "HELLO, SPROUT!" in out
        assert "hello, sprout!" in out

    def test_05_arrays(self):
        rc, out, _ = run_example("05_arrays.sp")
        assert rc == 0
        assert "[10, 20, 99, 40, 50]" in out

    def test_06_dicts(self):
        rc, out, _ = run_example("06_dicts.sp")
        assert rc == 0
        assert "Alice" in out
        assert "Japan" in out

    def test_07_functions(self):
        rc, out, _ = run_example("07_functions.sp")
        assert rc == 0
        assert "Hello, Alice!" in out
        assert "3628800" in out  # 10!
        assert "add5(10) = 15" in out

    def test_08_control_flow(self):
        rc, out, _ = run_example("08_control_flow.sp")
        assert rc == 0
        assert "Grade: B" in out
        assert "Found: 2 * 3 = 6" in out

    def test_09_fibonacci(self):
        rc, out, _ = run_example("09_fibonacci.sp")
        assert rc == 0
        assert "832040" in out  # fib(30)

    def test_10_sorting(self):
        rc, out, _ = run_example("10_sorting.sp")
        assert rc == 0
        assert "[11, 12, 22, 25, 34, 64, 90]" in out

    def test_11_higher_order(self):
        rc, out, _ = run_example("11_higher_order.sp")
        assert rc == 0
        assert "Sum of squares of evens: 220" in out

    def test_12_recursion(self):
        rc, out, _ = run_example("12_recursion.sp")
        assert rc == 0
        assert "Move disk 3 from A to C" in out
        assert "Search 23 at index: 5" in out

    def test_13_closures(self):
        rc, out, _ = run_example("13_closures.sp")
        assert rc == 0
        assert "fib(10) = 55" in out
        assert "add10(5) = 15" in out

    def test_14_primes(self):
        rc, out, _ = run_example("14_primes.sp")
        assert rc == 0
        assert "Total primes <= 100: 25" in out
        assert "Factors of 360: [2, 2, 2, 3, 3, 5]" in out

    def test_15_linked_list(self):
        rc, out, _ = run_example("15_linked_list.sp")
        assert rc == 0
        assert "Reversed:  [1, 2, 3, 4, 5]" in out

    def test_16_stack_queue(self):
        rc, out, _ = run_example("16_stack_queue.sp")
        assert rc == 0
        assert "balanced? true" in out
        assert "1  2  3  4  5" in out

    def test_17_string_processing(self):
        rc, out, _ = run_example("17_string_processing.sp")
        assert rc == 0
        assert "racecar -> true" in out
        assert "hello -> false" in out

    def test_18_math_module(self):
        rc, out, _ = run_example("18_math_module.sp")
        assert rc == 0
        assert "gcd(48, 18) = 6" in out
        assert "digit_sum(9875) = 29" in out

    def test_19_fizzbuzz(self):
        rc, out, _ = run_example("19_fizzbuzz.sp")
        assert rc == 0
        assert "FizzBuzz" in out
        assert "Fizz:      8" in out

    def test_20_game_of_life(self):
        rc, out, _ = run_example("20_game_of_life.sp")
        assert rc == 0
        assert "Generation 0" in out
        assert "Generation 4" in out
