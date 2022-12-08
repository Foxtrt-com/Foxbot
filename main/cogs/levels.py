import discord
from discord.ext.commands import *
from ..helpers import appwrite as app


class Levels(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Levels Loaded")

    @command(help="Usage: `!level [user]` returns a users level",
             brief="`!level [user]`",
             aliases=["Level", "lvl"])
    async def level(self, ctx, user: discord.User = None):
        if user is None:
            user = app.get_user_lvl(ctx.guild.id, ctx.message.author.id)
        else:
            user = app.get_user_lvl(ctx.guild.id, user.id)
        await ctx.message.reply(f"{ctx.guild.get_member(int(user['$id']))}: Lvl {user['lvl']} ({user['exp']}exp)")

    @command(help="Usage: `!leaderboard` returns a the servers top 5 users",
             brief="`!leaderboard`",
             aliases=["Leaderboard"])
    async def leaderboard(self, ctx):
        result = app.get_top_5(ctx.guild.id)
        msg = f"**Leaderboard:**"

        i = 1
        for user in result:
            msg += f"\n {i}. {ctx.guild.get_member(int(user['$id']))}: Lvl {user['lvl']} ({user['exp']}exp)"
            i += 1

        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Levels(bot))
