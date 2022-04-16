import nest_asyncio
import discord
import asyncio
#from async_timeout import timeout
#import youtube_dl
import os
##import sys
##import subprocess
from dotenv import load_dotenv
from discord.ext import commands
##subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'discord-py-slash-command'])
#from discord_slash import SlashCommand	
#from discord_slash.utils.manage_commands import create_option
#import openai
import random
##import re
from datetime import datetime
#from time import time, perf_counter
##from discord.utils import get
#from PIL import Image
#from typing import Optional
##import json
#import math
#import numpy as np
#import cv2
#import imageio
#import scipy.ndimage
##import urllib.parse, urllib.request
#import requests
import aiohttp
#import itertools
#import functools
#import wikipedia
#import ksoftapi
#import lavalink
#import pycountry
#import xkcd
#import pypokedex
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
		return db[str(message.guild.id)][1]
	return ">>"


bot = commands.Bot(command_prefix=get_prefix,
				   case_insensitive=True,
				   intents=intents,
				  activity=discord.Game(name="Offline college 😕"))
bot.remove_command('help')

async def zindahaikya():
	async with aiohttp.ClientSession() as session:
		async with session.get(url="https://discord.com/api/v1") as resp:
			try:
				print(f"Rate limit {int(resp.headers['Retry-After']) / 60} minutes left")
			except:
				print("No rate limit")
loop = asyncio.get_event_loop()
loop.run_until_complete(zindahaikya())
# r = requests.head(url="https://discord.com/api/v1")
# try:
# 	print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
# except:
# 	print("No rate limit")
#kclient = ksoftapi.Client('')
count = 7
temp = 0
players = {}
queues = {}
gaem = []
trusted = [
	785230154258448415, 781150150630440970, 777217934074445834,
	785564485384405033, 783643344202760213, 767752540980248586,
	786275986857525248
]

@bot.event
async def on_ready():
	# async with aiohttp.ClientSession() as session: 
	# 	async with session.get(url=url) as resp:
	# 		try:
	# 			print(f"Rate limit {int(resp.headers['Retry-After']) / 60} minutes left")
	# 		except:
	# 			print("No rate limit")
	# try:
	# 	with open("datafiles/data.txt") as json_file:
	# 		credits = json.load(json_file)
	# except FileNotFoundError:
	# 	print("Could not load file")
	# 	credits = {}
	await bot.wait_until_ready()
	# await bot.change_presence(activity=discord.Activity(
	# 	type=discord.ActivityType.watching, name="Avadhoot's birthday"))
	# await bot.change_presence(activity=discord.Game(name="Offline college? Online college?"))
	# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="my master panik about exams"))
	# await bot.change_presence(status=discord.Status.dnd)
	# await bot.change_presence(activity=discord.Streaming(name="the exam answers", url="https://youtu.be/dQw4w9WgXcQ"))
	# cur_date = datetime.utcnow()
	# if (cur_date >= datetime(2021, 9, 10, 5, 30, 0) and (once == 0)):
	# 	channel = bot.get_channel(828343472120922176)
	# 	await channel.send("@everyone your Nitro is about to end!")
	# 	once += 1


# @bot.event
# async def on_member_remove(member):
# 	channel = bot.get_channel(781150150630440973)
# 	await channel.send(f"{member} couldn't handle this server")


@bot.event
async def on_guild_join(guild):
	channel = guild.text_channels[0]
	#link = await channel.create_invite()
	user = bot.get_user(305341210443382785)
	await user.send(f"I have been added to a server {guild.name} (id: {guild.id}) and its owner is {guild.owner}")
	#await user.send(link)
	# with open('datafiles/prefixes.json') as fle:
		# prefixes = json.load(fle)
	if str(guild.id) not in db:
		db[str(guild.id)] = ['false', '>>', {}]
	# with open('datafiles/prefixes.json', 'w') as fle:
	# 	json.dump(prefixes, fle, indent=4)
	# with open('datafiles/onmessage.json', 'w') as fle:
	# 	json.dump(ar, fle, indent=4)
	i = 0
	while i < len(guild.text_channels):
		try:
			channel = guild.text_channels[i]
			if isinstance(channel, discord.abc.PrivateChannel):
				i += 1
				continue
			await channel.send(f"Hi! I'm SlaveBot, a bot made by SkullBlazer#9339. My prefix is `{db[str(guild.id)][1]}`, but you can customize it using `{db[str(guild.id)][1]}prefix newPrefix`.\n Do `{db[str(guild.id)][1]}help` to get a list of all commands.")
			break
		except:
			i += 1
		# await guild.create_role(name="Moderator", colour=discord.Colour(0x7289da), permissions=discord.Permissions.all())
	msg = await channel.send("Do you want me to add colour roles to be able to use the `>>colourchange` command?")
	emojis = ["✅", "❎"]
	await msg.add_reaction(emojis[0])
	await msg.add_reaction(emojis[1])

	def check2(reaction, user):
		return str(
			reaction.emoji
		) in emojis and (user.guild_permissions.administrator or user == guild.owner) and (not user.bot) and reaction.message == msg

	try:
		reaction, user = await bot.wait_for('reaction_add',
													check=check2,
													timeout=60)
		if str(reaction.emoji) == "✅":
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
			await channel.send("Added colour roles, you can get them by doing `>>colourchange <Colour>`. If you want to see the list of available colours, do `>>help colourchange`")
		else:
			await channel.send("Alright, no roles added")
	except asyncio.TimeoutError:
		await channel.send("No one responded, ig I won't add them")

@bot.event
async def on_guild_remove(guild):
	user = bot.get_user(305341210443382785)
	await user.send(f"Aww I just got kicked from {guild.name}")
	del db[str(guild.id)]

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
			if rng == 76:
				await ctx.send("You do not have permissions to run this command.")
				await asyncio.sleep(1)
				await ctx.send("~~Jk it's not a valid command, but you received the secret error message!~~")
			else:
				await ctx.send("That.... that's not a valid command")
	elif isinstance(error, commands.CommandOnCooldown):
		currency = bot.get_cog('Currency')
		e = discord.Embed(title=f'Error in {ctx.command.name}', description = f'[This command is ratelimited, please try again in {currency.convert(error.retry_after)}.]({ctx.message.jump_url})', timestamp=datetime.utcnow(), colour=discord.Color.red())
		e.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
		await ctx.reply(embed=e, mention_author=False)
	elif isinstance(error, commands.CheckAnyFailure):
		await ctx.send("That... that's not a valid command")
		return
	else:
		e = discord.Embed(title=f'Error in {ctx.command.name}', description = f'[{error}]({ctx.message.jump_url})', timestamp=datetime.utcnow(), colour=discord.Color.red())
		e.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
		await ctx.reply(embed=e, mention_author=False)

@bot.command()
@commands.check_any(commands.is_owner())
async def load(ctx, extension=None):
	if extension is None:
		await ctx.send("Missing cog extension, forcing loading of default pins.")
		return
	elif extension == "main":
		bot.load_extension(extension)
		await ctx.message.add_reaction('👍')
		return

	bot.load_extension(f'cogs.{extension}')
	await ctx.message.add_reaction('👍')

@bot.command()
@commands.check_any(commands.is_owner())
async def unload(ctx, extension=None):
	if extension is None:
		await ctx.send("Missing cog extension, forcing unloading of default pins.")
		return
	elif extension == "main":
		bot.unload_extension(extension)
		await ctx.message.add_reaction('👍')
		return

	bot.unload_extension(f'cogs.{extension}')
	await ctx.message.add_reaction('👍')

@bot.command()
@commands.check_any(commands.is_owner())
async def reload(ctx, extension=None):
	if extension is None:
		await ctx.send("Missing cog extension, forcing reloading of default pins.")
		return
	elif extension == "main":
		bot.unload_extension(extension)
		bot.load_extension(extension)
		await ctx.message.add_reaction('👍')
		return

	bot.unload_extension(f'cogs.{extension}')
	bot.load_extension(f'cogs.{extension}')
	await ctx.message.add_reaction('👍')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_message(message):
	global temp, gaem
	om = bot.get_cog('Fun')
	if (isinstance(message.channel, discord.DMChannel)
		and message.channel.id not in gaem) or (
			(not message.author.bot) and message.channel.id not in gaem):
		if message.guild:
			if db[str(message.guild.id)][0] == "false":
				await bot.process_commands(message)
				return
		something = await om.cmd_running(message)
		if not something:
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
		# elif "howdy" == message.content.lower(
		# ) or "howdy <@!176947217913872384>" == message.content.lower():
		# 	await message.channel.send("no")
		elif message.content.lower() == "how are you" or message.content.lower(
		) == "how are you?" or message.content.lower() == "how r you" or message.content.lower(
		) == "how r you?" or message.content.lower() == "how r u" or message.content.lower(
		) == "how r u?":
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
				title="A Pokémon has been Caught",
				description=
				f"**Name**: Spoilerman :star:\n**Level**: 69\n**IV Percent**: 42.069%\n\nCongratulations {message.author.mention}!"
			)
			e.set_footer(text="The Pokémon has been added to your collection.")
			e.timestamp = datetime.utcnow()
			await message.channel.send(embed=e)
		elif message.content.lower() == "bye" or message.content.lower(
		) == "byebye":
			if message.guild:
				if message.guild.id in trusted:
					await message.channel.send("Goodnight")
			else:
				await message.channel.send("Goodnight")
		elif message.content.lower() == "bai" or message.content.lower() == "baibai":
			if message.guild:
				if message.guild.id in trusted:
					await message.channel.send("Goodbye sir")
		elif 'chup' == message.content.lower(
		) or 'shup' == message.content.lower(
		) or 'shut up' == message.content.lower():
			await message.channel.send("no u")
		elif 'shut' == message.content.lower():
			if message.guild:
				await message.delete()
			fle = discord.File('images/shut.png')
			await message.channel.send(file=fle)
		elif message.content == 'E':
			if message.guild:
				await message.delete()
			mark = discord.File("images/e.jpeg")
			await message.channel.send(file=mark)
		elif message.content.lower() == "f" or message.content == ":regional_indicator_f:":
			if message.content == "F":
				await message.channel.send("F")
			elif message.content == "f":
				await message.channel.send("f")
			else:
				await message.channel.send("🇫")
		elif message.content.lower() == "no u":
			await message.channel.send("I can do this all day")
		elif "69" == message.content:
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
		elif 'kabam' in message.content.lower(
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
		# elif "why aren't pokemon spawning" in message.content.lower(
		# ):
		# 	if message.guild:
		# 		if message.guild.id in trusted:
		# 			await message.guild.me.edit(nick="Pokecord")
		# 			await message.channel.send("Mujhe kya pata, mai Pokecord nahi hu")
		# 			await message.channel.trigger_typing()
		# 			await asyncio.sleep(3)
		# 			await message.channel.send("wait a minute")
		# 			await asyncio.sleep(1)
		# 			await message.guild.me.edit(nick="SlaveBot")
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
		elif message.content.lower() == "troll hehe":
			if message.guild:
				await message.delete()
				await message.guild.me.edit(nick="Real Pokecord")
			fle = discord.File('images/tom.jpeg', filename="image.jpeg")
			e = discord.Embed(title = "A wild pokemon has appeared",\
							description = f"Use `pp!release <pokemon name> to catch it`")
			e.set_image(url="attachment://image.jpeg")
			e.set_footer(text="The next pokemon will replace this one!")
			e.timestamp = datetime.utcnow()
			await message.channel.send(file=fle, embed=e)
			if message.guild:
				await asyncio.sleep(30)
				await message.guild.me.edit(nick="SlaveBot")
		elif 'thanks' == message.content.lower():
			await message.channel.send("No problemo")
		# elif 'pping' == message.content.lower():
		# 	await message.channel.send(message.author.mention)
		# 	await message.channel.send(message.author.mention, allowed_mentions=discord.AllowedMentions.none())
		elif 'test' == message.content.lower() and str(
			message.author) == "SkullBlazer#9339":
			await message.channel.send(':ballot_box_with_check: Seen at ' + datetime.now().strftime("%H:%M:%S"))
			await message.channel.send(f':ballot_box_with_check: Seen at {datetime.utcnow()}')
		# elif message.content.lower() == "ping shubhi":
		# 	for i in range(6):
		# 		await message.channel.send("<@827085021705535488>")
#	 else:
#		 if str(message.author) == "Pokétwo#8236" and temp:
#			 temp = 0
#			 await message.channel.send("<@!305341210443382785>")
	await bot.process_commands(message)

keep_alive()
bot.run(token)