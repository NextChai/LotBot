# Code Quality
LotBot has a high code quality standard. This means that the code you write is expected to be clean, 
well-commented, well-tested, well-documented, and accurately typehinted.

## Typehints
LotBot makes use of [pyright](https://github.com/microsoft/pyright). Any development that is not done
with pyright and raises errors will be requested to be fixed. It's expected that your code be well 
typehinted and that you use correct typehints. It's recommended that you use `strict` typechecking mode, as
if you have any type errors they will be asked to be fixed.

### Message Intent Commands
It's required to import the correct Context subclass for your cogs.

All commands must be:

1. TypeHinted Accurately (this includes return typehint)
2. Have a name, brief, and description field in the command constructor.
3. The callback must have a help docstring that follows the NumpY Docstring Formating.

```python
import discord
from discord.ext import commands

from utils.cog import BaseCog
from utils.context import Context

class Commands(BaseCog, brief="Hello!", emoji="\N{SMILING FACE WITH SMILING EYES}"):

    @commands.command(
        name="hello",
        brief="Hello world!",
        description="This is a command that says hello world!"
    )
    async def hello_world(self, ctx: Context, *, argument: str) -> discord.Message:
        """|coro|

        A command to say hello world.

        Parameters
        ----------
        argument: :class:`str`
            The argument to say hello with.
        """
        return await ctx.send(f"Hello {argument}!")
```

### Application Commands
It's required to import the correct Interaction subclass for your cogs with
application commands.

All commands must be:
1. Typehinted Correctly
2. Have a name and description in the command constructor.
3. The callback must follow NumPY Docstring Formatting to describe the function's parameters. This
is not optional.

```python
import discord
from discord import app_commands

from utils import Interaction
from utils.cog import BaseCog

class Commands(BaseCog, brief="Hello!", emoji="\N{SMILING FACE WITH SMILING EYES}"):

    @app_commands.command(
        name="hello",
        description="This is a command that says hello world!"
    )
    async def hello_world(self, interaction: Interaction, name: str) -> None:
        """|coro|
        
        A command to say hello world.
        
        Parameters
        ----------
        name: :class:`str`
            The name to say hello with.
        """
        return await interaction.response.send_message(f"Hello, {name}!")
```