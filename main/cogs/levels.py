import discord
from discord.ext.commands import *
from ..helpers import database as db


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
            user = db.get_user(ctx.guild.id, ctx.message.author.id)
            duser = ctx.guild.get_member(int(user[0]))
        else:
            user = db.get_user(ctx.guild.id, duser.id)

        embed = discord.Embed(title=f"{ctx.guild.get_member(int(user[0])).display_name}",
                              description=f"Level {user[2]}",
                              color=0xf67f00
                              )

        embed.set_footer(text=f"{user[3]}exp")
        embed.set_thumbnail(url=duser.avatar.url)

        await ctx.message.reply(embed=embed)

    @command(help="Usage: `!leaderboard` returns a the servers top 5 users",
             brief="`!leaderboard`",
             aliases=["Leaderboard"])
    async def leaderboard(self, ctx):
        result = db.get_top_5(ctx.guild.id)

        embed = discord.Embed(title="Leaderboard",
                              color=0xf67f00
                              )

        i = 1
        for user in result:
            embed.add_field(name="\u200B", value=f"{i}. {ctx.guild.get_member(int(user[0])).display_name}", inline=True)
            embed.add_field(name="\u200B", value=f"LVL {user[2]} ({user[3]}exp)", inline=True)
            embed.add_field(name="\u200B", value="\u200B", inline=False)
            i += 1

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Levels(bot))
