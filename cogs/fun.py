import discord
import asyncio
from discord.ext import commands
import random
from datetime import datetime
from typing import Optional
import pycountry
import pypokedex
from replit import db

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.gaem = []
		self.onmessage = True

	@commands.command()
	async def game_running(self, ctx):
		return self.onmessage

	@commands.command(aliases=['rockpaperscissors'])
	async def rps(self, ctx, member: Optional[discord.Member], choice=None):
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

			reaction, user = await self.bot.wait_for('reaction_add', check=check)
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
					reaction1, user1 = await self.bot.wait_for('reaction_add',
														check=check1,
														timeout=30)
					reaction2, user2 = await self.bot.wait_for('reaction_add',
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


	@commands.command(aliases=['bs'])
	async def battleships(self, ctx):
		if ctx.channel.id in self.gaem:
			await ctx.send(
				"Another game is going on in this channel, please wait or play in a different channel"
			)
			return
		self.onmessage = False
		self.gaem.append(ctx.channel.id)
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
				message = await self.bot.wait_for('message', check=check, timeout=60.0)
				if str(message.content) == "end":
					await ctx.send("wimp")
					await ctx.send(f"My ship was at ({ship_col+1},{ship_row+1})")
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
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
							self.gaem.remove(ctx.channel.id)
							self.onmessage = True
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
								self.gaem.remove(ctx.channel.id)
								self.onmessage = True
							await ctx.send(embed=e)
							if turn == 8:
								await ctx.send(
									f"My ship was at ({ship_col+1},{ship_row+1})")
								return
					except ValueError:
						await ctx.send("Bruh you want me to attack WHERE?")
			except asyncio.TimeoutError:
				await ctx.send("You took too long to decide and your ship sank")
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
				return
		self.gaem.remove(ctx.channel.id)
		self.onmessage = True


	@commands.command(aliases=['guess', 'ng'])
	async def numguess(self, ctx):
		if ctx.channel.id in self.gaem:
			await ctx.send(
				"Another game is going on in this channel, please wait or play in a different channel"
			)
			return
		self.gaem.append(ctx.channel.id)
		self.onmessage = False
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
				message = await self.bot.wait_for('message', check=check, timeout=60.0)
				if str(message.content) == "end":
					await ctx.send("wimp")
					await ctx.send(f"Number was {num}")
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
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
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
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
							return
						else:
							db[aid][1] += 10
							e = discord.Embed(
								description="10 credits were added to your balance",
								colour=discord.Colour.green())
							e.set_author(name="Winner!",
										icon_url=ctx.author.avatar_url)
							await ctx.send(embed=e)
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
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
					return
			except asyncio.TimeoutError:
				await ctx.reply(
					"Yeah I don't have all day long, I closed the game.",
					mention_author=False)
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
				return


	@commands.command(aliases=['toss', 'ct'])
	async def cointoss(self, ctx):
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


	@commands.command()
	async def hangman(self, ctx, topic: str = None):
		if ctx.channel.id in self.gaem:
			await ctx.send(
				"Another game is going on in this channel, please wait or play in a different channel"
			)
			return
		self.gaem.append(ctx.channel.id)
		self.onmessage = False

		def check(m):
			return m.author == ctx.author and m.channel == ctx.message.channel

		specs = ':\'.,!@#$%^&*(){}[];<>?/\|`-_+=~é'
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
			self.gaem.remove(ctx.channel.id)
			self.onmessage = True
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
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
					return
			else:
				second += 1

			try:
				msg = await self.bot.wait_for('message', check=check, timeout=60.0)
				guess = str(msg.content).lower()
				if guess == 'end':
					await ctx.send("You quit :clown:")
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
					return
			except asyncio.TimeoutError:
				await ctx.send("You took too long :hourglass:")
				await guess_msg.delete()
				await word_msg.delete()
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
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
							self.gaem.remove(ctx.channel.id)
							self.onmessage = True
							return await ctx.send("You Lose :x:")
			else:
				if guess != word:
					if second > 0:
						turns = 0
						await word_msg.edit(content=f'**{word}**')
						self.gaem.remove(ctx.channel.id)
						self.onmessage = True
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
					self.gaem.remove(ctx.channel.id)
					self.onmessage = True
					return
			count -= 1


	@commands.command()
	@commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
	async def slots(self, ctx, amount: str = None):
		if ctx.channel.id in self.gaem:
			await ctx.send(
				"Another game is going on in this channel, please wait or play in a different channel"
			)
			return
		self.gaem.append(ctx.channel.id)
		self.onmessage = False
		emojis = "🍎🍊🍐🍍🍉🍇🍓🍒"
		a = random.choice(emojis)
		b = random.choice(emojis)
		c = random.choice(emojis)
		aid = str(ctx.author.id)
		if amount is None:
			await ctx.reply("You need to bet some money first",
							mention_author=False)
			self.gaem.remove(ctx.channel.id)
			self.onmessage = True
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
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
				return
			else:
				await ctx.reply("The casino only accepts credits not this garbage",
								mention_author=False)
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
				return
		amount = int(amount)
		if aid not in db:
			await ctx.reply("You don't have a bank account.", mention_author=False)
			self.gaem.remove(ctx.channel.id)
			self.onmessage = True
			return
		elif amount < 1:
			await ctx.reply(
				"If you're trying to find loopholes in my code, good job! Have a cookie! 🍪",
				mention_author=False)
			self.gaem.remove(ctx.channel.id)
			self.onmessage = True
			return
		elif amount > db[aid][1]:
			await ctx.send(
				"Sorry to be the bearer of bad news but you don't have that much money"
			)
			await ctx.reply(f"You have only ||{db[aid][1]:,}||",
							mention_author=False)
			self.gaem.remove(ctx.channel.id)
			self.onmessage = True
			return

		slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
		msg = await ctx.send(slotmachine)
		if db[str(ctx.author.id)][2]['supercharm']:
			await ctx.send("Supercharm active")
			for i in range(4):
				a = random.choice(emojis)
				b = random.choice(emojis)
				c = random.choice(emojis)
				slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
				await asyncio.sleep(1.2)
				await msg.edit(content=slotmachine)
				if i == 3:
					hax = random.randint(1, 10000)
					if hax in ([x for x in range(1,301)]):
						fruits = ["🍊", "🍐"]
						a = random.choice(fruits)
						a = b = c
					elif hax in ([x for x in range(350, 625)]):
						fruits = ["🍎", "🍍", "🍉"]
						a = random.choice(fruits)
						a = b = c
					elif hax in ([x for x in range(650, 910)]):
						fruits = ["🍇", '🍓', "🍒"]
						a = random.choice(fruits)
						a = b = c
					elif hax in ([x for x in range(1000, 2200)]):
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
					await asyncio.sleep(1.1)
					slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
					await msg.edit(content=slotmachine)
			db[str(ctx.author.id)][2]['supercharm'] -= 1
		elif db[str(ctx.author.id)][2]['charm']:
			await ctx.send("Charm active")
			for i in range(4):
				a = random.choice(emojis)
				b = random.choice(emojis)
				c = random.choice(emojis)
				slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
				await asyncio.sleep(1.2)
				await msg.edit(content=slotmachine)
				if i == 3:
					hax = random.randint(1, 10000)
					if hax in ([x for x in range(1,201)]):
						fruits = ["🍊", "🍐"]
						a = random.choice(fruits)
						a = b = c
					elif hax in ([x for x in range(250, 425)]):
						fruits = ["🍎", "🍍", "🍉"]
						a = random.choice(fruits)
						a = b = c
					elif hax in ([x for x in range(450, 610)]):
						fruits = ["🍇", '🍓', "🍒"]
						a = random.choice(fruits)
						a = b = c
					elif hax in ([x for x in range(700, 1500)]):
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
					await asyncio.sleep(1.1)
					slotmachine = f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ]"
					await msg.edit(content=slotmachine)
			db[str(ctx.author.id)][2]['charm'] -= 1
		else:
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
					await asyncio.sleep(1.1)
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
				db[aid][1] += (amount * multi) - amount
				e = discord.Embed(
					description=f"{amount*multi:,} credits added to account",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
				e.set_author(name="You win!", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=e)
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
		elif (a == b) or (a == c) or (b == c):
			await msg.edit(
				content=
				f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ] \n2 in a row, so close!"
			)
			if aid in db:
				db[aid][1] += (amount * 2) - amount
				e = discord.Embed(
					description=f"{amount*2:,} credits added to account",
					colour=discord.Colour.dark_blue(),
					timestamp=datetime.utcnow())
				e.set_author(name="You didn't lose!",
							icon_url=ctx.author.avatar_url)
				await ctx.send(embed=e)
				self.gaem.remove(ctx.channel.id)
				self.onmessage = True
		else:
			db[aid][1] -= amount
			await msg.edit(
				content=
				f"**{ctx.author.name}'s ~~gambling addiction~~ slots game** \n[ {a} {b} {c} ] \nNo match, you lost 😢"
			)
			self.gaem.remove(ctx.channel.id)
			self.onmessage = True


	@commands.command()
	async def roll(self, ctx, guess=None):
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


	# @commands.command(aliases=['rt'])
	# async def reactiontime(self, ctx):
	#	 global self.gaem
	#	 if ctx.channel.id in self.gaem:
	#		 await ctx.send("Another game is going on in this channel, please wait or play in a different channel")
	#		 return
	#	 self.gaem.append(ctx.channel.id)
	#	 emojis = ['😁','😎','💀','👌','👀','🥚','🍫','🍕','🎲','🛺','🔪','📈']
	#	 emoji = random.choice(emojis)
	#	 await ctx.send("React with the given emoji first to win!")
	#	 await asyncio.sleep(random.randint(5,10))
	#	 msg = await ctx.send(emoji)
	#	 def check(reaction, user):
	#		 return str(reaction.emoji) == emoji and user != bot.user and reaction.message == msg
	#	 try:
	#		 reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
	#		 await msg.clear_reactions()
	#		 await ctx.send(f"Congratulations {user.name} you won!")
	#		 aid = str(ctx.message.author.id)
	#		 self.gaem.remove(ctx.channel.id)
	#		 if aid in db:
	#			 db[aid][1] += 100
	#			 e = discord.Embed(title="Winner!", description="100 credits were added to your balance", colour=discord.Colour.green())
	#			 await ctx.send(embed=e)
	#			 await _save()
	#		 else:
	#			 await ctx.send("Register for an account to get credits for winning")
	#	 except asyncio.TimeoutError:
	#		 await ctx.reply("No one responded, how busy are ya idiots", mention_author=False)
	#		 self.gaem.remove(ctx.channel.id)
def setup(bot):
	bot.add_cog(Fun(bot))