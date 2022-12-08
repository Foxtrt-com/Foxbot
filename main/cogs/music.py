import discord
from discord import Activity, ActivityType
from discord.ext.commands import *
import wavelink


class CustomPlayer(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()


class Music(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def connect_nodes(self):
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='127.0.0.1',
                                            port=2333,
                                            password='LocalOnlyLavalinkPassword')

    @Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.connect_nodes())
        print("Cog: Music Loaded")

    @Cog.listener()
    async def on_wavelink_node_ready(self, node):
        print(f"Node {node.identifier} is ready")


    @Cog.listener()
    async def on_wavelink_track_end(self, player, track, reason):
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)
        else:
            await self.disconnect()

    @command(enabled=False,
             help="Usage: `!connect` causes the music bot to join your voice channel",
             brief="`!connect`",
             aliases=["Connect"])
    async def connect(self, ctx):
        vc = ctx.voice_client
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("Please join a voice channel to connect.")

        if not vc:
            await ctx.author.voice.channel.connect(cls=CustomPlayer())
        else:
            await ctx.send("The bot is already connected to a voice channel")

    @command(help="Usage: `!disconnect` causes the music bot to leave your voice channel",
             brief="`!disconnect`",
             aliases=["Stop", "stop", "Disconnect"])
    async def disconnect(self, ctx):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @command(help="Usage: `!play <youtube link | song name>` plays the song requested or adds it to the queue",
             brief="`!play <youtube link | song name>`",
             aliases=["Play"])
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        vc = ctx.voice_client
        if not vc:
            custom_player = CustomPlayer()
            vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

        if vc.is_playing():

            vc.queue.put(item=search)

            await ctx.send(embed=discord.Embed(
                title=search.title,
                url=search.uri,
                description=f"Queued {search.title} in {vc.channel}"
            ))
        else:
            await vc.play(search)

            await ctx.send(embed=discord.Embed(
                title=search.title,
                url=search.uri,
                description=f"Playing {search.title} in {vc.channel}"
            ))

    @command(help="Usage: `!skip` skips the current song",
             brief="`!skip`",
             aliases=["Skip", "next", "Next"])
    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send("Nothing is playing.")
            if vc.queue.is_empty:
                return await vc.stop()

            await vc.seek(vc.track.length * 1000)
            if vc.is_paused():
                await vc.resume()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @command(help="Usage: `!pause` pauses the current song",
             brief="`!pause`",
             aliases=["Pause"])
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
            else:
                await ctx.send("Nothing is playing.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    @command(help="Usage: `!resume` resumes playback",
             brief="`!resume`",
             aliases=["Resume"])
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
            else:
                await ctx.send("Nothing is paused.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    # error handling

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("Could not find a track.")
        else:
            await ctx.send("Please join a voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))
