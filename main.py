import discord
import aiohttp
import asyncio
import nest_asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from time import time, perf_counter
import os
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.all()
load_dotenv()
nest_asyncio.apply()
token = os.environ['DISCORD_TOKEN']
start_time = time()

def get_prefix(bot, message):
	if not isinstance(message.channel, discord.DMChannel):
		return db[str(message.guild.id)][0]
	return "$"

bot = commands.Bot(command_prefix=get_prefix,
				   case_insensitive=True,
				   intents=intents,
				  activity=discord.Activity(type=discord.ActivityType.listening, name="$help, unless you changed the prefix"))

async def zindahaikya():
	async with aiohttp.ClientSession() as session:
		async with session.get(url="https://discord.com/api/v1") as resp:
			try:
				print(f"Rate limit {int(resp.headers['Retry-After']) / 60} minutes left")
			except:
				print("No rate limit")
loop = asyncio.get_event_loop()
loop.run_until_complete(zindahaikya())

@bot.event
async def on_ready():
	await bot.wait_until_ready()

@bot.event
async def on_command_error(ctx, error):
	if ctx.guild:
		p = db[str(ctx.guild.id)][0]
	else:
		p = "$"
	if isinstance(error, commands.CommandNotFound):
		if p in str(error):
			await ctx.send(
					f"Bro how many {p} are you gonna put in the command")
		else:
			await ctx.send("That.... that's not a valid command")
	else:
		e = discord.Embed(title=f'Error in {ctx.command.name}', description = f'[{error}]({ctx.message.jump_url})', timestamp=datetime.utcnow(), colour=discord.Color.red())
		e.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
		await ctx.reply(embed=e, mention_author=False)

@bot.event
async def on_guild_join(guild):
	user = bot.get_user(305341210443382785)
	await user.send(f"I have been added to a server {guild.name} (id: {guild.id}) and its owner is {guild.owner}")
	if str(guild.id) not in db:
		db[str(guild.id)] = ['$']

@bot.event
async def on_guild_remove(guild):
	user = bot.get_user(305341210443382785)
	await user.send(f"Aww I just got kicked from {guild.name}")
	del db[str(guild.id)]

@bot.command(hidden=True)
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

@bot.command(hidden=True)
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

@bot.command(hidden=True)
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

@bot.command(aliases=['changeprefix'])
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def prefix(ctx, prefx='$'):
	"""Change the bot's prefix"""
	if db[str(ctx.guild.id)][0] == prefx:
		await ctx.reply(f"Your prefix is already {prefx}",
						mention_author=False)
	elif prefx == '$':
		db[str(ctx.guild.id)][0] = prefx
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

			try:
				reaction, user = await bot.wait_for('reaction_add', check=check2, timeout=30)

				await msg.clear_reactions()
				if str(reaction) == "✅":
					db[str(ctx.guild.id)][0] = prefx
					await ctx.reply(f"Prefix changed to {prefx}",
									mention_author=False)
			except asyncio.TimeoutError:
				await ctx.reply("Time's up, I got bored so now the new prefix is askdmkmlksdfsfnkjlsldkfmaksdaoewqejd", mention_author=False)
		else:
			db[str(ctx.guild.id)][0] = prefx
			await ctx.reply(f"Prefix changed to {prefx}", mention_author=False)

@bot.command(aliases=['ut'])
async def uptime(ctx):
	"""See how long the bot has been alive for"""
	await ctx.reply(f"Bot was started <t:{int(start_time)}:R>", mention_author = False)

@bot.command(aliases=['inv'])
async def invite(ctx):
	"""Invite the bot to your server"""
	e = discord.Embed(title="Click here for free Discord Nitro!", url="https://discord.com/api/oauth2/authorize?client_id=943947212310851685&permissions=8&scope=bot", description = "Jk, invite me to your server", timestamp = datetime.utcnow(), colour=discord.Colour.blurple())
	await ctx.reply(embed=e, mention_author=False)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
	"""Ping the bot and see its latency"""
	msg = await ctx.send("`Pinging bot latency...`")
	times = []
	embed = discord.Embed(
		title="More information:",
		description="Pinged 4 times and calculated the average.",
		colour=discord.Colour.random(), timestamp=datetime.utcnow())

	for counter in range(3):
		start = perf_counter()
		await msg.edit(content=f"Pinging... {counter+1}/3")
		end = perf_counter()
		speed = round((end - start) * 1000)
		times.append(speed)
		embed.add_field(name=f"Ping {counter+1}:",
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

@bot.command(hidden=True)
async def daily(ctx):
	await ctx.send("Wrong bot bruh")

@bot.command(hidden=True)
@commands.check_any(commands.is_owner())
async def getdata(ctx):
	s = ""
	for i in db:
		s += (i + ": " + db[i][0] + "\n")
	await ctx.send(f"```java\n{s}```")

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
bot.run(token)