import discord
import random
import yt_dlp
import asyncio
from rapidfuzz import process, fuzz
import json, requests
from uicord import *
import re

JUKEBOX = "<:jukebox:1474691139591340164>"

# ==========================================
# Random Chibi (UNCHANGED)
# ==========================================

def random_chibi():
    apikey = "LIVDSRZULELA"
    lmt = 32
    search_term = "umamusume dancing jukebox chibi"

    r = requests.get(
        f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}"
    )

    if r.status_code == 200:
        results = json.loads(r.content)["results"]
        res = random.choice(results)

        for _, media in res["media"][0].items():
            if "url" in media and media["url"].endswith(".gif"):
                return media["url"]

    return "https://c.tenor.com/uxnxEfCrQfYAAAAd/tenor.gif"


# ==========================================
# Duration
# ==========================================

def dur(seconds: int):
    times = {
        "d": 86400,
        "h": 3600,
        "m": 60,
        "s": 1
    }

    out = ""
    for k, v in times.items():
        if seconds >= v:
            out += f"{seconds//v}{k} "
            seconds %= v
    return out.strip()


# ==========================================
# yt-dlp
# ==========================================

ytdl_opts = {
    "format": "bestaudio[ext=m4a]/bestaudio",
    "quiet": True,
    "ignoreerrors": True,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "js_runtime": "auto",
    "js": True
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


# ==========================================
# Playlist Handling
# ==========================================

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def custom_score(query: str, title: str, **kwargs) -> float:
    query_norm = normalize(query)
    title_norm = normalize(title)

    token_score = fuzz.token_set_ratio(query_norm, title_norm)
    partial_score = fuzz.partial_ratio(query_norm, title_norm)
    full_score = fuzz.ratio(query_norm, title_norm)

    score = token_score * 0.5 + partial_score * 0.3 + full_score * 0.2
    return score

def search_song(query, playlist_file="playlist.txt"):
    with open(playlist_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    titles = [line.split(" | ")[0].lower() for line in lines]
    urls = [line.split(" | ")[1] for line in lines]

    match = process.extractOne(query, titles, scorer=custom_score)

    if match:
        best_title = match[0]
        index = titles.index(best_title)
        return urls[index]

    return None


def load_music_links(filename="playlist.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().split(" | ")[1] for line in f if line.strip()]


async def find_song(search=""):
    if search:
        link = search_song(search)
        if not link:
            return None
    else:
        links = load_music_links()
        link = random.choice(links)

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        if not info:
            return None
        info["source"] = link
        return info


class QueueItem:
    def __init__(self, info: dict):
        self.url = info["url"]
        self.title = info["title"]
        self.source = info["source"]
        self.duration = info.get("duration", 0)

    def display(self):
        return f"[{self.title}](<{self.source}>)"

class Queue:

    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.vc: discord.VoiceClient | None = None
        self.songs = []
        self.player_task: asyncio.Task | None = None
        self.currently_playing=None
        self.autoplay = False
    # ------------------------
    # Join
    # ------------------------
    async def ensure_joined(self, ctx):
        if not ctx.author.voice:
            await ctx.respond("Join a VC first.")
            return False

        channel = ctx.author.voice.channel

        perms = channel.permissions_for(ctx.guild.me)
        if not perms.connect:
            await ctx.respond("I don't have permission to **connect** to your voice channel!")
            return False
        if not perms.speak:
            await ctx.respond("I don't have permission to **speak** in your voice channel!")
            return False

        if self.vc and self.vc.is_connected():
            return True

        self.vc = await channel.connect()
        return True
    async def skip(self, ctx):
        if not ctx.author.voice:
            await ctx.respond("Join a VC first.")
            return False
        if self.currently_playing is None: return
        if self.player_task:
            self.player_task.cancel()
            self.player_task = None
        self.vc.stop()
        if self.songs or self.autoplay:
            self.player_task = asyncio.create_task(self.player_loop(ctx))
        p = "" if not self.songs else f"\nMoving to {self.songs[0].display()}"
        await ctx.respond(f"Skipped {self.currently_playing.display()}{p}")
    # ------------------------
    # Leave
    # ------------------------
    async def leave(self):
        if self.player_task:
            self.player_task.cancel()
            self.player_task = None

        if self.vc and self.vc.is_connected():
            await self.vc.disconnect()

        self.vc = None
        self.songs.clear()

    # ------------------------
    # Add Song
    # ------------------------
    async def add_song(self, ctx, query=""):
        info = await find_song(query)
        if not info:
            await ctx.respond("No result found.")
            return
        song = QueueItem(info)

        if ctx and self.currently_playing is not None:
            await ctx.respond(f"Added {song.display()} to queue")
        if ctx:
            self.songs.append(song)

        if not self.player_task:
            self.player_task = asyncio.create_task(self.player_loop(ctx))
        return song
    # ------------------------
    # Player Loop
    # ------------------------
    async def set_autoplay(self, ctx):
        self.autoplay=not self.autoplay

        await ctx.respond(
            f"Autoplay {"enabled" if self.autoplay else "disabled"}"
        )
    async def player_loop(self, ctx):
        while self.songs or self.autoplay:
            if not self.vc or not self.vc.is_connected():
                break
            if self.autoplay and not self.songs:
                song = await self.add_song(False)
            else:
                song = self.songs.pop(0)
            self.currently_playing=song

            source = discord.FFmpegOpusAudio(
                song.url,
                **ffmpeg_options
            )

            self.vc.play(source)

            await ctx.channel.send(
                view=View(
                    Container(
                        Section(
                            Text(f"## **{JUKEBOX}Now Playing**\n-# **{song.display()}**"),
                            Text(f"-# Duration {dur(song.duration)}"),
                            accessory=Thumbnail(url=random_chibi())
                        )
                    )
                )
            )

            while self.vc.is_playing():
                await asyncio.sleep(1)

        self.player_task = None
        self.currently_playing = None

# ==========================================
# GLOBAL QUEUE STORE
# ==========================================

queues: dict[int, Queue] = {}

def get_queue(guild_id: int):
    if guild_id not in queues:
        queues[guild_id] = Queue(guild_id)
    return queues[guild_id]
