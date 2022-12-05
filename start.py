import asyncio

from main.bot.bot import Bot

VERSION = "1.0.0"

if __name__ == '__main__':
    foxbot = Bot()
    asyncio.run(foxbot.run(VERSION))
