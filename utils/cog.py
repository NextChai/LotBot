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

import uuid
from typing import TYPE_CHECKING, Tuple, Any, Optional, Type
from typing_extensions import Self

from discord.ext import commands

if TYPE_CHECKING:
    from bot import LotBot

__all__: Tuple[str, ...] = ("BaseCog",)


class BaseCog(commands.Cog):
    """The base class for all Scott cogs.

    Attributes
    ----------
    bot: :class:`LotBot`
        The bot instance.
    """

    emoji: Optional[str] = None
    brief: Optional[str] = None
    id: int = int(str(int(uuid.uuid4()))[:20])

    __slots__: Tuple[str, ...] = ("bot",)

    def __init_subclass__(cls: Type[Self], **kwargs: Any) -> None:
        cls.emoji = kwargs.pop("emoji", None)
        cls.brief = kwargs.pop("brief", None)
        return super().__init_subclass__(**kwargs)

    def __init__(self, bot: LotBot, *args: Any, **kwargs: Any) -> None:
        self.bot: LotBot = bot
        super().__init__(*args, **kwargs)
