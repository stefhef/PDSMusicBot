import discord
from discord.ext import commands, tasks
import os
import logging
import asyncio

from settings import *

discord.utils.setup_logging()

# or, for example
discord.utils.setup_logging(level=logging.INFO, root=False)


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
            await ctx.send(f"{ctx.message.author.name}, подключитесь к голосовому каналу, пожалуйста", delete_after=MESSAGE_DELETE_TIME)
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
            await ctx.send("Бот не в голосовом канале", delete_after=MESSAGE_DELETE_TIME)

    # @bot.command(name='play', help='To play song')
    @commands.command(nape="play", aliases=["p", "играй"])
    async def play(self, ctx, path):
        await ctx.message.delete()
        try:
            async with ctx.typing():
                ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"{path}"))
            await ctx.send(f"Сейчас играет: {path}", delete_after=MESSAGE_DELETE_TIME)
        except Exception as e:
            logging.log(0, msg=f"{e}")
            print(e)
            await ctx.send("Бот не в голосовом канале", delete_after=MESSAGE_DELETE_TIME)


    # @bot.command(name='test', help='To play song')
    @commands.command()
    async def test(self, ctx):
        await ctx.message.delete()
        await ctx.send("Сосис член", delete_after=MESSAGE_DELETE_TIME)


    # @bot.command(name='pause', help='This command pauses the song')
    @commands.command()
    async def pause(self, ctx):
        await ctx.message.delete()
        if self.vc.is_playing():
            self.vc.pause()
        else:
            await ctx.send("Сейчас нет играющего трeка. Ты глухой?", delete_after=MESSAGE_DELETE_TIME)
        
    # @bot.command(name='resume', help='Resumes the song')
    @commands.command()
    async def resume(self, ctx):
        await ctx.message.delete()
        if self.vc.is_paused():
            self.vc.resume()
        else:
            await ctx.send("Бот ничего не играл, тупой ты", delete_after=MESSAGE_DELETE_TIME)


    # @bot.command(name='stop', help='Stops the song')
    @commands.command()
    async def stop(self, ctx):
        await ctx.message.delete()
        if self.vc.is_playing():
            self.vc.stop()
        else:
            await ctx.send("Сейчас нет играющего трэка. Ты глухой?", delete_after=MESSAGE_DELETE_TIME)

async def start_up(bot):
    await bot.add_cog(Music(bot))


if __name__ == "__main__" :
    asyncio.run(start_up(bot))
    bot.run(DISCORD_TOKEN)