from discord.ext.commands import *


class Levels(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Levels Loaded")

    @command(enabled=False,
             help="Usage: `!level [user]` returns a users level",
             brief="`!level [user]`",
             aliases=["Level", "lvl"])
    async def level(self, ctx):
        await ctx.send("Level")

    @command(enabled=False,
             help="Usage: `!level` returns a the servers top 5 users",
             brief="`!leaderboard`",
             aliases=["Leaderboard"])
    async def leaderboard(self, ctx):
        await ctx.send("Leaderboard")


async def setup(bot):
    await bot.add_cog(Levels(bot))
