import ast

from flake8_qa_style.checkers.node_visitors._node_visitor import NodeVisitor
from flake8_qa_style.errors import NestedWith, WithItemsOnSameLine


class WithVisitor(NodeVisitor):

    def _check_nested_with(self, node: ast.With | ast.AsyncWith) -> None:
        is_async = isinstance(node, ast.AsyncWith)

        # Check for nested "with" of the same type (sync-in-sync or async-in-async)
        if len(node.body) == 1:
            inner = node.body[0]
            if is_async and isinstance(inner, ast.AsyncWith):
                self.error_from_node(NestedWith, node)
            elif not is_async and isinstance(inner, ast.With):
                self.error_from_node(NestedWith, node)

    @staticmethod
    def _with_item_end_lineno(item: ast.withitem) -> int:
        if item.optional_vars is not None:
            return item.optional_vars.end_lineno
        return item.context_expr.end_lineno

    def _check_with_items_on_same_line(self, node: ast.With | ast.AsyncWith) -> None:
        items = node.items
        if len(items) < 2:
            return

        for prev_item, next_item in zip(items, items[1:]):
            if self._with_item_end_lineno(prev_item) >= next_item.context_expr.lineno:
                self.error_from_node(WithItemsOnSameLine, node)
                return

    def visit_With(self, node: ast.With) -> None:
        self._check_nested_with(node)
        self._check_with_items_on_same_line(node)
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self._check_nested_with(node)
        self._check_with_items_on_same_line(node)
        self.generic_visit(node)
