from flake8_plugin_utils import assert_error, assert_not_error

from flake8_qa_style.checkers.node_visitors import WithVisitor
from flake8_qa_style.errors import NestedWith
from tests.test_helpers import assert_errors


def test_nested_with_sync_in_sync():
    code = """\
    with open('a'):
        with open('b'):
            pass
    """
    assert_error(WithVisitor, code, NestedWith)


def test_nested_with_async_in_async():
    code = """\
    async with open('a'):
        async with open('b'):
            pass
    """
    assert_error(WithVisitor, code, NestedWith)


def test_nested_with_sync_in_async():
    code = """\
    async with open('a'):
        with open('b'):
            pass
    """
    assert_not_error(WithVisitor, code)


def test_nested_with_async_in_sync():
    code = """\
    with open('a'):
        async with open('b'):
            pass
    """
    assert_not_error(WithVisitor, code)


def test_single_with_no_error():
    code = """\
    with open('a'):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_single_async_with_no_error():
    code = """\
    async with open('a'):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_combined_with_parenthesized():
    code = """\
    with (
        open('a'),
        open('b'),
    ):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_nested_with_body_has_other_statements():
    code = """\
    with open('a'):
        x = 1
        with open('b'):
            pass
    """
    assert_not_error(WithVisitor, code)


def test_few_nested_with():
    code = """\
    with open('a'):
        with open('b'):
            with open('c'):
                pass
    """
    assert_errors(WithVisitor, code, [NestedWith, NestedWith])


def test_nested_with_single_item_each():
    code = """\
    with open('file') as f:
        with f.read() as data:
            pass
    """
    assert_error(WithVisitor, code, NestedWith)
