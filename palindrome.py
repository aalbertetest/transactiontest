"""Two approaches to palindrome detection."""

import re


def _normalize(s: str) -> str:
    """Lowercase and strip non-alphanumeric characters."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


# Approach 1 – Slice reversal (Pythonic one-liner)
def is_palindrome_slice(s: str) -> bool:
    """Return True if *s* is a palindrome, using slice reversal."""
    cleaned = _normalize(s)
    return cleaned == cleaned[::-1]


# Approach 2 – Two-pointer comparison
def is_palindrome_two_pointer(s: str) -> bool:
    """Return True if *s* is a palindrome, using two converging pointers."""
    cleaned = _normalize(s)
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True
