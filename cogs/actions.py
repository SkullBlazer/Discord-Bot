import discord
import asyncio
import os
from discord.ext import commands
#import openai
import random
import aiohttp
from datetime import datetime
from PIL import Image
from typing import Optional
import numpy as np
import cv2
import imageio
import scipy.ndimage
#import requests
import wikipedia
import xkcd

class Actions(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def choose(self, ctx, *, choices: str = None):
		if choices is None:
			await ctx.send(
				"I choose the first option. Oh wait, there are no options.")
		options = choices.split(",")
		await ctx.reply(random.choice(options), mention_author=False)


	@commands.command(aliases=['8ball', 'eightball'])
	async def ball8(self, ctx, *, q=None):
		apoora = discord.File('images/apoorafull.jpeg')
		if q is None:
			await ctx.send(
				"It is certain that the user of this command is an idiot.")
		else:
			trusted = [
				785230154258448415, 781150150630440970, 777217934074445834,
				785564485384405033, 783643344202760213, 767752540980248586
			]
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
					msg = await self.bot.wait_for('message', timeout=10.0)
					if "bruh" in str(
						msg.content).lower() or msg.content.startswith(
							'no') or "kekw" in str(msg.content).lower():
						await ctx.send("<:kekw:889720617316802561>")
				except asyncio.TimeoutError:
					return


	@commands.command(name="say")
	async def _say(self, ctx, member:Optional[discord.Member], *, phrase: str = None):
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


	@commands.command(aliases=['xkcd'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def xkcdcomic(self, ctx, num=None):
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
				"```Click on 📎 for the link, ❓ for explanation, or ❌ to cancel```")
			await msg.add_reaction("📎")
			await msg.add_reaction("❓")
			await msg.add_reaction("❌")

			def check(reaction, user):
				return user == ctx.author and str(reaction.emoji) in ("📎", "❓", "❌")

			try:
				reaction, user = await self.bot.wait_for('reaction_add',
													timeout=20,
													check=check)
				await msg.delete()
				if str(reaction) == "📎":
					await ctx.send(f"```{link}```")
				elif str(reaction) == "❓":
					await ctx.send(xkcd.getComic(num).getExplanation())
				else:
					return
			except asyncio.TimeoutError:
				await msg.delete()


	@commands.command()
	async def joke(self, ctx):
		user = random.randint(1,200)
		if user == 111:
			await ctx.send(ctx.author.avatar_url)
			await ctx.send("<:yeet:819137093476286496>")
			return
		
		URL = 'https://official-joke-api.appspot.com/random_joke'

		async def check_valid_status_code(request):
			if request.status == 200:
				return await request.json()
			return False

		async def get_joke():
			async with aiohttp.ClientSession() as session: 
				async with session.get(url=URL) as resp:
					# request = requests.get(URL)
					data = await check_valid_status_code(resp)
					return data

		joke = await get_joke()
		if joke == False:
			await ctx.send("Couldn't get joke from API. Try again later.")
		else:
			await ctx.send(joke['setup'] + '\n' + f"||{joke['punchline']}||")


	async def download_file(self, url, destination):
		async with aiohttp.ClientSession() as session: 
			async with session.get(url=url) as resp:
				#req = requests.get(url)
				file = open(destination, "wb")
				async for chunk in resp.content.iter_chunked(100000):
					file.write(chunk)
				file.close()


	def get_avatar(self, user, animate=True):
		if user.avatar_url and not animate:
			avatar = str(user.avatar_url).replace(".webp", ".png")
		elif user.avatar_url and animate:
			avatar = str(user.avatar_url)
		else:
			avatar = str(user.default_avatar_url)
		return avatar


	def rescale(self, image, dimensions):
		image.thumbnail(dimensions, Image.ANTIALIAS)
		return image


	def grayscale(self, rgb):
		return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


	def dodge(self, front, back):
		result = front * 255 / (256 - back)
		result[result > 255] = 255
		result[back == 255] = 255
		return result.astype('uint8')


	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def trigger(self, ctx, *, member: discord.Member = None):
		#	 await ctx.channel.trigger_typing()
		if member is None:
			member = ctx.author
		actions = self.bot.get_cog('Actions')
		await actions.download_file(actions.get_avatar(member, True), "images/trigger.png")
		avatar = Image.open("images/trigger.png")
		triggered = actions.rescale(Image.open("images/triggered.jpeg"), avatar.size)
		position = 0, avatar.getbbox()[3] - triggered.getbbox()[3]
		avatar.paste(triggered, position)
		avatar.save("images/trigger.png")
		await ctx.send(file=discord.File("images/trigger.png"))


	@commands.command(aliases=['bw', 'bnw', 'b&w'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def blackandwhite(self, ctx, user: discord.Member = None):
		if user is None:
			user = ctx.author
		actions = self.bot.get_cog('Actions')
		await actions.download_file(actions.get_avatar(user, True), "images/blackandwhite.png")
		avatar = Image.open("images/blackandwhite.png").convert("L")
		avatar.save("images/blackandwhite.png")
		await ctx.send(file=discord.File("images/blackandwhite.png"))


	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def cartoon(self, ctx, user: discord.Member = None):
		if user is None:
			user = ctx.author
		actions = self.bot.get_cog('Actions')
		await actions.download_file(actions.get_avatar(user, False), "images/cartoon.jpg")
		img = cv2.imread("images/cartoon.jpg")
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.medianBlur(gray, 5)
		edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
									cv2.THRESH_BINARY, 9, 9)
		color = cv2.bilateralFilter(img, 9, 250, 250)
		cartoon = cv2.bitwise_and(color, color, mask=edges)
		cv2.imwrite("images/cartoon.jpg", cartoon)
		await ctx.send(file=discord.File("images/cartoon.jpg"))


	@commands.command(aliases=['sketch'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def draw(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author
		actions = self.bot.get_cog('Actions')
		await actions.download_file(actions.get_avatar(user, False), "images/draw.png")
		s = imageio.imread("images/draw.png")
		g = actions.grayscale(s)
		i = 255 - g
		b = scipy.ndimage.filters.gaussian_filter(i, sigma=10)
		r = actions.dodge(b, g)
		cv2.imwrite('images/draw.png', r)
		await ctx.send(file=discord.File("images/draw.png"))


	# @commands.command()
	# @commands.cooldown(rate=1, per=5 * 60, type=commands.BucketType.user)
	# async def chat(self, ctx):
	# 	channel = await ctx.author.create_dm()
	# 	await channel.send(
	# 		"Hello! I am SlaveBot, ask me questions and I will answer them! Type `end chat` if you get annoyed, which you will."
	# 	)
	# 	openai.api_key = os.environ["OPENAI_KEY"]

	# 	def check(m):
	# 		return m.author == ctx.author and m.channel == channel

	# 	while True:
	# 		try:
	# 			question = await self.bot.wait_for('message', check=check, timeout=60.0)
	# 			if str(question.content).lower() == "end chat":
	# 				self.gaem.remove(channel.id)
	# 				await channel.send(
	# 					"Didn't take a lot to annoy you huh? Anyway, bye!")
	# 				return
	# 			# if str(question.content)[-1] != "?":
	# 			# 	await channel.send(
	# 			# 		"Either that's a stupid question or it doesn't end in a `?`. Ask again."
	# 			# 	)
	# 			# 	continue
	# 			response = openai.Completion.create(
	# 				engine="davinci",
	# 				prompt=
	# 				f"SlaveBot is a chatbot that reluctantly answers questions.\nYou: How many pounds are in a kilogram?\nSlaveBot: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nSlaveBot: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nSlaveBot: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nSlaveBot: I’m not sure. I’ll ask my friend Google.\nYou: {str(question.content)}\nSlaveBot:",
	# 				temperature=0.3,
	# 				max_tokens=60,
	# 				top_p=0.3,
	# 				frequency_penalty=0.5,
	# 				presence_penalty=0.0,
	# 				stop=["\n", "SlaveBot:"])
	# 			await channel.send(response.choices[0].text)
	# 		except asyncio.TimeoutError:
	# 			await channel.send("Wow the awkward silence is killing me, bye.")
	# 			return


	@commands.command()
	async def fight(self, ctx, user: discord.Member = None, *, weapon: str = None):
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


	@commands.command(aliases=['poll'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def quickpoll(self, ctx, *, question: str = None):
		def check(m):
			return m.author == ctx.author and m.channel == ctx.message.channel

		if question is None:
			b = await ctx.send("Ask your question:")
			try:
				question = await self.bot.wait_for('message', check=check, timeout=30.0)
				await b.delete()
				q = question.content
				if q.lower() == "cancel":
					await ctx.send("Cancelled")
					return
				if ctx.guild:
					await question.delete()
			except asyncio.TimeoutError:
				await ctx.send("Poll closed due to inactivity.")
				return
		else:
			q = question
		if ctx.guild:
			await ctx.message.delete()
		a = await ctx.send("Add options (max. 10) separated by `|`")
		try:
			msg = await self.bot.wait_for('message', check=check, timeout=90.0)
			if msg.content.lower() == "cancel":
				await ctx.send("Cancelled")
				return
			options = str(msg.content).split("|")
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
		embed.set_author(name=q,
						icon_url=ctx.author.avatar_url)
		embed.set_footer(text=f"Asked by {ctx.author}")
		react_message = await ctx.send(embed=embed)
		for reaction in reactions[:len(options)]:
			await react_message.add_reaction(reaction)
		await react_message.edit(embed=embed)


	@commands.command(aliases=['patpat'])
	async def pat(self, ctx,
				members: commands.Greedy[discord.Member] = None,
				*,
				reason='for doing an excellent job'):
		if members is None:
			patted = "<@305341210443382785>"
		elif ctx.author in members:
			await ctx.send(
				"Patting yourself is banned in 130 countries. Ask someone else to do it"
			)
			return
		else:
			patted = ", ".join(x.mention for x in members)
		await ctx.send('{} just got patted {}'.format(patted, reason), allowed_mentions=discord.AllowedMentions.none())
		if "<@783314693086380032>" in patted:
			await asyncio.sleep(1)
			await ctx.send("yay")
		if patted == 'SkullBlazer' or patted == "<@305341210443382785>":
			await ctx.send(file=discord.File('images/patpat.jpeg'))


	@commands.command(aliases=['stabby', 'hauserify'])
	async def stab(self, ctx,
				members: commands.Greedy[discord.Member] = None,
				*,
				reason='for no reason'):
		if "@everyone" in reason or "@here" in reason:
			await ctx.send("Excuse me this is a mass-murder free zone.")
			return
		if members is None:
			stabbed = ctx.guild.me
		elif ctx.author in members:
			fle = discord.File('images/scarn.gif')
			await ctx.send(file=fle)
			return
		else:
			stabbed = ", ".join(x.mention for x in members)
		if stabbed == '<@767734877515939900>' or stabbed == '<@785348314019266560>':
			await ctx.send(file=discord.File('images/scary.jpeg'))
		else:
			await ctx.send('{} just got stabbed {}'.format(stabbed, reason), allowed_mentions=discord.AllowedMentions.none())
			if "<@783314693086380032>" in stabbed:
				await ctx.channel.trigger_typing()
				await asyncio.sleep(1)
				await ctx.send("owie")


	@commands.command(aliases=['vibecheck'])
	async def bonk(self, ctx,
				bonked: Optional[discord.Member],
				bonker: Optional[discord.Member],
				*,
				reason: str = 'for no reason'):
		a = self.bot.get_cog("Actions")
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
	#		 actions.download_file(ctx.guild.me.avatar_url, "bonky/bonk2.png")
	#		 av2 = Image.open("bonky/bonk2.png")
		if bonker is None:
			bonker = ctx.author
		if ctx.author == bonked:
			fle = discord.File('images/scarn.gif')
			await ctx.send(file=fle)
			return
		else:
			#		 bonked = member.name
			await a.download_file(a.get_avatar(bonked, False), "bonky/bonk2.png")
			av2 = Image.open("bonky/bonk2.png")
		base = Image.open("bonky/cheemsbonk.png")
		await a.download_file(a.get_avatar(bonker, False), "bonky/bonk1.png")
		av1 = Image.open("bonky/bonk1.png")
		#	 txt = Image.new("RGBA", base.size, (255,255,255,0))
		#	 fnt = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS_Bold.ttf", 40)
		#	 bonker = str(ctx.message.author).split('#')
		#	 d = ImageDraw.Draw(txt)
		#	 d.text((100,40), bonker[0], font=fnt, fill=(0,0,0,255))
		#	 d.text((420,215), bonked[0], font=fnt, fill=(0,0,0,255))
		#	 out = Image.alpha_composite(base, txt)
		#	 out.save('bonky/edit.png')
		rav1 = a.rescale(av1, (190, 190))
		rav2 = a.rescale(av2, (190, 190))
		rav1 = rav1.convert("RGBA")
		rav2 = rav2.convert("RGBA")
		base.paste(rav1, (149, 38), rav1)
		base.paste(rav2, (498, 182), rav2)
		base.save("bonky/edit.png")
		if bonker == ctx.author:
			await ctx.send('{} just got bonked {}'.format(bonked.mention, reason), allowed_mentions=discord.AllowedMentions.none())
		else:
			await ctx.send('{} just got bonked by {} {}'.format(
				bonked.mention, bonker.mention, reason), allowed_mentions=discord.AllowedMentions.none())
		await ctx.send(file=discord.File('bonky/edit.png'))
		if bonked.name == "SlaveBot":
			await ctx.channel.trigger_typing()
			await asyncio.sleep(1)
			await ctx.send("ouch indeed")

	@commands.command()
	async def yeet(self, ctx, member:Optional[discord.Member], *, reason:str="why not"):
		a = self.bot.get_cog("Actions")
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
		await a.download_file(a.get_avatar(member, False), "yeetus/yeet2.png")
		av2 = Image.open("yeetus/yeet2.png")
		base = Image.open("yeetus/yeet.png")
		await a.download_file(a.get_avatar(ctx.author, False), "yeetus/yeet1.png")
		av1 = Image.open("yeetus/yeet1.png")
		rav1 = a.rescale(av1, (35, 35))
		rav2 = a.rescale(av2, (35, 35))
		rav1 = rav1.convert("RGBA")
		rav2 = rav2.convert("RGBA")
		base.paste(rav1, (50, 30), rav1)
		base.paste(rav2, (0, 9), rav2)
		base.paste(rav1, (220, 40), rav1)
		base.paste(rav2, (305, 12), rav2)
		base.save("yeetus/yedit.png")
		await ctx.send(f"{ctx.author.mention} yeeted {member.mention} into oblivion because {reason}", allowed_mentions=discord.AllowedMentions.none())
		await ctx.send(file=discord.File('yeetus/yedit.png'))
		if member.name == "SlaveBot":
			await ctx.channel.trigger_typing()
			await asyncio.sleep(1)
			await ctx.send("AAAAAAAAAᴬᴬᴬᴬᴬᴬᴬᴬᴬᴬᴬᴬᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃᵃ")

	@commands.command(aliases=['wiki'])
	@commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
	async def wikisearch(self, ctx, *, term: str = None):
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

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def weather(self, ctx, *, city=None):
		if not city:
			await ctx.send("Temperature: 0K \nHumidity: 101% \nDescription: Dry")
			await ctx.send("That doesn't sound right? Oh maybe that's because you DIDN'T ENTER A CITY")
			return
		api_key = os.environ['WEATHER_KEY']
		base_url = "https://api.openweathermap.org/data/2.5/weather?"
		complete_url = base_url + "appid=" + api_key + "&q=" + city
		async with aiohttp.ClientSession() as session:
			async with session.get(url=complete_url) as resp:
				#response = requests.get(complete_url)
				x = await resp.json()
				if x["cod"] != "404":
					y = x["main"]
					current_temperature_celsius = str(round(y["temp"] - 273.15))
					current_pressure = (y["pressure"]*100/101325)
					current_humidity = y["humidity"]
					z = x["weather"]
					desc = z[0]["description"]
					embed = discord.Embed(title=f"Weather in {city.title()}",
										color=discord.Colour.random(),
										timestamp=ctx.message.created_at)
					embed.add_field(name="Description", value=f"**{desc.capitalize()}**", inline=False)
					embed.add_field(name="Temperature", value=f"**{current_temperature_celsius}°C**", inline=False)
					embed.add_field(name="Humidity", value=f"**{current_humidity}%**", inline=False)
					embed.add_field(name="Atmospheric Pressure", value=f"**{round(current_pressure,3)}atm**", inline=False)
					if "clouds" in desc:
						fle = discord.File("weather/cloudy.png", filename="image.png")
					elif desc == "haze" or desc == "smoke":
						fle = discord.File("weather/haze.png", filename="image.png")
					elif desc == "clear sky":
						fle = discord.File("weather/sunny.png", filename="image.png")
					elif desc == "light rain" or desc == "light intensity drizzle":
						fle = discord.File("weather/light_rain.png", filename="image.png")
					elif desc == "moderate rain" or desc == "heavy intensity rain":
						fle = discord.File("weather/heavy_rain.png", filename="image.png")
					elif desc == "light snow":
						fle = discord.File("weather/snowy.png", filename="image.png")
					elif desc == "mist":
						fle = discord.File("weather/mist.png", filename="image.png")
					else:
						fle = discord.File("weather/wind.png", filename="image.png")
					embed.set_thumbnail(url="attachment://image.png")
					embed.set_footer(icon_url=ctx.author.avatar_url,
										text=f"Requested by {ctx.author.name}")
					await ctx.reply(file=fle, embed=embed, mention_author=False)
				else:
					await ctx.reply("That city doesn't exist yet", mention_author=False)

def setup(bot):
	bot.add_cog(Actions(bot))