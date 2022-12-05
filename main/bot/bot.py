import os
import discord
import discord.ext
from discord.ext.commands import AutoShardedBot as DiscordBot
from discord.ext.commands.errors import (BadArgument, CommandNotFound)


class Bot(DiscordBot):
    def __init__(self):
        self.INTENTS = discord.Intents.all()
        self.INTENTS.members = True
        self.INTENTS.presences = True
        self.INTENTS.message_content = True

        self.OWNER_IDS = [145255535900360704]
        self.IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

        self.TOKEN = None
        self.VERSION = None

        self.ready = False

        super(Bot, self).__init__(command_prefix="!", owner_ids=self.OWNER_IDS, intents=self.INTENTS)

    async def on_ready(self):
        if not self.ready:
            self.ready = True

            appearance = self.get_cog("Appearance")

            await appearance.set()

            print("Bot connected!")
        else:
            print("Bot reconnected")

    async def load_cogs(self):
        for filename in os.listdir("./main/cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await self.load_extension(f"main.cogs.{filename[:-3]}")

    async def run(self, version):
        self.VERSION = version
        with open("./data/restricted/token.txt", "r") as f:
            self.TOKEN = f.readline()

        if self.TOKEN is not None:
            await self.load_cogs()
            await self.start(self.TOKEN, reconnect=True)
        else:
            print("No Token found in './data/restricted/token.txt'")