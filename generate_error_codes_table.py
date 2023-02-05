"""Tool to generate all possible error messages/codes for this package."""
from itertools import product

from flake8_no_implicit_str_concat_in_list import TYPE_NUM_MAPPINGS
from flake8_no_implicit_str_concat_in_list import _map_error  # noqa: H306

for parent_type_name, is_bytes, is_on_same_line in product(
    TYPE_NUM_MAPPINGS.keys(), [True, False], [False, True]
):
    error_code, message = _map_error(parent_type_name, is_on_same_line, is_bytes)
    print(f"| {error_code} | {message:<80} |")
