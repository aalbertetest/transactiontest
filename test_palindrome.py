"""Tests for both palindrome implementations."""

import pytest
from palindrome import is_palindrome_slice, is_palindrome_two_pointer

IMPLEMENTATIONS = [is_palindrome_slice, is_palindrome_two_pointer]


@pytest.mark.parametrize("fn", IMPLEMENTATIONS)
@pytest.mark.parametrize(
    "text, expected",
    [
        ("racecar", True),
        ("A man, a plan, a canal: Panama", True),
        ("Madam", True),
        ("", True),
        ("a", True),
        ("ab", False),
        ("hello", False),
        ("Was it a car or a cat I saw?", True),
        ("No 'x' in Nixon", True),
        ("not a palindrome", False),
    ],
)
def test_palindrome(fn, text, expected):
    assert fn(text) is expected
