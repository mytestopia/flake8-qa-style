import ast

from flake8_qa_style.checkers.node_visitors._node_visitor import NodeVisitor
from flake8_qa_style.errors import AsyncFunctionWithoutAsynchronous


class _AwaitFinder(ast.NodeVisitor):
    def __init__(self):
        self.has_await = False

    def visit_Await(self, _node: ast.Await):
        self.has_await = True

    def visit_AsyncWith(self, _node: ast.AsyncWith):
        self.has_await = True

    def visit_AsyncFor(self, _node: ast.AsyncFor):
        self.has_await = True

    def visit_AsyncFunctionDef(self, _node: ast.AsyncFunctionDef):
        pass  # don't descend into nested async functions


class AsyncVisitor(NodeVisitor):

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        finder = _AwaitFinder()
        for child in ast.iter_child_nodes(node):
            finder.visit(child)

        if not finder.has_await:
            self.error_from_node(AsyncFunctionWithoutAsynchronous, node, func_name=node.name)

        self.generic_visit(node)
