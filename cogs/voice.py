from types import NoneType
from discord.ext import commands
from discord.utils import get
from discord.commands import slash_command
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from youtubesearchpython.__future__ import VideosSearch
from os import getenv
from dotenv import load_dotenv, find_dotenv

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    dotenvfile = find_dotenv('../.env')
    load_dotenv(dotenvfile)
    guild_id = int(getenv("GUILD_ID"))


    @slash_command(guild_ids=[guild_id], name="join")
    async def join(self, ctx):
        """Join current voice channel"""
        await ctx.author.voice.channel.connect()
        await ctx.respond("I'm in!")


    @slash_command(guild_ids=[guild_id], name="play")
    async def play(self, ctx, video: str):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice is NoneType: 
            ctx.author.voice.channel.connect()
            voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        if not voice.is_playing():
            voice.stop()
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'youtube_include_dash_manifest':False}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            with YoutubeDL(YDL_OPTIONS) as ydl:
                if not video.startswith('http') or not video.startswith("www.") or not video.startswith("youtube.com/watch?v="):
                    videoSearch = VideosSearch(video, limit=1)
                    video = await videoSearch.next()
                    video = f"https://www.youtube.com/watch?v={video['result'][0]['id']}"
                info = ydl.extract_info(video, download=False)
                URL = info['formats'][0]['url']
                title = info.get('title', None)
            
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            
            await ctx.respond(f"Now playing {title}! :musical_note: :musical_note: ")

    
    @slash_command(guild_ids=[guild_id], name="stop")
    async def stop(self, ctx):
        """Stop the current playing audio"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if (voice.is_playing()):
            voice.stop()
            await ctx.respond("Stopped the audio")


    @slash_command(guild_ids=[guild_id], name="pause")
    async def pause(self, ctx):
        """Stop the current playing audio"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if (voice.is_playing()):
            voice.pause()
            await ctx.respond("Paused the audio")
        
    
    @slash_command(guild_ids=[guild_id], name="resume")
    async def resume(self, ctx):
        """Stop the current playing audio"""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if (voice.is_paused()):
            voice.resume()
            await ctx.respond("Resumed the audio")
