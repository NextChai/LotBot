"""
MIT License

Copyright (c) 2022 NextChai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import logging
import time
import asyncio
import asyncpg
from typing import TYPE_CHECKING, Tuple, Union, Type, Any, Dict, TypeVar, Callable, Optional, Awaitable, Coroutine, ParamSpec
from typing_extensions import Self

import discord
from discord.ext import commands

from utils.context import Context

if TYPE_CHECKING:
    import aiohttp

    from utils import Interaction

__all__: Tuple[str, ...] = ("LotBot",)

T = TypeVar("T")
P = ParamSpec("P")

log = logging.getLogger(__name__)

initial_extensions: Tuple[str, ...] = (
    # Utilities
    "jishaku",
)


def _wrap_extension(func: Callable[P, Awaitable[T]]) -> Callable[P, Coroutine[Any, Any, Optional[T]]]:
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> Optional[T]:
        fmt_args = 'on ext "{}"{}'.format(args[1], f" with kwargs {kwargs}" if kwargs else "")
        start = time.perf_counter()

        try:
            result = await func(*args, **kwargs)
        except Exception as exc:
            return log.warning(
                f"Failed to load extension in {time.perf_counter() - start:.2f} seconds {fmt_args}", exc_info=exc
            )

        fmt = f"{func.__name__} took {time.perf_counter() - start:.2f} seconds {fmt_args}"
        log.info(fmt)

        return result

    return wrapped


class LotBot(commands.Bot):
    """The main LotBot instance! This inherits :class:`~commands.Bot` and adds some extra
    functionality to it that makes the bot's commands more usable.

    Attributes
    ----------
    pool: :class:`asyncpg.Pool`
        The database pool.
    session: :class:`aiohttp.ClientSession`
        The aiohttp session.
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop for the bot.
    """

    def __init__(
        self, pool: asyncpg.Pool[asyncpg.Record], session: aiohttp.ClientSession, loop: asyncio.AbstractEventLoop
    ) -> None:
        self.pool: asyncpg.Pool[asyncpg.Record] = pool
        self.session: aiohttp.ClientSession = session
        self.loop: asyncio.AbstractEventLoop = loop

    @classmethod
    async def setup_pool(cls: Type[Self], *, uri: str, **kwargs: Any) -> asyncpg.Pool[asyncpg.Record]:
        """:meth: `asyncpg.create_pool` with some extra functionality.

        Parameters
        ----------
        uri: :class:`str`
            The Postgres Connectionection URI.
        **kwargs:
            Extra keyword arguments to pass to :meth:`asyncpg.create_pool`.

        Raises
        ------
        Exception
            The pool failed to be created because the pool was ``None``.
        """

        def _encode_jsonb(value: Dict[Any, Any]) -> str:
            return discord.utils._to_json(value)  # type: ignore

        def _decode_jsonb(value: str) -> Dict[Any, Any]:
            return discord.utils._from_json(value)  # type: ignore

        old_init = kwargs.pop("init", None)

        async def init(con: asyncpg.Connection[asyncpg.Record]) -> None:
            await con.set_type_codec(
                "jsonb", schema="pg_catalog", encoder=_encode_jsonb, decoder=_decode_jsonb, format="text"
            )
            if old_init is not None:
                await old_init(con)

        pool = await asyncpg.create_pool(uri, init=init, **kwargs)
        if pool is None:
            raise Exception("Failed to create pool, pool was None!")

        return pool

    async def setup_hook(self) -> None:
        """|coro|

        A method called shortly after the bot logs in to manage internal cache and load
        extensions for the client.
        """
        for extension in initial_extensions:
            await self.load_extension(extension)

    async def get_context(self, origin: Union[discord.Message, Interaction], /, *, cls: Type[Context] = Context) -> Context:  # type: ignore
        """|coro|

        A method used to get a context from a message or interation.

        Parameters
        ----------
        origin: Union[:class:`discord.Message`, :class:`discord.Interaction`]
            The message or interaction to get the context from.
        cls: Type[:class:`Context`]
            The class to use for the context.

        Returns
        -------
        :class:`Context`
            An instance of the context class.
        """
        return await super().get_context(origin, cls=cls)

    def create_task(self, coro: Coroutine[T, Any, Any], *, name: Optional[str] = None) -> asyncio.Task[T]:
        """Create a task from a coroutine object.

        Parameters
        ----------
        coro: :class:`~asyncio.Coroutine`
            The coroutine to create the task from.
        name: Optional[:class:`str`]
            The name of the task.

        Returns
        -------
        :class:`~asyncio.Task`
            The task that was created.
        """
        return self.loop.create_task(coro, name=name)

    @_wrap_extension
    def load_extension(self, name: str, *, package: Optional[str] = None) -> Coroutine[Any, Any, None]:
        return super().load_extension(name, package=package)

    @_wrap_extension
    def reload_extension(self, name: str, *, package: Optional[str] = None) -> Coroutine[Any, Any, None]:
        return super().reload_extension(name, package=package)

    @_wrap_extension
    def unload_extension(self, name: str, *, package: Optional[str] = None) -> Coroutine[Any, Any, None]:
        return super().unload_extension(name, package=package)
