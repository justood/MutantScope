
# ──────────────────────────────────────────────
# SECTION 1: Palindrome Checker
# ──────────────────────────────────────────────

import re
import string
from collections import Counter

def is_palindrome(text: str) -> bool:
    """
    Return True if *text* is a palindrome after normalising to
    lowercase alphanumeric characters only.

    Mutation targets:
        - reversed comparison (== vs !=)
        - character-filter logic (isalnum)
        - empty-string return value
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())

    if len(cleaned) == 0:
        return True  # mutation target: True vs False

    return cleaned == cleaned[::-1]


def is_palindrome_strict(text: str) -> bool:
    """
    Palindrome check WITHOUT normalisation — spaces and case matter.

    Mutation target: the equality comparison.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return text == text[::-1]


def longest_palindromic_substring(text: str) -> str:
    """
    Find the longest palindromic substring using expand-around-centre.

    Returns the empty string when text is empty.
    Mutation targets: loop bounds, slice indices, length comparison.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if len(text) == 0:
        return ""

    start, end = 0, 0

    def expand(left: int, right: int) -> tuple:
        while left >= 0 and right < len(text) and text[left] == text[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for i in range(len(text)):
        # odd-length palindromes
        l, r = expand(i, i)
        if r - l > end - start:
            start, end = l, r

        # even-length palindromes
        l, r = expand(i, i + 1)
        if r - l > end - start:
            start, end = l, r

    return text[start:end + 1]


def count_palindromic_words(sentence: str) -> int:
    """
    Count how many words in *sentence* are palindromes (case-insensitive,
    alphanumeric only).

    Mutation targets: word extraction, the count increment, return value.
    """
    if not isinstance(sentence, str):
        raise TypeError("Input must be a string")

    words = sentence.split()
    return sum(1 for w in words if is_palindrome(w))