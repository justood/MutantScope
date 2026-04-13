
import pytest
from palindrome_checker import (
    is_palindrome,
    is_palindrome_strict,
    longest_palindromic_substring,
    count_palindromic_words,
)


# ═══════════════════════════════════════════════════════════════════
# SECTION A — is_palindrome (normalised)
# ═══════════════════════════════════════════════════════════════════

class TestIsPalindrome:

    # classic palindromes
    def test_racecar(self):
        assert is_palindrome("racecar") is True

    def test_level(self):
        assert is_palindrome("level") is True

    def test_madam(self):
        assert is_palindrome("madam") is True

    def test_hello_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_python_not_palindrome(self):
        assert is_palindrome("python") is False

    # case normalisation
    def test_case_insensitive_racecar(self):
        assert is_palindrome("RaceCar") is True

    def test_mixed_case_level(self):
        assert is_palindrome("LeVeL") is True

    # space and punctuation stripping
    def test_phrase_a_man_a_plan_a_canal_panama(self):
        assert is_palindrome("A man, a plan, a canal: Panama") is True

    def test_was_it_a_car(self):
        assert is_palindrome("Was it a car or a cat I saw?") is True

    def test_never_odd_or_even(self):
        assert is_palindrome("Never odd or even") is True

    # single-character and empty
    def test_single_char(self):
        assert is_palindrome("a") is True

    def test_empty_string(self):
        """Empty string should return True (mutation target)."""
        assert is_palindrome("") is True

    def test_only_spaces(self):
        """Spaces stripped → effectively empty → True."""
        assert is_palindrome("   ") is True

    def test_only_punctuation(self):
        assert is_palindrome("!!!") is True

    # two-character
    def test_two_same_chars(self):
        assert is_palindrome("aa") is True

    def test_two_different_chars(self):
        assert is_palindrome("ab") is False

    # numeric palindromes
    def test_numeric_palindrome(self):
        assert is_palindrome("12321") is True

    def test_numeric_not_palindrome(self):
        assert is_palindrome("12345") is False

    # type guard
    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            is_palindrome(12321)

    def test_none_raises(self):
        with pytest.raises(TypeError):
            is_palindrome(None)


class TestIsPalindromeStrict:

    def test_exact_palindrome(self):
        assert is_palindrome_strict("racecar") is True

    def test_case_matters(self):
        assert is_palindrome_strict("Racecar") is False

    def test_space_matters(self):
        assert is_palindrome_strict("race car") is False

    def test_empty_string(self):
        assert is_palindrome_strict("") is True

    def test_single_char(self):
        assert is_palindrome_strict("x") is True

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            is_palindrome_strict(123)


class TestLongestPalindromicSubstring:

    def test_basic(self):
        assert longest_palindromic_substring("babad") in ("bab", "aba")

    def test_single_char(self):
        assert longest_palindromic_substring("a") == "a"

    def test_empty_string(self):
        assert longest_palindromic_substring("") == ""

    def test_all_same_chars(self):
        assert longest_palindromic_substring("aaaa") == "aaaa"

    def test_no_palindrome_longer_than_1(self):
        result = longest_palindromic_substring("abcd")
        assert len(result) >= 1

    def test_even_length_palindrome(self):
        assert longest_palindromic_substring("abba") == "abba"

    def test_embedded_palindrome(self):
        assert longest_palindromic_substring("xabbayz") == "abba"

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            longest_palindromic_substring(["a", "b"])


class TestCountPalindromicWords:

    def test_basic(self):
        assert count_palindromic_words("racecar level hello") == 2

    def test_no_palindromes(self):
        assert count_palindromic_words("hello world") == 0

    def test_all_palindromes(self):
        assert count_palindromic_words("madam racecar level") == 3

    def test_empty_string(self):
        assert count_palindromic_words("") == 0

    def test_single_palindrome(self):
        assert count_palindromic_words("noon") == 1

    def test_punctuation_in_words(self):
        # "A" → palindrome after normalisation
        assert count_palindromic_words("A") == 1