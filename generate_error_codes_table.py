from itertools import product
from flake8_no_implicit_str_concat_in_list import map_error, TYPE_NUM_MAPPINGS

for parent_type_name,is_bytes,is_on_same_line  in product(TYPE_NUM_MAPPINGS.keys(),[True, False], [False, True] ):
    error_code, message = map_error(parent_type_name, is_on_same_line, is_bytes)
    print(f"| {error_code} | {message:<80} |")
