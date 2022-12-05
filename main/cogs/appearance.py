from discord import Activity, ActivityType
from discord.ext.commands import *


class Appearance(Cog):
    def __init__(self, bot):
        self.bot = bot

        self._message = "listening your !commands"

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Appearance Loaded")

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if value.split()[0] not in ("playing", "watching", "listening"):
            raise ValueError("Invalid activity type")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.bot.change_presence(
            activity=Activity(name=_name,
                              type=getattr(ActivityType, _type, ActivityType.playing)))


async def setup(bot):
    await bot.add_cog(Appearance(bot))
