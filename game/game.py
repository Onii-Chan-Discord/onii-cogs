import asyncio
import random

import discord
from Discord_Games import (
    aki,
    aki_buttons,
    connect_four,
    twenty_48,
    twenty_48_buttons,
)
from discord_games_original import battleship, hangman, typeracer
from redbot.core import commands

from .games import minesweeper, tictactoe, twenty, wumpus


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["aki"], help="Play akinator!")
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def akinator(self, ctx):
        if discord.__version__ != "2.0.0a":
            return await aki.Akinator.start(self, ctx)
        else:
            await aki_buttons.BetaAkinator().start(
                ctx, color=(await ctx.embed_colour())
            )

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(
        name="2048", aliases=["twenty48"], help="Play 2048 game."
    )
    async def _twenty_48(self, ctx):
        if discord.__version__ != "2.0.0a":
            return await twenty_48.Twenty48.start(self, ctx)
        else:
            await twenty_48_buttons.BetaTwenty48().start(ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="minesweeper", help="Play Minesweeper")
    async def minesweeper(self, ctx, columns=None, rows=None, bombs=None):
        await minesweeper.play(ctx, columns, rows, bombs)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="wumpus", help="Play Wumpus game")
    async def _wumpus(self, ctx):
        await wumpus.play(self.bot, ctx)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["ttt", "tic-tac-toe"], help="Play Tic-Tac-Toe")
    async def tictactoe(self, ctx):
        await tictactoe.play_game(
            self.bot, ctx, chance_for_error=0.2
        )  # Win Plausible

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        name="rps",
        aliases=["rockpaperscissors"],
        help="Play Rock, Paper, Scissors game",
    )
    async def rps(self, ctx):
        def check_win(p, b):
            if p == "🌑":
                return b != "📄"
            return b != "✂" if p == "📄" else b != "🌑"

        async with ctx.typing():
            reactions = ["🌑", "📄", "✂"]
            game_message = await ctx.send(
                "**Rock Paper Scissors**\nChoose your shape:",
                delete_after=15.0,
            )
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return (
                user != self.bot.user
                and user == ctx.author
                and (str(reaction.emoji) == "🌑" or "📄" or "✂")
            )

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", timeout=10.0, check=check
            )
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(
                f"**Your Choice:\t{reaction.emoji}\nMy Choice:\t{bot_emoji}**"
            )
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**You win :sparkles:**")
            else:
                await ctx.send("**I win :robot:**")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        name="typerace",
        help="How fast can you type? Test it out with typeracer!",
    )
    async def typeracer(self, ctx):
        await typeracer.TypeRacer.start(self, ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="hangman", help="Play Hangman")
    async def hangman(self, ctx):
        await hangman.Hangman.start(self, ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        name="connect4", aliases=["connectfour"], help="Play Connect4"
    )
    async def connect4(self, ctx):
        await connect_four.ConnectFour.start(self, ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="battleship", help="Play Battleship")
    async def _battleship(self, ctx):
        await battleship.BattleShip.start(self, ctx)


def setup(bot):
    bot.add_cog(Games(bot))
