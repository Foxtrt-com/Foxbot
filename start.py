import asyncio

from main.bot.bot import Bot

VERSION = "0.0.1"

if __name__ == '__main__':
    foxbot = Bot()
    asyncio.run(foxbot.run(VERSION))
