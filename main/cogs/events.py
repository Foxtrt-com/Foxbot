import datetime
import random
import discord
from discord.ext.commands import *
from ..helpers import appwrite as app


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Utilities Loaded")
        async for guild in self.bot.fetch_guilds():
            app.create_guild_database(guild.id)
            async for member in guild.fetch_members():
                app.add_member(guild.id, member.id, member.joined_at)

    @Cog.listener()
    async def on_guild_join(self, guild):
        app.create_guild_database(guild.id)
        async for member in guild.fetch_members():
            app.add_member(guild.id, member.id, member.joined_at)

    @Cog.listener()
    async def on_guild_remove(self, guild):
        app.delete_guild_database(guild.id)

    @Cog.listener()
    async def on_member_join(self, member):
        app.add_member(member.guild.id, member.id, member.joined_at)
        message = app.get_welcome_msg(member.guild.id)
        message = message.replace("{user}", member.mention)
        message = message.replace("{server}", member.guild.name)

        embed = discord.Embed(title=message,
                              description="Be sure to read the #Rules and have fun! <3",
                              timestamp=datetime.datetime.now(),
                              color=0xf67f00
                              )

        embed.set_footer(text="Joined")
        embed.set_thumbnail(url=member.avatar_url)

        await member.guild.system_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        app.delete_member(member.guild.id, member.id)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.application_id:
            return

        has_lvl_up, lvl = app.add_exp(message.guild.id, message.author.id, message.created_at, random.randint(15, 25))

        user = app.get_user_lvl(message.guild.id, message.author.id)

        if has_lvl_up:
            embed = discord.Embed(title="LEVEL UP!",
                                  description=f"{message.author.mention} is now lvl{lvl}!",
                                  color=0xf67f00
                                  )

            embed.set_footer(text=f"{user['exp']}exp")
            embed.set_thumbnail(url=message.author.avatar_url)

            await message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))
