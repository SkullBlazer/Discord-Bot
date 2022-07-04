import discord
import asyncio
from async_timeout import timeout
import youtube_dl
from discord.ext import commands
import os
import aiohttp
import random
import math
import itertools
from datetime import datetime
import functools
import spotipy
import spotipy.util as util
from lyricsgenius import Genius
import subprocess

youtube_dl.utils.bug_reports_message = lambda: ''

class VoiceError(Exception):
	pass

class YTDLError(Exception):
	pass

class YTDLSource(discord.PCMVolumeTransformer):
	YTDL_OPTIONS = {
		'format': 'bestaudio/best',
		'extractaudio': True,
		'audioformat': 'mp3',
		'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
		'restrictfilenames': True,
		'noplaylist': True,
		'nocheckcertificate': True,
		'ignoreerrors': False,
		'logtostderr': False,
		'quiet': True,
		'no_warnings': False,
		'default_search': 'auto',
		'source_address': '0.0.0.0',
	}

	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
		'options': '-vn',
	}

	ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

	def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
		super().__init__(source, volume)

		self.requester = ctx.author
		self.channel = ctx.channel
		self.data = data

		self.uploader = data.get('uploader')
		self.uploader_url = data.get('uploader_url')
		date = data.get('upload_date')
		self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
		self.title = data.get('title')
		self.thumbnail = data.get('thumbnail')
		self.description = data.get('description')
		self.duration = self.parse_duration(int(data.get('duration')))
		self.tags = data.get('tags')
		self.url = data.get('webpage_url')
		self.views = data.get('view_count')
		self.likes = data.get('like_count')
		self.dislikes = data.get('dislike_count')
		self.stream_url = data.get('url')

	def __str__(self):
		return '**{0.title}** by **{0.uploader}**'.format(self)

	@classmethod
	async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
		loop = loop or asyncio.get_event_loop()

		partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
		data = await loop.run_in_executor(None, partial)

		if data is None:
			raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

		if 'entries' not in data:
			process_info = data
		else:
			process_info = None
			for entry in data['entries']:
				if entry:
					process_info = entry
					break

			if process_info is None:
				raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

		webpage_url = process_info['webpage_url']
		partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
		processed_info = await loop.run_in_executor(None, partial)

		if processed_info is None:
			raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

		if 'entries' not in processed_info:
			info = processed_info
		else:
			info = None
			while info is None:
				try:
					info = processed_info['entries'].pop(0)
				except IndexError:
					raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

		return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

	@staticmethod
	def parse_duration(duration: int):
		minutes, seconds = divmod(duration, 60)
		hours, minutes = divmod(minutes, 60)
		days, hours = divmod(hours, 24)

		duration = []
		if days > 0:
			if days == 1:
				duration.append('{} day'.format(days))
			else:
				duration.append('{} days'.format(days))
		if hours > 0:
			if hours == 1:
				duration.append('{} hour'.format(hours))
			else:
				duration.append('{} hours'.format(hours))
		if minutes > 0:
			if minutes == 1:
				duration.append('{} minute'.format(minutes))
			else:
				duration.append('{} minutes'.format(minutes))
		if seconds > 0:
			if seconds == 1:
				duration.append('{} second'.format(seconds))
			else:
				duration.append('{} seconds'.format(seconds))

		return ', '.join(duration)


class Song:
	__slots__ = ('source', 'requester')

	def __init__(self, source: YTDLSource):
		self.source = source
		self.requester = source.requester

	def create_embed(self):
		embed = (discord.Embed(title='Now playing',
							description='```{0.source.title}\n```'.format(self),
							color=discord.Color.blurple())
				.add_field(name='Duration', value=self.source.duration)
				.add_field(name='Requested by', value=self.requester.mention)
				.add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
				.add_field(name='Uploaded on', value=self.source.upload_date)
				.add_field(name='URL', value='[Click]({0.source.url})'.format(self))
				.set_thumbnail(url=self.source.thumbnail))

		return embed


class SongQueue(asyncio.Queue):
	def __getitem__(self, item):
		if isinstance(item, slice):
			return list(itertools.islice(self._queue, item.start, item.stop, item.step))
		else:
			return self._queue[item]

	def __iter__(self):
		return self._queue.__iter__()

	def __len__(self):
		return self.qsize()

	def clear(self):
		self._queue.clear()

	def shuffle(self):
		random.shuffle(self._queue)

	def remove(self, index: int):
		del self._queue[index]


class VoiceState:
	def __init__(self, bot: commands.Bot, ctx: commands.Context):
		self.bot = bot
		self._ctx = ctx

		self.current = None
		self.voice = None
		self.next = asyncio.Event()
		self.songs = SongQueue()
		self.exists = True

		self._loop = False
		self._volume = 0.5
		self.skip_votes = set()

		self.audio_player = bot.loop.create_task(self.audio_player_task())

	def __del__(self):
		self.audio_player.cancel()

	@property
	def loop(self):
		return self._loop

	@loop.setter
	def loop(self, value: bool):
		self._loop = value

	@property
	def volume(self):
		return self._volume

	@volume.setter
	def volume(self, value: float):
		self._volume = value

	@property
	def is_playing(self):
		return self.voice and self.current

	def stop_playing_you_idiot(self):
		self.current = None

	def volume_change(self, value: float):
		self._volume = value

	# def play_next(self, ctx, source):
	# 	if len(self.song_queue) >= 1:
	# 		del self.song_queue[0]
	# 		vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
	# 		vc.play(discord.FFmpegPCMAudio(source=source, after=lambda e: self.play_next(ctx)))
	# 		asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."))#, self.bot.loop)
		
	async def audio_player_task(self):
		while True:
			self.next.clear()
			self.now = None

			if not self.loop:
				# Try to get the next song within 3 minutes.
				# If no song will be added to the queue in time,
				# the player will disconnect due to performance
				# reasons.
				try:
					async with timeout(180):  # 3 minutes
						self.current = await self.songs.get()
				except asyncio.TimeoutError:
					self.bot.loop.create_task(self.stop())
					self.exists = False
					return

				self.current.source.volume = self._volume
				self.voice.play(self.current.source, after=self.play_next_song)
				self.skip_votes = set()
				await self.current.source.channel.send(embed=self.current.create_embed())

			elif self.loop:
				self.now = discord.FFmpegPCMAudio(self.current.source.stream_url, **YTDLSource.FFMPEG_OPTIONS)
				self.voice.play(self.now, after=self.play_next_song)
			await self.next.wait()

	def play_next_song(self, error=None):
		if error:
			raise VoiceError(str(error))

		self.next.set()

	def skip(self):
		self.skip_votes.clear()

		if self.is_playing:
			self.voice.stop()

	async def stop(self):
		self.songs.clear()

		if self.voice:
			await self.voice.disconnect()
			self.voice = None


class Music(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.voice_states = {}

	def get_voice_state(self, ctx: commands.Context):
		state = self.voice_states.get(ctx.guild.id)
		if not state or not state.exists:
			state = VoiceState(self.bot, ctx)
			self.voice_states[ctx.guild.id] = state

		return state

	def cog_unload(self):
		for state in self.voice_states.values():
			self.bot.loop.create_task(state.stop())

	def cog_check(self, ctx: commands.Context):
		if not ctx.guild:
			raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

		return True

	async def cog_before_invoke(self, ctx: commands.Context):
		ctx.voice_state = self.get_voice_state(ctx)

	@commands.command(name='join', invoke_without_subcommand=True)
	async def _join(self, ctx: commands.Context):
		"""Make the bot join the voice channel you're connected to."""
		destination = ctx.author.voice.channel

		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.send(f"Joined **{ctx.guild.me.voice.channel}**")
		

	@commands.command(name='leave', aliases=['disconnect'])
	@commands.has_permissions(manage_guild=True)
	async def _leave(self, ctx: commands.Context):
		"""Make the bot leave the joined voice channel"""
		if not ctx.voice_state.voice:
			return await ctx.send('Not connected to any voice channel.')
		try:
			ctx.author.voice.channel
		except AttributeError:
			return await ctx.send("You're not in a voice channel.")
		
		await ctx.voice_state.stop()
		del self.voice_states[ctx.guild.id]
		await ctx.send(f"Left **{ctx.guild.me.voice.channel}**")

	@commands.command(name='volume')
	async def _volume(self, ctx: commands.Context, *, volume: int=50):
		"""Change the volume of the bot, from 0 to 100."""
		try:
			ctx.author.voice.channel
		except AttributeError:
			return await ctx.send("You're not in a voice channel.")

		if not ctx.voice_state.is_playing:
			return await ctx.send('Nothing being played at the moment.')

		if 0 > volume or volume > 100:
			return await ctx.send('Volume must be between 0 and 100')

		#music = self.bot.get_cog('Music')
		#voice, voice.source = await music.voice_connect(ctx)
		voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		voice.source.volume = volume/100
		#state = VoiceState(self.bot, ctx)
		#state._volume = volume/100
		#state.volume = volume/100
		#state.volume_change(volume/100)
		#ctx.voice_state.volume = volume / 100
		await ctx.send('Volume of the player set to {}%'.format(volume))
		

	@commands.command(name='now', aliases=['current', 'playing'])
	async def _now(self, ctx: commands.Context):
		"""See the details of the song playing currently"""
		if not ctx.voice_state.is_playing:
			
			return await ctx.send('Nothing being played at the moment.')
		await ctx.send(embed=ctx.voice_state.current.create_embed())
		

	@commands.command(name='pause')
	# @commands.has_permissions(manage_guild=True)
	async def _pause(self, ctx: commands.Context):
		"""Pause the music."""
		try:
			ctx.author.voice.channel
		except AttributeError:
			
			return await ctx.send("You're not in a voice channel.")

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
			ctx.voice_state.voice.pause()
			await ctx.message.add_reaction('⏸️')
		else:
			
			return await ctx.send('Nothing being played at the moment.')
		

	@commands.command(name='resume')
	# @commands.has_permissions(manage_guild=True)
	async def _resume(self, ctx: commands.Context):
		"""Resume paused music"""
		try:
			ctx.author.voice.channel
		except AttributeError:
			
			return await ctx.send("You're not in a voice channel.")

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
			ctx.voice_state.voice.resume()
			await ctx.message.add_reaction('⏯')
		else:
			
			return await ctx.send('Nothing being played at the moment.')
		

	@commands.command(name='stop')
	@commands.has_permissions(manage_guild=True)
	async def _stop(self, ctx: commands.Context):
		"""Stop the music playing."""
		try:
			ctx.author.voice.channel
		except AttributeError:
			
			return await ctx.send("You're not in a voice channel.")

		ctx.voice_state.songs.clear()

		if ctx.voice_state.is_playing:
			ctx.voice_state.voice.stop()
			ctx.voice_state.stop_playing_you_idiot()
			await ctx.message.add_reaction('⏹')
		else:
			
			return await ctx.send('Nothing being played at the moment.')
		

	@commands.command(name='skip')
	async def _skip(self, ctx: commands.Context):
		"""Vote to skip a song. The requester can automatically skip. 3 skip votes are needed for the song to be skipped.
		"""
		try:
			ctx.author.voice.channel
		except AttributeError:
			return await ctx.send("You're not in a voice channel.")

		if not ctx.voice_state.is_playing:
			return await ctx.send('Not playing any music right now...')

		voter = ctx.message.author
		if voter == ctx.voice_state.current.requester:
			await ctx.message.add_reaction('⏭')
			ctx.voice_state.skip()

		elif voter.id not in ctx.voice_state.skip_votes:
			ctx.voice_state.skip_votes.add(voter.id)
			total_votes = len(ctx.voice_state.skip_votes)

			if total_votes >= 3:
				await ctx.message.add_reaction('⏭')
				ctx.voice_state.skip()
			else:
				await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

		else:
			await ctx.send('You have already voted to skip this song.')

	@commands.command(aliases=['fs'])
	async def forceskip(self, ctx: commands.Context):
		"""Force skip a song. The requester, server owner, or an admin can automatically skip."""
		try:
			ctx.author.voice.channel
		except AttributeError:
			return await ctx.send("You're not in a voice channel.")

		if not ctx.voice_state.is_playing:
			return await ctx.send('Not playing any music right now...')
		
		if ctx.author.guild_permissions.administrator or ctx.author == ctx.guild.owner or ctx.author == ctx.voice_state.current.requester:
			await ctx.message.add_reaction('⏭')
			ctx.voice_state.skip()
		else:
			await ctx.reply("Plebs can't use this command lol get rekt", mention_author=False)

	@commands.command(name="replay")
	async def _replay(self, ctx:commands.Context):
		pass
	
	@commands.command(aliases=['q'])
	async def _queue(self, ctx: commands.Context, *, page: int = 1):
		"""See the song queue."""
		if len(ctx.voice_state.songs) == 0:
			return await ctx.send('Empty queue.')

		items_per_page = 10
		pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

		start = (page - 1) * items_per_page
		end = start + items_per_page

		queue = ''
		for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
			queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

		embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
				.set_footer(text='Viewing page {}/{}'.format(page, pages)))
		await ctx.send(embed=embed)
		

	@commands.command(name='shuffle')
	async def _shuffle(self, ctx: commands.Context):
		"""Shuffle the queue"""
		try:
			ctx.author.voice.channel
		except AttributeError:
			
			return await ctx.send("You're not in a voice channel.")

		if len(ctx.voice_state.songs) == 0:
			
			return await ctx.send('Empty queue.')

		ctx.voice_state.songs.shuffle()
		await ctx.message.add_reaction('🔀')
		
	
	@commands.command(name='remove')
	async def _remove(self, ctx: commands.Context, index: int=None):
		"""Remove a song from the queue"""
		try:
			ctx.author.voice.channel
		except AttributeError:
			return await ctx.send("You're not in a voice channel.")

		if not index:
			return await ctx.send("Since no song index was specified, all songs will be removed <:yeet:817301996256231444>")

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send('Empty queue.')

		ctx.voice_state.songs.remove(index - 1)
		await ctx.message.add_reaction('✅')
		

	@commands.command(name='loop')
	async def _loop(self, ctx: commands.Context):
		"""Loop/unloop the currently playing song."""
		try:
			ctx.author.voice.channel
		except AttributeError:
			return await ctx.send("You're not in a voice channel.")

		if not ctx.voice_state.is_playing:
			return await ctx.send('Nothing being played at the moment.')

		# Inverse boolean value to loop and unloop.
		ctx.voice_state.loop = not ctx.voice_state.loop
		await ctx.message.add_reaction('🔁')
		

	@commands.command(name='play')
	@commands.guild_only()
	async def _play(self, ctx: commands.Context, *, search: str):
		"""Plays a song. If there are songs in the queue, this will be queued until the other songs finished playing.
		"""
		if not ctx.voice_state.voice:
			await ctx.invoke(self._join)
		# elif ctx.voice_state.voice and len(ctx.voice_state.songs) == 0:
		# 	await ctx.invoke(self._leave)
		# 	await ctx.invoke(self._join)

		ctx.voice_state.skip_votes = set()

		if not search.startswith("https://open.spotify.com/"):
			async with ctx.typing():
				try:
					subprocess.check_call(["youtube-dl", "--rm-cache-dir"])
					source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
				except YTDLError as e:
					await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
				else:
					song = Song(source) #creates embed
					# vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
					# if not vc.is_playing():
					await ctx.voice_state.songs.put(song)
					await ctx.send('Enqueued {}'.format(str(source)))
		else:
			username = 'xzxtecn4384hqvazcdhvjeoij'
			client_id = os.environ['SPOTIPY_CLIENT_ID']
			client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
			redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
			scope = 'playlist-modify-public'
			manager=spotipy.oauth2.SpotifyOAuth(username=username, scope=scope,\
								redirect_uri=redirect_uri, client_id=client_id, client_secret=client_secret)
			# cc = self.bot.get_channel(853643406329118740)
			# await cc.send(manager.get_authorize_url())
			token = util.prompt_for_user_token(username=username, scope=scope, redirect_uri=redirect_uri, client_id=client_id, client_secret=client_secret)
			sp = spotipy.Spotify(auth=token,auth_manager=manager)
			if "playlist" in search:
				playlist = search.split("/")[-1]
				playlist = playlist.split("?")[0]
				try:
					res = sp.user_playlist_tracks(username, playlist)
				except spotipy.SpotifyException:
					return await ctx.send("That playlist does not exist.")
				for items in res["items"]:
					song = items["track"]["name"]
					artist = items["track"]["artists"][0]["name"]
					songToPlay = str(song) + " " + str(artist)
					if "--lyrics" in search:
						songToPlay += " lyrics"
					subprocess.check_call(["youtube-dl", "--rm-cache-dir"])
					try:
						await self.spotify_play(ctx, search=songToPlay)
					except YTDLError:
						songToPlay = str(song)
						try:
							await self.spotify_play(ctx, search=songToPlay)
						except YTDLError:
							songToPlay = str(song) + " lyrics"
							await self.spotify_play(ctx, search=songToPlay)
				for i in range(math.ceil(len(ctx.voice_state.songs) / 10)):
					await self._queue(ctx, page=i+1)
			elif "track" in search:
				track = search.split("/")[-1]
				try:
					res = sp.track(track)
				except spotipy.SpotifyException:
					return await ctx.send("That track does not exist.")
				song = res['name']
				artist = res['artists'][0]['name']
				songToPlay = str(song) + " " + str(artist)
				if "--lyrics" in search:
						songToPlay += " lyrics"
				subprocess.check_call(["youtube-dl", "--rm-cache-dir"])
				try:
					await self._play(ctx, search=songToPlay)
				except YTDLError:
						songToPlay = str(song)
						try:
							await self._play(ctx, search=songToPlay)
						except YTDLError:
							songToPlay = str(song) + " lyrics"
							await self._play(ctx, search=songToPlay)
			elif "album" in search:
				album = search.split("/")[-1]
				album = album.split("?")[0]
				try:
					res = sp.album_tracks(album)
				except spotipy.SpotifyException:
					return await ctx.send("That album does not exist.")
				for items in res["items"]:
					song = items["name"]
					artist = items["artists"][0]["name"]
					songToPlay = str(song) + " " + str(artist)
					if "--lyrics" in search:
						songToPlay += " lyrics"
					subprocess.check_call(["youtube-dl", "--rm-cache-dir"])
					try:
						await self.spotify_play(ctx, search=songToPlay)
					except YTDLError:
						songToPlay = str(song)
						try:
							await self.spotify_play(ctx, search=songToPlay)
						except YTDLError:
							songToPlay = str(song) + " lyrics"
							await self.spotify_play(ctx, search=songToPlay)
				for i in range(math.ceil(len(ctx.voice_state.songs) / 10)):
					await self._queue(ctx, page=i+1)

	@commands.command(aliases=['splay'], hidden=True)
	@commands.guild_only()
	@commands.check_any(commands.is_owner())
	async def spotify_play(self, ctx, *, search:str):
		ctx.voice_state.skip_votes = set()

		# vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		# if not vc.is_playing():
		async with ctx.typing():
			try:
				subprocess.check_call(["youtube-dl", "--rm-cache-dir"])
				source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
			except YTDLError as e:
				await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
			else:
				song = Song(source) #embed
				await ctx.voice_state.songs.put(song)
				#await ctx.send('Enqueued {}'.format(str(source)))
	
	@commands.command(name='lyrics')
	@commands.guild_only()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def get_lyrics(self, ctx, *, query: str=""):
		"""Get the lyrics to a song."""
		LYRICS_URL = "https://some-random-api.ml/lyrics?title="
		if not query:
			songs = ctx.voice_state.current
			if songs:
				query = songs.source.title
				# _start = query.find("(")
				# _end = query.find(")")
				# if _start >= 0 and _start < _end:
				# 	query = query[:_start] + query[_end+1:]
			else:
				return await ctx.reply("I'm not currently playing anything", mention_author=False)
		# if not player.is_playing():
		# 	return await ctx.reply("I'm not currently playing anything", mention_author=False)
		async with ctx.typing():
			async with aiohttp.request("GET", LYRICS_URL + query, headers={}) as r:
				if not 200 <= r.status <= 299:
					g_api = os.environ['GENIUS_API']
					genius = Genius(g_api)
					genius.verbose = False
					genius.remove_section_headers = True
					genius.skip_non_songs = True
					genius.excluded_terms = ["(Remix", "(Cover", "(Live", "Remix)", "Cover)", "Live)"]
					songs = genius.search_songs(query)
					try:
						url = songs['hits'][1]['result']['url']
						song_lyrics = (genius.lyrics(song_url=url))[:-27]
						for i in range(1, 5):
							if not song_lyrics[-1].isdigit():
								break
							song_lyrics = song_lyrics[:-1]
						song_lyrics = song_lyrics.replace("*", "\*")
						# for i in range(len(song_lyrics)):
						# 	if song_lyrics[i] == "*":
						if len(song_lyrics) > 4095:
							stop = song_lyrics[:4095][::-1].find("\n")
							e = discord.Embed(title=songs['hits'][1]['result']['title'], description=(song_lyrics[:4095-stop]), colour=discord.Colour.random(), timestamp=datetime.utcnow())
							e.set_author(name=songs['hits'][1]['result']['artist_names'])
							e.set_thumbnail(url=songs['hits'][1]['result']['song_art_image_url'])
							e.set_footer(text=f"Full lyrics at {songs['hits'][1]['result']['url']}")
							return await ctx.send(embed=e)
						e = discord.Embed(title=songs['hits'][1]['result']['title'], description=song_lyrics, colour=discord.Colour.random(), timestamp=datetime.utcnow())
						e.set_author(name=songs['hits'][1]['result']['artist_names'])
						e.set_thumbnail(url=songs['hits'][1]['result']['header_image_thumbnail_url'])
						e.set_footer(text=f"Requested by {ctx.author}")
						return await ctx.send(embed=e)
					except IndexError:
						return await ctx.send("I couldn't find that song!")

				data = await r.json()
				if len(data["lyrics"]) > 4095:
					stop = data["lyrics"][:4095][::-1].find("\n")
					embed = discord.Embed(
					title=data["title"],
					description=(data["lyrics"][:4095-stop] + "..."),
					colour=discord.Colour.random(),
					timestamp=datetime.utcnow(),
					)
					embed.set_thumbnail(url=data["thumbnail"]["genius"])
					embed.set_author(name=data["author"])
					embed.set_footer(text=f"Full lyrics at {data['links']['genius']}")
					return await ctx.send(embed=embed)

				embed = discord.Embed(
					title=data["title"],
					description=data["lyrics"],
					colour=discord.Colour.random(),
					timestamp=datetime.utcnow(),
				)
				embed.set_thumbnail(url=data["thumbnail"]["genius"])
				embed.set_author(name=data["author"])
				embed.set_footer(text=f"Requested by {ctx.author}")
				await ctx.send(embed=embed)
			r.close()

	@_join.before_invoke
	@_play.before_invoke
	async def ensure_voice_state(self, ctx: commands.Context):
		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.CommandError('You are not connected to any voice channel.')

		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				raise commands.CommandError('Bot is already in a voice channel.')
def setup(bot):
	bot.add_cog(Music(bot))