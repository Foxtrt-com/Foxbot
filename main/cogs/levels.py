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
    async def level(self, ctx, duser: discord.User = None):
        if duser is None:
            user = app.get_user_lvl(ctx.guild.id, ctx.message.author.id)
        else:
            user = app.get_user_lvl(ctx.guild.id, duser.id)

        embed = discord.Embed(title=f"{ctx.guild.get_member(int(user['$id']))}",
                              description=f"Level {user['lvl']}",
                              color=0xf67f00
                              )

        embed.set_footer(text=f"{user['exp']}exp")
        embed.set_thumbnail(url=duser.avatar.url)

        await ctx.message.reply(embed)

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
        # TODO: Make this an embed
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Levels(bot))
