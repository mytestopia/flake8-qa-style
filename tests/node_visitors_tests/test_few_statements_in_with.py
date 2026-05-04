from flake8_plugin_utils import assert_error, assert_not_error

from flake8_qa_style.checkers.node_visitors import WithVisitor
from flake8_qa_style.errors import WithItemsOnSameLine


def test_combined_with_comma_on_same_line():
    code = """\
    with open('a'), open('b'):
        pass
    """
    assert_error(WithVisitor, code, WithItemsOnSameLine)


def test_combined_with_comma_as_clause():
    code = """\
    with open('a') as f, open('b'):
        pass
    """
    assert_error(WithVisitor, code, WithItemsOnSameLine)


def test_parenthesized_items_on_same_line():
    code = """\
    with (
        open('a') as something, open('b'),
    ):
        pass
    """
    assert_error(WithVisitor, code, WithItemsOnSameLine)


def test_parenthesized_multiline_call_items_on_same_line():
    code = """\
    with (
        open(
            'a',
        ) as something, open('b'),
    ):
        pass
    """
    assert_error(WithVisitor, code, WithItemsOnSameLine)


def test_async_combined_with_comma_on_same_line():
    code = """\
    async with open('a'), open('b'):
        pass
    """
    assert_error(WithVisitor, code, WithItemsOnSameLine)


def test_parenthesized_each_on_own_line():
    code = """\
    with (
        open('a') as something,
        open('b'),
    ):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_parenthesized_multiline_call_each_on_own_line():
    code = """\
    with (
        open(
            'a',
        ) as something,
        open('b'),
    ):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_async_parenthesized_each_on_own_line():
    code = """\
    async with (
        open('a'),
        open('b'),
    ):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_backslash_each_on_own_line():
    code = """\
    with open('a') as something, \\
         open('b'):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_backslash_multiline_call_each_on_own_line():
    code = """\
    with open(
        'a',
    ) as something, \\
         open('b'):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_async_backslash_each_on_own_line():
    code = """\
    async with open('a'), \\
               open('b'):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_backslash_items_on_same_line():
    code = """\
    with open('a'), open('b') \\
         :
        pass
    """
    assert_error(WithVisitor, code, WithItemsOnSameLine)


def test_backslash_three_items_each_on_own_line():
    code = """\
    with open('a') as f, \\
         open('b') as g, \\
         open('c'):
        pass
    """
    assert_not_error(WithVisitor, code)


def test_list_in_with_statement():
    code = """\
    with mock([1, 2, 3]):
        pass
    """
    assert_not_error(WithVisitor, code)
