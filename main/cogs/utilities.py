from discord.ext.commands import *

class Utilities(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Utilities Loaded")

    @command(enabled=False,
             help="Usage: WIP",
             brief="WIP",
             aliases=["Pronouns"])
    async def pronouns(self, ctx):
        await ctx.send("Pronouns")


async def setup(bot):
    await bot.add_cog(Utilities(bot))
