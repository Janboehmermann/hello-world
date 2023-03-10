import discord
from discord.ext import commands
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

# YouTube Player
class YTPlayer:
    def __init__(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto'
        }
        self.ydl = youtube_dl.YoutubeDL(ydl_opts)
        self.url = url

    def download(self):
        info = self.ydl.extract_info(self.url, download=False)
        return {'title': info['title'], 'url': info['url']}

# Spotify Player
class SpotifyPlayer:
    def __init__(self, track_uri):
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.track_uri = track_uri
        self.track_info = sp.track(self.track_uri)

    def download(self):
        return {'title': self.track_info['name'], 'url': self.track_info['preview_url']}

@bot.command()
async def play(ctx, *, url):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Du bist nicht in einem Sprachkanal.")
        return
    if 'youtube.com' in url:
        player = YTPlayer(url)
    elif 'spotify.com' in url:
        player = SpotifyPlayer(url.split('/')[-1])
    else:
        await ctx.send("Ungültige URL.")
        return

    vc = await voice_channel.connect()
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(player.download()['url']))
    vc.play(source)
    await ctx.send(f"{player.download()['title']} wird abgespielt.")

bot.run("YOUR_DISCORD_BOT_TOKEN")