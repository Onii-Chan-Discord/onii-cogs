"""
Copyright 2021 Onii-chan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import logging
import random

import aiohttp
import discord
from redbot.core import commands


async def api_call(call_uri, returnObj=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{call_uri}") as response:
            response = await response.json()
            if returnObj == False:
                return response["url"]
            elif returnObj == True:
                return response

log = logging.getLogger("red.onii.wallpaper")

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["i"])
    async def image(self, ctx):
        """All the commands in the image cog"""

    @image.group(aliases=["c"])
    async def character(self, ctx):
        """The character commands in the wallpaper part of the image cog"""

    @image.group(aliases=["o"])
    async def other(self, ctx):
        """The uncategorised commands in the image cog"""

    @character.command(aliases=["zen"], name="zenitsu")
    @commands.bot_has_permissions(embed_links=True)
    async def zenitsu(self, ctx):
        embed = discord.Embed(color=0xFFF300)
        embed.add_field(
            name="Zenitsu", value="You asked for some Zenitsu wallpapers?", inline=False
        )
        embed.set_image(
            url=random.choice(
                (
                    "https://images2.alphacoders.com/100/thumb-1920-1007550.jpg",
                    "https://cdn.discordapp.com/attachments/736113073328357386/813287821355778108/thumb-1920-1007788.jpg",
                    "https://cdn.discordapp.com/attachments/736113073328357386/801781638991183903/thumb-1920-1026796.jpg",
                    "https://www.enjpg.com/img/2020/zenitsu-12.jpg",
                    "https://images.wallpapersden.com/image/download/breath-of-thunder-zenitsu-agatsuma_a21oameUmZqaraWkpJRobWllrWdma2U.jpg",
                )
            )
        )
        embed.set_footer(text=f"Requested by: {str(ctx.author)}", icon_url=ctx.author.avatar_url),
        await ctx.reply(embed=embed, mention_author=False)

    @other.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def naruto(self, ctx: commands.Context):
        """Shows some naruto wallpapers from reddit.

        Wallpapers shown are taken from r/narutowallpapers.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/narutowallpapers/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/narutowallpapers",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)

    @image.group(aliases=["a"])
    async def anime(self, ctx):
        """Image commands"""

    @anime.command(name="chibi")
    @commands.bot_has_permissions(embed_links=True)
    async def chibi(self, ctx):
        """Random cute wallpaper(Will contain characters from multiple anime's)"""
        embed = discord.Embed(colour=0xFF00AB)
        embed.add_field(name="Chibi", value="Aren't they cute?", inline=False)
        embed.set_image(
            url=random.choice(
                (
                    "https://cdn.discordapp.com/attachments/763154622675681331/836852290933489664/bg-01.png",
                    "https://cdn.discordapp.com/attachments/763154622675681331/836908773146361906/bg-02.png",
                )
            )
        )
        embed.set_footer(text=f"Requested by: {str(ctx.author)}", icon_url=ctx.author.avatar_url),
        await ctx.reply(embed=embed, mention_author=False)

    @other.command(aliases=["rando"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def random(self, ctx: commands.Context):
        """Shows some anime wallpaper from reddit.

        Wallpapers shown are taken from r/Animewallpaper.

        Warning: Some Images Could Be Considered Nsfw In Some Servers.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/Animewallpaper/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/Animewallpaper",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)

    @other.command(name="randomavatar", aliases=["rav"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar_random(self, ctx: commands.Context):
        """Shows some profile pictures from reddit.

        Pictures shown are taken from r/ProfilePic.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/ProfilePic/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/ProfilePic",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @other.command()
    async def neko(self, ctx):
        embed = discord.Embed(
            title="Neko's For You!",
            color=discord.Colour.random(),
            timestamp=ctx.message.created_at,
        )

        embed.set_footer(
            text="Powered by nekos.best",
            icon_url=ctx.message.author.avatar_url,
        )
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)

        embed.set_image(url=await api_call("https://nekos.best/nekos"))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx: commands.Context):
        """Shows some memes from reddit.

        Memes shown are taken from r/memes.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/memes/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/memes",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)

    @other.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def space(self, ctx: commands.Context):
        """Shows some space wallpapers from reddit.

        Wallpapers shown are taken from r/spaceporn.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/spaceporn/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/spaceporn",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["animeme"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animememe(self, ctx: commands.Context):
        """Shows some anime memes from reddit.

        Wallpapers shown are taken from r/Animemes.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/Animemes/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/Animemes",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)

    @other.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def moe(self, ctx: commands.Context):
        """Shows some space wallpapers from reddit.

        Wallpapers shown are taken from r/awwnime.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.reddit.com/r/awwnime/new.json?sort=hot"
            ) as resp:
                data = await resp.json()
                data = data["data"]
                children = data["children"]
                post = random.choice(children)["data"]
                title = post["title"]
                url = post["url_overridden_by_dest"]

        embed = discord.Embed(title=title, colour=discord.Colour.random())
        embed.set_image(url=url)
        embed.set_footer(
            text="Powered by r/awwnime",
            icon_url=ctx.message.author.avatar_url,
        )
        await session.close()
        await ctx.reply(embed=embed, mention_author=False)
