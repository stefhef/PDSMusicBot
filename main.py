import discord
from discord.ext import commands,tasks
import os
import logging
from dotenv import load_dotenv
import asyncio


discord.utils.setup_logging()

# or, for example
discord.utils.setup_logging(level=logging.INFO, root=False)


load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

ffmpeg_options = {
    'options': '-vn'
}

@bot.event
async def on_ready():
    print("Бот запущен!")

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @bot.command(name='join', help='Tells the bot to join the voice channel')
    @commands.command()
    async def join(self, ctx):
        await ctx.message.delete()
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name), delete_after=5.0)
            return
        else:
            channel = ctx.message.author.voice.channel
        self.vc = await channel.connect()

    
    # @bot.command(name='leave', help='To make the bot leave the voice channel')
    @commands.command()
    async def leave(self, ctx):
        await ctx.message.delete()
        if self.vc.is_connected():
            await self.vc.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.", delete_after=5.0)

    # @bot.command(name='play', help='To play song')
    @commands.command()
    async def play(self, ctx, path):
        await ctx.message.delete()
        try:
            async with ctx.typing():
                self.vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"{path}"))
            await ctx.send(f"Now playing: {path}", delete_after=5.0)
        except Exception as e:
            logging.log(0, msg=f"{e}")
            print(e)
            await ctx.send("The bot is not connected to a voice channel.", delete_after=5.0)


    # @bot.command(name='test', help='To play song')
    @commands.command()
    async def test(self, ctx):
        await ctx.message.delete()
        await ctx.send("Сосис член", delete_after=5.05)


    # @bot.command(name='pause', help='This command pauses the song')
    @commands.command()
    async def pause(self, ctx):
        await ctx.message.delete()
        if self.vc.is_playing():
            self.vc.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.", delete_after=5.0)
        
    # @bot.command(name='resume', help='Resumes the song')
    @commands.command()
    async def resume(self, ctx):
        await ctx.message.delete()
        if self.vc.is_paused():
            self.vc.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command", delete_after=5.0)


    # @bot.command(name='stop', help='Stops the song')
    @commands.command()
    async def stop(self, ctx):
        await ctx.message.delete()
        if self.vc.is_playing():
            self.vc.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.", delete_after=5.0)

async def start_up(bot):
    await bot.add_cog(Music(bot))


if __name__ == "__main__" :
    asyncio.run(start_up(bot))
    bot.run(DISCORD_TOKEN)