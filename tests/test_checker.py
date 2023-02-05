"""Test ICL Chekcer."""

import ast
import tokenize
import unittest

from io import BytesIO
from typing import Iterable

from flake8_no_implicit_str_concat_in_list import Checker


def _tokenize(input_: str) -> Iterable[tokenize.TokenInfo]:
    return tokenize.tokenize(BytesIO(input_.encode("utf-8")).readline)


class TestChecker(unittest.TestCase):
    """Test ICL Chekcer."""

    def test_noerror(self) -> None:
        """Test checker with valid input."""
        input_ = "a = 'aaa'"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 0)
        return

    def test_error_in_list(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = ['aaa' 'bbb']"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 1)
        return

    def test_error_in_multiline_list(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = """
a = [
 'aaa' 
 'bbb'
]
"""
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 1)
        return

    def test_error_in_list_format_string(self) -> None:
            """Test checker with invalid input."""
            # Contents of results are checked in run_flake8/
            input_ = 'a = [f"{1+1}" ""]'
            checker = Checker(ast.parse(input_), _tokenize(input_))
            result = checker.run()
            self.assertEqual(len(list(result)), 1)
            return
    def test_error_in_list_format_string_single_interpolation(self) -> None:
            """Test checker with invalid input."""
            # Contents of results are checked in run_flake8/
            input_ = 'a = [f"a{1+1}" f"b{2+2}"]'
            checker = Checker(ast.parse(input_), _tokenize(input_))
            result = checker.run()
            self.assertEqual(len(list(result)), 1)
            return
    def test_no_error_in_list_format_string(self) -> None:
            """Test checker with invalid input."""
            # Contents of results are checked in run_flake8/
            
            input_ = 'a = [f"a{1+1}b{2+2}"]'
            checker = Checker(ast.parse(input_), _tokenize(input_))
            result = checker.run()
            self.assertEqual(len(list(result)), 0)
            return
    def test_no_error_in_list(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = ['aaa', 'bbb']"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 0)
        return

    def test_error_in_tuple(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = ('aaa' 'bbb',)"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 1)
        return
    def test_error_in_tuple_no_parenthesis(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = 'aaa' 'bbb', 'cc'"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 1)
        return
    def test_no_error_in_tuple(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = ('aaa', 'bbb',)"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 0)
        return

    def test_error_in_set(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = {'aaa' 'bbb'}"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 1)
        return

    def test_no_error_in_set(self) -> None:
        """Test checker with invalid input."""
        # Contents of results are checked in run_flake8/
        input_ = "a = {'aaa', 'bbb'}"
        checker = Checker(ast.parse(input_), _tokenize(input_))
        result = checker.run()
        self.assertEqual(len(list(result)), 0)
        return


if __name__ == "__main__":
    unittest.main()
