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

import os
import asyncio
import logging
import aiohttp
from bot import LotBot

from utils import col

os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true"
os.environ["JISHAKU_RETAIN"] = "true"

log = logging.getLogger("launcher")

logging.basicConfig(
    level=logging.INFO,
    format=f"{col()}[{col(7)}%(asctime)s{col()} | {col(4)}%(name)s{col()}:{col(3)}%(levelname)s{col()}] %(message)s",
)


def _get_or_fail(env_var: str) -> str:
    val = os.environ.get(env_var)
    if not val:
        raise RuntimeError(f"{env_var} not set in .env file. Set it.")

    return val


TOKEN = _get_or_fail("BOT_TOKEN")
POSTGRES_URI = _get_or_fail("POSTGRES_URI")


async def main() -> None:
    loop = asyncio.get_event_loop()

    try:
        pool = await LotBot.setup_pool(uri=POSTGRES_URI)
    except Exception as exc:
        return log.warning(f"{col(1)}Failed to connect to database: {exc}")

    async with aiohttp.ClientSession() as session:
        async with pool:
            try:
                bot = LotBot(pool=pool, session=session, loop=loop)
            except Exception as exc:
                return log.warning("Failed to create bot instance", exc_info=exc)

            await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
