import discord
from discord.ext import commands
import asyncio
from datetime import datetime, date
from typing import Optional
from replit import db

class Currency(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.shop = {
			"daily": 1000000000,
			"charm": 25000000,
			"supercharm": 15000000000
		}

	@commands.command()
	async def _save(self):
		pass

	@commands.command()
	async def save(self, ctx):
		await ctx.channel.trigger_typing()
		await ctx.send("Progress saved.")

	@commands.command(pass_context=True, aliases=['bal'])
	async def balance(self, ctx,
					  member: Optional[discord.Member],
					  mid: int = None):
		if ctx.guild:
			p = db[str(ctx.guild.id)][1]
		else:
			p = ">>"
		if mid is None:
			member = member or ctx.message.author
			aid = str(member.id)
			if member == ctx.message.author:
				if str(aid) in db:
					e = discord.Embed(
						description=f"You have {db[aid][1]:,} in the bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					if "69" in str(db[aid][1]):
						e.set_footer(text="nice")
					elif str(db[aid][1]) == "0":
						e.set_footer(text="sucks to be you")
					elif str(db[aid][1]).startswith("-"):
						e.set_footer(
							text="how the hell did you manage to do that")
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
							f"{member.mention} has {db[aid][1]:,} in their bank",
							colour=discord.Colour.green(),
							timestamp=datetime.utcnow())
						e.set_footer(text="nice")
					elif str(db[aid][1]) == "0":
						e = discord.Embed(
							description=
							f"{member.mention} has {db[aid][1]:,} in their bank",
							colour=discord.Colour.green(),
							timestamp=datetime.utcnow())
						e.set_footer(text="sucks to be them")
					elif str(db[aid][1]).startswith("-"):
						e = discord.Embed(
							description=
							f"{member.mention} has {db[aid][1]:,} in their bank",
							colour=discord.Colour.green(),
							timestamp=datetime.utcnow())
						e.set_footer(
							text="how the hell did they manage to do that")
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
			if aid == ctx.author.id:
				if "69" in str(db[aid][1]):
					e = discord.Embed(
						description=f"You have {db[aid][1]:,} in your bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_footer(text="nice")
				elif str(db[aid][1]) == "0":
					e = discord.Embed(
						description=f"You have {db[aid][1]:,} in your bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_footer(text="sucks to be you")
				elif str(db[aid][1]).startswith("-"):
					e = discord.Embed( 
						description=f"You have {db[aid][1]:,} in your bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_footer(text="how the hell did you manage to do that")
				else:
					e = discord.Embed(
						description=f"You have {db[aid][1]:,} in your bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
				e.set_author(name=f"Balance", icon_url=member.avatar_url)
				await ctx.reply(embed=e, mention_author=False)
			elif aid in db:
				if "69" in str(db[aid][1]):
					e = discord.Embed(
						description=
						f"<@!{aid}> has {db[aid][1]:,} in their bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_footer(text="nice")
				elif str(db[aid][1]) == "0":
					e = discord.Embed(
						description=
						f"<@!{aid}> has {db[aid][1]:,} in their bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_footer(text="sucks to be them")
				elif str(db[aid][1]).startswith("-"):
					e = discord.Embed(
						description=
						f"<@!{aid}> has {db[aid][1]:,} in their bank",
						colour=discord.Colour.green(),
						timestamp=datetime.utcnow())
					e.set_footer(
						text="how the hell did they manage to do that")
				else:
					e = discord.Embed(
						description=
						f"<@!{aid}> has {db[aid][1]:,} in their bank",
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
		mid = str(ctx.author.id)
		if mid not in db:
			db[mid] = [0, 100, {'daily': False, 'charm': 0, 'supercharm': 0}]
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
	async def edit(self, ctx,
				   member: Optional[discord.Member],
				   aid: str = None):
		def check(m):
			return m.author == ctx.author and m.channel == ctx.message.channel

		if aid is None:
			member = member or ctx.author
			mid = str(member.id)
			if mid not in db:
				await ctx.reply(
					"The user does not have an account, what a dweeb",
					mention_author=False)
				return
			await ctx.send("Operator and amount")
			mesg = await self.bot.wait_for("message", check=check, timeout=20)
			emojis = ["✅", "❎"]
			amt = str(mesg.content)
			amt = amt.replace(",", "")
			if amt[-1] == "s":
				if amt[0] == "+":
					e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:-1]):,} supercharms to {member.mention}'s inventory?",\
						colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "-":
					if int(amt[1:-1]) > db[mid][2]["supercharm"]:
						await ctx.send(
							f"{member.name} has only ||{db[mid][2]['supercharm']:,}|| in their inventory"
						)
						return
					e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:-1]):,} supercharms from {member.mention}'s inventory?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "=":
					e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change {member.mention}'s supercharms to {int(amt[1:-1]):,}?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				else:
					await ctx.reply("Transaction error 3913",
									mention_author=False)
					return
			elif amt[-1] == "c":
				if amt[0] == "+":
					e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:-1]):,} charms to {member.mention}'s inventory?",\
						colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "-":
					if int(amt[1:-1]) > db[mid][2]["charm"]:
						await ctx.send(
							f"{member.name} has only ||{db[mid][2]['charm']:,}|| in their inventory"
						)
						return
					e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:-1]):,} charms from {member.mention}'s inventory?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "=":
					e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change {member.mention}'s charms to {int(amt[1:-1]):,}?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				else:
					await ctx.reply("Transaction error 3913",
									mention_author=False)
					return
			else:
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
					await ctx.reply("Transaction error 3913",
									mention_author=False)
					return
		else:
			mid = str(aid)
			if mid not in db:
				await ctx.reply(
					"The user does not have an account, what a dweeb",
					mention_author=False)
				return
			await ctx.send("Operator and amount")
			mesg = await self.bot.wait_for("message", check=check, timeout=20)
			emojis = ["✅", "❎"]
			amt = str(mesg.content)
			amt = amt.replace(",", "")
			if amt[-1] == "s":
				if amt[0] == "+":
					e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:-1]):,} supercharms to <@!{aid}>'s inventory?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "-":
					if int(amt[1:]) > db[mid][2]["supercharm"]:
						await ctx.send(
							f"<@!{aid}> has only ||{db[mid][2]['supercharm']:,}|| in their inventory"
						)
						return
					e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:-1]):,} supercharms from <@!{aid}>'s inventory?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "=":
					e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change <@!{aid}>'s supercharms to {int(amt[1:-1]):,}?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				else:
					await ctx.reply("Transaction error 3913",
									mention_author=False)
					return
			elif amt[-1] == "c":
				if amt[0] == "+":
					e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:-1]):,} charms to <@!{aid}>'s inventory?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "-":
					if int(amt[1:]) > db[mid][2]["charm"]:
						await ctx.send(
							f"<@!{aid}> has only ||{db[mid][2]['charm']:,}|| in their inventory"
						)
						return
					e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:-1]):,} charms from <@!{aid}>'s inventory?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "=":
					e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change <@!{aid}>'s charms to {int(amt[1:-1]):,}?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				else:
					await ctx.reply("Transaction error 3913",
									mention_author=False)
					return
			else:
				if amt[0] == "+":
					e = discord.Embed(title="Addition confirmation", description = f"Are you sure you want to add {int(amt[1:]):,} to <@!{aid}>'s account?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "-":
					if int(amt[1:]) > db[mid][1]:
						await ctx.send(
							f"<@!{aid}> has only ||{db[mid][1]:,}|| in their account"
						)
						return
					e = discord.Embed(title="Subtraction confirmation", description = f"Are you sure you want to subtract {int(amt[1:]):,} from <@!{aid}>'s account?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				elif amt[0] == "=":
					e = discord.Embed(title="Eval confirmation", description = f"Are you sure you want to change <@!{aid}>'s balance to {int(amt[1:]):,}?",\
						 colour = discord.Colour.random(), timestamp=datetime.utcnow())
				else:
					await ctx.reply("Transaction error 3913",
									mention_author=False)
					return
		msg = await ctx.send(embed=e)
		await msg.add_reaction(emojis[0])
		await msg.add_reaction(emojis[1])

		def check2(reaction, user):
			return str(
				reaction.emoji
			) in emojis and user == ctx.author and reaction.message == msg

		reaction, user = await self.bot.wait_for('reaction_add',
												 check=check2,
												 timeout=20)
		await msg.delete()
		if str(reaction.emoji) == "✅":
			if amt[0] == "+":
				if amt[-1] == "s":
					db[mid][2]["supercharm"] += int(amt[1:-1])
				elif amt[-1] == "c":
					db[mid][2]["charm"] += int(amt[1:-1])
				else:
					db[mid][1] += int(amt[1:])
				await ctx.reply("Added", mention_author=False)
			elif amt[0] == "-":
				if amt[-1] == "s":
					db[mid][2]["supercharm"] -= int(amt[1:-1])
				elif amt[-1] == "c":
					db[mid][2]["charm"] -= int(amt[1:-1])
				else:
					db[mid][1] -= int(amt[1:])
				await ctx.reply("Subtracted", mention_author=False)
			elif amt[0] == "=":
				if amt[-1] == "s":
					db[mid][2]["supercharm"] = int(amt[1:-1])
				elif amt[-1] == "c":
					db[mid][2]["charm"] = int(amt[1:-1])
				else:
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
	async def getdata(self, ctx, _id:str=None):
		if _id:
			if _id in db:
				await ctx.send(db[_id].value)
			else:
				await ctx.send("That id does not exist")
		else:
			s = ""
			for i in db:
				s += ("db[\"" + str(i) + "\"]=[" + str(db[i][0]) + "," +
					str(db[i][1]) + "," + str(db[i][2].value) + "]\n")
			if len(s) < 2000:
				await ctx.send(f"```java\n{s}```")
			else:
				await ctx.send(f"```java\n{s[:len(s)//2]}```")
				await ctx.send(f"```java\n{s[len(s)//2:]}```")

	@commands.command()
	@commands.check_any(commands.is_owner())
	async def deldata(self, ctx, uid: str = None):
		if uid in db:
			emojis = ["✅", "❎"]
			msg = await ctx.send(f"Do you want to remove {db[uid]}?")
			await msg.add_reaction(emojis[0])
			await msg.add_reaction(emojis[1])

			def check2(reaction, user):
				return str(
					reaction.emoji
				) in emojis and user == ctx.author and reaction.message == msg

			reaction, user = await self.bot.wait_for('reaction_add',
														check=check2,
														timeout=30)
			# await msg.delete()
			if str(reaction.emoji) == "✅":
				del db[uid]
				await ctx.message.add_reaction('🗑️')
			else:
				await ctx.send(f"<@!{uid}> gets to live another day")
		else:
			await ctx.send("Error 404 not found")

	@commands.command(pass_context=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def transfer(self, ctx,
					   other: discord.Member = None,
					   amount: str = None):
		if other is None:
			await ctx.reply(
				"Since no recipient was mentioned, all your money will go to ~~me~~ charity",
				mention_author=False)

		elif amount is None:
			await ctx.reply(
				f"Amount not provided, resorting to default value, which is all of {ctx.author.name}'s money",
				mention_author=False)

		else:
			val = False
			amount = amount.replace(",", "")
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
			elif amount[-1].lower() == 'i':
				amount = int(amount[:-1]) * 1000000000000000000
			elif amount[:1] == "sc" or amount[0] == "s":
				amount = amount.split(" ")
				if len(amount) != 2:
					return await ctx.send(
						"So you're just going to transfer anything you want?")
				val = True
			elif amount[0] == "c":
				amount = amount.split(" ")
				if len(amount) != 2:
					return await ctx.send(
						"So you're just going to transfer anything you want?")
				val = True
			else:
				amount = int(amount)
			if not val:
				primary_id = str(ctx.message.author.id)
				other_id = str(other.id)
				if primary_id == other_id:
					await ctx.send("What are you even doing")

				elif amount <= 0:
					await ctx.send("Trying to fool me, eh?")

				elif primary_id not in db:
					embed = discord.Embed(
						colour=discord.Colour.red(),
						title="Error",
						description="You do not have an account",
						timestamp=datetime.utcnow())
					await ctx.send(embed=embed)
					return
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

					reaction, user = await self.bot.wait_for('reaction_add',
															 check=check2,
															 timeout=30)
					await msg.delete()

					if str(reaction) == "✅":
						e = discord.Embed(title="Success!",
										  description="Transaction complete",
										  colour=discord.Colour.gold(),
										  timestamp=datetime.utcnow())
						e.add_field(
							name="Receipt",
							value=f"Transferred {amount:,} to {other.mention}")
						await ctx.reply(embed=e, mention_author=False)
						db[primary_id][1] -= amount
						db[other_id][1] += amount
					else:
						await ctx.send(
							f"Sorry {other.mention}, it's not your lucky day", allowed_mentions=discord.AllowedMentions.none())
			else:
				primary_id = str(ctx.message.author.id)
				other_id = str(other.id)
				num = int(amount[1])
				if amount[0] == "c":
					s = "charm"
				else:
					s = "supercharm"
				if primary_id == other_id:
					await ctx.send("What are you even doing")

				elif primary_id not in db:
					embed = discord.Embed(
						colour=discord.Colour.red(),
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
				elif db[primary_id][2][s] < num:
					embed = discord.Embed(
						colour=discord.Colour.red(),
						title="Error",
						description="You cannot afford this transaction",
						timestamp=datetime.utcnow())
					await ctx.send(embed=embed)
				else:
					emojis = ["✅", "❎"]
					e = discord.Embed(title="Transfer confirmation", description = f"Are you sure you want to transfer {num:,} {s} to {other.mention}?",\
						colour = discord.Colour.random(), timestamp=datetime.utcnow())
					msg = await ctx.send(embed=e)
					await msg.add_reaction(emojis[0])
					await msg.add_reaction(emojis[1])

					def check2(reaction, user):
						return str(
							reaction.emoji
						) in emojis and user == ctx.author and reaction.message == msg

					reaction, user = await self.bot.wait_for('reaction_add',
															 check=check2,
															 timeout=30)
					await msg.delete()

					if str(reaction) == "✅":
						e = discord.Embed(title="Success!",
										  description="Transaction complete",
										  colour=discord.Colour.gold(),
										  timestamp=datetime.utcnow())
						e.add_field(
							name="Receipt",
							value=f"Transferred {num:,} to {other.mention}")
						await ctx.reply(embed=e, mention_author=False)
						db[primary_id][2][s] -= num
						db[other_id][2][s] += num
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

	@commands.command(aliases=['leaderboard', 'lb'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def rich(self, ctx, term: str = None, glbal: str = None):
		count = 0
		d = {}
		s = ""
		L = ["<:1st:836165759390449675>", "<:2nd:836165758932221992>", "<:3rd:836165759221760000> ", \
		 "<:4th:836165757641162792>", "<:5th:836165757418209292>", "<:6th:836165757595025430>", \
		 "<:7th:836165757502095471>", "<:8th:836165757309550603>", "<:9th:836165757561602048>", \
		 "<:769010theqts:836165757926113290>"]
		p = db[str(ctx.guild.id)][1]
		if not term and not glbal:
			async with ctx.typing():
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
			return

		elif term.lower() == "g" or term.lower() == "global" and not glbal:
			async with ctx.typing():
				for i in db:
					if type(db[i][1]) == int or type(db[i][1]) == float:
						d[await self.bot.fetch_user(i)] = db[i][1]
				sorted_dict = dict(
					sorted(d.items(), key=lambda item: item[1], reverse=True))
				for i in sorted_dict:
					count += 1
					if count > 10:
						break
					s += f"{L[count-1]} **{i}** - `{sorted_dict[i]:,}`\n"
				e = discord.Embed(title=f"Global leaderboard", description=s)
				e.timestamp = datetime.utcnow()
				e.set_footer(text="Oh Mars is first? Who woulda expected that")
				e.colour = discord.Colour.random()
				await ctx.send(embed=e)
			return

		elif (term.lower() == "d" or term.lower() == "daily") and not glbal:
			async with ctx.typing():
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
			return
		elif (term.lower() == "d"
			  or term.lower() == "daily") and (glbal.lower() == "g"
											   or glbal.lower() == "global"):
			async with ctx.typing():
				for i in db:
					if type(db[i][1]) == int or type(db[i][1]) == float:
						d[await self.bot.fetch_user(i)] = db[i][0]
				sorted_dict = dict(
					sorted(d.items(), key=lambda item: item[1], reverse=True))
				for i in sorted_dict:
					count += 1
					if count > 10:
						break
					s += f"{L[count-1]} **{i}** - `{sorted_dict[i]:,}`\n"
				e = discord.Embed(title=f"Global leaderboard for `{p}daily`",
								  description=s)
				e.timestamp = datetime.utcnow()
				e.colour = discord.Colour.random()
				await ctx.send(embed=e)
			return

	@commands.command(pass_context=True)
	@commands.cooldown(1, 23 * 60 * 60, commands.BucketType.user)
	async def daily(self, ctx, param:str=None):
		if param == "ready":
			await ctx.send("Duh")
			ctx.command.reset_cooldown(ctx)
			return
		aid = str(ctx.author.id)
		if aid not in db:
			embed = discord.Embed(colour=discord.Colour.red(),
								  title="Error",
								  description="You do not have an account",
								  timestamp=datetime.utcnow())
			await ctx.reply(embed=embed, mention_author=False)
			return
		if (ctx.guild.id == 828343472120922173 and ctx.message.channel.id != 828545948338749470):
			await ctx.send(f"Why {ctx.author.mention} why, just do it in <#828545948338749470>", allowed_mentions=discord.AllowedMentions.none())
			ctx.command.reset_cooldown(ctx)
			return
		else:
			try:
				db[aid][0] += 1
				s = db[aid][0]
			except KeyError:
				db[aid][0] = 0
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
			if date.today() == date(2022, 10, 12):
				e = discord.Embed(
					description=f"Added 1,000,000,000 credits to bank.",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
				e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
				e.set_footer(text=f"Daily streak of {s} days")
				await ctx.reply(embed=e, mention_author=False)
				db[aid][1] += 1000000000
				return
			if date.today() == date(2022, 12, 1):
				await ctx.send("It's my birthday today!")
				e = discord.Embed(
					description=f"Added 1,000,000,000 credits to bank.",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
				e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
				e.set_footer(text=f"Daily streak of {s} days")
				await ctx.reply(embed=e, mention_author=False)
				db[aid][1] += 1000000000
				return
			# if db[str(ctx.author.id)][0] == 70:
			# 	e1 = discord.Embed(
			# 		description=
			# 		"You will lose your 69 day streak, do you wish to continue?",
			# 		colour=discord.Colour.red(),
			# 		timestamp=datetime.utcnow())
			# 	e1.set_author(name="Confirmation",
			# 				  icon_url=ctx.author.avatar_url)
			# 	msg = await ctx.send(embed=e1)
			# 	await msg.add_reaction("✅")
			# 	await msg.add_reaction("❎")

			# 	def check(reaction, user):
			# 		return str(reaction.emoji) in [
			# 			"✅", "❎"
			# 		] and user == ctx.author and reaction.message == msg

			# 	try:
			# 		reaction, user = await self.bot.wait_for("reaction_add",
			# 												 check=check,
			# 												 timeout=69)
			# 		await msg.delete()
			# 		if str(reaction.emoji) == "✅":
			# 			pass
			# 		else:
			# 			db[str(ctx.author.id)][0] -= 1
			# 			return
			# 	except asyncio.TimeoutError:
			# 		await ctx.reply(
			# 			"Easter egg heheh \n also here's a ping for no reason")
			if db[str(ctx.author.id)][2]["daily"]:
				e = discord.Embed(
					description=f"Added {10000+(2000*s):,} credits to bank.",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
				e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
			else:
				e = discord.Embed(
					description=f"Added {1000+(250*s):,} credits to bank.",
					colour=discord.Colour.green(),
					timestamp=datetime.utcnow())
				e.set_author(name="Success!", icon_url=ctx.author.avatar_url)
			if "666" in str(s):
				if db[aid][1] <= 666666:
					e.add_field(
						name=f"You've been visited by Satan",
						value=
						"He was going to steal money from you, but seeing you don't have a lot, he's giving you 1,000,000,000! (Courtesy of the richest guy using this bot)"
					)
					db[aid][1] += 1000000000
					dct = {}
					for i in db:
						if type(db[i][1]) == int or type(db[i][1]) == float:
							dct[i] = db[i]
					sorted_dict = dict(
						sorted(dct.items(),
							   key=lambda item: item[1],
							   reverse=True))
					richest = list(sorted_dict.keys())[0]
					db[richest][1] -= 1000000000
				else:
					e.add_field(
						name=f"You've been visited by Satan",
						value="He stole 666,666 credits from your account!")
					db[aid][1] -= 666666
			if db[str(ctx.author.id)][2]["daily"]:
				db[aid][1] += 10000 + (2000 * s)
			else:
				db[aid][1] += 1000 + (250 * s)
			if s % 500 == 0 and s != 0:
				if db[str(ctx.author.id)][2]["daily"]:
					e.add_field(
						name=f"{s} days wtf",
						value=f"Damn bruh you a real one, have {s//10} supercharms")
					db[aid][2]['supercharm'] += s//10
				else:
					e.add_field(name=f"{s} days wth",
								value=f"Damn bruh you a real one, have {s//10} charms")
					db[aid][2]['charm'] += s//10
			elif s % 50 == 0 and s != 0:
				if db[str(ctx.author.id)][2]["daily"]:
					e.add_field(
						name=f"{s} daily streak bonus",
						value=f"Extra {5000*s:,} added (`daily` active)")
					db[aid][1] += 1000 * s
				else:
					e.add_field(name=f"{s} daily streak bonus",
								value=f"Extra {(10000*s//50):,} added")
					db[aid][1] += 200 * s
			elif s > 689 and s < 700:
				if db[str(ctx.author.id)][2]["daily"]:
					e.add_field(
						name=f"noice",
						value=f"Extra {int('6969'*(s-689)):,} added (`daily` active)")
					db[aid][1] += int("6969"*(s-689))
				else:
					e.add_field(name=f"noice",
								value=f"Extra {int('69'*(s-689)):,} added")
					db[aid][1] += int("69"*(s-689))
			elif "69" in str(s):
				if db[str(ctx.author.id)][2]["daily"]:
					e.add_field(
						name=f"Funny number bonus",
						value=f"Extra 69,696,969 added (`daily` active)")
					db[aid][1] += 69696969
				else:
					e.add_field(name=f"Funny number bonus",
								value=f"Extra 696,969 added")
					db[aid][1] += 696969
			elif "420" in str(s):
				if db[str(ctx.author.id)][2]["daily"]:
					e.add_field(
						name=f"||Weed|| number bonus",
						value=
						f"Extra 420,420,420,420,420 added (`daily` active)")
					db[aid][1] += 420420420420420
				else:
					e.add_field(name=f"||Weed|| number bonus",
								value=f"Extra 420,420,420,420 added")
					db[aid][1] += 420420420420
			e.set_footer(text=f"Daily streak of {s} days")
			await ctx.reply(embed=e, mention_author=False)

	def convert(self, seconds):
		seconds = seconds % (24 * 3600)
		hours = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		hplur = "hours"
		mplur = "minutes"
		splur = "seconds"
		if hours == 1:
			hplur = "hour"
		if minutes == 1:
			mplur = "minute"
		if seconds == 1:
			splur = "second"
		if hours == 0 and minutes == 0:
			return f"%02d {splur}" % seconds
		elif hours == 0 and int(seconds) == 0:
			return f"%02d {mplur}" % minutes
		elif minutes == 0 and int(seconds) == 0:
			return f"%02d {hplur}" % hours
		elif hours == 0:
			return f"%02d {mplur} %02d {splur}" % (minutes, seconds)
		elif minutes == 0:
			return f"%d {hplur} %02d {splur}" % (hours, seconds)
		elif int(seconds) == 0:
			return f"%d {hplur} %02d {mplur}" % (hours, minutes)
		else:
			return f"%d {hplur} %02d {mplur} %02d {splur}" % (hours, minutes, seconds)

	# @daily.error
	# async def daily_error(self, ctx, error):
	# 	if isinstance(error, commands.CommandOnCooldown):
	# 		currency = self.bot.get_cog('Currency')
	# 		msg = ('This command is ratelimited, please try again in %s' %
	# 			   currency.convert(error.retry_after))
	# 		await ctx.reply(msg, mention_author=False)
	# 	else:
	# 		raise error

	@commands.command()
	async def shop(self, ctx, page: str = "1"):
		if ctx.guild:
			p = db[str(ctx.guild.id)][1]
		else:
			p = ">>"
		if page == "1":
			if str(ctx.author.id) != "348257666193293314":
				e = discord.Embed(
					title=f"Balance: ||{db[str(ctx.author.id)][1]:,}||",
					colour=discord.Colour.purple(),
					timestamp=datetime.utcnow())
			else:
				e = discord.Embed(title=f"Balance: ||A lot.||",
								  colour=discord.Colour.purple(),
								  timestamp=datetime.utcnow())
			e.add_field(name="Extra daily coins (`daily`)",
						value="Cost - 1,000,000,000 coins",
						inline=True)
			e.add_field(name=f"Lucky charm (pack of 5) for `{p}slots` (`charm`)",
						value="Cost - 25,000,000 coins",
						inline=True)
			e.add_field(
				name=f"Super lucky charm (pack of 3) for `{p}slots` (`supercharm`)",
				value="Cost - 0.5% of your balance or 15,000,000,000",
				inline=True)
			e.set_footer(
				text=
				f"Use {p}buy <itemname> to buy an item, and {p}shop <itemname> to get more info on that item"
			)
		elif page in self.shop:
			e = discord.Embed(title=f"Info about {page}",
							  colour=discord.Colour.dark_blue(),
							  timestamp=datetime.utcnow())
			if page == "daily":
				e.description = f"Increases your amount gained in `{p}daily` by a substantial amount. Lasts forever."
			elif page == "supercharm":
				e.description = f"Increases your chances of winning in `{p}slots` by 2.75% for 3 fruits, and 13% for 2 fruits, for 3 games"
			elif page == "charm":
				e.description = f"Increases your chances of winning in `{p}slots` by 1.25% for 3 fruits, and 5.5% for 2 fruits, for 5 games"
			e.set_footer(text=f"Price: {self.shop[page]:,}")
		else:
			await ctx.send("That's not a valid item")
			return
		e.set_author(name="Shop", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=e)

	@commands.command()
	async def buy(self, ctx, item: str = None, amt: int = 1):
		if item is None:
			await ctx.send(
				"Congratulations! You just bought all the items from the shop! Next time specify what you want to buy"
			)
			return
		if item.startswith("<@") and item[-1] == ">" and item[2:-1].isdigit():
			await ctx.send("Wh- why would you wanna buy a person?")
			return
		if item.lower() == "stuff":
			await ctx.send(
				"When I said 'Buy stuff from shop', I didn't mean it literally"
			)
			return
		if amt > 50:
			await ctx.send(
				"Whoa there, calm down! Don't buy the entire store sheesh")
			return
		if amt < 1:
			await ctx.send("-_-")
			return
		if item.lower() == "sc" or item.lower() == "s" or item.lower() == "sp":
			item = "supercharm"
		if item.lower() == "c" or item.lower() == "cp":
			item = "charm"
		if item.lower() in self.shop:
			bal = db[str(ctx.author.id)][1]
			bal2 = bal
			price = 0
			count = 0
			# if item.lower() != "supercharm":
			# 	bal2 -= amt*self.shop[item.lower()]
			for i in range(amt):
				if price > bal2:
					break
				if item.lower() == "supercharm":
					if bal2 // 200 >= 15000000000:
						price += bal2 // 200
						bal2 -= bal2 // 200
						count += 1
					else:
						price += 15000000000
						bal2 -= 15000000000
						count += 1
				else:
					price += self.shop[item.lower()]
					count += 1
			if price > bal2:
				await ctx.send(
					f"You do not have sufficient funds to purchase that item, you can only buy {count-1} of those."
				)
				return
			if bal2 < 0:
				await ctx.send(
					"You do not have sufficient funds to purchase that item.")
				return
			if item.lower() == "daily" and db[str(ctx.author.id)][2]["daily"]:
				await ctx.send(
					"You already have purchased a daily, how much more money do you want?"
				)
				return
			else:
				e = discord.Embed(
					title="Confirmation",
					description=
					f"Are you sure you want to buy {amt} {item} pack for {price:,}?",
					timestamp=datetime.utcnow(),
					colour=discord.Colour.green())
				if item.lower() != "supercharm":
					e.set_footer(text=f"Your balance will be {bal2-price:,}")
				else:
					e.set_footer(text=f"Your balance will be {bal2:,}")
			msg = await ctx.send(embed=e)
			await msg.add_reaction("✅")
			await msg.add_reaction("❎")

			def check(reaction, user):
				return str(reaction.emoji) in [
					"✅", "❎"
				] and user == ctx.author and reaction.message == msg

			try:
				reaction, user = await self.bot.wait_for("reaction_add",
														 check=check,
														 timeout=30)
				await msg.clear_reactions()
				if str(reaction.emoji) == "✅":
					db[str(ctx.author.id)][1] -= price
					if item.lower() == "supercharm":
						db[str(ctx.author.id)][2]["supercharm"] += 3 * amt
					elif item.lower() == "daily":
						db[str(ctx.author.id)][2]["daily"] = True
					elif item.lower() == "charm":
						db[str(ctx.author.id)][2]["charm"] += 5 * amt
					await ctx.send(f"{item} purchased and in effect!")
				else:
					await ctx.send("Order cancelled")
			except asyncio.TimeoutError:
				await ctx.reply(
					"I'm cancelling the deal, I've got other customers waiting.",
					mention_author=False)
		else:
			await ctx.send("That item code doesn't exist :/")
			return

	@commands.command()
	async def sell(self, ctx, item: str = None, amt: int = 1):
		if item is None:
			await ctx.send("Sold all of your items and your money")
			return
		if item.lower() not in self.shop:
			await ctx.send(
				"Do I look like a scrap dealer that you can sell anything to")
			return
		if amt > db[str(ctx.author.id)][2][item.lower()]:
			await ctx.send(
				"Why are you trying to sell more things than you have")
			return
		if amt < 1:
			await ctx.send(
				"Either you're bug hunting or you're just plain stupid")
			return
		e = discord.Embed(
			title="Confirmation",
			description=
			f"Are you sure you want to sell {amt} {item} for {(amt * self.shop[item.lower()]//50):,}?",
			timestamp=datetime.utcnow(),
			colour=discord.Colour.dark_gold())
		msg = await ctx.send(embed=e)
		await msg.add_reaction("✅")
		await msg.add_reaction("❎")

		def check(reaction, user):
			return str(reaction.emoji) in [
				"✅", "❎"
			] and user == ctx.author and reaction.message == msg

		try:
			reaction, user = await self.bot.wait_for("reaction_add",
													 check=check,
													 timeout=30)
			await msg.clear_reactions()
			if str(reaction.emoji) == "✅":
				db[str(ctx.author.id)][2][item.lower()] -= amt
				db[str(
					ctx.author.id)][1] += amt * self.shop[item.lower()] // 50
				await ctx.send(
					f"Sold {amt} {item} for {amt * self.shop[item.lower()]//50}"
				)
			else:
				await ctx.send("Selling cancelled")
		except asyncio.TimeoutError:
			await ctx.reply(
				f"If you're too attached to your {item}s, you could just say so. Why waste my time?",
				mention_author=False)

	@commands.command(aliases=['inv'])
	async def inventory(self,
						ctx,
						member: Optional[discord.Member],
						aid: int = None):
		if ctx.guild:
			p = db[str(ctx.guild.id)][1]
		else:
			p = ">>"
		if aid:
			member = await self.bot.fetch_user(aid)
		if member:
			aid = str(member.id)
			if aid not in db:
				await ctx.send(
					"That person doesn't even have an account, let alone items"
				)
				return
			if db[aid][2]["daily"] == False and db[aid][2][
					"supercharm"] == 0 and db[aid][2]["charm"] == 0:
				await ctx.send(
					f"{member.name} has no items in their inventory.")
				return
			e = discord.Embed(colour=discord.Colour.random(),
							  timestamp=datetime.utcnow())
			if db[aid][2]["daily"]:
				e.add_field(name="Daily bonus",
							value=db[aid][2]["daily"],
							inline=True)
			if db[aid][2]["supercharm"]:
				e.add_field(name="Supercharm",
							value=db[aid][2]["supercharm"],
							inline=True)
			if db[aid][2]["charm"]:
				e.add_field(name="Charm",
							value=db[aid][2]["charm"],
							inline=True)
			e.set_author(name=f"{member.name}'s inventory",
						 icon_url=member.avatar_url)
			e.set_footer(text=f"Buy stuff from {p}shop")
			await ctx.send(embed=e)
		else:
			aid = str(ctx.author.id)
			if aid not in db:
				await ctx.send(
					"Make an account using `>>reg` first, then we'll talk about inventory"
				)
				return
			if db[aid][2]["daily"] == False and db[aid][2][
					"supercharm"] == 0 and db[aid][2]["charm"] == 0:
				await ctx.send(
					f"You have no items in your inventory. Go buy some from `{p}shop` smh"
				)
				return
			e = discord.Embed(colour=discord.Colour.random(),
							  timestamp=datetime.utcnow())
			if db[aid][2]["daily"]:
				e.add_field(name="Daily bonus",
							value=db[aid][2]["daily"],
							inline=True)
			if db[aid][2]["supercharm"]:
				e.add_field(name="Supercharm",
							value=db[aid][2]["supercharm"],
							inline=True)
			if db[aid][2]["charm"]:
				e.add_field(name="Charm",
							value=db[aid][2]["charm"],
							inline=True)
			e.set_author(name=f"{ctx.author.name}'s inventory",
						 icon_url=ctx.author.avatar_url)
			e.set_footer(text=f"Buy stuff from {p}shop")
			await ctx.send(embed=e)


def setup(bot):
	bot.add_cog(Currency(bot))
