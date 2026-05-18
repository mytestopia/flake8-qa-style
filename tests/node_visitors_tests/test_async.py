from flake8_plugin_utils import assert_error, assert_not_error

from flake8_qa_style.checkers.node_visitors import AsyncVisitor
from flake8_qa_style.errors import AsyncFunctionWithoutAsynchronous


def test_async_function_without_await():
    code = """
    async def foo():
        return 1
    """
    assert_error(AsyncVisitor, code, AsyncFunctionWithoutAsynchronous, func_name='foo')


def test_async_function_with_await():
    code = """
    async def foo():
        await bar()
    """
    assert_not_error(AsyncVisitor, code)


def test_async_function_with_await_in_loop():
    code = """
    async def foo():
        for i in range(10):
            await bar(i)
    """
    assert_not_error(AsyncVisitor, code)


def test_async_function_with_await_in_if():
    code = """
    async def foo():
        if True:
            await bar()
    """
    assert_not_error(AsyncVisitor, code)


def test_async_function_with_await_in_with():
    code = """
    async def foo():
        async with ctx() as c:
            pass
    """
    assert_not_error(AsyncVisitor, code)


def test_async_function_with_await_for():
    code = """
    async def foo():
        async for item in aiter():
            pass
    """
    assert_not_error(AsyncVisitor, code)


def test_nested_async_without_await_outer():
    code = """
    async def outer():
        async def inner():
            await bar()
    """
    assert_error(AsyncVisitor, code, AsyncFunctionWithoutAsynchronous, func_name='outer')


def test_nested_async_without_await_inner():
    code = """
    async def outer():
        await bar()
        async def inner():
            return 1
    """
    assert_error(AsyncVisitor, code, AsyncFunctionWithoutAsynchronous, func_name='inner')


def test_sync_function_no_error():
    code = """
    def foo():
        return 1
    """
    assert_not_error(AsyncVisitor, code)


def test_async_function_only_sync_calls():
    code = """
    async def foo():
        bar()
        baz()
    """
    assert_error(AsyncVisitor, code, AsyncFunctionWithoutAsynchronous, func_name='foo')


def test_async_function_with_await_in_expr():
    code = """
    async def foo(self):
        self.var = 5 *(1 + (await self.bar())[0])
    """
    assert_not_error(AsyncVisitor, code)


def test_async_method_without_await():
    code = """
    class MyClass:
        async def method(self):
            return 1
    """
    assert_error(AsyncVisitor, code, AsyncFunctionWithoutAsynchronous, func_name='method')


def test_async_method_with_await():
    code = """
    class MyClass:
        async def method(self):
            await self.do_something()
    """
    assert_not_error(AsyncVisitor, code)
