import random
from discord.ext.commands import *


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Cog: Fun Loaded")

    @command(help="Usage: `!flip` returns Heads or Tails Like Flipping a Coin.",
             brief="`!flip`",
             aliases=["Flip", "Coin", "coin"])
    async def flip(self, ctx):
        values = ["Heads", "Tails"]
        await ctx.message.reply(f":coin: **{random.choice(values)}!**")

    @command(help="Usage: `!roll [number of dice]` returns x number of dice rolls (D6)",
             brief="`!roll [num_dice]`",
             aliases=["Roll", "Dice", "dice"])
    async def roll(self, ctx, num_dice: int = 1):
        message = f":game_die: **{random.choice(range(1, 7))}**"
        if num_dice > 1:
            for dice in range(num_dice - 1):
                message += f"\n:game_die: **{random.choice(range(1, 7))}**"

        await ctx.message.reply(message)

    @command(help="Usage: `!rps <your choice (r,p,s,Rock,Paper,Scissors)>` runs a classic game of Rock, Paper, "
                  "Scissors and determines the winner, you or the bot!",
             brief="`!rps <choice>`",
             aliases=["RPS", "RockPaperScissors"])
    async def rps(self, ctx, choice: str = None):
        choices = ["r", "p", "s"]
        alt_choices = ["rock", "paper", "scissors"]
        values = [":rock:", ":page_with_curl:", ":scissors:"]
        if choice.lower() in choices:
            user_choice = values[choices.index(choice.lower())]
        elif choice in alt_choices:
            user_choice = values[alt_choices.index(choice.lower())]
        else:
            return

        cpu_choice = random.choice(values)
        result = "CPU WINS!"

        if user_choice == cpu_choice:
            result = "DRAW!"
        elif (user_choice == ":rock:" and cpu_choice == ":scissors:") \
                or \
                (user_choice == ":page_with_curl:" and cpu_choice == ":rock:") \
                or \
                (user_choice == ":scissors:" and cpu_choice == ":page_with_curl:"):
            result = f"** {ctx.message.author.display_name} WINS! **"

        await ctx.message.reply(f"{ctx.message.author.display_name}: {user_choice} **vs** {cpu_choice} :CPU\n\n"
                                f"{result}")


async def setup(bot):
    await bot.add_cog(Fun(bot))
