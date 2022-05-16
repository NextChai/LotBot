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

from typing import TYPE_CHECKING, Tuple, Optional

import discord

if TYPE_CHECKING:
    from bot import LotBot

__all__: Tuple[str, ...] = ("Interaction", "KnownInteraction", "col")


class Interaction(discord.Interaction):
    client: LotBot  # type: ignore -> it's nessecary.


class KnownInteraction(Interaction):
    guild: discord.Guild  # type: ignore -> created for guild specific interactions.


def col(color: Optional[int] = None, /, *, fmt: int = 0, bg: bool = False) -> str:
    """
    Returns the ascii color escape string for the given number.

    Parameters
    ----------
    color: Optional[:class:`int`]
        The color number. Colors can be either 0-15 or 0-255.
    fmt: :class:int`
        The format number.
    bg: :class:`bool`
        Whether to return the background color. Defaults to ``False``.

    Returns
    -------
    :class:`str`
        The ascii color escape string.
    """
    base = "\u001b["
    if fmt != 0:
        base += "{fmt};"
    if color is None:
        base += "{color}m"
        color = 0
    else:
        if bg is True:
            base += "4{color}m"
        else:
            base += "3{color}m"

    return base.format(fmt=fmt, color=color)
