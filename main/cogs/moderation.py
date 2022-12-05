from discord.ext.commands import *
from ..helpers.message_eq_user import MessageEqUser


class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Moderation Loaded")

    @has_permissions(administrator=True)
    @command(help="Usage: `!clear <number> [user]` clears a number of messages form all or one user",
             brief="`!clear <number> [user]`",
             aliases=["Clear", "cls", "purge", "Purge"])
    async def clear(self, ctx, number: int, user=None):
        channel = ctx.message.channel

        q, r = divmod(number + 1, 100)

        if user is None:
            for _ in range(q):
                await channel.purge(limit=100, reason=f"{ctx.message.author} ran !clear")

            await channel.purge(limit=r, reason=f"{ctx.message.author} ran !clear")
        else:
            meu = MessageEqUser(user)
            for _ in range(q):
                await channel.purge(limit=100, check=meu.check, reason=f"{ctx.message.author} ran !clear")

            await channel.purge(limit=r, check=meu.check, reason=f"{ctx.message.author} ran !clear")

    @has_permissions(administrator=True)
    @command(help="Usage: `!ping` gets the bot latency",
             brief="`!ping`",
             aliases=["Ping"])
    async def ping(self, ctx):
        await ctx.message.reply(f"Pong! ({round(self.bot.latency * 1000)}ms)")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
