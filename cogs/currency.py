import discord
from discord.ext import commands
from datetime import datetime
from typing import Optional
from replit import db

class Currency(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def _save():
		pass

	@commands.command()
	async def save(self, ctx):
		await ctx.channel.trigger_typing()
		await ctx.send("Progress saved.")


	@commands.command(pass_context=True, aliases=['bal'])
	async def balance(self, ctx, member: Optional[discord.Member], mid: int = None):
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
			member = await self.bot.fetch_user(mid)
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


	@commands.command(pass_context=True, aliases=['reg'])
	async def register(self, ctx):
		mid = str(ctx.message.author.id)
		if mid not in db:
			db[mid] = [0, 100]
			e = discord.Embed(description="You are now registered!",
							colour=discord.Colour.gold(),
							timestamp=datetime.utcnow())
			e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
			await ctx.reply(embed=e, mention_author=False)
		else:
			await ctx.reply("You already have an account idiot",
							mention_author=False)


	@commands.command()
	@commands.check_any(commands.is_owner())
	async def edit(self, ctx, member: Optional[discord.Member], aid: str = None):
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
			mesg = await self.bot.wait_for("message", check=check)
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
			mesg = await self.bot.wait_for("message", check=check)
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

		reaction, user = await self.bot.wait_for('reaction_add', check=check2)
		await msg.delete()
		if str(reaction.emoji) == "✅":
			if amt[0] == "+":
				db[mid][1] += int(amt[1:])
				await ctx.reply("Added", mention_author=False)
			elif amt[0] == "-":
				db[mid][1] -= int(amt[1:])
				await ctx.reply("Subtracted", mention_author=False)
			elif amt[0] == "=":
				db[mid][1] = int(amt[1:])
				await ctx.reply("Changed", mention_author=False)
		else:
			await ctx.send("Well that saved me a bunch of time and processing")

	@edit.error
	async def edit_error(self, ctx, error):
		if isinstance(error, commands.CheckAnyFailure):
			await ctx.send("That.... that's not a valid command")

	@commands.command()
	@commands.check_any(commands.is_owner())
	async def getdata(self, ctx):
		s = ""
		for i in db:
			s += (str(i) + ": [" + str(db[i][0]) + "," + str(db[i][1]) + "]\n")
		await ctx.send(f"```java\n{s}```")

	@commands.command(pass_context=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def transfer(self, ctx, other: discord.Member = None, amount: str = None):
		if other is None:
			await ctx.reply(
				"Since no recipient was mentioned, all your money will go to ~~me~~ charity",
				mention_author=False)
		elif amount is None:
			await ctx.reply(
				f"Amount not provided, resorting to default value, which is all of {ctx.author.name}'s money",
				mention_author=False)
		else:
			if amount[-1].lower() == 'k':
				amount = int(amount[:-1]) * 1000
			elif amount[-1].lower() == 'm':
				amount = int(amount[:-1]) * 1000000
			elif amount[-1].lower() == 'b':
				amount = int(amount[:-1]) * 1000000000
			elif amount[-1].lower() == 't':
				amount = int(amount[:-1]) * 1000000000000
			elif amount[-1].lower() == 'q':
				amount = int(amount[:-1]) * 1000000000000000
			else:
				amount = int(amount)
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

				reaction, user = await self.bot.wait_for('reaction_add', check=check2)
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
				else:
					await ctx.send(
						f"Sorry {other.mention}, it's not your lucky day")


	@transfer.error
	async def transfer_error(self, ctx, error):
		if ctx.guild:
			p = db[str(ctx.guild.id)][1]
		else:
			p = ">>"
		if isinstance(error, commands.BadArgument):
			await ctx.reply(
				f"The `transfer` command has been updated, new format is `{p}transfer <@member> <amount>`",
				mention_author=False)


	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def rich(self, ctx, term: str = None, glbal: str = None):
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


	@commands.command(pass_context=True)
	@commands.cooldown(1, 23*60*60, commands.BucketType.user)
	async def daily(self, ctx):
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
				reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=69)
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


	def convert(self, seconds):
		seconds = seconds % (24 * 3600)
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60

		return "%d hours %02d minutes %02d seconds" % (hour, minutes, seconds)


	@daily.error
	async def daily_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			currency = self.bot.get_cog('Currency')
			msg = ('This command is ratelimited, please try again in %s' %
				currency.convert(error.retry_after))
			await ctx.reply(msg, mention_author=False)
		else:
			raise error
def setup(bot):
	bot.add_cog(Currency(bot))