import argparse
import ast
from typing import Callable, List, Optional

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin, Visitor

from flake8_qa_style.checkers.node_visitors import (
    AnnotationVisitor,
    AssertVisitor,
    AsyncVisitor,
    FunctionCallVisitor,
    WithVisitor,
)
from flake8_qa_style.checkers.raw_checkers import FileStartChecker

from .checkers.raw_checkers._raw_checker import RawChecker
from .config import Config


def str_to_bool(string):
    return string.lower() in ('true', 'yes', 't', '1')


class QAStylePlugin(Plugin):
    name = 'flake8_qa_style'
    version = '1.2.0'

    visitors = [
        AnnotationVisitor,
        FunctionCallVisitor,
        AssertVisitor,
        AsyncVisitor,
        WithVisitor,
    ]

    checkers = [
        FileStartChecker,
    ]

    def __init__(self, tree: ast.AST, filename: str, lines: list[str]):
        super().__init__(tree)
        self.filename = filename
        self.lines = lines

    def run(self):
        for checker_cls in self.checkers:
            checker = self._create_checker(checker_cls, filename=self.filename, lines=self.lines)
            checker.check()
            for error in checker.errors:
                yield self._error(error)

        for visitor_cls in self.visitors:
            visitor = self._create_visitor(visitor_cls, filename=self.filename)
            visitor.visit(self._tree)
            for error in visitor.errors:
                yield self._error(error)

    @classmethod
    def _create_checker(
        cls, checker_cls: Callable, filename: Optional[str] = None, lines: Optional[list[str]] = None
    ) -> RawChecker:
        kwargs = {}

        if filename is not None:
            kwargs['filename'] = filename
        if lines is not None:
            kwargs['lines'] = lines

        return checker_cls(**kwargs)

    @classmethod
    def _create_visitor(
        cls, visitor_cls: Callable, filename: Optional[str] = None
    ) -> Visitor:
        kwargs = {}

        if filename is not None:
            kwargs['filename'] = filename
        if cls.config is not None:
            kwargs['config'] = cls.config

        return visitor_cls(**kwargs)

    @classmethod
    def add_options(cls, option_manager: OptionManager):
        option_manager.add_option(
            '--skip-property-return-annotation',
            type=str,
            default='false',
            parse_from_config=True,
            help='Flag to skip return value annotation check. '
                 '(Default: False)',
        )

    @classmethod
    def parse_options_to_config(
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(
            skip_property_return_annotation=str_to_bool(options.skip_property_return_annotation),
        )
