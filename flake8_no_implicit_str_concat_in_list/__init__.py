"""Flake8 plugin that forbids implicit str/bytes literal concatenations inside literals such as lists, sets and tuples."""

import ast
import tokenize
import typing

from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from ._version import __version__

_ERROR = Tuple[int, int, str, None]


def _get_node_start_position_tuple(node: ast.AST) -> Tuple[int, int]:
    return node.lineno, node.col_offset


_WS_TOKENS = (
    tokenize.NL,
    tokenize.NEWLINE,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.COMMENT,
)

TYPE_NUM_MAPPINGS = {list.__name__: 1, tuple.__name__: 2, set.__name__: 3}


def _map_error(
    parent_type_name: str, is_on_same_line: bool, is_bytes: bool
) -> typing.Tuple[str, str]:
    t_num = TYPE_NUM_MAPPINGS.get(parent_type_name, 0)
    return (
        f"ICL{t_num}{1 if is_on_same_line else 2}{1 if not is_bytes else 2}",
        f"Implicitly concatenated {'str' if not is_bytes else 'bytes'} literals"
        + f" in {parent_type_name} literal{'' if is_on_same_line else ' over multiple lines'}.",
    )


class _NoImplicitConcatInsideIterableLiteralVisitor(ast.NodeVisitor):
    def __init__(self, file_tokens: Iterable[tokenize.TokenInfo]):
        self.file_tokens = file_tokens
        self.errors: List[_ERROR] = []

    def check_tokens_for_node(
        self,
        node: ast.AST,
        parent_type_name: str,
        ignore_start_tokens: Iterable[int] = (),
    ) -> None:
        last_token: Optional[tokenize.TokenInfo] = None
        node_pos = _get_node_start_position_tuple(node)
        found_start = False
        for token in self.file_tokens:
            if node_pos > token.start:
                continue
            if node_pos == token.start:
                found_start = True
            elif not found_start and node_pos < token.start:
                raise RuntimeError(
                    f"Missed start token, current token at {token.start}, node starting at {node_pos}"
                )
            if token.type in _WS_TOKENS:
                continue
            if token.type == tokenize.STRING:
                if last_token is not None:
                    if isinstance(node, ast.Constant) and isinstance(node.value, bytes):
                        is_bytes = True
                    else:
                        is_bytes = False
                    error_data = _map_error(
                        parent_type_name,
                        is_on_same_line=node_pos[0] != last_token.end[0],
                        is_bytes=is_bytes,
                    )
                    self.errors.append(
                        (
                            last_token.end[0],
                            last_token.end[1],
                            error_data[0] + " " + error_data[1],
                            None,
                        )
                    )
                last_token = token
            elif last_token is not None or token.type not in ignore_start_tokens:
                break

    def handle_iterable_type(self, node: ast.AST) -> None:
        class_name: str = node.__class__.__name__.lower()
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Constant):
                if isinstance(child.value, str) or isinstance(child.value, bytes):
                    self.check_tokens_for_node(child, class_name)
            elif isinstance(child, ast.FormattedValue):
                self.check_tokens_for_node(child, class_name)
            elif isinstance(child, ast.JoinedStr):
                self.check_tokens_for_node(child, class_name)
        self.generic_visit(node)

    def visit_List(self, node: ast.List) -> None:  # noqa: N802
        self.handle_iterable_type(node)

    def visit_Set(self, node: ast.Set) -> None:  # noqa: N802
        self.handle_iterable_type(node)

    def visit_Tuple(self, node: ast.Tuple) -> None:  # noqa: N802
        self.handle_iterable_type(node)

    def visit_Constant(self, node: ast.Constant) -> None:  # noqa: N802
        if isinstance(node.value, tuple):
            self.check_tokens_for_node(
                node, "tuple", ignore_start_tokens=(tokenize.LPAR,)
            )
        self.generic_visit(node)


class Checker:
    """ICL Checker definition."""

    name = "no_implicit_str_concat_in_list"
    version = __version__

    def __init__(self, tree: ast.AST, file_tokens: Iterable[tokenize.TokenInfo]):
        """Intialize Checker.

        :param tree: File AST
        :param file_tokens: File tokens
        """
        self.tree = tree
        self.file_tokens = file_tokens
        return

    def run(self) -> Iterable[_ERROR]:
        """Run checker.

        :yields: Errors found.
        """
        visitor = _NoImplicitConcatInsideIterableLiteralVisitor(self.file_tokens)
        visitor.visit(self.tree)
        yield from visitor.errors
