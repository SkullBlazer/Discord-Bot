import nest_asyncio
import discord
import asyncio
from async_timeout import timeout
import youtube_dl
import os
#import sys
#import subprocess
from dotenv import load_dotenv
from discord.ext import commands
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'discord-py-slash-command'])
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import openai
import random
#import re
from datetime import datetime
from time import time, perf_counter
#from discord.utils import get
from PIL import Image
from typing import Optional
#import json
import math
import numpy as np
import cv2
import imageio
import scipy.ndimage
#import urllib.parse, urllib.request
import requests
import itertools
import functools
import wikipedia
#import ksoftapi
#import lavalink
import pycountry
import xkcd
import pypokedex
from keep_alive import keep_alive
from replit import db

intents = discord.Intents.all()
load_dotenv()
nest_asyncio.apply()
token = os.environ['DISCORD_TOKEN']

def get_prefix(bot, message):
	# with open('datafiles/prefixes.json') as fle:
		# prefixes = json.load(fle)
	if not isinstance(message.channel, discord.DMChannel):
		return db[str(message.guild.id)]
	else:
		return ">>"


bot = commands.Bot(command_prefix=get_prefix,
				   case_insensitive=True,
				   intents=intents)
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)
r = requests.head(url="https://discord.com/api/v1")
try:
	print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
	print("No rate limit")
#kclient = ksoftapi.Client('')
count = 7
temp = 0
players = {}
queues = {}
d_author = {}
d_content = {}
e_author = {}
e_content1 = {}
e_content2 = {}
gaem = []
start_time = time()
once = 0
flag = False
trusted = [
	785230154258448415, 781150150630440970, 777217934074445834,
	785564485384405033, 783643344202760213, 767752540980248586
]

words = [
	'conversation', 'bowtie', 'skateboard', 'penguin', 'hospital', 'player',
	'kangaroo', 'garbage', 'whisper', 'achievement', 'flamingo', 'calculator',
	'offense', 'spring', 'performance', 'sunburn', 'reverse', 'round', 'horse',
	'nightmare', 'popcorn', 'hockey', 'exercise', 'programming', 'platypus',
	'blading', 'music', 'opponent', 'electricity', 'telephone', 'scissors',
	'pressure', 'monkey', 'coconut', 'backbone', 'rainbow', 'frequency',
	'factory', 'cholesterol', 'lighthouse', 'president', 'palace', 'excellent',
	'telescope', 'python', 'government', 'pineapple', 'volcano', 'alcohol',
	'mailman', 'nature', 'dashboard', 'science', 'computer', 'circus',
	'earthquake', 'bathroom', 'toast', 'football', 'cowboy', 'mattress',
	'translate', 'entertainment', 'glasses', 'download', 'water', 'violence',
	'whistle', 'alligator', 'independence', 'pizza', 'permission', 'board',
	'pirate', 'battery', 'outside', 'condition', 'shallow', 'baseball',
	'lightsaber', 'dentist', 'pinwheel', 'snowflake', 'stomach', 'reference',
	'password', 'strength', 'mushroom', 'student', 'mathematics',
	'instruction', 'newspaper', 'gingerbread', 'emergency', 'lawnmower',
	'industry', 'evidence', 'dominoes', 'lightbulb', 'stingray', 'background',
	'atmosphere', 'treasure', 'mosquito', 'popsicle', 'aircraft', 'photograph',
	'imagination', 'landscape', 'digital', 'pepper', 'roller', 'bicycle',
	'toothbrush', 'newsletter', 'rhythm', 'quixotic', 'vanquish', 'jeopardy'
]

images = [
	'```\n	   +--┬--+ \n	   |  | \n	   |  😵 \n	   | /|\\ \n	   | / \\ \n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |  | \n	   |  O \n	   | /|\\ \n	   | /	\n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |  | \n	   |  O \n	   | /|\\ \n	   |	  \n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |  | \n	   |  O \n	   | /|   \n	   |	  \n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |  | \n	   |  O \n	   |  |   \n	   |	  \n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |  | \n	   |  O \n	   |	  \n	   |	  \n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |  | \n	   |	\n	   |	  \n	   |	  \n	   | \n		‾‾‾‾‾```',
	'```\n	   +--┬--+ \n	   |	\n	   |	\n	   |	  \n	   |	  \n	   | \n		‾‾‾‾‾```'
]

movies = ['The Shawshank Redemption', 'The Godfather', 'The Hurt Locker', 'The Dark Knight', "Ocean's Eleven",\
		  "Schindler's List", 'The Incredibles','Pulp Fiction', 'The Good, the Bad and the Ugly',\
		  'The Wolf of Wall Street', 'Fight Club','Forrest Gump', 'Inception', 'Get Out', 'Titanic',\
		  'The Matrix', 'Lost in Translation', "The Terminator", 'No Country For Old Men', 'Se7en',\
		  'The Exorcist', 'Rocky', 'The Silence of the Lambs', "Captain America: Civil War",\
		  'Saving Private Ryan', 'The Green Mile', 'La La Land', 'Interstellar', 'Parasite', 'Drive',\
		  'Die Hard', 'The Usual Suspects', 'The Lion King', 'Jurassic Park', 'Back to the Future',\
		  'Terminator 2: Judgment Day', 'Blade Runner 2049', 'Modern Times', 'Gladiator', 'Psycho',\
		  'The Departed', 'City Lights', 'Beauty and the Beast', 'Mary Poppins', 'Groundhog Day',\
		  'Apocalypse Now', 'Memento', 'The Great Dictator', 'The Big Lebowski', 'Hamilton',\
		  'Django Unchained', 'Joker', 'WALL-E', 'The Shining', 'Avengers: Infinity War',\
		  'Spider-Man: Into the Spider-Verse', 'The Dark Knight Rises', 'Avengers: Endgame',\
		  'American Beauty', 'Braveheart', 'Toy Story', 'Inglourious Basterds', 'Good Will Hunting',\
		  '2001: A Space Odyssey', 'Requiem for a Dream' 'Eternal Sunshine of the Spotless Mind',\
		  'Citizen Kane', 'Escape Room']


wordmovies = ['Argo', 'Maleficent', 'Planes', 'Jumanji', 'Frozen', "Brave", 'Pinocchio','Gravity', 'Scream',\
			 'Skyfall', 'Cinderella', 'Cube', 'Inception', 'Divergent', 'Ratatouille', 'Salt',\
			 "Batman", 'Madagascar', 'Se7en', 'Up', 'Cars', 'Saw', "Tangled", 'Aladdin', 'Shrek', 'Enchanted',\
			 'Bolt', 'Interstellar','Parasite', 'Jaws', 'Twilight', 'Superman', 'Rocky', 'Bambi', 'Gladiator',\
			 'Psycho', 'Titanic', 'Moana', 'Speed', 'Avatar', 'Ghostbusters', 'Predator', 'Casablanca',\
			 'Matilda', 'Robocop', 'Alien', 'Dumbo', 'Memento', 'Deadpool', 'Annabelle', 'Hamilton', 'Joker',\
			 'Aliens', 'Coco', 'Braveheart', 'Vertigo', 'Taken', 'JFK', 'Extraction', 'Zootopia', 'Her',\
			 'Arrival', 'Thor', 'Armageddon', 'Logan', 'Dunkirk', 'Troy', 'Juno', 'Chef', 'Nightcrawler',\
			 'Hancock', 'Poseidon', 'Transformers', 'Wanted', 'Hulk', 'Tarzan', 'Rango', 'Tron', 'Megamind',\
			 'Godzilla', 'Zoolander', 'Paddington', 'Ted', 'Drive', 'Zodiac', 'Unbreakable', 'Midsommar',\
			 'Glass', 'Unstoppable', 'Grey', 'Hereditary', 'Chappie', 'Bumblebee', 'Legend', 'Rocketman',\
			 'Bombshell', 'Tenet']


@bot.event
async def on_ready():
	global once
	# try:
	# 	with open("datafiles/data.txt") as json_file:
	# 		credits = json.load(json_file)
	# except FileNotFoundError:
	# 	print("Could not load file")
	# 	credits = {}
	await bot.wait_until_ready()
	# await bot.change_presence(activity=discord.Activity(
	# 	type=discord.ActivityType.watching, name="Avadhoot's birthday"))
	await bot.change_presence(activity=discord.Game(name="End of First Year"))
	# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="my master panik about exams"))
	# await bot.change_presence(status=discord.Status.dnd)
	# await bot.change_presence(activity=discord.Streaming(name="the exam answers", url="https://youtu.be/dQw4w9WgXcQ"))
	cur_date = datetime.utcnow()
	if (cur_date >= datetime(2021, 9, 10, 5, 30, 0) and (once == 0)):
		channel = bot.get_channel(828343472120922176)
		await channel.send("@everyone your Nitro is about to end!")
		once += 1


# @bot.event
# async def on_member_remove(member):
#	 channel = bot.get_channel(781150150630440973)
#	 await channel.send(f"{member} couldn't handle this server")


@bot.event
async def on_guild_join(guild):
	channel = guild.text_channels[0]
	link = await channel.create_invite()
	user = bot.get_user(305341210443382785)
	await user.send(f"I have been added to a server {guild.name} and its owner is {guild.owner}")
	await user.send(link)
	# with open('datafiles/prefixes.json') as fle:
		# prefixes = json.load(fle)
	db[str(guild.id)] = ['false', '>>']
	# with open('datafiles/prefixes.json', 'w') as fle:
	# 	json.dump(prefixes, fle, indent=4)
	# with open('datafiles/onmessage.json', 'w') as fle:
	# 	json.dump(ar, fle, indent=4)


#	await guild.create_role(name="Moderator", colour=discord.Colour(0x7289da), permissions=discord.Permissions.all())
	await guild.create_role(name="Invisible", colour=discord.Colour(0x36393e))
	await guild.create_role(name="Red", colour=discord.Colour(0xff0000))
	await guild.create_role(name="Blue", colour=discord.Colour(0x0075ff))
	await guild.create_role(name="Green", colour=discord.Colour(0xb0ff00))
	await guild.create_role(name="Yellow", colour=discord.Colour(0xffff00))
	await guild.create_role(name="Gold", colour=discord.Colour(0xffb700))
	await guild.create_role(name="Purple", colour=discord.Colour(0x8700ff))
	await guild.create_role(name="Orange", colour=discord.Colour(0xff8b00))
	await guild.create_role(name="Cyan", colour=discord.Colour(0x1abc9c))
	await guild.create_role(name="Pink", colour=discord.Colour(0xff1493))
	await guild.create_role(name="White", colour=discord.Colour(0xffffff))
	await guild.create_role(name="Black", colour=discord.Colour(0x000001))

@bot.event
async def on_guild_remove(guild):
	del db[str(guild.id)]

@bot.event
async def on_message_delete(message):
	global d_author, d_content, flag
	if not (message.author.bot):
		d_author[message.channel.id] = message.author
		d_content[message.channel.id] = message.content
		if not d_content[message.channel.id]:
			d_content[message.channel.id] = message.attachments[0].proxy_url
			flag = True
		await asyncio.sleep(75)
		try:
			del d_author[message.channel.id]
			del d_content[message.channel.id]
		except KeyError:
			d_author = {}
			d_content = {}
	if message.guild.id == 785230154258448415:
		c = bot.get_channel(853643406329118740)
		try:
			await c.send(message.content)
		except discord.errors.HTTPException:
			await c.send(message.attachments[0].proxy_url)


@bot.event
async def on_message_edit(message_before, message_after):
	global e_author, e_content1, e_content2
	if not (message_before.author.bot):
		e_author[message_before.channel.id] = message_before.author
		e_content1[message_before.channel.id] = message_before.content
		e_content2[message_after.channel.id] = message_after.content
		await asyncio.sleep(90)
		try:
			del e_author[message_before.channel.id]
			del e_content1[message_before.channel.id]
			del e_content2[message_after.channel.id]
		except KeyError:
			e_author = {}
			e_content1 = {}
			e_content2 = {}


@bot.event
async def on_command_error(ctx, error):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	if isinstance(error, commands.CommandNotFound):
		if p in str(error):
			if p != '.':
				await ctx.send(
					f"Bro how many {p} are you gonna put in the command")
		else:
			rng = random.randint(1,100)
			if rng == 78:
				await ctx.send("You do not have permissions to run this command.")
				await asyncio.sleep(1)
				await ctx.send("~~Jk that's not a real command, but you received the secret error message!~~")
			else:
				await ctx.send("That.... that's not a valid command")
	elif isinstance(error, commands.CheckAnyFailure) and (ctx.command.name == edit):
		await ctx.send("That.... that's not a valid command")
		return
	elif (not isinstance(error, commands.CheckAnyFailure)) and (ctx.command.name != edit):
		await ctx.send(error)

@bot.command(aliases=['h'])
@commands.cooldown(1, 2, commands.BucketType.user)
async def help(ctx, page: str = None):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	if page is None or page.lower() in ("1", "2", "3", "4", "5", "6", "7",
										"action", "actions", "utilities",
										"utils", "fun", "games", "currency",
										"stonks", "youtube"):
		contents = [
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Utilities**\n \
		`{p}help [query]` \n > Gives a list of commands, as you should have figured out by now\n \
		`{p}invite` \n > Invite me to your server so I can hack it, I mean attack, no, uhh bring back it.\n \
		`{p}colourchange <colour>` \n > Change your name's colour to distract people from your inability to make a cool username.\n \
		`{p}userinfo [@person]` \n > Get your info, or someone else's, like a stalker\n \
		`{p}serverinfo` \n > Get your server's info (insert joke here because I ran out)\n \
		`{p}kick <@person> [reason]` \n > Yeet someone out of the server, but give a reason.\n \
		`{p}ban <@person> [reason]` \n > Strike the banhammer on a poor victim, with good reason.\n \
		`{p}suggest` \n > Suggest a command to be added, report a bug, or report that the bot is monitoring you (Warning: You will mysteriously die if you do the last one)",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Utilities** (continued)\n \
		`{p}ping` \n > See how fast your internet is. (Code copied by my 290ms latency internet) \n \
		`{p}unban <User ID>` \n > Feeling terrible for banning someone? Well, I gotchu\n \
		`{p}nick [@person] [name]`\n > Something embarrassing happened to you? Well, now you can change your name and move to Antarctica! (Tickets not included)\n \
		`{p}uptime`\n > See how long the bot has been alive for. I'll tell you right now, not more than Queen Elizabeth.\n \
		`{p}prefix <prefix>`\n > Hate typing two `>>`s? Well now you can change it!\n \
		`{p}stalkermode [true|false]` \n > Hate it when the bot reads your messages? Now you can get a false sense of belief it's not doing that anymore!\n \
		`{p}patchnotes`\n > Gives info on the new features\n \
		`{p}snipe` \n > This command is not for hiring a hitman, it just sends you the last deleted message in the channel.\n \
		`{p}editsnipe` \n > See what your \"friend\" actually thinks of you, by seeing what they originally said but didn't delete the message to avoid getting `{p}snipe`d ",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Actions**\n \
		`{p}choose <options separated by spaces>` \n > Give the bot some options, and it will choose one for you!\n \
		`{p}hello` \n > Just say hello, you don't need to be a rocket scientist to figure this out\n \
		`{p}stab [@person(s)] [reason]` \n > Stab someone (or many people, in case you're really mad) for some reason\n \
		`{p}pat [@person(s)] [reason]` \n > Pat someone (I am that 'someone')\n \
		`{p}bonk [@person] [reason]` \n > Bonk someone to their senses. Or just do a :sparkles: Vibe check :sparkles:\n \
		`{p}yeet [@person] [reason]`\n > Yeet someone when you're sick of them\n \
		`{p}say <phrase>`\n > Make the bot say something, like admit to a crime ~~you committed~~ it didn't commit \n \
		`{p}poll <question>`\n > ~~Watch live footage of SlaveBot dancing on a pole.~~ Make a poll. \n \
		`{p}fight <@person> <weapon>` \n > Worried someone might defeat you in a fight in real life? Well now you can test the outcomes!",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Actions** (continued)\n \
		`{p}trigger` \n > Angry because someone used `{p}fight` on you and won? Well now you can express your emotions!\n \
		`{p}blackandwhite` \n > Want to feel like a 90's kid? Guess what\n \
		`{p}cartoon` \n > Cartoonify yourself. **[BETA]** \n \
		`{p}draw` \n > Draw my life, except it draws nothing from your life except for your profile picture\n \
		`{p}encrypt <message>` \n > Encrypt your messages so you think the bot wouldn't be able to read them.\n \
		`{p}decrypt <message>` \n > Decrypt your ~~already decrypted and sent to the FBI~~ plans your friend sent you to overthrow the government \n \
		`{p}wikisearch <term>` \n > Want to settle a debate? This command brings you facts from Wikipedia! ~~I accept cash in case you want the Wiki page to be slightly edited in your favour~~\n \
		`{p}weather <location>` \n > A one stop command for all your weather needs!",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Fun**\n \
		`{p}rps <rock|paper|scissors>` \n > Play rock, paper, scissors with the bot (which is you)\n \
		`{p}cointoss` \n > Toss a coin, leave your decisions up to me, unless it's a bad decision. Then that's your fault.\n \
		`{p}roll [guess]` \n > Roll a 6-sided die to decide your fate. Or to play Snakes and Ladders, I don't care. \n \
		`{p}numguess` \n > Guess a number. If you keep guessing ||69|| I will punch you. \n \
		`{p}8ball <question>` \n > Ask the Magic 8 Ball a question. Again, SlaveBot is not responsible for damage of any hopes or property that you destroyed in anger.\n \
		`{p}battleships` \n > Find my 1x1 ship in a 5x5 grid, or ***D I E*** \n \
		`{p}hangman [gamemode]` \n > Contrary to popular belief, this game is not to hang a real person. \n \
		`{p}slots` \n > Get 3 of the same fruit to win tons of money. Someone calculate and tell me what the chances of winning are. \n \
		`{p}joke` \n > Get a joke instantly to remove the awkward tension \n \
		`{p}xkcd [parameter]` \n > Get an xkcd comic then cry because you can't understand it, and cry even more when you can't even understand the explanation.",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Currency**\n \
		`{p}register` \n > Register for a life of fun (and some ~~fake~~ dolla bills)\n \
		`{p}daily` \n > Get that dough as you pass Go, every 23 hours (Hey that rhymed)\n \
		`{p}balance [@person]` \n > Check how rich you are\n \
		`{p}transfer <@person> <amount>` \n > Feeling like a Good Samaritan? Donate! (5% of the money transferred goes to ~~me~~ taxes)\n \
		`{p}save` \n > Save your progress \n \
		`{p}rich` \n > See the richest people in the server (Don't ask how I got 100 decillion, 10^35 for the nerds out here)",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
	 and `x|y` signifies x OR y**\n \
	*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
	**Youtube**\n \
		`{p}join` \n > Join our cult. Jk, makes the bot join your voice channel ~~to spy on your conversations~~\n \
		`{p}play <URL|song name>` \n > Play dem beats. Give either the link to the Youtube video or type its name\n \
		`{p}pause` \n > Pause the music to hear your friend's ranting\n \
		`{p}resume` \n > Resume the music because their ranting's too boring\n \
		`{p}stop` \n > Stop the music ~~Get some help~~\n \
		`{p}lyrics <song name>` \n > See the lyrics to a song and realize you've been singing nonsense this whole time\n \
		`{p}leave` \n > Make the bot leave the channel ~~because you found out that the bot records conversations~~"
		]
		#57
		cur_page = 1
		ncontents = []
		if page:
			if page == "1" or page.lower() == "utilities" or page.lower(
			) == "utils":
				if page.isalpha():
					ncontents.append(contents[0])
					ncontents.append(contents[1])
				else:
					ncontents = contents
					cur_page = 1
			elif page == "2":
				ncontents = contents
				cur_page = 2
			elif page == "3" or page.lower() == "action" or page.lower(
			) == "actions":
				if page.isalpha():
					ncontents.append(contents[2])
					ncontents.append(contents[3])
				else:
					ncontents = contents
					cur_page = 3
			elif page == "4":
				ncontents = contents
				cur_page = 4
			elif page == "5" or page.lower() == "fun" or page.lower(
			) == "games":
				if page.isalpha():
					ncontents.append(contents[4])
				else:
					ncontents = contents
					cur_page = 5
			elif page == "6" or page.lower() == "currency" or page.lower(
			) == "stonks":
				if page.isalpha():
					ncontents.append(contents[5])
				else:
					ncontents = contents
					cur_page = 6
			elif page == "7" or page.lower() == "youtube" or page.lower(
			) == "music":
				if page.isalpha():
					ncontents.append(contents[6])
				else:
					ncontents = contents
					cur_page = 7
		else:
			ncontents = contents

		pages = len(ncontents) + 1
		e = discord.Embed(title="List of commands for ya noobs",
						  description=ncontents[cur_page - 1])
		e.colour = discord.Colour.dark_blue()
		e.timestamp = datetime.utcnow()
		e.set_footer(text=f"Page {cur_page} of {pages-1}")
		message = await ctx.send(embed=e)

		if len(ncontents) == 1:
			await message.add_reaction("⏹️")
		else:
			await message.add_reaction("◀️")
			await message.add_reaction("⏹️")
			await message.add_reaction("▶️")

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in [
				"◀️", "⏹️", "▶️"
			] and reaction.message == message

		while True:
			try:
				reaction, user = await bot.wait_for("reaction_add",
													timeout=120.0,
													check=check)
				if str(reaction.emoji) == "▶️" and pages > 2:
					if cur_page != pages - 1:
						cur_page += 1
						e = discord.Embed(
							title="List of commands for ya noobs",
							description=ncontents[cur_page - 1])
						e.colour = discord.Colour.dark_blue()
						e.timestamp = datetime.utcnow()
						e.set_footer(text=f"Page {cur_page} of {pages-1}")
						await message.edit(embed=e)
						if ctx.guild:
							await message.remove_reaction(reaction, user)
					else:
						cur_page = 1
						e = discord.Embed(
							title="List of commands for ya noobs",
							description=ncontents[cur_page - 1])
						e.colour = discord.Colour.dark_blue()
						e.timestamp = datetime.utcnow()
						e.set_footer(text=f"Page {cur_page} of {pages-1}")
						await message.edit(embed=e)
						if ctx.guild:
							await message.remove_reaction(reaction, user)

				elif str(reaction.emoji) == "◀️" and pages > 2:
					if cur_page > 1:
						cur_page -= 1
						e = discord.Embed(
							title="List of commands for ya noobs",
							description=ncontents[cur_page - 1])
						e.colour = discord.Colour.dark_blue()
						e.timestamp = datetime.utcnow()
						e.set_footer(text=f"Page {cur_page} of {pages-1}")
						await message.edit(embed=e)
						if ctx.guild:
							await message.remove_reaction(reaction, user)
					else:
						cur_page = pages - 1
						e = discord.Embed(
							title="List of commands for ya noobs",
							description=ncontents[cur_page - 1])
						e.colour = discord.Colour.dark_blue()
						e.timestamp = datetime.utcnow()
						e.set_footer(text=f"Page {cur_page} of {pages-1}")
						await message.edit(embed=e)
						if ctx.guild:
							await message.remove_reaction(reaction, user)

				elif str(reaction.emoji) == '⏹️':
					if ctx.guild:
						await message.clear_reactions()
					break
				else:
					if ctx.guild:
						await message.remove_reaction(reaction, user)
			except asyncio.TimeoutError:
				if ctx.guild:
					await ctx.message.delete()
					await message.delete()
				return

	elif page == "help" or page == 'h' or page == 'plshelp':
		e = discord.Embed(title=f"Help on `{p}help`", description="Get help!")
		e.add_field(name="Syntax", value=f"`{p}help|h [command]`")
	elif page == "invite" or page == 'inv':
		e = discord.Embed(title=f"Help on `{p}invite`",
						  description="Invite this bot to your server")
		e.add_field(name="Syntax", value=f"`{p}invite|inv`")
	elif page == "colourchange" or page == 'cc':
		e = discord.Embed(
			title=f"Help on `{p}colourchange`",
			description=
			f"Change your color.\nColors you can choose:\nBlue\nRed\nYellow\nOrange\nGreen\nPurple\nPink\nGold\nBlack\nWhite\n\
						 Do `{p}colourchange` to remove your colour role.")
		e.add_field(
			name="Syntax",
			value=
			f"`{p}colourchange|cc [Red|Blue|Green|Yellow|Orange|Gold|Purple|Pink|Black|White]`"
		)
	elif page == "userinfo" or page == 'ui':
		e = discord.Embed(title=f"Help on `{p}userinfo`",
						  description="Get anyone's info")
		e.add_field(name="Syntax", value=f"`{p}userinfo|uinfo|ui [@mention]`")
	elif page == "serverinfo" or page == 'si':
		e = discord.Embed(title=f"Help on `{p}serverinfo`",
						  description="Get server info")
		e.add_field(name="Syntax", value=f"`{p}serverinfo|si|sinfo`")
	elif page == "kick":
		e = discord.Embed(title=f"Help on `{p}kick`",
						  description="Kick someone off of your server")
		e.add_field(name="Syntax", value=f"`{p}kick <@mention> [reason]`")
	elif page == "ban":
		e = discord.Embed(
			title=f"Help on `{p}ban`",
			description="Ban someone from this server. Use wisely.")
		e.add_field(name="Syntax", value=f"`{p}ban <@mention> [reason]`")
	elif page == "ping":
		e = discord.Embed(
			title=f"Help on `{p}ping`",
			description=
			"Check how long it takes to send a packet from the bot and back to you"
		)
		e.add_field(name="Syntax", value=f"`{p}ping`")
	elif page == "unban":
		e = discord.Embed(title=f"Help on `{p}unban`",
						  description="Unban someone.")
		e.add_field(name="Syntax", value=f"`{p}unban <User ID>`")
	elif page == "nick":
		e = discord.Embed(
			title=f"Help on `{p}nick`",
			description=
			"Change your (or someone else's) nickname.\n Leave blank to reset."
		)
		e.add_field(name="Syntax", value=f"`{p}nick [@mention] [newname]`")
	elif page == "patchnotes" or page == 'pn':
		e = discord.Embed(title=f"Help on `{p}patchnotes`",
						  description="See latest updates and commands here")
		e.add_field(name="Syntax", value=f"`{p}patchnotes|pn`")
	elif page == "uptime" or page == 'ut':
		e = discord.Embed(
			title=f"Help on `{p}uptime`",
			description="Check how long the bot has been online for")
		e.add_field(name="Syntax", value=f"`{p}uptime|ut`")
	elif page == "prefix":
		e = discord.Embed(
			title=f"Help on `{p}prefix`",
			description=
			"Change the prefix to some other prefix. Leave blank to reset.")
		e.add_field(name="Syntax", value=f"`{p}nick [@mention] [newname]`")
	elif page == "snipe":
		e = discord.Embed(
			title=f"Help on `{p}snipe`",
			description=
			"See the message that was deleted in the channel. \nNote: Does not work for images."
		)
		e.add_field(name="Syntax", value=f"`{p}snipe`")
	elif page == "editsnipe":
		e = discord.Embed(
			title=f"Help on `{p}editsnipe`",
			description="See the message that was edited in the channel.")
		e.add_field(name="Syntax", value=f"`{p}editsnipe|esnipe`")
	elif page == "stalkermode" or page == "autoresponse":
		e = discord.Embed(
			title=f"Help on {p}stalkermode",
			description="Change the bot's autoresponse to either true or false."
		)
		e.add_field(name="Syntax",
					value=f"`{p}stalkermode|autoresponse [true|false]`")
	elif page == "suggest":
		e = discord.Embed(
			title=f"Help on {p}suggest",
			description="Suggest changes, report bugs, or any other important message related to SlaveBot"
		)
		e.add_field(name="Syntax",
					value=f"`{p}suggest`")
	elif page == "rps" or page == 'rockpaperscissors':
		e = discord.Embed(title=f"Help on `{p}rps`",
						  description="Play rock, paper, scissors with me")
		e.add_field(name="Syntax",
					value=f"`{p}rps|rockpaperscissors <rock|paper|scissors>`")
	elif page == "cointoss" or page == 'ct' or page == 'toss':
		e = discord.Embed(
			title=f"Help on `{p}cointoss`",
			description="Toss a coin\n ~~1% chance to lie on its side~~")
		e.add_field(name="Syntax", value=f"`{p}cointoss|ct`")
	elif page == "numguess" or page == 'ng' or page == 'guess':
		e = discord.Embed(
			title=f"Help on `{p}numguess`",
			description="Guess a number between 1 and 250 in 7 chances.")
		e.add_field(name="Syntax",
					value=f"`{p}numguess|ng|guess` \n `<guess>`")
	elif page == "roll":
		e = discord.Embed(title=f"Help on `{p}roll`",
						  description="Roll a 6-sided die. Duh.")
		e.add_field(name="Syntax", value=f"`{p}roll [guess]`")
	elif page == "8ball" or page == 'eightball':
		e = discord.Embed(
			title=f"Help on `{p}8ball`",
			description=
			"Ask the magic 8 ball a question. \n 1 in 20 chance for a surprise, you'll know it when you see it"
		)
		e.add_field(name="Syntax",
					value=f"`{p}8ball|eightball|ball8 <question>`")
	elif page == "battleships":
		e = discord.Embed(
			title=f"Help on `{p}battleships`",
			description=
			"Play a game of single player battleships to find a ship in 7 tries"
		)
		e.add_field(name="Syntax", value=f"`{p}battleships`")
	elif page == "hangman":
		e = discord.Embed(
			title=f"Help on `{p}hangman`",
			description="Guess a word within 6 tries or the little guy gets it."
		)
		e.add_field(
			name="Syntax",
			value=f"`{p}hangman [countries|movies|onewordmovies|pokemon]`")
	elif page == "slots":
		e = discord.Embed(
			title=f"Help on `{p}slots`",
			description="Get three of the same emoji to win a huge money prize"
		)
		e.add_field(name="Syntax", value=f"`{p}slots`")
	elif page == "joke":
		e = discord.Embed(
			title=f"Help on `{p}joke`",
			description="Impress the ladies with your very original jokes.")
		e.add_field(name="Syntax", value=f"`{p}joke`")
	elif page == "xkcd" or page == 'xkcdcomic':
		e = discord.Embed(
			title=f"Help on `{p}xkcd`",
			description=
			"Impress the smart ladies with this, and don't forget to get the explanation to sound smart\n \
						 Don't provide any argument to get a random comic.")
		e.add_field(name="Syntax",
					value=f"`{p}xkcd|xkcdcomic [comicnumber|latest|what if]`")
	elif page == "choose":
		e = discord.Embed(title=f"Help on `{p}choose`",
						  description="Chooses one from various options")
		e.add_field(name="Syntax",
					value=f"`{p}choose <options separated by spaces>`")
	elif page == "hello" or page == "hemlo" or page == 'henlo' or page == 'hi' or page == 'hai':
		e = discord.Embed(title=f"Help on `{p}{page}`",
						  description="Greet the bot.\n Fun fact: This is the first command I made!")
		e.add_field(name="Syntax", value=f"`{p}hello|hemlo|henlo|hai|hi`")
	elif page == "trigger":
		e = discord.Embed(
			title=f"Help on `{p}trigger`",
			description="To show how triggered you are by someone")
		e.add_field(name="Syntax", value=f"`{p}trigger [@member]`")
	elif page == "blackandwhite" or page == 'b&w' or page == 'bw' or page == 'bnw':
		e = discord.Embed(
			title=f"Help on `{p}blackandwhite`",
			description="Shows your profile photo, old timey style")
		e.add_field(name="Syntax",
					value=f"`{p}blackandwhite|b&w|bw|bnw [@member]`")
	elif page == "cartoon":
		e = discord.Embed(
			title=f"Help on `{p}cartoon`",
			description=
			"Change your profile picture to a cartoon. (Command is still in beta)"
		)
		e.add_field(name="Syntax", value=f"`{p}cartoon [@member]`")
	elif page == "draw" or page == "sketch":
		e = discord.Embed(title=f"Help on `{p}draw`",
						  description="Turns your photo into a drawing")
		e.add_field(name="Syntax", value=f"`{p}draw|sketch [@member]`")
	elif page == "fight":
		e = discord.Embed(
			title=f"Help on `{p}fight`",
			description="Fight someone with a weapon of your choice.")
		e.add_field(name="Syntax", value=f"`{p}fight <@mention> <weapon>`")
	elif page == "stab" or page == 'hauserify':
		e = discord.Embed(
			title=f"Help on `{p}stab`",
			description=
			"Angy? Stab someone. If that someone is SkullBlazer(aka me), don't."
		)
		e.add_field(name="Syntax",
					value=f"`{p}stab|hauserify [@mention] [reason]`")
	elif page == "pat" or page == 'patpat':
		e = discord.Embed(
			title=f"Help on `{p}pat`",
			description=
			"Pat someone, if that someone isn't SkullBlazer(aka me), don't bother."
		)
		e.add_field(name="Syntax",
					value=f"`{p}pat|patpat [@mention] [reason]`")
	elif page == "bonk" or page == 'vibecheck':
		e = discord.Embed(
			title=f"Help on `{p}bonk`",
			description=
			"Person annoying you? Bonk em. \n ~~I will allow bonking me.~~")
		e.add_field(name="Syntax",
					value=f"`{p}bonk|vibecheck [@mention] [reason]`")
	elif page == "yeet":
		e = discord.Embed(
			title=f"Help on `{p}yeet`",
			description=
			"Throw someone like REALLY hard"
		)
		e.add_field(name="Syntax", value=f"`{p}yeet [@mention] [reason]`")
	elif page == "encrypt":
		e = discord.Embed(
			title=f"Help on `{p}encrypt`",
			description=
			"Encrypt your message, then click on the trash can to hide the evidence."
		)
		e.add_field(name="Syntax", value=f"`{p}encrypt <message>`")
	elif page == "decrypt":
		e = discord.Embed(
			title=f"Help on `{p}decrypt`",
			description=
			"Decrypt a message, then click on the trash can to hide the evidence."
		)
		e.add_field(name="Syntax", value=f"`{p}decrypt <message>`")
	elif page == "register" or page == 'reg':
		e = discord.Embed(title=f"Help on `{p}register`",
						  description="Register for an account")
		e.add_field(name="Syntax", value=f"`{p}register|reg`")
	elif page == "daily":
		e = discord.Embed(title=f"Help on `{p}daily`",
						  description="Collect credits every 23 hours")
		e.add_field(name="Syntax", value=f"`{p}daily|d`")
	elif page == "balance" or page == 'bal':
		e = discord.Embed(title=f"Help on `{p}balance`",
						  description="Check your (or someone else's) balance")
		e.add_field(name="Syntax", value=f"`{p}balance|bal [@mention]`")
	elif page == "transfer":
		e = discord.Embed(title=f"Help on `{p}transfer`",
						  description="Transfer money to someone")
		e.add_field(name="Syntax", value=f"`{p}transfer <@mention> <amount>`")
	elif page == "save":
		e = discord.Embed(title=f"Help on `{p}save`",
						  description="Save your progress")
		e.add_field(name="Syntax", value=f"`{p}save`")
	elif page == "rich":
		e = discord.Embed(title=f"Help on `{p}rich`",
						  description="See the richest people in the server")
		e.add_field(name="Syntax", value=f"`{p}rich`")
	elif page == "poll":
		e = discord.Embed(
			title=f"Help on `{p}poll`",
			description=
			"Make a poll by giving a question with the command, then options separated by commas (max. 10)"
		)
		e.add_field(name="Syntax", value=f"`{p}poll|quickpoll <question>`")
	elif page == "say":
		e = discord.Embed(title=f"Help on `{p}say`",
						  description="Make the bot repeat what you said")
		e.add_field(name="Syntax", value=f"`{p}say <phrase>`")
	elif page == "wikisearch" or page == 'wiki':
		e = discord.Embed(
			title=f"Help on `{p}wikisearch`",
			description=
			"Look up various terms on Wikipedia. Doesn't work all the time :/")
		e.add_field(name="Syntax", value=f"`{p}wikisearch|wiki <search term>`")
	elif page == "weather":
		e = discord.Embed(title=f"Help on `{p}weather`",
						  description="Check the weather of any city")
		e.add_field(name="Syntax", value=f"`{p}weather <city name>`")
	elif page == "join":
		e = discord.Embed(
			title=f"Help on `{p}join`",
			description=
			"Make the bot join the voice channel you're connected to.")
		e.add_field(name="Syntax", value=f"`{p}join`")
	elif page == "play":
		e = discord.Embed(
			title=f"Help on `{p}play`",
			description="Play the url or search the song on Youtube")
		e.add_field(name="Syntax", value=f"`{p}play <URL|song name>`")
	elif page == "pause":
		e = discord.Embed(title=f"Help on `{p}pause`",
						  description="Pause the music.")
		e.add_field(name="Syntax", value=f"`{p}pause`")
	elif page == "resume":
		e = discord.Embed(title=f"Help on `{p}resume`",
						  description="Resume paused music")
		e.add_field(name="Syntax", value=f"`{p}resume`")
	elif page == "stop":
		e = discord.Embed(title=f"Help on `{p}stop`",
						  description="Stop the music playing.")
		e.add_field(name="Syntax", value=f"`{p}stop`")
	elif page == "leave":
		e = discord.Embed(
			title=f"Help on `{p}leave`",
			description="Make the bot leave the joined voice channel")
		e.add_field(name="Syntax", value=f"`{p}leave`")
	elif page == "lyrics":
		e = discord.Embed(
			title=f"Help on `{p}lyrics`",
			description="Get the lyrics to a song, credits to KSoft.Si API")
		e.add_field(name="Syntax", value=f"`{p}lyrics <song name>`")
	else:
		await ctx.send("Why do you need help with stuff that doesn't exist")
		page = None
	if page:
		e.set_footer(
			text=
			"Text in <brackets> is required, [brackets] is optional, and | means OR."
		)
		e.colour = discord.Colour.dark_blue()
		e.timestamp = datetime.utcnow()
		await ctx.send(embed=e)


# =========================================Utilities=========================================================================================================================


def is_owner():
	async def predicate(ctx):
		return ctx.author.id == 305341210443382785

	return commands.check(predicate)


def is_mod():
	@commands.has_role("Moderator")
	async def predicate(ctx):
		role = discord.utils.find(lambda r: r.name == 'Moderator',
								  ctx.guild.roles)
		if role in ctx.author.roles:
			return True
		else:
			return False

	return commands.check(predicate)


@bot.command(name='eval')
@commands.check_any(commands.is_owner(), is_owner(), is_mod())
async def _eval(ctx):
	await ctx.message.add_reaction("👀")


# @bot.check
# async def check_bot(ctx):
#	 return not ctx.author.bot


@bot.command(aliases=['hemlo', 'henlo', 'hi', 'hai'])
async def hello(ctx):
	now = datetime.utcnow()
	replies = [
		'Hello!', 'Hey there!',
		(':ballot_box_with_check: Seen at ' + now.strftime("%H:%M:%S")), 'Hi!',
		'Ew'
	]
	choose = random.randint(0, 4)
	await ctx.send(replies[choose])


#	 gid = ctx.guild.id
#	 server = bot.get_guild(gid)
@bot.command(aliases=['colorchange', 'cc'])
@commands.guild_only()
@commands.cooldown(1, 15, commands.BucketType.user)
async def colourchange(ctx,
					   member: Optional[discord.Member],
					   role: discord.Role = None):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	member = member or ctx.author
	colours = ("Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan",
			   "Pink", "Gold", "Black", "White", "Invisible", "JAIL")
	rem = False
	if role is None:
		for usr_role in member.roles:
			if usr_role.name in colours:
				rem = True
				await member.remove_roles(usr_role)
				await ctx.send("All colour roles removed")
		if not rem:
			if member == ctx.author:
				await ctx.send("You don't have any colour roles to be removed")
			else:
				await ctx.send(
					"The user doesn't have any colour roles to be removed")
	else:
		embed = discord.Embed(title="Working..",
							  description="Contacting the search monkeys..")
		message = await ctx.send(embed=embed)
		if role not in ctx.guild.roles:
			embed = discord.Embed(colour = discord.Colour.red(), title = "Error",\
								  description = f"{role.name} does not exist. Do `{p}help colourchange` to see available colours")
			await message.edit(embed=embed)
			return
		elif role in member.roles:
			if ctx.author == member:
				embed = discord.Embed(
					colour=discord.Colour.red(),
					title="Error",
					description=f"You already have {role.name}")
			else:
				embed = discord.Embed(
					colour=discord.Colour.red(),
					title="Error",
					description=f"{member.mention} already has {role.name}")
			await message.edit(embed=embed)
			if role.name == "Invisible":
				await asyncio.sleep(3)
				await message.delete()
				await ctx.message.delete()
			return
		elif role.name == "Moderator":
			if ctx.author == "SkullBlazer#9339" or ctx.author == ctx.guild.owner:
				await member.add_roles(role, atomic=True)
				embed.title = "Success!"
				if member == ctx.author:
					embed.description = f"I've given you the {role.name} role!"
				else:
					embed.description = f"I've given {member.mention} the {role.name} role!"
				embed.colour = discord.Colour(0x7289da)
				await message.edit(embed=embed)
				return
			else:
				embed.title = "Error"
				embed.description = "You do not have the sufficient permissions to assign the Moderator role"
				embed.colour = discord.Colour.dark_red()
				await message.edit(embed=embed)
				return
		elif role.name == "JAIL":
			if ctx.author.top_role > member.top_role and member != ctx.author:
				for usr_role in member.roles:
					if usr_role.name != "@everyone":
						await member.remove_roles(usr_role)
				await member.add_roles(role, atomic=True)
				embed.title = "Success!"
				embed.description = f"{member.mention} has been successfully jailed!"
				embed.colour = discord.Colour(0x546e7a)
				await message.edit(embed=embed)
				return
			elif member == ctx.author:
				await ctx.send("Why would you ever want to jail yourself")
				await message.delete()
				return
			else:
				await ctx.send(
					"Shut up peasant you don't have the rights to jail that person"
				)
				await message.delete()
				return
		for usr_role in member.roles:
			if usr_role.name in colours:
				await member.remove_roles(usr_role)
				if usr_role.name != "Invisible":
					embed.add_field(name="Removed:",
									value=f"Role removed: {usr_role.name}")
				else:
					embed.add_field(name="Removed:",
									value="Role removed: **[REDACTED]**")
		await message.edit(embed=embed)
		await member.add_roles(role, atomic=True)
		embed.title = "Success!"
		if member == ctx.author:
			embed.description = f"I've given you the {role.name} role!"
		else:
			embed.description = f"I've given {member.mention} the {role.name} role!"
		if role.name == "Red":
			embed.colour = discord.Colour.red()
		elif role.name == "Blue":
			embed.colour = discord.Colour.blue()
		elif role.name == "Green":
			embed.colour = discord.Colour.green()
		elif role.name == "Yellow":
			embed.colour = discord.Colour.from_rgb(255, 255, 0)
		elif role.name == "Purple":
			embed.colour = discord.Colour.purple()
		elif role.name == "Orange":
			embed.colour = discord.Colour.orange()
		elif role.name == "Cyan":
			embed.colour = discord.Colour.teal()
		elif role.name == "Pink":
			embed.colour = discord.Colour.from_rgb(255, 20, 147)
		elif role.name == "Gold":
			embed.colour = discord.Colour.dark_gold()
		elif role.name == "White":
			embed.colour = discord.Colour.from_rgb(255, 255, 254)
		elif role.name == "Invisible":
			embed.colour = discord.Colour.dark_theme()
		await message.edit(embed=embed)
		if role.name == "Invisible":
			await asyncio.sleep(2)
			await message.delete()
			await ctx.message.delete()


# @colourchange.error
# async def cc_error(ctx, error):
#	 if isinstance(error, commands.CommandInvokeError):
#		 await ctx.send("That role does not exist")


@bot.command(aliases=['inv'])
async def invite(ctx):
	if str(ctx.message.author) != "SkullBlazer#9339":
		user = bot.get_user(305341210443382785)
		await user.send(f"{ctx.message.author} made an invite for your bot")
	e = discord.Embed(
		title="Click here for free V-bucks!",
		url=
		"https://discord.com/oauth2/authorize?client_id=783314693086380032&scope=bot&permissions=2081156351",
		description="Jk, invite me to your server",
		timestamp=datetime.utcnow(),
		color=0x00ebff)
	await ctx.reply(embed=e, mention_author=False)


@bot.command(aliases=['ui', 'uinfo'])
@commands.guild_only()
async def userinfo(ctx, user: Optional[discord.Member], uid: int = None):
	if user is None and uid is None:
		user = ctx.author
	elif uid:
		user = await bot.fetch_user(uid)
	date_format = "%a, %d %b %Y %I:%M %p"
	embed = discord.Embed(color=user.colour,
						  description=user.mention,
						  timestamp=datetime.utcnow())
	embed.set_author(name=str(user), icon_url=user.avatar_url)
	embed.set_thumbnail(url=user.avatar_url)
	try:
		embed.add_field(name='Status', value=str(user.status).title())
	except AttributeError:
		await ctx.send(
			"This user is not in this guild. Invite them here maybe, server's dead anyway"
		)
		return
	embed.add_field(name='Acccount created on',
					value=user.created_at.strftime(date_format))
	embed.add_field(name='Joined server on',
					value=user.joined_at.strftime(date_format),
					inline=False)
	if len(user.roles) > 1:
		role_string = ' '.join([r.mention for r in user.roles][1:])
		embed.add_field(name="Roles [{}]".format(len(user.roles) - 1),
						value=role_string,
						inline=False)
	embed.set_footer(text='ID: ' + str(user.id))
	if user.pending:
		embed.add_field(name="Verified account", value="No")
	else:
		embed.add_field(name="Verified account", value="Yes")
	if user.premium_since:
		embed.add_field(name="Nitro boosting since",
						value=user.premium_since.strftime(date_format),
						inline=False)
	await ctx.send(embed=embed)


@bot.command(aliases=['si', 'sinfo'])
@commands.guild_only()
async def serverinfo(ctx):
	date_format = "%a, %d %b %Y %I:%M %p"
	s1 = ""
	s2 = ""
	embed = discord.Embed(title=f"{ctx.guild.name} info",
						  colour=ctx.guild.owner.colour,
						  timestamp=datetime.utcnow())
	embed.set_thumbnail(url=ctx.guild.icon_url)
	embed.add_field(name='Owner', value=ctx.guild.owner)
	embed.add_field(name='Region', value=str(ctx.guild.region).title())
	embed.add_field(name='Server created on',
					value=ctx.guild.created_at.strftime(date_format))
	embed.add_field(name='Humans',
					value=len(
						list(filter(lambda m: not m.bot, ctx.guild.members))))
	embed.add_field(name='Bots',
					value=len(list(filter(lambda m: m.bot,
										  ctx.guild.members))))
	online = 0
	for i in ctx.guild.members:
		if str(i.status) == 'online' or str(i.status) == 'dnd':
			online += 1
	embed.add_field(name="Online", value=online)
	for i in ctx.guild.text_channels:
		s1 += f"<#{i.id}>\n"
	embed.add_field(name='Text channels', value=s1, inline=False)
	for i in ctx.guild.voice_channels:
		s2 += f"<#{i.id}>\n"
	embed.add_field(name='Voice channels', value=s2, inline=True)
	embed.add_field(name='Roles', value=(len(ctx.guild.roles) - 1))
	embed.add_field(name="Emojis", value=len(ctx.guild.emojis))
	embed.set_footer(text='ID: ' + str(ctx.guild.id))
	await ctx.send(embed=embed)


@bot.command()
async def encrypt(ctx, *, s: str):
	a = ''
	try:
		for letter in s:
			a += chr(ord(letter) + len(s))
		cleanS = await commands.clean_content().convert(ctx, a)
	except Exception as e:
		await ctx.send(
			f"**Error: `{e}`. This probably means the input is malformed. Sorry, I'm not perfect and my creator is dumb**"
		)
	if len(cleanS) <= 479:
		message = await ctx.reply(f"||```{cleanS}.```||", mention_author=False)
	else:
		try:
			message = await ctx.author.send(f"```{cleanS}```")
			await ctx.send(
				f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
			)
		except Exception:
			await ctx.send(
				f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
			)
	if ctx.guild:
		await message.add_reaction("🗑️")

		def check(reaction, user):
			return user == ctx.author and str(
				reaction.emoji) == "🗑️" and reaction.message == message

		reaction, user = await bot.wait_for("reaction_add", check=check)
		await message.delete()
		await ctx.message.delete()


@bot.command()
async def decrypt(ctx, *, s2: str):
	if s2[-1] == ".":
		s2 = s2[:-1]
	a2 = ''
	try:
		for letter in s2:
			a2 += chr(ord(letter) - len(s2))
		cleanS2 = await commands.clean_content().convert(ctx, a2)
	except Exception as e:
		await ctx.send(
			f"**Error: `{e}`. This probably means the input is malformed. Sorry, I'm not perfect and my creator is dumb**"
		)
	if len(cleanS2) <= 479:
		message2 = await ctx.reply(f"||```{cleanS2}```||",
								   mention_author=False)
	else:
		try:
			message2 = await ctx.author.send(f"```{cleanS2}```")
			await ctx.send(
				f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**"
			)
		except Exception:
			await ctx.send(
				f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**"
			)
	if ctx.guild:
		await message2.add_reaction("🗑️")

		def check(reaction, user):
			return user == ctx.author and str(
				reaction.emoji) == "🗑️" and reaction.message == message2

		reaction2, user2 = await bot.wait_for("reaction_add", check=check)
		await message2.delete()
		await ctx.message.delete()


@bot.command(name="kick", pass_context=True)
@commands.guild_only()
@commands.has_permissions(manage_roles=True, kick_members=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def _kick(ctx, member: discord.Member = None, *, reason=None):
	if member is None:
		await ctx.reply(
			"Since no member was given to kick, the user of this command will be kicked",
			mention_author=False)
	elif str(member) == "SkullBlazer#9339":
		e = discord.Embed(title="ERROR",
						  description="YOU CANNOT KICK THE ALMIGHTY CREATOR",
						  colour=discord.Colour.red(),
						  timestamp=datetime.utcnow())
		e.set_footer(
			text=
			'This incident has been recorded and necessary action will be taken'
		)
		await ctx.reply(embed=e)
	elif member == ctx.author:
		await ctx.reply("This idiot", mention_author=False)
	elif str(member) == "SlaveBot#1382":
		await ctx.reply("Hah I cannot be kicked", mention_author=False)
	else:
		e = discord.Embed(title=f"{member} has been kicked", description = f"{ctx.author} kicked {member} due to the following reason:```{reason}```",\
								 colour = discord.Colour.dark_red(), timestamp=datetime.utcnow())
		await ctx.reply(embed=e, mention_author=False)
		await member.kick(reason=reason)


@_kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.reply("I'm sorry but peasants are not allowed to kick",
						mention_author=False)


@bot.command(name="ban", pass_context=True)
@commands.guild_only()
@commands.has_permissions(manage_roles=True, kick_members=True)
@commands.cooldown(1, 60, commands.BucketType.user)
async def _ban(ctx, member: discord.Member = None, *, reason=None):
	if member is None:
		await ctx.reply(f"Banning {ctx.message.author}...",
						mention_author=False)
	elif str(ctx.message.author) != "SkullBlazer#9339":
		if member == ctx.author:
			await ctx.reply("bruh", mention_author=False)
			return
		elif str(member) == "SlaveBot#1382":
			await ctx.reply("Hah I cannot be banned", mention_author=False)
			return
		emojis = ["✅", "❎"]
		e = discord.Embed(title="Ban confirmation", description = f"Are you sure you want to ban {member.mention}?",\
							 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		msg = await ctx.send(embed=e)
		await msg.add_reaction(emojis[0])
		await msg.add_reaction(emojis[1])

		def check2(reaction, user):
			return str(
				reaction.emoji
			) in emojis and user == ctx.author and reaction.message == msg

		reaction, user = await bot.wait_for('reaction_add', check=check2)

		await msg.delete()
		if str(reaction) == "✅":
			if str(member) == "SkullBlazer#9339":
				e = discord.Embed(
					title="ERROR",
					description="YOU CANNOT BAN THE ALMIGHTY CREATOR",
					colour=discord.Colour.red(),
					timestamp=datetime.utcnow())
				e.set_footer(
					text=
					'This incident has been recorded and necessary action will be taken'
				)
				await ctx.reply(embed=e)
			else:
				e = discord.Embed(title=f"{member} has been banned", description = f"{ctx.author.mention} banned {member} for the following reason: ```{reason}```",\
							 colour = discord.Colour.dark_red(), timestamp=datetime.utcnow())
				await member.ban(reason=reason)
				await ctx.reply(embed=e)
		else:
			await ctx.reply("Hmmmmm seems sus", mention_author=False)
	else:
		emojis = ["✅", "❎"]
		e = discord.Embed(title="Ban confirmation", description = f"Are you sure you want to ban {member.mention}?",\
							 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		msg = await ctx.send(embed=e)
		await msg.add_reaction(emojis[0])
		await msg.add_reaction(emojis[1])

		def check2(reaction, user):
			return str(
				reaction.emoji
			) in emojis and user == ctx.author and reaction.message == msg

		reaction, user = await bot.wait_for('reaction_add', check=check2)

		await msg.delete()
		if str(reaction.emoji) == "✅":
			if str(member) == "SkullBlazer#9339":
				await ctx.reply("Bro what are you doing", mention_author=False)
			elif str(member) == "SlaveBot#1382":
				await ctx.reply(
					"Hah I cannot be banned, even by the master himself",
					mention_author=False)
				return
			else:
				e = discord.Embed(title=f"{member} has been banned", description = f"The master himself has struck the banhammer on {member} due to the following reason:```{reason}```",\
								 colour = discord.Colour.dark_red(), timestamp=datetime.utcnow())
				await member.ban(reason=reason)
				await ctx.reply(embed=e)
		else:
			await ctx.send(
				"Dang what did you do to convince the supreme master not to ban you"
			)


@_ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		text = "The AUDACITY of this peasant to try and ban someone"
		await ctx.reply(text, mention_author=False)


@bot.command(name='unban')
@commands.guild_only()
async def _unban(ctx, uid: int):
	user = await bot.fetch_user(uid)
	await ctx.guild.unban(user)
	await ctx.reply(f"Unbanned <!@{uid}>", mention_author=False)


# @bot.command()
# async def ping(ctx):
# 	e = discord.Embed(title="Pong!",
# 					  description=("Latency: " +
# 								   str(round(bot.latency, 3) * 1000) + "ms"),
# 					  color=discord.Colour.teal(),
# 					  timestamp=datetime.utcnow())
# 	await ctx.reply(embed=e, mention_author=False)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ping(ctx):
	msg = await ctx.send("`Pinging bot latency...`")
	times = []
	counter = 0
	embed = discord.Embed(
		title="More information:",
		description="Pinged 4 times and calculated the average.",
		colour=discord.Colour.random())

	for _ in range(3):
		counter += 1
		start = perf_counter()
		await msg.edit(content=f"Pinging... {counter}/3")
		end = perf_counter()
		speed = round((end - start) * 1000)
		times.append(speed)
		embed.add_field(name=f"Ping {counter}:",
						value=f"{speed}ms",
						inline=True)

	embed.set_author(name="Pong!", icon_url=ctx.author.avatar_url)
	embed.add_field(name="Bot latency",
					value=f"{round(bot.latency * 1000)}ms",
					inline=True)
	embed.add_field(
		name="Average speed",
		value=f"{round((round(sum(times)) + round(bot.latency * 1000))/4)}ms")
	embed.set_footer(
		text=f"Estimated total time elapsed: {round(sum(times))}ms")
	await msg.edit(
		content=
		f":ping_pong: **{round((round(sum(times)) + round(bot.latency * 1000))/4)}ms**",
		embed=embed)


@bot.command()
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def nick(ctx, member: Optional[discord.Member], *, name: str = None):
	member = member or ctx.author
	og = str(member.name)
	if name is None:
		if member.display_name == og:
			await ctx.reply(f"Believe it or not, {og} is their real name",
							mention_author=False)
			return
	else:
		if member.display_name == name:
			await ctx.reply(f"Believe it or not, {og} is their real name",
							mention_author=False)
			return
	if name:
		if len(name) > 32:
			await ctx.reply(
				"Are you trying to beat the record for longest name in the world? Keep it below 32 characters",
				mention_author=False)
			return
	if name is None:
		name = og
		await member.edit(nick=name)
		if member == ctx.author:
			await ctx.reply("Your name has been reset.", mention_author=False)
		else:
			await ctx.reply(f"{member.mention}'s name has been reset.",
							mention_author=False)
	else:
		await member.edit(nick=name)
		if member == ctx.author:
			await ctx.reply(f"Your name has been changed to {name}",
							mention_author=False)
		else:
			await ctx.reply(
				f"{member.mention}'s name has been changed to {name}",
				mention_author=False)


@bot.command(aliases=['changeprefix'])
@commands.guild_only()
@commands.cooldown(1, 15, commands.BucketType.user)
async def prefix(ctx, prefx='>>'):
	if db[str(ctx.guild.id)][1] == prefx:
		await ctx.reply(f"Your prefix is already {prefx}",
						mention_author=False)
	elif prefx == '>>':
		db[str(ctx.guild.id)][1] = prefx
		await ctx.reply(f"Prefix reset to {prefx}", mention_author=False)
	else:
		if prefx.isalnum():
			emojis = ["✅", "❎"]
			e = discord.Embed(title="Prefix change confirmation", description = f"Are you sure you want letters and/or numbers in your prefix?",\
							 colour = discord.Colour.random(), timestamp=datetime.utcnow())
			msg = await ctx.send(embed=e)
			await msg.add_reaction(emojis[0])
			await msg.add_reaction(emojis[1])

			def check2(reaction, user):
				return str(
					reaction.emoji
				) in emojis and user == ctx.author and reaction.message == msg

			reaction, user = await bot.wait_for('reaction_add', check=check2)

			await msg.clear_reactions()
			if str(reaction) == "✅":
				db[str(ctx.guild.id)][1] = prefx
				await ctx.reply(f"Prefix changed to {prefx}",
								mention_author=False)
		else:
			db[str(ctx.guild.id)][1] = prefx
			await ctx.reply(f"Prefix changed to {prefx}", mention_author=False)


@bot.command(aliases=['autoresponse'])
@commands.guild_only()
@commands.cooldown(1, 15, commands.BucketType.user)
async def stalkermode(ctx, flag: str = None):
	if flag is None:
		if db[str(ctx.guild.id)][0] == "false":
			db[str(ctx.guild.id)][0] = "true"
			await ctx.reply(
				"Stalker mode toggled to True. The bot will now automatically send your chats to the NSA.",
				mention_author=False)
		else:
			db[str(ctx.guild.id)][0] = "false"
			await ctx.reply(
				"Stalker mode toggled to False. The bot will no longer respond without a prefix \
~~but it will still sell your chat logs~~.",
				mention_author=False)
	elif flag.lower() == "false":
		if db[str(ctx.guild.id)][0] == "false":
			await ctx.reply("Stalker mode is already False.",
							mention_author=False)
		else:
			db[str(ctx.guild.id)][0] = "false"
			await ctx.reply(
				"Stalker mode set to False. The bot will no longer respond without a prefix \
~~but it will still sell your chat logs~~.",
				mention_author=False)
	elif flag.lower() == "true":
		if db[str(ctx.guild.id)][0] == "false":
			db[str(ctx.guild.id)][0] = "true"
			await ctx.reply(
				"Stalker mode set to True. The bot will now automatically send your chats to the NSA.",
				mention_author=False)
		else:
			await ctx.reply("Stalker mode is already True.",
							mention_author=False)


@bot.command()
async def snipe(ctx, cid: int = None):
	global flag
	if cid:
		channel = await bot.fetch_channel(cid)
	else:
		channel = ctx.channel
		cid = channel.id
	try:
		if not flag:
			em = discord.Embed(title=f"Last deleted message in {channel.name}",
								description=d_content[cid])
		else:
			em = discord.Embed(title=f"Last deleted image in {channel.name}")
			em.set_image(url=d_content[cid])
			flag = False
		em.set_footer(text=f"Author: {d_author[cid]}")
		await ctx.send(embed=em)
	except KeyError:
		await ctx.send(f"There are no recently deleted messages in <#{cid}>")


@bot.command(aliases=['esnipe'])
async def editsnipe(ctx, cid: int = None):
	if cid:
		channel = await bot.fetch_channel(cid)
	else:
		channel = ctx.channel
		cid = channel.id
	try:
		em = discord.Embed(
			title=f"Last edited message in {channel.name}",
			description=f"**Original message:** {e_content1[cid]}\n \n \
		**Edited message:** {e_content2[cid]}")
		em.set_footer(text=f"Author: {e_author[cid]}")
		await ctx.send(embed=em)
	except KeyError:
		await ctx.send(f"There are no recently edited messages in <#{cid}>")


# @bot.command()
# async def delete(ctx, mid:int=None):
#	 if mid is None:
#		 await ctx.send(f"Deleting {ctx.author.name}'s account...")
#		 return
#	 else:
#		 message = await ctx.fetch_message(mid)
#		 if message:
#			 await message.delete()
#			 await ctx.message.delete()


@bot.command(aliases=['ut'])
async def uptime(ctx):
	second = time() - start_time
	minute, second = divmod(second, 60)
	hour, minute = divmod(minute, 60)
	day, hour = divmod(hour, 24)
	await ctx.send("Bot has been alive ~~since the beginning of time~~ for " +
				   str(int(day)) + " days, " + str(int(hour)) + " hours, " +
				   str(int(minute)) + " minutes and %.2f seconds" % second)


@bot.command(aliases=['pn'])
async def patchnotes(ctx):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	e = discord.Embed(title="Updates for SlaveBot v1.15.1",
					  description=f"\
	**1. IMPORTANT ANNOUNCEMENT**: CHANGED PROBABILITIES OF JACKPOT!\n \
	 Winning the `100,000x` multiplier has a `0.1%` chance, `10,000x` is `0.25%`, and `1,000x` is `0.5%`. Edit: Changing the probabilities did nothing <:mikebruh:828462333926834176>\n \
	**2.** Added support for using commands in DMs (WARNING: Lots of errors, every error reported has a 10000 SlaveBot currency (trademark pending) reward.)\n \
	**3.** Since many of you (read: no one) have been asking for this, new **Utility**, `{p}editsnipe`\n \
	**4.** Added an **Action**, `{p}yeet`\n \
	**5.** Added a **Utility**, `{p}suggest`\n \
	**6.** Bug fixes\n \
	**7.** Removed Herobrine.",
					  colour=discord.Color.dark_grey())
	await ctx.send(embed=e)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def suggest(ctx):
	msg = await ctx.send("Select 1 if you're reporting a bug, 2 if you want to suggest a command to be added, 3 for other, or 4 to cancel")
	await msg.add_reaction("1⃣")
	await msg.add_reaction("2⃣")
	await msg.add_reaction("3⃣")
	await msg.add_reaction("4⃣")
	def check(reaction, user):
		return str(reaction.emoji) in ['1⃣', '2⃣', "3⃣", "4⃣"] and user == ctx.author and msg == reaction.message
	try:
		reaction, user = await bot.wait_for('reaction_add', check=check, timeout=60)
		await msg.delete()
		user = bot.get_user(305341210443382785)
		if str(reaction.emoji) == "1⃣":
			await user.send(f"{ctx.author.name} from {ctx.guild.name} wants to report a bug")
		elif str(reaction.emoji) == "2⃣":
			await user.send(f"{ctx.author.name} from {ctx.guild.name} wants to suggest something")
		elif str(reaction.emoji) == "3⃣":
			await user.send(f"{ctx.author.name} from {ctx.guild.name} has something else to say")
		else:
			await ctx.send("Cancelled.")
			return
		await ctx.send("Send your message")
		def check2(message):
			return message.author == ctx.author and message.channel == ctx.message.channel
		try:
			message = await bot.wait_for('message', check=check2, timeout=60)
			try:
				await user.send(message.content)
			except discord.errors.HTTPException:
				await user.send(message.attachments[0].proxy_url)
			await ctx.send("Message sent!")
		except asyncio.TimeoutError:
			await ctx.send("Message sent to my master that you're stupid")	
	except asyncio.TimeoutError:
		await ctx.send("Message sent to my master that you're stupid")
# ============================================Balance========================================================================================================================


@bot.command()
async def _save():
	pass


@bot.command()
async def save(ctx):
	await ctx.channel.trigger_typing()
	await _save()
	await ctx.send("Progress saved.")


@bot.command(pass_context=True, aliases=['bal'])
async def balance(ctx, member: Optional[discord.Member], mid: int = None):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	if mid is None:
		member = member or ctx.message.author
		aid = str(member.id)
		if member == ctx.message.author:
			if str(aid) in db:
				if "69" in str(db[aid][1]):
					e = discord.Embed(
						description=
						f"You have {db[aid][1]:,} in the bank\n\n nice",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
				else:
					e = discord.Embed(
						description=f"You have {db[aid][1]:,} in the bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
				e.set_author(name="Balance", icon_url=member.avatar_url)
				await ctx.reply(embed=e, mention_author=False)
			else:
				embed = discord.Embed(colour = discord.Colour.red(), title = "Error",\
									  description = f"You do not have an account, make one using `{p}register`", timestamp=datetime.utcnow())
				await ctx.reply(embed=embed, mention_author=False)
		else:
			if str(aid) in db:
				if "69" in str(db[aid][1]):
					e = discord.Embed(
						description=
						f"{member.mention} has {db[aid][1]:,} in their bank\n\n nice",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
				else:
					e = discord.Embed(
						description=
						f"{member.mention} has {db[aid][1]:,} in their bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
				e.set_author(name=f"{member.name}'s balance",
							 icon_url=member.avatar_url)
				await ctx.reply(embed=e, mention_author=False)
			else:
				embed = discord.Embed(colour = discord.Colour.red(), title = "Error",\
									  description = f"The mentioned user does not have an account, tell them to make one using `{p}register`", timestamp=datetime.utcnow())
				await ctx.reply(embed=embed, mention_author=False)
	else:
		aid = str(mid)
		member = await bot.fetch_user(mid)
		if aid in db:
			if "69" in str(db[aid][1]):
				e = discord.Embed(
					description=
					f"<@!{aid}> has {db[aid][1]:,} in their bank\n\n nice",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
			else:
				e = discord.Embed(
					description=f"<@!{aid}> has {db[aid][1]:,} in their bank",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
			e.set_author(name=f"{member.name}'s balance",
						 icon_url=member.avatar_url)
			await ctx.reply(embed=e, mention_author=False)
		else:
			embed = discord.Embed(colour = discord.Colour.red(), title = "Error",\
								  description = f"The mentioned user does not have an account, tell them to make one using `{p}register`", timestamp=datetime.utcnow())
			await ctx.reply(embed=embed, mention_author=False)


@bot.command(pass_context=True, aliases=['reg'])
async def register(ctx):
	mid = str(ctx.message.author.id)
	if mid not in db:
		db[mid] = [0, 100]
		e = discord.Embed(description="You are now registered!",
						  colour=discord.Colour.gold(),
						  timestamp=datetime.utcnow())
		e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
		await ctx.reply(embed=e, mention_author=False)
		await _save()
	else:
		await ctx.reply("You already have an account idiot",
						mention_author=False)


@bot.command()
@commands.check_any(commands.is_owner(), is_owner())
async def edit(ctx, member: Optional[discord.Member], aid: str = None):
	def check(m):
		return m.author == ctx.author and m.channel == ctx.message.channel

	if aid is None:
		member = member or ctx.author
		mid = str(member.id)
		if mid not in db:
			await ctx.reply("The user does not have an account, what a dweeb",
							mention_author=False)
			return
		await ctx.send("Operator and amount")
		mesg = await bot.wait_for("message", check=check)
		emojis = ["✅", "❎"]
		amt = str(mesg.content)
		if amt[0] == "+":
			e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:]):,} to {member.mention}'s account?",\
								 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		elif amt[0] == "-":
			if int(amt[1:]) > db[mid][1]:
				await ctx.send(
					f"{member.name} has only ||{db[mid][1]:,}|| in their account"
				)
				return
			e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:]):,} from {member.mention}'s account?",\
								 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		elif amt[0] == "=":
			e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change {member.mention}'s balance to {int(amt[1:]):,}?",\
								 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		else:
			await ctx.reply("Transaction error 3913", mention_author=False)
			return
	else:
		mid = str(aid)
		if mid not in db:
			await ctx.reply("The user does not have an account, what a dweeb",
							mention_author=False)
			return
		await ctx.send("Operator and amount")
		mesg = await bot.wait_for("message", check=check)
		emojis = ["✅", "❎"]
		amt = str(mesg.content)
		if amt[0] == "+":
			e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:]):,} to <@!{aid}>'s account?",\
								 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		elif amt[0] == "-":
			if int(amt[1:]) > db[mid][1]:
				await ctx.send(
					f"<@!{aid}> has only ||{db[mid][1]:,}|| in their account")
				return
			e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:]):,} from <@!{aid}>'s account?",\
								 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		elif amt[0] == "=":
			e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change <@!{aid}>'s balance to {int(amt[1:]):,}?",\
								 colour = discord.Colour.random(), timestamp=datetime.utcnow())
		else:
			await ctx.reply("Transaction error 3913", mention_author=False)
			return
	msg = await ctx.send(embed=e)
	await msg.add_reaction(emojis[0])
	await msg.add_reaction(emojis[1])

	def check2(reaction, user):
		return str(
			reaction.emoji
		) in emojis and user == ctx.author and reaction.message == msg

	reaction, user = await bot.wait_for('reaction_add', check=check2)
	await msg.delete()
	if str(reaction.emoji) == "✅":
		if amt[0] == "+":
			db[mid][1] += int(amt[1:])
			await _save()
			await ctx.reply("Added", mention_author=False)
		elif amt[0] == "-":
			db[mid][1] -= int(amt[1:])
			await _save()
			await ctx.reply("Subtracted", mention_author=False)
		elif amt[0] == "=":
			db[mid][1] = int(amt[1:])
			await _save()
			await ctx.reply("Changed", mention_author=False)
	else:
		await ctx.send("Well that saved me a bunch of time and processing")

@edit.error
async def edit_error(ctx, error):
	if isinstance(error, commands.CheckAnyFailure):
		await ctx.send("That.... that's not a valid command")

@bot.command()
@commands.check_any(commands.is_owner())
async def getdata(ctx):
	s = ""
	for i in db:
		s += (str(i) + ": [" + str(db[i][0]) + "," + str(db[i][1]) + "]\n")
	await ctx.send(f"```java\n{s}```")

@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def transfer(ctx, other: discord.Member = None, amount: int = None):
	if other is None:
		await ctx.reply(
			"Since no recipient was mentioned, all your money will go to ~~me~~ charity",
			mention_author=False)
	elif amount is None:
		await ctx.reply(
			f"Amount not provided, resorting to default value, which is all of {ctx.author.name}'s money",
			mention_author=False)
	else:
		primary_id = str(ctx.message.author.id)
		other_id = str(other.id)
		if primary_id == other_id:
			await ctx.send("What are you even doing")
		elif amount <= 0:
			await ctx.send("Trying to fool me, eh?")
		elif primary_id not in db:
			embed = discord.Embed(colour=discord.Colour.red(),
								  title="Error",
								  description="You do not have an account",
								  timestamp=datetime.utcnow())
			await ctx.send(embed=embed)
		elif other_id not in db:
			embed = discord.Embed(
				colour=discord.Colour.red(),
				title="Error",
				description="The other party does not have an account",
				timestamp=datetime.utcnow())
			await ctx.send(embed=embed)
		elif db[primary_id][1] < amount:
			embed = discord.Embed(
				colour=discord.Colour.red(),
				title="Error",
				description="You cannot afford this transaction",
				timestamp=datetime.utcnow())
			await ctx.send(embed=embed)
		else:
			emojis = ["✅", "❎"]
			e = discord.Embed(title="Transfer confirmation", description = f"Are you sure you want to transfer {amount:,} to {other.mention}?",\
							 colour = discord.Colour.random(), timestamp=datetime.utcnow())
			msg = await ctx.send(embed=e)
			await msg.add_reaction(emojis[0])
			await msg.add_reaction(emojis[1])

			def check2(reaction, user):
				return str(
					reaction.emoji
				) in emojis and user == ctx.author and reaction.message == msg

			reaction, user = await bot.wait_for('reaction_add', check=check2)
			await msg.delete()

			if str(reaction) == "✅":
				e = discord.Embed(title="Success!",
								  description="Transaction complete",
								  colour=discord.Colour.gold(),
								  timestamp=datetime.utcnow())
				e.add_field(name="Receipt",
							value=f"Transferred {amount:,} to {other.mention}")
				await ctx.reply(embed=e, mention_author=False)
				db[primary_id][1] -= amount
				db[other_id][1] += amount
				await _save()
			else:
				await ctx.send(
					f"Sorry {other.mention}, it's not your lucky day")


@transfer.error
async def transfer_error(ctx, error):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	if isinstance(error, commands.BadArgument):
		await ctx.reply(
			f"The `transfer` command has been updated, new format is `{p}transfer <@member> <amount>`",
			mention_author=False)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rich(ctx, term: str = None, glbal: str = None):
	count = 0
	d = {}
	s = ""
	L = ["<:1st:836165759390449675>", "<:2nd:836165758932221992>", "<:3rd:836165759221760000> ", \
		 "<:4th:836165757641162792>", "<:5th:836165757418209292>", "<:6th:836165757595025430>", \
		 "<:7th:836165757502095471>", "<:8th:836165757309550603>", "<:9th:836165757561602048>", \
		 "<:769010theqts:836165757926113290>"]
	count = 0
	if not term and not glbal:
		if not ctx.guild:
			await ctx.send(
				"This command is not available in DMs. But if I had to guess, I'm the richest. Unless you're Mars."
			)
			return
		guild = ctx.guild
		for member in guild.members:
			mid = str(member.id)
			if mid in db:
				d[member] = db[mid][1]
		sorted_dict = dict(
			sorted(d.items(), key=lambda item: item[1], reverse=True))
		for i in sorted_dict:
			count += 1
			s += f"{L[count-1]} **{i}** - `{sorted_dict[i]:,}`\n"
		e = discord.Embed(title=f"Richest people in {guild.name}",
						  description=s)
		e.timestamp = datetime.utcnow()
		e.colour = discord.Colour.random()
		await ctx.send(embed=e)

	elif term.lower() == "g" or term.lower() == "global" and not glbal:
		for i in db:
			if type(db[i][1]) == int or type(db[i][1]) == float:
				d[i] = db[i][1]
		sorted_dict = dict(
			sorted(d.items(), key=lambda item: item[1], reverse=True))
		for i in sorted_dict:
			count += 1
			if count > 10:
				break
			s += f"{L[count-1]} **<@!{i}>** - `{sorted_dict[i]:,}`\n"
		e = discord.Embed(title=f"Global leaderboard", description=s)
		e.timestamp = datetime.utcnow()
		e.colour = discord.Colour.random()
		await ctx.send(embed=e)

	elif (term.lower() == "d" or term.lower() == "daily") and not glbal:
		if not ctx.guild:
			await ctx.send("This command is not available in DMs.")
			return
		guild = ctx.guild
		# with open('datafiles/daily.txt') as fle:
			# streak = json.load(fle)
		for member in guild.members:
			mid = str(member.id)
			if mid in db:
				d[member] = db[mid][0]
		sorted_dict = dict(
			sorted(d.items(), key=lambda item: item[1], reverse=True))
		for i in sorted_dict:
			count += 1
			s += f"{L[count-1]} **{i}** - `{sorted_dict[i]:,}`\n"
		e = discord.Embed(
			title=
			f"Members with ~~no life~~ most dailies collected in {guild.name}",
			description=s)
		e.timestamp = datetime.utcnow()
		e.colour = discord.Colour.random()
		await ctx.send(embed=e)
	elif (term.lower() == "d" or term.lower()
		  == "daily") and (glbal.lower() == "g" or glbal.lower() == "global"):
		for i in db:
			if type(db[i][1]) == int or type(db[i][1]) == float:
				d[i] = db[i][0]
		sorted_dict = dict(
			sorted(d.items(), key=lambda item: item[1], reverse=True))
		for i in sorted_dict:
			count += 1
			if count > 10:
				break
			s += f"{L[count-1]} **<@!{i}>** - `{sorted_dict[i]:,}`\n"
		e = discord.Embed(title=f"Global leaderboard for `>>daily`",
						  description=s)
		e.timestamp = datetime.utcnow()
		e.colour = discord.Colour.random()
		await ctx.send(embed=e)


@bot.command(pass_context=True)
@commands.cooldown(1, 23*60*60, commands.BucketType.user)
async def daily(ctx):
	aid = str(ctx.message.author.id)
	if aid not in db:
		embed = discord.Embed(colour=discord.Colour.red(),
							  title="Error",
							  description="You do not have an account",
							  timestamp=datetime.utcnow())
		await ctx.reply(embed=embed, mention_author=False)
	else:
		try:
			db[str(ctx.author.id)][0] += 1
			s = db[str(ctx.author.id)][0]
		except KeyError:
			db[str(ctx.author.id)][0] = 0
			s = 0
		# if str(ctx.author.id) in streak:
		# 	s = streak[str(ctx.author.id)]
		# 	nstreak = {
		# 		str(ctx.author.id) : s + 1
		# 	}
		# 	streak.update(nstreak)
		# 	with open('datafiles/daily.txt', 'w') as fle2:
		# 		json.dump(streak, fle2, indent=4)
		# 	s += 1
		# else:
		# 	streak[str(ctx.author.id)] = 1
		# 	with open('datafiles/daily.txt', 'w') as fle3:
		# 		json.dump(streak, fle3, indent=4)
		# 	s = 0
		if db[str(ctx.author.id)][0] == 70:
			e1 = discord.Embed(
				description="You will lose your 69 day streak, do you wish to continue?",
				colour=discord.Colour.red(),
				timestamp=datetime.utcnow()
			)
			e1.set_author(name="Confirmation", icon_url=ctx.author.avatar_url)
			msg = await ctx.send(embed=e1)
			await msg.add_reaction("✅")
			await msg.add_reaction("❎")
			def check(reaction, user):
				return str(reaction.emoji) in [
				"✅", "❎"
			] and user == ctx.author and reaction.message == msg
			reaction, user = await bot.wait_for("reaction_add", check=check, timeout=69)
			await msg.delete()
			if str(reaction.emoji) == "✅":
				pass
			else:
				db[str(ctx.author.id)][0] -= 1
				return
		e = discord.Embed(
			description=f"Added {1000+(250*s):,} credits to bank.",
			colour=discord.Colour.green(),
			timestamp=datetime.utcnow())
		e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
		if "666" in str(s):
			if db[aid][1] <= 666:
				e.add_field(
					name=f"You've been visited by Satan",
					value=
					"He was going to steal money from you, but seeing you don't have a lot, he's giving you 1,000,000! (Courtesy of the richest guy using this bot)"
				)
				db[aid][1] += 1000000
				dct = {}
				for i in db:
					if type(db[i][1]) == int or type(db[i][1]) == float:
						dct[i] = db[i]
				sorted_dict = dict(sorted(dct.items(), key=lambda item: item[1], reverse=True))
				richest = list(sorted_dict.keys())[0]
				db[richest][1] -= 1000000
			else:
				e.add_field(
					name=f"You've been visited by Satan",
					value=
					"He stole 666 coins from your account!"
				)
				db[aid][1] -= 666
		db[aid][1] += 1000 + (250 * s)
		if s % 50 == 0 and s != 0:
			e.add_field(name=f"{s} daily streak bonus",
						value=f"Extra {10000*s//50} added")
			db[aid][1] += 200 * s
		elif "69" in str(s):
			e.add_field(name=f"Funny number bonus",
						value=f"Extra 696,969 added")
			db[aid][1] += 696969
		elif "420" in str(s):
			e.add_field(name=f"||Weed|| number bonus",
						value=f"Extra 420,420,420,420 added")
			db[aid][1] += 420420420420
		e.set_footer(text=f"Daily streak of {s} days")
		await ctx.reply(embed=e, mention_author=False)
		await _save()


def convert(seconds):
	seconds = seconds % (24 * 3600)
	hour = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60

	return "%d hours %02d minutes %02d seconds" % (hour, minutes, seconds)


@daily.error
async def daily_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		msg = ('This command is ratelimited, please try again in %s' %
			   convert(error.retry_after))
		await ctx.reply(msg, mention_author=False)
	else:
		raise error


#===========================================Fun======================================================================


@bot.command(aliases=['rockpaperscissors'])
async def rps(ctx, member: Optional[discord.Member], choice=None):
	if choice is None and member is None:
		await ctx.reply(
			"I choose rock and it has chosen to knock your teeth out",
			mention_author=False)
	elif member:
		if member == ctx.author:
			file = discord.File("images/killyou.png")
			await ctx.send(file=file)
			return
		if member.bot:
			await ctx.send(
				"Imagine being so bad at rock paper scissors that you need to play with a bot to win"
			)
			return
		await ctx.send(
			f"{member.mention}, you have been summoned by {ctx.author.name} to play a game of rock, paper, scissors."
		)
		msg = await ctx.send("Do you accept?")
		await msg.add_reaction("✅")
		await msg.add_reaction("❎")

		def check(reaction, user):
			return str(reaction.emoji) in [
				"✅", "❎"
			] and user == member and reaction.message == msg

		reaction, user = await bot.wait_for('reaction_add', check=check)
		await msg.delete()
		if reaction.emoji == "✅":
			await ctx.send("Check DMs")
			c1 = await ctx.author.create_dm()
			c2 = await member.create_dm()
			m1 = await c1.send(
				"Select 🪨 for rock, 📄 for paper, or ✂️ for scissors")
			m2 = await c2.send(
				"Select 🪨 for rock, 📄 for paper, or ✂️ for scissors")
			await m1.add_reaction("🪨")
			await m2.add_reaction("🪨")
			await m1.add_reaction("📄")
			await m2.add_reaction("📄")
			await m1.add_reaction("✂️")
			await m2.add_reaction("✂️")

			def check1(reaction, user):
				return str(reaction.emoji) in [
					"🪨", "📄", "✂️"
				] and (reaction.message in [m1, m2])

			def check2(reaction, user):
				if reaction1.message == m1:
					m = m2
				else:
					m = m1
				return str(reaction.emoji) in ["🪨", "📄", "✂️"
											   ] and (reaction.message == m)

			try:
				reaction1, user1 = await bot.wait_for('reaction_add',
													  check=check1,
													  timeout=30)
				reaction2, user2 = await bot.wait_for('reaction_add',
													  check=check2,
													  timeout=30)
				if user1 == member:
					reaction1, reaction2 = reaction2, reaction1
					c1, c2 = c2, c1
				if str(reaction1.emoji) == str(reaction2.emoji):
					w = 0
				elif str(reaction1.emoji) == "🪨" and str(
					reaction2.emoji) == "📄":
					w = c2
					l = c1
				elif str(reaction1.emoji) == "🪨" and str(
					reaction2.emoji) == "✂️":
					w = c1
					l = c2
				elif str(reaction1.emoji) == "📄" and str(
					reaction2.emoji) == "🪨":
					w = c1
					l = c2
				elif str(reaction1.emoji) == "📄" and str(
					reaction2.emoji) == "✂️":
					w = c2
					l = c1
				elif str(reaction1.emoji) == "✂️" and str(
					reaction2.emoji) == "🪨":
					w = c2
					l = c1
				elif str(reaction1.emoji) == "✂️" and str(
					reaction2.emoji) == "📄":
					w = c1
					l = c2
				else:
					await ctx.send(reaction1.emoji)
					await ctx.send(reaction2.emoji)
				if w == c1:
					await c1.send(f"You won! {member.name} picked {reaction2}!"
								  )
					await c2.send(
						f"You lose. {ctx.author.name} picked {reaction1}")
					l = [
						f"Game ended. {ctx.author.name} won",
						f"Game ended. {ctx.author.name} won and gets to keep {member.name}'s kidneys",
						f"Game ended. {ctx.author.name} won and has the right to own {member.name}'s soul"
					]
					await ctx.send(random.choice(l))
				elif w == c2:
					await c2.send(
						f"You won! {ctx.author.name} picked {reaction1}!")
					await c1.send(f"You lose. {member.name} picked {reaction2}"
								  )
					l = [
						f"Game ended. {member.name} won",
						f"Game ended. {member.name} won and gets to keep {ctx.author.name}'s kidneys",
						f"Game ended. {member.name} won and has the right to own{ctx.author.name}'s soul"
					]
					await ctx.send(random.choice(l))
				else:
					await c1.send(f"Both picked {reaction1}, it's a tie!")
					await c2.send(f"Both picked {reaction2}, it's a tie!")
					l = [
						f"Game ended. It was a tie",
						f"Game ended. I get to keep both of your kidneys.",
						f"Game ended. Wasted so much time for it to be a tie."
					]
					await ctx.send(random.choice(l))
			except asyncio.TimeoutError:
				await m1.delete()
				await m2.delete()
				await ctx.send(
					"Someone didn't respond, and my master doesn't know how to check who was it, so you two figure it out amongst yourselves"
				)
		else:
			await ctx.send(
				f"oof looks like {member.name} is either busy or hates your guts. No other reason to reject a simple game of rock, paper, scissors"
			)

	else:
		options = ['rock', 'paper', 'scissors']
		options2 = ['rock', 'paper', 'scissors']
		if choice in options:
			for i in options:
				if i != choice:
					options2.append(i)
			bchoice = options2[random.randint(0, 4)]
			await ctx.reply(bchoice, mention_author=False)
			if bchoice == choice:
				await ctx.send("Tie")
			elif bchoice == 'rock' and choice.lower() == 'paper':
				await ctx.send("WHAT! how did you win")
			elif bchoice == 'rock' and choice.lower() == 'scissors':
				await ctx.send("Hah I won now all your money is mine")
			elif bchoice == 'paper' and choice.lower() == 'rock':
				await ctx.send("Hah I won now all your money is mine")
			elif bchoice == 'paper' and choice.lower() == 'scissors':
				await ctx.send("WHAT! how did you win")
			elif bchoice == 'scissors' and choice.lower() == 'paper':
				await ctx.send("Hah I won now all your money is mine")
			elif bchoice == 'scissors' and choice.lower() == 'rock':
				await ctx.send("WHAT! how did you win")
		else:
			await ctx.reply(
				"You have entered an invalid input. Bot will self destruct in",
				mention_author=False)
			for i in range(3, 0, -1):
				await asyncio.sleep(1)
				await ctx.send(i)
			await ctx.send("boom")


@bot.command(aliases=['bs'])
async def battleships(ctx):
	global gaem
	if ctx.channel.id in gaem:
		await ctx.send(
			"Another game is going on in this channel, please wait or play in a different channel"
		)
		return
	gaem.append(ctx.channel.id)
	board = []
	turn = 0

	def check(m):
		return m.author == ctx.author and m.channel == ctx.message.channel

	for x in range(0, 5):
		board.append(["🟦"] * 5)

	e = discord.Embed(description=f"\
 1  2  3  4  5\n \
{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}1\n\
{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}2\n\
{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}3\n\
{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}4\n\
{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}{board[0][0]}5\n\
 1  2  3  4  5")
	e.set_author(name="Battleships", icon_url=ctx.author.avatar_url)
	e.set_footer(text=f"Turn {turn + 1} | Enter co-ordinates (Format: x,y)")
	await ctx.send(embed=e)

	def random_row(board):
		return random.randint(0, len(board) - 1)

	def random_col(board):
		return random.randint(0, len(board[0]) - 1)

	ship_row = random_row(board)
	ship_col = random_col(board)
	while turn < 8:
		try:
			message = await bot.wait_for('message', check=check, timeout=60.0)
			if str(message.content) == "end":
				await ctx.send("wimp")
				await ctx.send(f"My ship was at ({ship_col+1},{ship_row+1})")
				gaem.remove(ctx.channel.id)
				return
			elif "," not in str(message.content):
				continue
			else:
				coords = str(message.content).split(",")
				try:
					guess_row = int(coords[1]) - 1
					guess_col = int(coords[0]) - 1
					if guess_row == ship_row and guess_col == ship_col:
						await ctx.send(
							"Congratulations! You sank my battleship!")
						gaem.remove(ctx.channel.id)
						return
					else:
						if guess_row > 4 or guess_col > 4 or guess_row < 0 or guess_col < 0:
							await ctx.send(
								"Oops, that's not even in the ocean.")
							continue
						elif board[guess_row][guess_col] == "🟥":
							await ctx.send("You guessed that one already.")
							continue
						else:
							await ctx.send("You missed my battleship!")
							board[guess_row][guess_col] = "🟥"
							turn += 1
						if turn == 8:
							board[ship_row][ship_col] = "🇽"
						e = discord.Embed(description=f"\
{board[0][0]}{board[0][1]}{board[0][2]}{board[0][3]}{board[0][4]}\n\
{board[1][0]}{board[1][1]}{board[1][2]}{board[1][3]}{board[1][4]}\n\
{board[2][0]}{board[2][1]}{board[2][2]}{board[2][3]}{board[2][4]}\n\
{board[3][0]}{board[3][1]}{board[3][2]}{board[3][3]}{board[3][4]}\n\
{board[4][0]}{board[4][1]}{board[4][2]}{board[4][3]}{board[4][4]}")
						e.set_author(name=f"Turn {turn + 1}",
									 icon_url=ctx.author.avatar_url)
						e.set_footer(text="Format: x,y")
						if turn == 8:
							e.title = "Game over"
							gaem.remove(ctx.channel.id)
						await ctx.send(embed=e)
						if turn == 8:
							await ctx.send(
								f"My ship was at ({ship_col+1},{ship_row+1})")
							return
				except ValueError:
					await ctx.send("Bruh you want me to attack WHERE?")
		except asyncio.TimeoutError:
			await ctx.send("You took too long to decide and your ship sank")
			gaem.remove(ctx.channel.id)
			return
	gaem.remove(ctx.channel.id)


@bot.command(aliases=['guess', 'ng'])
async def numguess(ctx):
	global gaem
	if ctx.channel.id in gaem:
		await ctx.send(
			"Another game is going on in this channel, please wait or play in a different channel"
		)
		return
	gaem.append(ctx.channel.id)
	num = random.randint(1, 250)
	l = []
	await ctx.send("Number guesser")
	await ctx.send(
		"Guess a number between 1 and 250 in 7 chances!\nType `end` to end the game"
	)
	count = 7

	def check(m):
		return m.author == ctx.author and m.channel == ctx.message.channel

	while count > 0:
		try:
			message = await bot.wait_for('message', check=check, timeout=60.0)
			if str(message.content) == "end":
				await ctx.send("wimp")
				await ctx.send(f"Number was {num}")
				gaem.remove(ctx.channel.id)
				return
			try:
				guess = int(message.content)
			except ValueError:
				await ctx.reply(
					"What part of **number** guess do you not understand",
					mention_author=False)
				continue
			if int(message.content) in l:
				await ctx.reply(
					"Guessing the same number again isn't going to change my answer",
					mention_author=False)
				continue
			else:
				l.append(int(message.content))
			if guess > 250:
				if count > 1:
					await ctx.reply(
						"I asked for a number between 1 and 250, not your mom's weight",
						mention_author=False)
					continue
			elif guess < 1:
				if count > 1:
					await ctx.reply(
						"I asked for a number between 1 and 250, not your IQ",
						mention_author=False)
					continue
			elif (num - guess) == 1 or (guess - num) == 1:
				if count > 1:
					await ctx.reply(
						f"You have no idea how close you are to the number. Won't tell if higher or lower. \
					\nChances left: {count-1}",
						mention_author=False)
			elif (num - guess) < 6 and (num - guess) > 0:
				if count > 1:
					await ctx.reply(
						f"You're soo close! A tiny bit higher \nChances left: {count-1}",
						mention_author=False)
			elif (guess - num) < 6 and (guess - num) > 0:
				if count > 1:
					await ctx.reply(
						f"You're soo close! A tiny bit lower \nChances left: {count-1}",
						mention_author=False)
			elif guess < num:
				if count > 1:
					await ctx.reply(f"Higher \nChances left: {count-1}",
									mention_author=False)
			elif guess > num:
				if count > 1:
					await ctx.reply(f"Lower \nChances left: {count-1}",
									mention_author=False)
			else:
				await asyncio.sleep(2)
				await ctx.send("You won!")
				await ctx.send(f"You did it in {8 - count} chances!")
				aid = str(ctx.message.author.id)
				gaem.remove(ctx.channel.id)
				if aid in db:
					if num == 69 or num == 169:
						db[aid][1] += 6969
						e = discord.Embed(
							description=
							"6,969 credits were added to your balance",
							colour=discord.Colour.green())
						e.set_author(name="Winner!",
									 icon_url=ctx.author.avatar_url)
						await ctx.send(embed=e)
						await _save()
						return
					elif 8 - count == 1:
						await ctx.send("~~Hello police there's a hacker here~~"
									   )
						db[aid][1] += 100000000000
						e = discord.Embed(
							description=
							"100,000,000,000 credits were added to your balance",
							colour=discord.Colour.green())
						e.set_author(name="Winner!",
									 icon_url=ctx.author.avatar_url)
						await ctx.send(embed=e)
						await _save()
						return
					elif 8 - count <= 3:
						db[aid][1] += 10000
						e = discord.Embed(
							description=
							"10,000 credits were added to your balance",
							colour=discord.Colour.green())
						e.set_author(name="Winner!",
									 icon_url=ctx.author.avatar_url)
						await ctx.send(embed=e)
						await _save()
						return
					elif 8 - count <= 5:
						db[aid][1] += 100
						e = discord.Embed(
							description=
							"100 credits were added to your balance",
							colour=discord.Colour.green())
						e.set_author(name="Winner!",
									 icon_url=ctx.author.avatar_url)
						await ctx.send(embed=e)
						await _save()
						return
					else:
						db[aid][1] += 10
						e = discord.Embed(
							description="10 credits were added to your balance",
							colour=discord.Colour.green())
						e.set_author(name="Winner!",
									 icon_url=ctx.author.avatar_url)
						await ctx.send(embed=e)
						await _save()
						return
				else:
					return
			if count == 3:
				ns = str(num)
				await asyncio.sleep(1)
				await ctx.reply(
					f"I see you're having a hard time guessing \nFirst digit is {ns[0]}, thank me later",
					mention_author=False)
			count -= 1
			if count == 0:
				await asyncio.sleep(2)
				await ctx.reply("You lose.", mention_author=False)
				await ctx.send(f"The number was {num}")
				gaem.remove(ctx.channel.id)
				return
		except asyncio.TimeoutError:
			await ctx.reply(
				"Yeah I don't have all day long, I closed the game.",
				mention_author=False)
			gaem.remove(ctx.channel.id)
			return


@bot.command(aliases=['toss', 'ct'])
async def cointoss(ctx):
	if ctx.guild:
		p = db[str(ctx.guild.id)][1]
	else:
		p = ">>"
	aid = str(ctx.message.author.id)
	toss = random.randint(0, 1)
	num = random.randint(1, 100)
	await ctx.send("Tossing a coin.....")
	await asyncio.sleep(1)
	if num == 49:
		await ctx.send("Wait what")
		await ctx.reply("THE COIN LANDED ON ITS SIDE")
		if aid in db:
			db[aid][1] += 100000000
			await ctx.send("(Check your balance btw)")
			await _save()
		else:
			await ctx.send(
				"If you had an account right now, you would be swimming in money"
			)
			await ctx.send(f"(Do `{p}register` to make an account)")
	else:
		if toss == 1:
			result = "Heads"
		else:
			result = "Tails"
		await ctx.reply(result, mention_author=False)


@bot.command()
async def hangman(ctx, topic: str = None):
	global gaem
	if ctx.channel.id in gaem:
		await ctx.send(
			"Another game is going on in this channel, please wait or play in a different channel"
		)
		return
	gaem.append(ctx.channel.id)

	def check(m):
		return m.author == ctx.author and m.channel == ctx.message.channel

	specs = ':\'.,!@#$%^&*(){}[];<>?/\|`-_+=~é'
	guesses = ''
	turns = 7
	chars = []
	second = 0
	if not topic:
		word = random.choice(words)
	elif topic.lower() == "countries" or topic.lower(
	) == "country" or topic.lower() == "c":
		counts = [
			country.name.lower() for country in list(pycountry.countries)
		]
		word = random.choice(counts)
	elif topic.lower() == "movies" or topic.lower() == "movie" or topic.lower(
	) == "films" or topic.lower() == "m":
		word = random.choice(movies).lower()
	elif topic.lower() == "onewordmovie" or topic.lower(
	) == "onewordmovies" or topic.lower() == "owm":
		word = random.choice(wordmovies).lower()
	elif topic.lower() == "pokemon" or topic.lower(
	) == "pokémon" or topic.lower() == "p":
		num = random.randint(1, 898)
		p = pypokedex.get(dex=num)
		word = p.name.lower()
	else:
		await ctx.send("That's not even a word")
		gaem.remove(ctx.channel.id)
		return
	await ctx.send("Guess the characters:")
	guess_msg = await ctx.send(images[turns])
	blanks = ""
	if not topic:
		word_msg = await ctx.send(f"`{' '.join('_'*len(word))}`")
	else:
		for char in word:
			if char.isspace():
				blanks += " "
			else:
				blanks += "_ "
		word_msg = await ctx.send(blanks)
	strg = ""
	count = 7
	while turns > 0:
		if second != 1:
			out = ''
			rem_chars = 0
			for char in word:
				if char in guesses:
					out += char
				elif char.isalnum():
					out += '_'
					rem_chars += 1
				else:
					out += char
			await word_msg.edit(content=f"`{' '.join(out)}`")
			if rem_chars == 0:
				await word_msg.edit(content=f'**{word}**')
				await guess_msg.edit(content=f"{images[turns]}")
				await ctx.send("**You Win :trophy:**")
				if str(ctx.author.id) in db:
					db[str(ctx.author.id)][1] += 1000 * (turns)
					e = discord.Embed(
						description=
						f"{1000*(turns):,} credits added to account",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_author(name="You win!",
								 icon_url=ctx.author.avatar_url)
					await ctx.send(embed=e)
					await _save()
				gaem.remove(ctx.channel.id)
				return
		else:
			second += 1

		try:
			msg = await bot.wait_for('message', check=check, timeout=60.0)
			guess = str(msg.content).lower()
			if guess == 'end':
				await ctx.send("You quit :clown:")
				gaem.remove(ctx.channel.id)
				return
		except asyncio.TimeoutError:
			await ctx.send("You took too long :hourglass:")
			await guess_msg.delete()
			await word_msg.delete()
			gaem.remove(ctx.channel.id)
			return

		if len(guess) > 1:
			temp2 = False
		elif len(guess) == 1:
			temp2 = True
			guesses += guess
		if ctx.guild:
			await msg.delete()

		if temp2:
			if guess in chars:
				await ctx.send("You've already guessed that smh",
							   delete_after=1.0)
			elif guess in specs:
				await ctx.send(
					"Don't use special characters, they're taken care of.",
					delete_after=1.0)
			else:
				chars.append(guess)
				if count == 7 or (second == 2 and count == 7):
					strg += guess
				else:
					strg += ", " + guess
				await guess_msg.edit(
					content=f"{images[turns]} \n`Characters guessed: {strg}`")
				if guess not in word:
					turns -= 1
					await ctx.send("Wrong :x:", delete_after=1.0)
					await guess_msg.edit(
						content=f"{images[turns]} \n`Characters guessed: {strg}`"
					)
					if turns == 0:
						await word_msg.edit(content=f'**{word}**')
						gaem.remove(ctx.channel.id)
						return await ctx.send("You Lose :x:")
		else:
			if guess != word:
				if second > 0:
					turns = 0
					await word_msg.edit(content=f'**{word}**')
					gaem.remove(ctx.channel.id)
					return await ctx.send("You Lose :x:")
				else:
					await ctx.send("You won!", delete_after=5.0)
					await asyncio.sleep(1)
					await ctx.send("sike", delete_after=4.0)
					await ctx.send(
						"Since that answer was so bad, I'm going to give you another chance.",
						delete_after=4.0)
					second += 1
					count += 1
			else:
				await word_msg.edit(content=f'**{word}**')
				await guess_msg.edit(content=f"{images[turns]}")
				await ctx.send("**You Win :trophy:**")
				if str(ctx.author.id) in db:
					db[str(ctx.author.id)][1] += 1000 * (turns)
					e = discord.Embed(
						description=
						f"{1000*(turns):,} credits added to account",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_author(name="You win!",
								 icon_url=ctx.author.avatar_url)
					await ctx.send(embed=e)
					await _save()
				gaem.remove(ctx.channel.id)
				return
		count -= 1


@bot.command()
@commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
async def slots(ctx, amount: str = None):
	global gaem
	if ctx.channel.id in gaem:
		await ctx.send(
			"Another game is going on in this channel, please wait or play in a different channel"
		)
		return
	gaem.append(ctx.channel.id)
	emojis = "🍎🍊🍐🍍🍉🍇🍓🍒"
	a = random.choice(emojis)
	b = random.choice(emojis)
	c = random.choice(emojis)
	aid = str(ctx.author.id)
	if amount is None:
		await ctx.reply("You need to bet some money first",
						mention_author=False)
		gaem.remove(ctx.channel.id)
		return
	if not amount.isdigit():
		if amount[-1].lower() in ["k", "m", "b", "t", "q"
								  ] and amount[:-1].isdigit():
			amt2 = amount[:-1]
			mul = amount[-1].lower()
			if mul == "k":
				amount = int(amt2) * 1000
			elif mul == "m":
				amount = int(amt2) * 1000000
			elif mul == "b":
				amount = int(amt2) * 1000000000
			elif mul == "t":
				amount = int(amt2) * 1000000000000
			elif mul == "q":
				amount = int(amt2) * 1000000000000000
		elif amount.lower() == "table":
			e = discord.Embed(title="Slots table",
							  description="**3 in a row (Jackpot):**\n \
🍇, 🍓, 🍒: 100,000 × <amount> \n🍎, 🍍, 🍉: 10,000 × <amount> \n🍊, 🍐: 1,000 × <amount> \n \n \
**2 in a row:** \n2 × <amount>")
			e.colour = discord.Colour.random()
			e.timestamp = datetime.utcnow()
			e.set_footer(
				text=
				"All winnings listed here are before subtracting the amount bet"
			)
			await ctx.send(embed=e)
			gaem.remove(ctx.channel.id)
			return
		else:
			await ctx.reply("The casino only accepts credits not this garbage",
							mention_author=False)
			gaem.remove(ctx.channel.id)
			return
	amount = int(amount)
	if aid not in db:
		await ctx.reply("You don't have a bank account.", mention_author=False)
		gaem.remove(ctx.channel.id)
		return
	elif amount < 1:
		await ctx.reply(
			"If you're trying to find loopholes in my code, good job! Have a cookie! 🍪",
			mention_author=False)
		gaem.remove(ctx.channel.id)
		return
	elif amount > db[aid][1]:
		await ctx.send(
			"Sorry to be the bearer of bad news but you don't have that much money"
		)
		await ctx.reply(f"You have only ||{db[aid][1]:,}||",
						mention_author=False)
		gaem.remove(ctx.channel.id)
		return

	db[aid][1] -= amount
	await _save()
	slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
	msg = await ctx.send(slotmachine)
	for i in range(4):
		a = random.choice(emojis)
		b = random.choice(emojis)
		c = random.choice(emojis)
		slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
		await asyncio.sleep(1.2)
		await msg.edit(content=slotmachine)
		if i == 3:
			hax = random.randint(1, 10000)
			if hax in ([x for x in range(1,51)]):
				fruits = ["🍊", "🍐"]
				a = random.choice(fruits)
				a = b = c
			elif hax in ([x for x in range(100, 125)]):
				fruits = ["🍎", "🍍", "🍉"]
				a = random.choice(fruits)
				a = b = c
			elif hax in ([x for x in range(150, 160)]):
				fruits = ["🍇", '🍓', "🍒"]
				a = random.choice(fruits)
				a = b = c
			elif hax in ([x for x in range(200, 400)]):
				if a != b:
					a = b
					if b == c:
						c = random.choice(emojis)
				elif b != c:
					b = c
					if a == c:
						a = random.choice(emojis)
				elif c != a:
					a = c
					if b == c:
						b = random.choice(emojis)
			await asyncio.sleep(1)
			slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
			await msg.edit(content=slotmachine)

	if (a == b == c):
		await msg.edit(
			content=
			f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ] \nAll matching, you won! 🎉"
		)
		if a == "🍒" or a == "🍓" or a == "🍇":
			multi = 100000
		elif a == "🍎" or a == "🍍" or a == "🍉":
			multi = 10000
		else:
			multi = 1000
		if aid in db:
			db[aid][1] += amount * multi
			e = discord.Embed(
				description=f"{amount*multi:,} credits added to account",
				colour=discord.Colour.green(),
				timestamp=datetime.utcnow())
			e.set_author(name="You win!", icon_url=ctx.author.avatar_url)
			await ctx.send(embed=e)
			await _save()
			gaem.remove(ctx.channel.id)
	elif (a == b) or (a == c) or (b == c):
		await msg.edit(
			content=
			f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ] \n2 in a row, so close!"
		)
		if aid in db:
			db[aid][1] += amount * 2
			e = discord.Embed(
				description=f"{amount*2:,} credits added to account",
				colour=discord.Colour.dark_blue(),
				timestamp=datetime.utcnow())
			e.set_author(name="You didn't lose!",
						 icon_url=ctx.author.avatar_url)
			await ctx.send(embed=e)
			await _save()
			gaem.remove(ctx.channel.id)
	else:
		await msg.edit(
			content=
			f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ] \nNo match, you lost 😢"
		)
		gaem.remove(ctx.channel.id)


@bot.command()
async def roll(ctx, guess=None):
	dieroll = random.randint(1, 6)
	if guess is None:
		await ctx.send(f"The die says {dieroll}!")
	else:
		if guess.isdigit():
			if dieroll == int(guess):
				await ctx.reply(f"Your guess was correct, it is a {dieroll}!",
								mention_author=False)
			else:
				await ctx.reply(
					f"Aw man, you didn't get it right! The die gave a {dieroll}.",
					mention_author=False)


# @bot.command(aliases=['rt'])
# async def reactiontime(ctx):
#	 global gaem
#	 if ctx.channel.id in gaem:
#		 await ctx.send("Another game is going on in this channel, please wait or play in a different channel")
#		 return
#	 gaem.append(ctx.channel.id)
#	 emojis = ['😁','😎','💀','👌','👀','🥚','🍫','🍕','🎲','🛺','🔪','📈']
#	 emoji = random.choice(emojis)
#	 await ctx.send("React with the given emoji first to win!")
#	 await asyncio.sleep(random.randint(5,10))
#	 msg = await ctx.send(emoji)
#	 def check(reaction, user):
#		 return str(reaction.emoji) == emoji and user != bot.user and reaction.message == msg
#	 try:
#		 reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
#		 await msg.clear_reactions()
#		 await ctx.send(f"Congratulations {user.name} you won!")
#		 aid = str(ctx.message.author.id)
#		 gaem.remove(ctx.channel.id)
#		 if aid in db:
#			 db[aid][1] += 100
#			 e = discord.Embed(title="Winner!", description="100 credits were added to your balance", colour=discord.Colour.green())
#			 await ctx.send(embed=e)
#			 await _save()
#		 else:
#			 await ctx.send("Register for an account to get credits for winning")
#	 except asyncio.TimeoutError:
#		 await ctx.reply("No one responded, how busy are ya idiots", mention_author=False)
#		 gaem.remove(ctx.channel.id)

#============================================Actions=================================================================


@bot.command()
async def choose(ctx, *, choices: str = None):
	if choices is None:
		await ctx.send(
			"I choose the first option. Oh wait, there are no options.")
	options = choices.split()
	await ctx.reply(random.choice(options), mention_author=False)


@bot.command(aliases=['8ball', 'eightball'])
async def ball8(ctx, *, q=None):
	apoora = discord.File('images/apoorafull.jpeg')
	if q is None:
		await ctx.send(
			"It is certain that the user of this command is an idiot.")
	else:
		rples = [
			"It is certain.", "It is decidedly so.", "Without a doubt.",
			"Definitely.", "You may rely on it", "As I see it, yes",
			"Most likely.", 'Outlook good.', apoora, 'Signs point to yes',
			'Reply hazy, ask again.', 'Better not tell you now',
			'Cannot predict now.', 'Ask again later.',
			'Concentrate and ask again.', "Don't count on it.",
			'My reply is no.', 'My sources say no.', 'Outlook not so good.',
			'Very doubtful.'
		]
		ans = random.randint(0, 19)
		if (q.lower() == "will avaneesh get stabbed today?" or q.lower() == "will avaneesh get stabbed today" or\
		(str(ctx.author) == "SkullBlazer#9339" and (q.lower() == "will i get stabbed today?" or q.lower() == "will i get stabbed today"))) and ctx.guild.id in trusted:
			await ctx.reply(file=apoora, mention_author=False)
		elif ans == 8:
			if ctx.guild.id in trusted:
				await ctx.reply(file=apoora, mention_author=False)
			else:
				await ctx.reply("Yes.", mention_author=False)
		else:
			await ctx.reply(rples[ans], mention_author=False)
			try:
				msg = await bot.wait_for('message', timeout=20.0)
				if "bruh" in str(
					msg.content).lower() or msg.content.startswith(
						'no') or "kekw" in str(msg.content).lower():
					await ctx.send("<:kekw:819137093514297365>")
			except asyncio.TimeoutError:
				return


@bot.command(name="say")
async def _say(ctx, member:Optional[discord.Member], *, phrase: str = None):
	if phrase is None:
		await ctx.reply("What do you want me to say, dumdum",
						mention_author=False)
		return
	if member is None:
		member = ctx.author
	elif "@everyone" in phrase or "@here" in phrase:
		await ctx.send(
			f"<:mikebruh:819137093850759169> Did you seriously just try and make me say that {ctx.author.mention}"
		)
		await ctx.message.delete()
		return
	elif "batman" in phrase.lower():
		batsy = discord.File("images/batsy.png")
		await ctx.reply(file=batsy, mention_author=False)
		return
	n = datetime.now()
	mt = ""
	for i in range(len(phrase) // 2):
		mt += "⠀"
	await ctx.reply(f'"{phrase}"\n {mt} **-{member}, {n.year}**',
					mention_author=False)


@bot.command(aliases=['xkcd'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def xkcdcomic(ctx, num=None):
	f = True
	if num:
		if num.isdigit():
			num = int(num)
			link = xkcd.getComic(num).getImageLink()
		else:
			num = str(num).lower()
			if num == "latest" or num == "recent" or num == "r" or num == "l":
				num = xkcd.getLatestComicNum()
				link = xkcd.getLatestComic().getImageLink()
			elif num == "what if" or num == "wi":
				f = False
				link = xkcd.getRandomWhatIf().getLink()
			else:
				f = False
				link = "Valid arguments include a comic number, 'what if', or 'latest'"
	else:
		num = random.randint(1, xkcd.getLatestComicNum())
		link = xkcd.getComic(num).getImageLink()
	await ctx.send(link)
	if f:
		await asyncio.sleep(3)
		msg = await ctx.send(
			"```Click on 📎 for the link, or ❓ for explanation```")
		await msg.add_reaction("📎")
		await msg.add_reaction("❓")

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in ("📎", "❓")

		try:
			reaction, user = await bot.wait_for('reaction_add',
												timeout=40,
												check=check)
			if ctx.guild:
				await msg.clear_reactions()
			if reaction == "📎":
				await ctx.send(f"```{link}```")
			else:
				await ctx.send(xkcd.getComic(num).getExplanation())
		except asyncio.TimeoutError:
			await msg.delete()


@bot.command()
async def joke(ctx):
	URL = 'https://official-joke-api.appspot.com/random_joke'

	def check_valid_status_code(request):
		if request.status_code == 200:
			return request.json()
		return False

	def get_joke():
		request = requests.get(URL)
		data = check_valid_status_code(request)
		return data

	joke = get_joke()
	if joke == False:
		await ctx.send("Couldn't get joke from API. Try again later.")
	else:
		await ctx.send(joke['setup'] + '\n' + joke['punchline'])


def download_file(url, destination):
	req = requests.get(url)
	file = open(destination, "wb")
	for chunk in req.iter_content(100000):
		file.write(chunk)
	file.close()


def get_avatar(user, animate=True):
	if user.avatar_url:
		avatar = str(user.avatar_url).replace(".webp", ".png")
	else:
		avatar = str(user.default_avatar_url)
	if not animate:
		avatar = avatar.replace(".gif", ".png")
	return avatar


def rescale(image, dimensions):
	image.thumbnail(dimensions, Image.ANTIALIAS)
	return image


def grayscale(rgb):
	return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def dodge(front, back):
	result = front * 255 / (256 - back)
	result[result > 255] = 255
	result[back == 255] = 255
	return result.astype('uint8')


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def trigger(ctx, *, member: discord.Member = None):
	#	 await ctx.channel.trigger_typing()
	if member is None:
		member = ctx.author
	download_file(get_avatar(member, True), "images/trigger.png")
	avatar = Image.open("images/trigger.png")
	triggered = rescale(Image.open("images/triggered.jpeg"), avatar.size)
	position = 0, avatar.getbbox()[3] - triggered.getbbox()[3]
	avatar.paste(triggered, position)
	avatar.save("images/trigger.png")
	await ctx.send(file=discord.File("images/trigger.png"))


@bot.command(aliases=['bw', 'bnw', 'b&w'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def blackandwhite(ctx, user: discord.Member = None):
	if user is None:
		user = ctx.author
	download_file(get_avatar(user, True), "images/blackandwhite.png")
	avatar = Image.open("images/blackandwhite.png").convert("L")
	avatar.save("images/blackandwhite.png")
	await ctx.send(file=discord.File("images/blackandwhite.png"))


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def cartoon(ctx, user: discord.Member = None):
	if user is None:
		user = ctx.author
	download_file(get_avatar(user, False), "images/cartoon.jpg")
	img = cv2.imread("images/cartoon.jpg")
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.medianBlur(gray, 5)
	edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
								  cv2.THRESH_BINARY, 9, 9)
	color = cv2.bilateralFilter(img, 9, 250, 250)
	cartoon = cv2.bitwise_and(color, color, mask=edges)
	cv2.imwrite("images/cartoon.jpg", cartoon)
	await ctx.send(file=discord.File("images/cartoon.jpg"))


@bot.command(aliases=['sketch'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def draw(ctx, user: discord.Member = None):
	if not user:
		user = ctx.author
	download_file(get_avatar(user, False), "images/draw.png")
	s = imageio.imread("images/draw.png")
	g = grayscale(s)
	i = 255 - g
	b = scipy.ndimage.filters.gaussian_filter(i, sigma=10)
	r = dodge(b, g)
	cv2.imwrite('images/draw.png', r)
	await ctx.send(file=discord.File("images/draw.png"))


@bot.command()
@commands.cooldown(rate=1, per=5 * 60, type=commands.BucketType.user)
async def chat(ctx):
	channel = await ctx.author.create_dm()
	await channel.send(
		"Hello! I am SlaveBot, ask me questions and I will answer them! Type `end chat` if you get annoyed, which you will."
	)
	openai.api_key = os.environ["OPENAI_KEY"]
	gaem.append(channel.id)

	def check(m):
		return m.author == ctx.author and m.channel == channel

	while True:
		try:
			question = await bot.wait_for('message', check=check, timeout=60.0)
			if str(question.content).lower() == "end chat":
				gaem.remove(channel.id)
				await channel.send(
					"Didn't take a lot to annoy you huh? Anyway, bye!")
				return
			# if str(question.content)[-1] != "?":
			# 	await channel.send(
			# 		"Either that's a stupid question or it doesn't end in a `?`. Ask again."
			# 	)
			# 	continue
			response = openai.Completion.create(
				engine="davinci",
				prompt=
				f"SlaveBot is a chatbot that reluctantly answers questions.\nYou: How many pounds are in a kilogram?\nSlaveBot: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nSlaveBot: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nSlaveBot: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nSlaveBot: I’m not sure. I’ll ask my friend Google.\nYou: {str(question.content)}\nSlaveBot:",
				temperature=0.3,
				max_tokens=60,
				top_p=0.3,
				frequency_penalty=0.5,
				presence_penalty=0.0,
				stop=["\n", "SlaveBot:"])
			await channel.send(response.choices[0].text)
		except asyncio.TimeoutError:
			await channel.send("Wow the awkward silence is killing me, bye.")
			return


@bot.command()
async def fight(ctx, user: discord.Member = None, *, weapon: str = None):
	user2 = (str(user).split("#"))[0]
	if user2 == "asgardian88" or user2 == "Akshita":
		e = discord.Embed(
			title="Attack failed",
			description="You want to fight Batman???? Hah good luck with that.",
			colour=discord.Colour.from_rgb(0, 0, 0))
		await ctx.send(embed=e)
	else:
		if (user2 is None) or (user == ctx.author):
			e = discord.Embed(title="Attack failed",\
							  description=f"{ctx.author.mention} just tried to fight themselves, so now they're in a ~~mental~~ hospital", colour=discord.Colour.dark_red())
			await ctx.send(embed=e)
		elif weapon is None:
			e = discord.Embed(title="Attack failed",\
							  description=f"{ctx.author.mention} tried to fight {user.mention} with nothing and now instead of 206 bones they have nothing", colour=discord.Colour.dark_red())
			await ctx.send(embed=e)
		else:
			if user2 == "SlaveBot":
				await ctx.channel.trigger_typing()
				await ctx.send("What did I ever do to you")
			lst = [["Attack successful (?)", f"{user.mention} wimped out after seeing {ctx.author.mention}'s {weapon}", discord.Colour.dark_teal()],
				   ["Attack successful", f"{ctx.author.mention} absolutely wrecked {user.mention} using their {weapon}", discord.Colour.gold()],
				   ["Attack successful",f"{ctx.author.mention} managed to beat {user.mention}, but barely. {ctx.author.mention}'s {weapon} broke in the fight", discord.Colour.green()],
				   ["Tie",f"{ctx.author.mention} and {user.mention} both wimped out", discord.Colour.lighter_grey()],
				   ["Tie",f"{ctx.author.mention} and {user.mention}'s fight lasted for days, and they finally came to an agreement and declared it a tie.", discord.Colour.greyple()],
				   ["Attack failed",\
f"{ctx.author.mention} might have had their trusty {weapon}, but it was no match against {user.mention}'s secret weapon. Is the weapon friendship? Or a Tsar Bomba? Who knows!",\
					discord.Colour.blurple()],
				   ["Attack failed",f"{ctx.author.mention} would have easily destroyed {user.mention}, if {ctx.author.mention} actually knew how to use their {weapon}", discord.Colour.magenta()],
				   ["Attack failed",f"{ctx.author.mention}'s {weapon} broke 20 seconds later and it all went sideways after that. Easy win for {user.mention}.", discord.Colour.red()],
				   ["Attack failed", f"{ctx.author.mention} for some reason started the attack on {user.mention} but wimped out a second later", discord.Colour.dark_magenta()]]
			ch = random.choice(lst)
			e = discord.Embed(title=ch[0],
							  description=ch[1],
							  colour=ch[2],
							  timestamp=datetime.utcnow())
			await ctx.send(embed=e)
			if ch[0] == "Attack failed" and user2 == "SlaveBot":
				await ctx.send("<:kekw:819137093514297365>")


@bot.command(aliases=['poll'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def quickpoll(ctx, *, question: str = None):
	def check(m):
		return m.author == ctx.author and m.channel == ctx.message.channel

	if question is None:
		await ctx.send("You can't make a poll without a question now, can you?"
					   )
	else:
		if ctx.guild:
			await ctx.message.delete()
		a = await ctx.send("Add options (max. 10) separated by commas")
		try:
			msg = await bot.wait_for('message', check=check, timeout=60.0)
			options = str(msg.content).split(",")
		except asyncio.TimeoutError:
			await ctx.send("Poll closed due to inactivity.")
			return
		await a.delete()
		if ctx.guild:
			await msg.delete()
		if len(options) <= 1:
			await ctx.send('You need more than one option to make a poll')
			return
		if len(options) > 10:
			await ctx.send('You cannot make a poll for more than 10 things!')
			return
		if len(options) == 2 and (options[0].lower() == 'yes' or options[1].lower() == 'y')\
		and (options[1].lower() == 'no' or options[1].lower() == 'n'):
			reactions = ['✅', '❎']
		else:
			reactions = [
				'1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟'
			]

		description = []
		for x, option in enumerate(options):
			description += '\n {} {}'.format(reactions[x], option)
		embed = discord.Embed(description=''.join(description),
							  color=discord.Colour.random(),
							  timestamp=datetime.utcnow())
		embed.set_author(name=f"{ctx.author.name} asks: {question}",
						 icon_url=ctx.author.avatar_url)
		react_message = await ctx.send(embed=embed)
		for reaction in reactions[:len(options)]:
			await react_message.add_reaction(reaction)
		await react_message.edit(embed=embed)


@bot.command(aliases=['patpat'])
async def pat(ctx,
			  members: commands.Greedy[discord.Member] = None,
			  *,
			  reason='for doing an excellent job'):
	if members is None:
		patted = "SkullBlazer"
	elif ctx.author in members:
		await ctx.send(
			"Patting yourself is banned in 130 countries. Ask someone else to do it"
		)
		return
	else:
		patted = ", ".join(x.name for x in members)
	await ctx.send('{} just got patted {}'.format(patted, reason))
	if patted == "SlaveBot":
		await asyncio.sleep(1)
		await ctx.send("yay")
	if patted == 'SkullBlazer':
		await ctx.send(file=discord.File('images/patpat.jpeg'))


@bot.command(aliases=['stabby', 'hauserify'])
async def stab(ctx,
			   members: commands.Greedy[discord.Member] = None,
			   *,
			   reason='for no reason'):
	if "@everyone" in reason or "@here" in reason:
		await ctx.send("Excuse me this is a mass-murder free zone.")
		return
	if members is None:
		stabbed = "SlaveBot"
	elif ctx.author in members:
		fle = discord.File('images/scarn.gif')
		await ctx.send(file=fle)
		return
	else:
		stabbed = ", ".join(x.name for x in members)
	if stabbed == 'asgardian88' or stabbed == 'Akshita':
		await ctx.send(file=discord.File('images/scary.jpeg'))
	else:
		await ctx.send('{} just got stabbed {}'.format(stabbed, reason))
		if stabbed == "SlaveBot":
			await ctx.channel.trigger_typing()
			await asyncio.sleep(1)
			await ctx.send("owie")


@bot.command(aliases=['vibecheck'])
async def bonk(ctx,
			   bonked: Optional[discord.Member],
			   bonker: Optional[discord.Member],
			   *,
			   reason: str = 'for no reason'):
	if "@everyone" in reason or "@here" in reason:
		await ctx.send(
			"Bonking so many people at once is a great way to break your bonking bat."
		)
		await ctx.send(
			"~~\"Break your bonking bat\" sounds like a tongue twister. I wouldn't know, I don't have a tongue~~"
		)
		return
	if bonked is None:
		bonked = ctx.guild.me


#		 bonked = ["SlaveBot", "Say 'Found the easter egg' if you read this line"]
#		 download_file(ctx.guild.me.avatar_url, "images/bonk2.png")
#		 av2 = Image.open("images/bonk2.png")
	if bonker is None:
		bonker = ctx.author
	if ctx.author == bonked:
		fle = discord.File('images/scarn.gif')
		await ctx.send(file=fle)
		return
	else:
		#		 bonked = member.name
		download_file(get_avatar(bonked, False), "images/bonk2.png")
		av2 = Image.open("images/bonk2.png")
	base = Image.open("images/cheemsbonk.jpg")
	download_file(get_avatar(bonker, False), "images/bonk1.png")
	av1 = Image.open("images/bonk1.png")
	#	 txt = Image.new("RGBA", base.size, (255,255,255,0))
	#	 fnt = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS_Bold.ttf", 40)
	#	 bonker = str(ctx.message.author).split('#')
	#	 d = ImageDraw.Draw(txt)
	#	 d.text((100,40), bonker[0], font=fnt, fill=(0,0,0,255))
	#	 d.text((420,215), bonked[0], font=fnt, fill=(0,0,0,255))
	#	 out = Image.alpha_composite(base, txt)
	#	 out.save('images/edit.png')
	rav1 = rescale(av1, (190, 190))
	rav2 = rescale(av2, (190, 190))
	rav1 = rav1.convert("RGBA")
	rav2 = rav2.convert("RGBA")
	base.paste(rav1, (149, 38), rav1)
	base.paste(rav2, (498, 182), rav2)
	base.save("images/edit.png")
	if bonker == ctx.author:
		await ctx.send('{} just got bonked {}'.format(bonked.name, reason))
	else:
		await ctx.send('{} just got bonked by {} {}'.format(
			bonked.name, bonker.name, reason))
	await ctx.send(file=discord.File('images/edit.png'))
	if bonked.name == "SlaveBot":
		await ctx.channel.trigger_typing()
		await asyncio.sleep(1)
		await ctx.send("ouch indeed")

@bot.command()
async def yeet(ctx, member:Optional[discord.Member], *, reason:str="why not"):
	if "@everyone" in reason or "@here" in reason:
		await ctx.send(
			"You try to yeet a ton of people and break your arm. Great job!"
		)
		return
	if not member:
		member = ctx.guild.me
	if member == ctx.author:
		fle = discord.File('images/scarn.gif')
		await ctx.send(file=fle)
		return
	download_file(get_avatar(member, False), "images/yeet2.png")
	av2 = Image.open("images/yeet2.png")
	base = Image.open("images/yeet.png")
	download_file(get_avatar(ctx.author, False), "images/yeet1.png")
	av1 = Image.open("images/yeet1.png")
	rav1 = rescale(av1, (35, 35))
	rav2 = rescale(av2, (35, 35))
	rav1 = rav1.convert("RGBA")
	rav2 = rav2.convert("RGBA")
	base.paste(rav1, (50, 30), rav1)
	base.paste(rav2, (0, 9), rav2)
	base.paste(rav1, (220, 40), rav1)
	base.paste(rav2, (305, 12), rav2)
	base.save("images/yedit.png")
	await ctx.send(f"{ctx.author.name} yeeted {member.name} into oblivion because {reason}")
	await ctx.send(file=discord.File('images/yedit.png'))
	if member.name == "SlaveBot":
		await ctx.channel.trigger_typing()
		await asyncio.sleep(1)
		await ctx.send("AAAAAAAAAᴬᴬᴬᴬᴬᴬᴬᴬᴬᴬᴬᴬᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃ")

@bot.command(aliases=['wiki'])
@commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
async def wikisearch(ctx, *, term: str = None):
	wikipedia.set_lang("en")
	if term is None:
		await ctx.send("Searching for a random term...")
		randm = wikipedia.random(1)
		p = wikipedia.page(randm, auto_suggest=False)
		#		 for i in p.sections:
		#			 if p.section(i) is not None:
		#				 await ctx.send(p.section(i))
		results = wikipedia.summary(randm, sentences=10, auto_suggest=False)
		e = discord.Embed(title=randm,
						  url=p.url,
						  description=results,
						  timestamp=datetime.utcnow(),
						  colour=discord.Colour(0xff4500))
		e.set_footer(icon_url=ctx.author.avatar_url,
					 text=f"Requested by: {ctx.author}")
		await ctx.send(embed=e)
	elif term.lower() == "anime":
		await ctx.send("Ew no")
	else:
		p = wikipedia.page(term, auto_suggest=False)
		results = wikipedia.summary(term, sentences=10, auto_suggest=False)
		if results is None:
			await ctx.reply("Couldn't find that term, try something else",
							mention_author=False)
		else:
			e = discord.Embed(title=str(term).title(),
							  url=p.url,
							  description=results,
							  timestamp=datetime.utcnow(),
							  colour=discord.Colour(0xff4500))
			e.set_footer(icon_url=ctx.author.avatar_url,
						 text=f"Requested by: {ctx.author}")
			await ctx.send(embed=e)

@bot.command()
async def meme(ctx):
	complete_url = "https://api.imgflip.com/get_memes"
	response = requests.get(complete_url)
	x = response.json()['data']['memes']
	await ctx.send(random.choice(x))

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def weather(ctx, *, city=None):
	if not city:
		await ctx.send("Temperature: 0K \nHumidity: 101% \nDescription: Dry")
		await ctx.send("That doesn't sound right? Oh maybe that's because you DIDN'T ENTER A CITY")
		return
	api_key = os.environ['WEATHER_KEY']
	base_url = "https://api.openweathermap.org/data/2.5/weather?"
	complete_url = base_url + "appid=" + api_key + "&q=" + city
	response = requests.get(complete_url)
	x = response.json()
	if x["cod"] != "404":
		y = x["main"]
		current_temperature = y["temp"]
		current_humidity = y["humidity"]
		z = x["weather"]
		weather_description = z[0]["description"]
		ans = "Temperature: " +\
			  str(round(current_temperature-273.15,3)) + "°C"\
			  "\nHumidity: " +\
			  str(current_humidity) + "%"\
			  "\nDescription: " +\
			  str(weather_description)
		await ctx.reply(ans, mention_author=False)
	else:
		await ctx.reply("That city doesn't exist yet", mention_author=False)


#============================================Youtube=================================================================


# @bot.command(pass_context=True)
# @commands.guild_only()
# async def join(ctx):
# 	try:
# 		channel = ctx.message.author.voice.channel
# 	except AttributeError:
# 		await ctx.reply("You're not connected to a voice channel.",
# 						mention_author=False)
# 		return
# 	voice = get(bot.voice_clients, guild=ctx.guild)
# 	if voice and voice.is_connected():
# 		await voice.move_to(channel)
# 	else:
# 		voice = await channel.connect()
# 	await voice.disconnect()
# 	if voice and voice.is_connected():
# 		await voice.move_to(channel)
# 	else:
# 		voice = await channel.connect()
# 	await ctx.reply(f"Joined {channel}", mention_author=False)


# @bot.command(pass_context=True)
# @commands.guild_only()
# async def play(ctx, *, url: str = None):
# 	song_there = os.path.isfile("ssong.mp3")
# 	try:
# 		if song_there:
# 			os.remove("song.mp3")
# 	except PermissionError:
# 		await ctx.send(
# 			"Wait for the current playing music end or use the 'stop' command")
# 		return
# 	await ctx.send("Getting everything ready, playing audio soon")
# 	print("Someone wants to play music let me get that ready for them...")

# 	voice = get(bot.voice_clients, guild=ctx.guild)
# 	if voice is None:
# 		await ctx.reply("I'm not in a voice channel.", mention_author=False)
# 	else:
# 		ydl_opts = {
# 			'format':
# 			'bestaudio/best',
# 			'postprocessors': [{
# 				'key': 'FFmpegExtractAudio',
# 				'preferredcodec': 'mp3',
# 				'preferredquality': '192',
# 			}],
# 		}
# 		if "https://" not in url:
# 			await ctx.send(f"Searching YouTube for {url}...")
# 			query_string = urllib.parse.urlencode({'search_query': url})
# 			htm_content = urllib.request.urlopen(
# 				'http://www.youtube.com/results?' + query_string)
# 			search_results = re.findall(r'/watch\?v=(.{11})',
# 										htm_content.read().decode())
# 			url = 'http://www.youtube.com/watch?v=' + search_results[0]
# 			await ctx.reply(url, mention_author=False)
# 		else:
# 			useful = url.split()
# 			url = useful[0]
# 		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 			ydl.download([url])
# 		for file in os.listdir("./"):
# 			if file.endswith(".mp3"):
# 				os.rename(file, 'song.mp3')
# 		voice.play(discord.FFmpegPCMAudio("song/song.mp3"))
# 		voice.volume = 100
# 		voice.is_playing()


# @bot.command(pass_context=True)
# @commands.guild_only()
# async def pause(ctx):
# 	voice = get(bot.voice_clients, guild=ctx.guild)
# 	if voice and voice.is_playing():
# 		print("Music paused")
# 		voice.pause()
# 		await ctx.reply("Music paused", mention_author=False)
# 	else:
# 		print("Music not playing")
# 		await ctx.reply("Music not playing", mention_author=False)


# @bot.command(pass_context=True)
# @commands.guild_only()
# async def resume(ctx):
# 	voice = get(bot.voice_clients, guild=ctx.guild)
# 	if voice and voice.is_paused():
# 		print("Resumed music")
# 		voice.resume()
# 		await ctx.reply("Resumed music", mention_author=False)
# 	else:
# 		print("Music is not paused")
# 		await ctx.reply("Music is not paused", mention_author=False)


# @bot.command(pass_context=True)
# @commands.guild_only()
# async def stop(ctx):
# 	voice = get(bot.voice_clients, guild=ctx.guild)
# 	if voice and voice.is_playing():
# 		print("Music stopped")
# 		voice.stop()
# 		await ctx.reply("Music stopped", mention_author=False)
# 	else:
# 		print("No music playing")
# 		await ctx.reply("No music playing", mention_author=False)
##################################################################################################################

#@bot.command(name='lyrics')
#@commands.guild_only()
#async def get_lyrics(ctx, *, query: str=""):
#	if not query:
#		player = lavalink.PlayerManager.get(ctx.guild.id)
#	if not player.is_playing:
#		return await ctx.reply("I'm not currently playing anything", mention_author=False)
#	query = player.current.title

#	try:
#		async with ctx.typing():
#			results = await kclient.music.lyrics(query, limit=1)
#		results.close()
#	except ksoftapi.NoResults:
#		await ctx.reply(f'No lyrics found for `{query}`', mention_author=False)
#	else:
#		lyrics = results[0].lyrics
#		result = results[0]
#		embed = discord.Embed(title=f'{result.name} - {result.artist}', color=discord.Color(0xCCFF00), description=lyrics[:2048])
#		embed.set_thumbnail(url=result.album_art)
#		embed.set_author(name="Lyrics:")
#		lyrics = lyrics[2048:]
#		embeds = [embed]
#		while len(lyrics) > 0 and len(embeds) < 10:
#			embed = discord.Embed(color=discord.Color(0xCCFF00), description=lyrics[:2048])
#		lyrics = lyrics[len(embeds)*2048:]
#		embeds.append(embed)
#		embeds[-1].set_footer(text="Source: KSoft.Si")
#		for embed in embeds:
#			await ctx.send(embed=embed)
#	kclient.close()

#####################################################################################################################
# @bot.command(pass_context=True)
# @commands.guild_only()
# async def leave(ctx):
# 	guild = ctx.message.guild
# 	channel = guild.me.voice.channel
# 	voice = guild.voice_client
# 	await ctx.reply(f"Left {channel}", mention_author=False)
# 	await voice.disconnect()

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
		'no_warnings': True,
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
			duration.append('{} days'.format(days))
		if hours > 0:
			duration.append('{} hours'.format(hours))
		if minutes > 0:
			duration.append('{} minutes'.format(minutes))
		if seconds > 0:
			duration.append('{} seconds'.format(seconds))

		return ', '.join(duration)


class Song:
	__slots__ = ('source', 'requester')

	def __init__(self, source: YTDLSource):
		self.source = source
		self.requester = source.requester

	def create_embed(self):
		embed = (discord.Embed(title='Now playing',
							   description='```css\n{0.source.title}\n```'.format(self),
							   color=discord.Color.blurple())
				 .add_field(name='Duration', value=self.source.duration)
				 .add_field(name='Requested by', value=self.requester.mention)
				 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
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

	async def audio_player_task(self):
		while True:
			self.next.clear()

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
					return

			self.current.source.volume = self._volume
			self.voice.play(self.current.source, after=self.play_next_song)
			await self.current.source.channel.send(embed=self.current.create_embed())

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
		if not state:
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

	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		await ctx.send('An error occurred: {}'.format(str(error)))

	@commands.command(name='join', invoke_without_subcommand=True)
	async def _join(self, ctx: commands.Context):
		"""Joins a voice channel."""

		destination = ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.send(f"Joined {ctx.guild.me.voice.channel}")

	@commands.command(name='leave', aliases=['disconnect'])
	@commands.has_permissions(manage_guild=True)
	async def _leave(self, ctx: commands.Context):
		"""Clears the queue and leaves the voice channel."""

		if not ctx.voice_state.voice:
			return await ctx.send('Not connected to any voice channel.')

		await ctx.voice_state.stop()
		del self.voice_states[ctx.guild.id]
		await ctx.send(f"Left {ctx.guild.me.voice.channel}")

	@commands.command(name='volume')
	async def _volume(self, ctx: commands.Context, *, volume: int):
		"""Sets the volume of the player."""

		if not ctx.voice_state.is_playing:
			return await ctx.send('Nothing being played at the moment.')

		if 0 > volume > 100:
			return await ctx.send('Volume must be between 0 and 100')

		ctx.voice_state.volume = volume / 100
		await ctx.send('Volume of the player set to {}%'.format(volume))

	@commands.command(name='now', aliases=['current', 'playing'])
	async def _now(self, ctx: commands.Context):
		"""Displays the currently playing song."""

		await ctx.send(embed=ctx.voice_state.current.create_embed())

	@commands.command(name='pause')
	@commands.has_permissions(manage_guild=True)
	async def _pause(self, ctx: commands.Context):
		"""Pauses the currently playing song."""

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
			ctx.voice_state.voice.pause()
			await ctx.message.add_reaction('⏸️')

	@commands.command(name='resume')
	@commands.has_permissions(manage_guild=True)
	async def _resume(self, ctx: commands.Context):
		"""Resumes a currently paused song."""

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
			ctx.voice_state.voice.resume()
			await ctx.message.add_reaction('⏯')

	@commands.command(name='stop')
	@commands.has_permissions(manage_guild=True)
	async def _stop(self, ctx: commands.Context):
		"""Stops playing song and clears the queue."""

		ctx.voice_state.songs.clear()

		if ctx.voice_state.is_playing:
			ctx.voice_state.voice.stop()
			await ctx.message.add_reaction('⏹')

	@commands.command(name='skip')
	async def _skip(self, ctx: commands.Context):
		"""Vote to skip a song. The requester can automatically skip.
		3 skip votes are needed for the song to be skipped.
		"""

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

	@commands.command(name='queue')
	async def _queue(self, ctx: commands.Context, *, page: int = 1):
		"""Shows the player's queue.

		You can optionally specify the page to show. Each page contains 10 elements.
		"""

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
		"""Shuffles the queue."""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send('Empty queue.')

		ctx.voice_state.songs.shuffle()
		await ctx.message.add_reaction('🔀')

	@commands.command(name='remove')
	async def _remove(self, ctx: commands.Context, index: int):
		"""Removes a song from the queue at a given index."""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send('Empty queue.')

		ctx.voice_state.songs.remove(index - 1)
		await ctx.message.add_reaction('✅')

	@commands.command(name='loop')
	async def _loop(self, ctx: commands.Context):
		"""Loops the currently playing song.

		Invoke this command again to unloop the song.
		"""

		if not ctx.voice_state.is_playing:
			return await ctx.send('Nothing being played at the moment.')

		# Inverse boolean value to loop and unloop.
		ctx.voice_state.loop = not ctx.voice_state.loop
		await ctx.message.add_reaction('🔁')

	@commands.command(name='play')
	async def _play(self, ctx: commands.Context, *, search: str):
		"""Plays a song.

		If there are songs in the queue, this will be queued until the
		other songs finished playing.

		This command automatically searches from various sites if no URL is provided.
		A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
		"""

		if not ctx.voice_state.voice:
			await ctx.invoke(self._join)

		async with ctx.typing():
			try:
				source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
			except YTDLError as e:
				await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
			else:
				song = Song(source)

				await ctx.voice_state.songs.put(song)
				await ctx.send('Enqueued {}'.format(str(source)))

	@_join.before_invoke
	@_play.before_invoke
	async def ensure_voice_state(self, ctx: commands.Context):
		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.CommandError('You are not connected to any voice channel.')

		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				raise commands.CommandError('Bot is already in a voice channel.')

bot.add_cog(Music(bot))


#============================================Slash===================================================================


@slash.slash(name="test")
async def _test(ctx: SlashContext,
				description="This is just a test command, nothing more."):
	await ctx.send("tesst")


@slash.slash(description="Make the bot say, but this time without quoting you",
			 options=[
				 create_option(name="sentence",
							   description="Type the sentence here",
							   option_type=3,
							   required=True)
			 ])
async def say(ctx: SlashContext, sentence):
	await ctx.send(sentence)


#====================================================================================================================


@bot.event
async def on_message(message):
	global temp, gaem
	if (isinstance(message.channel, discord.DMChannel)
		and message.channel.id not in gaem) or (
			(not message.author.bot) and message.channel.id not in gaem):
		if message.guild:
			if db[str(message.guild.id)][0] == "false":
				await bot.process_commands(message)
				return
		if message.content.lower(
		) == "<@!783314693086380032> hello" or message.content.lower(
		) == "hello <@!783314693086380032>":
			if str(message.author) != "SkullBlazer#9339":
				await message.channel.send(
					f"Hey {message.author.name}! Nice to meet ya, my default prefix is `>>`"
				)
			else:
				await message.channel.send("What do you want now -_-")
		elif message.content.lower(
		) == "<@!783314693086380032> you better not die on me again" or message.content.lower(
		) == "you better not die on me again <@!783314693086380032>":
			await message.channel.send("yes sir sorry sir")
		elif "hello" == message.content.lower(
		) or "hey" == message.content.lower():
			now = datetime.utcnow()
			replies = [
				'Hello!', 'Hey there!',
				(':ballot_box_with_check: Seen at ' +
				 now.strftime("%H:%M:%S")), 'Hi!', 'Ew'
			]
			choose = random.randint(0, 4)
			await message.channel.send(replies[choose])
		elif "hemlo" == message.content.lower(
		) or 'henlo' == message.content.lower(
		) and message.guild.id in trusted:
			await message.channel.send("Hai!!")
		elif "howdy" == message.content.lower(
		) or "howdy <@!176947217913872384>" == message.content.lower():
			await message.channel.send("no")
		elif message.content.lower() == "how are you" or message.content.lower(
		) == "how are you?":
			pinata = discord.File("images/pinata.jpeg")
			replies = ['Terrible', pinata, "Suffering", "I'm good wbu", 'Doing just fine until you started talking',\
					   "I was at peace until SOMEONE decided to wake me up"]
			ans = random.choice(replies)
			if ans == pinata:
				await message.channel.send(file=pinata)
			else:
				await message.channel.send(ans)
		elif message.content.lower(
		) == "how you doin" or message.content.lower(
		) == "how you doin?":
			if message.guild:
				if message.guild.id in trusted:
					await message.channel.send(":relaxed:")
			else:
				await message.channel.send(":relaxed:")
		elif message.content.lower(
		) == "pp!release spoilerman":  # or message.content.lower() == "pp!release apoora":
			e = discord.Embed(
				title="Pokémon Caught",
				description=
				f"{message.author.mention} ~~stole~~ caught a level **69 Spoilerman:star:**."
			)
			e.set_footer(text="You have caught a Pokémon.")
			e.timestamp = datetime.utcnow()
			await message.channel.send(embed=e)
		elif message.content.lower() == "bye" or message.content.lower(
		) == "byebye":
			if message.guild:
				if message.guild.id in trusted:
					await message.channel.send("Goodnight")
			else:
				await message.channel.send("Goodnight")
		elif message.content.lower() == "bai":
			if message.guild:
				if message.guild.id in trusted:
					await message.channel.send("Goodbye sir")
			else:
				await message.channel.send("Goodbye sir")
		elif 'chup' == message.content.lower(
		) or 'shup' == message.content.lower(
		) or 'shut up' == message.content.lower():
			await message.channel.send("no u")
		elif 'shut' == message.content.lower():
			fle = discord.File('images/shut.png')
			await message.channel.send(file=fle)
		elif message.content == 'E':
			mark = discord.File("images/e.jpeg")
			await message.channel.send(file=mark)
		elif message.content.lower() == "f":
			if message.content.isupper():
				await message.channel.send("F")
			else:
				await message.channel.send("f")
		elif message.content.lower() == "no u":
			await message.channel.send("I can do this all day")
		elif str(6 * 9 + 6 + 9) == message.content:
			await message.channel.send("nice")
		elif message.content.lower() == "not you" or message.content.lower(
		) == 'not u':
			await message.channel.send("Alrighty then, imma head out")
			await bot.change_presence(status=discord.Status.invisible)
			await asyncio.sleep(20)
			# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀"),status=discord.Status.online)
			# await bot.change_presence(activity=discord.Game(name="Tank Trouble"),status=discord.Status.online)
			await bot.change_presence(activity=discord.Activity(
				type=discord.ActivityType.listening,
				name="https://youtu.be/dQw4w9WgXcQ"),
									  status=discord.Status.online)
		elif "did this bot just reply without the prefix" == message.content.lower(
		):
			await message.channel.send(file=discord.File('images/robot.jpeg'))
		elif message.content.lower() == "excuse me" or message.content.lower(
		) == "excuse me?":
			await message.channel.send("You are excused.")
		elif '420 ' in message.content:
			await message.channel.send(":fire: Blaze it :fire:")
		elif 'sorry' == message.content.lower():
			await message.channel.send("It's okay I forgive you")
		elif 'kabam' == message.content.lower(
		):
			if message.guild:
				if message.guild.id in trusted:
					rplies = [
						'Ghar pe ja', 'KABABYBABYBABYOOOOHHHHHM', 'Go to home idiot'
					]
					ans = random.randint(0, 2)
					await message.channel.send(rplies[ans])
		elif '49 ' in message.content:
			if message.guild:
				if message.guild.id in [
				767752540980248586, 783643344202760213, 781150150630440970,
				812261291632099348
				]:
					await message.channel.send(":bear:")
		elif message.content.lower(
		) == "i know":
			if message.guild:
				if message.guild.id in trusted:
					monica = discord.File("images/tenor.gif")
					await message.channel.send(file=monica)
		elif message.content.lower(
		) == "i know!":
			if message.guild:
				if message.guild.id in trusted:
					candylady = discord.File("images/index.gif")
					await message.channel.send(file=candylady)
		elif message.content.lower() == "i'm sad" or message.content.lower(
		) == "i am sad" or message.content.lower(
		) == "i'm depressed" or message.content.lower() == "i am depressed":
			await message.channel.send("nice")
		elif 'where did you go' in message.content.lower():
			await message.channel.send(
				"Where did you come from Cotton Eyed Joe")
		elif message.content.lower() == 'stonks':
			await message.channel.send(file=discord.File('images/stonks.jpg'))
		elif "why aren't pokemon spawning" in message.content.lower(
		):
			if message.guild:
				if message.guild.id in trusted:
					await message.guild.me.edit(nick="Pokecord")
					await message.channel.send("Mujhe kya pata, mai Pokecord nahi hu")
					await message.channel.trigger_typing()
					await asyncio.sleep(3)
					await message.channel.send("wait a minute")
					await asyncio.sleep(1)
					await message.guild.me.edit(nick="SlaveBot")
#		 elif 'start the spam' == message.content.lower():
#			 temp = 1
#			 while True:
#				 if temp:
#					 await message.channel.send('spam spawn pokemon spawning Pokémon')
#					 await asyncio.sleep(2)
#				 else:
#					 break
#		 elif 'end spam' == message.content.lower():
#			 temp = 0
		elif "leat" in message.content.lower(
		) and "fingies" not in message.content.lower(
		):
			if message.guild:
				if message.guild.id in trusted:
					await message.channel.send("fingies")
			else:
				await message.channel.send("fingies")
		elif message.content.lower() == "yes.":
			if message.guild:
				if message.guild.id in trusted:
					apoora = discord.File('images/apoorafull.jpeg')
					await message.channel.send(file=apoora)
		elif message.content.lower() == "troll hehe" and message.channel.guild:
			await message.delete()
			await message.guild.me.edit(nick="Real Pokecord")
			fle = discord.File('images/tom.jpg', filename="image.jpeg")
			e = discord.Embed(title = "A wild pokemon has appeared",\
							  description = f"Use `pp!release <pokemon name> to catch it`")
			e.set_image(url="attachment://image.jpeg")
			e.set_footer(text="The next pokemon will replace this one!")
			e.timestamp = datetime.utcnow()
			await message.channel.send(file=fle, embed=e)
			await asyncio.sleep(30)
			await message.guild.me.edit(nick="SlaveBot")
		elif 'thanks' == message.content.lower():
			await message.channel.send("No problemo")
		elif 'test' == message.content.lower() and str(
			message.author) == "SkullBlazer#9339":
			await message.channel.send(message.channel.id)
#	 else:
#		 if str(message.author) == "Pokétwo#8236" and temp:
#			 temp = 0
#			 await message.channel.send("<@!305341210443382785>")
	await bot.process_commands(message)

keep_alive()
bot.run(token)