import datetime
import random
import discord
from discord.ext.commands import *
from ..helpers import database as db


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Utilities Loaded")
        async for guild in self.bot.fetch_guilds():
            db.create_guild_database(guild.id)
            async for member in guild.fetch_members():
                db.add_user(guild.id, member.id, member.joined_at)

    @Cog.listener()
    async def on_guild_join(self, guild):
        db.create_guild_database(guild.id)
        async for member in guild.fetch_members():
            db.add_user(guild.id, member.id, member.joined_at)

    @Cog.listener()
    async def on_guild_remove(self, guild):
        db.delete_guild_database(guild.id)

    @Cog.listener()
    async def on_member_join(self, member):
        db.add_user(member.guild.id, member.id, member.joined_at)
        message = db.get_welcome_msg(member.guild.id)
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
        db.delete_user(member.guild.id, member.id)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.application_id:
            return

        has_lvl_up, lvl = db.add_exp(message.guild.id, message.author.id, message.created_at, random.randint(15, 25))

        user = db.get_user(message.guild.id, message.author.id)

        if has_lvl_up:
            embed = discord.Embed(title="LEVEL UP!",
                                  description=f"{message.author.mention} is now lvl{lvl}!",
                                  color=0xf67f00
                                  )

            embed.set_footer(text=f"{user[3]}exp")
            embed.set_thumbnail(url=message.author.avatar_url)

            await message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))
