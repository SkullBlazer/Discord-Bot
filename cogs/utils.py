import discord
import asyncio
from discord.ext import commands
import random
from datetime import datetime
from time import time, perf_counter
from typing import Optional
from replit import db

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.start_time = time()
		self.flag = False
		self.flag2 = True
		self.d_author = {}
		self.d_content = {}
		self.e_author = {}
		self.e_content1 = {}
		self.e_content2 = {}
		self.helpers = [827085021705535488, 752966473227698246, 549239308104499212, 545160834918121497, 481105381159075861, 805840189074440202, 672488766891622430, 766252351060312074, 812228206358560768, 783301818980630588, 348257666193293314, 755987916311756882, 785348314019266560]

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.guild.id == 785230154258448415:
			c = self.bot.get_channel(853643406329118740)
			try:
				await c.send(message.content)
			except discord.errors.HTTPException:
				try:
					await c.send(message.attachments[0].proxy_url)
				except:
					await c.send(message.embeds[0].to_dict())
		if not (message.author.bot):
			self.d_author[message.channel.id] = message.author
			self.d_content[message.channel.id] = message.content
			if not self.d_content[message.channel.id]:
				self.d_content[message.channel.id] = message.attachments[0].proxy_url
				self.d_author[message.channel.id] = message.author
				self.flag = True
			else:
				self.flag = False
			await asyncio.sleep(60)
			try:
				del self.d_author[message.channel.id]
				del self.d_content[message.channel.id]
			except KeyError:
				self.d_author = {}
				self.d_content = {}
		elif len(message.embeds):
			self.d_author[message.channel.id] = message.author
			self.d_content[message.channel.id] = message.embeds[0].to_dict()
			self.flag = True
			self.flag2 = False


	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
		if not (message_before.author.bot):
			self.e_author[message_before.channel.id] = message_before.author
			self.e_content1[message_before.channel.id] = message_before.content
			self.e_content2[message_after.channel.id] = message_after.content
			await asyncio.sleep(60)
			try:
				del self.e_author[message_before.channel.id]
				del self.e_content1[message_before.channel.id]
				del self.e_content2[message_after.channel.id]
			except KeyError:
				self.e_author = {}
				self.e_content1 = {}
				self.e_content2 = {}
	
	@commands.command(aliases=['h'])
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def help(self, ctx, page: str = None):
		if ctx.guild:
			p = db[str(ctx.guild.id)][1]
		else:
			p = ">>"
		if page is None or page.lower() in ("1", "2", "3", "4", "5", "6", "7", "8",
											"action", "actions", "utilities",
											"utils", "fun", "games", "currency",
											"stonks", "music", "songs"):
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
		**Music**\n \
			`{p}join` \n > Join our cult. Jk, makes the bot join your voice channel ~~to spy on your conversations~~\n \
			`{p}play <song name>` \n > Play dem beats.\n \
			`{p}pause` \n > Pause the music to hear your friend's ranting\n \
			`{p}resume` \n > Resume the music because their ranting's too boring\n \
			`{p}stop` \n > Stop the music ~~Get some help~~\n \
			`{p}lyrics <song name>` \n > See the lyrics to a song and realize you've been singing nonsense this whole time\n \
			`{p}leave` \n > Make the bot leave the channel ~~because you found out that the bot records conversations~~",
			f"**Side note: Commands in `<brackets>` are required, commands in `[brackets]` are optional,\
		and `x|y` signifies x OR y**\n \
		*Pssst, you! Yes I'm talking to you! You can do `{p}help <command>` for more info on any command!*\n \n \
		**Music** (continued)\n \
			`{p}now` \n > See what garbage song is playing now so you can `{p}skip` it\n \
			`{p}queue` \n > See how long the queue is for a COVID-19 vacc- I mean, see the music queue.\n \
			`{p}volume [volume]` \n > Change the volume to 100 when that beat drops.\n \
			`{p}remove [index]` \n > Remove that one song from the playlist that no one likes.\n \
			`{p}skip` \n > When the person next to you has one Uno card left, use this. Or you can also use it to skip a song.\n \
			`{p}shuffle` \n > Use the bot's specially engineered shuffling mechanism to ensure all the bad songs are played together.\n \
			`{p}loop` \n > When the song is just too good."
			]
			#64
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
				elif page == "7" or page.lower() == "music" or page.lower(
				) == "songs":
					if page.isalpha():
						ncontents.append(contents[6])
						ncontents.append(contents[7])
					else:
						ncontents = contents
						cur_page = 7
				elif page == "8":
					ncontents = contents
					cur_page = 8
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

			while 1:
				try:
					reaction, user = await self.bot.wait_for("reaction_add",
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
						return
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
		elif page == "colourchange" or page == 'cc' or page == 'colorchange':
			e = discord.Embed(
				title=f"Help on `{p}colourchange`",
				description=
				f"Change your color.\nColors you can choose:\nBlue\nRed\nYellow\nOrange\nGreen\nPurple\nPink\nGold\nBlack\nWhite\n\
							Do `{p}colourchange` to remove your colour role.")
			e.add_field(
				name="Syntax",
				value=
				f"`{p}colourchange|cc|colorchange [Red|Blue|Green|Yellow|Orange|Gold|Purple|Pink|Black|White]`"
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
		elif page == "volume":
			e = discord.Embed(
				title=f"Help on `{p}volume`",
				description="Change the volume of the bot, from 0 to 100.")
			e.add_field(name="Syntax", value=f"`{p}volume [value]`")
		elif page == "now":
			e = discord.Embed(
				title=f"Help on `{p}now`",
				description="See the details of the song playing currently")
			e.add_field(name="Syntax", value=f"`{p}now`")
		elif page == "skip":
			e = discord.Embed(
				title=f"Help on `{p}skip`",
				description="Skip the current song. (Person who requested the song can skip instantly, others need 3 skips.)")
			e.add_field(name="Syntax", value=f"`{p}skip`")
		elif page == "queue" or page == "q":
			e = discord.Embed(
				title=f"Help on `{p}queue`",
				description="See the song queue.")
			e.add_field(name="Syntax", value=f"`{p}queue|q`")
		elif page == "shuffle":
			e = discord.Embed(
				title=f"Help on `{p}shuffle`",
				description="Shuffle the queue")
			e.add_field(name="Syntax", value=f"`{p}shuffle`")
		elif page == "remove":
			e = discord.Embed(
				title=f"Help on `{p}remove`",
				description="Remove a song from the queue")
			e.add_field(name="Syntax", value=f"`{p}remove <index>`")
		elif page == "loop":
			e = discord.Embed(
				title=f"Help on `{p}loop`",
				description="Loop/unloop the currently playing song.")
			e.add_field(name="Syntax", value=f"`{p}loop`")
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

	def is_owner():
		async def predicate(self, ctx):
			return ctx.author.id == 305341210443382785

		return commands.check(predicate)


	def is_mod():
		@commands.has_role("Moderator")
		async def predicate(self, ctx):
			role = discord.utils.find(lambda r: r.name == 'Moderator',
									ctx.guild.roles)
			if role in ctx.author.roles:
				return True
			else:
				return False

		return commands.check(predicate)


	@commands.command(name='eval')
	@commands.check_any(commands.is_owner(), is_owner())#, is_mod())
	async def _eval(self, ctx):
		await ctx.message.add_reaction("👀")


	# @self.bot.check
	# async def check_bot(self, ctx):
	#	 return not ctx.author.bot


	@commands.command(aliases=['hemlo', 'henlo', 'hi', 'hai'])
	async def hello(self, ctx):
		now = datetime.utcnow()
		replies = [
			'Hello!', 'Hey there!',
			(':ballot_box_with_check: Seen at ' + now.strftime("%H:%M:%S")), 'Hi!',
			'Ew'
		]
		choose = random.randint(0, 4)
		await ctx.send(replies[choose])


	#	 gid = ctx.guild.id
	#	 server = self.bot.get_guild(gid)
	@commands.command(aliases=['colorchange', 'cc'])
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def colourchange(self, ctx,
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
						if usr_role.name != "@everyone" or not usr_role.is_premium_subscriber() or not usr_role.is_bot_managed():
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
	# async def cc_error(self, ctx, error):
	#	 if isinstance(error, commands.CommandInvokeError):
	#		 await ctx.send("That role does not exist")


	@commands.command()
	async def invite(self, ctx):
		if str(ctx.message.author) != "SkullBlazer#9339":
			user = self.bot.get_user(305341210443382785)
			await user.send(f"{ctx.message.author} made an invite for your bot")
		e = discord.Embed(
			title="Click here for free V-bucks!",
			url=
			"https://discord.com/oauth2/authorize?client_id=783314693086380032&scope=bot&permissions=2081156351",
			description="Jk, invite me to your server",
			timestamp=datetime.utcnow(),
			color=0x00ebff)
		await ctx.reply(embed=e, mention_author=False)


	@commands.command(aliases=['ui', 'uinfo'])
	@commands.guild_only()
	async def userinfo(self, ctx, user: Optional[discord.Member], uid: int = None):
		if user is None and uid is None:
			user = ctx.author
		elif uid:
			user = await self.bot.fetch_user(uid)
		date_format = "%a, %d %b %Y %I:%M %p"
		embed = discord.Embed(color=user.colour,
							description=user.mention,
							timestamp=datetime.utcnow())
		embed.set_author(name=str(user), icon_url=user.avatar_url)
		embed.set_thumbnail(url=user.avatar_url)
		try:
			user.premium_since
		except:
			await ctx.send(
				"This user is not in this guild. Invite them here maybe, server's dead anyway"
			)
			return
		if user.premium_since:
			if user.id == 305341210443382785 or user.id == 822702422303571989:
				embed.add_field(name="Badges", value="<:SupremeLeader:885084480543522849>   <a:ServerBooster:885089057963638810>", inline=False)
			elif user.id == 324941809799397377 or user.id == 176947217913872384:
				embed.add_field(name = "Badges", value="<a:FellowBotDeveloper:885084820592549938>   <:BetaTester:885084426818687026>   <a:ServerBooster:885089057963638810>", inline=False)
			elif user.id in self.helpers:
				embed.add_field(name="Badges", value="<:BetaTester:885084426818687026>   <a:ServerBooster:885089057963638810>", inline=False)
			else:
				embed.add_field(name="Badges", value="<a:ServerBooster:885089057963638810>", inline=False)
		else:
			if user.id == 305341210443382785 or user.id == 822702422303571989:
				embed.add_field(name="Badges", value="<:SupremeLeader:885084480543522849>", inline=False)
			elif user.id == 324941809799397377 or user.id == 176947217913872384:
				embed.add_field(name = "Badges", value="<a:FellowBotDeveloper:885084820592549938>  <:BetaTester:885084426818687026>", inline=False)
			elif user.id in self.helpers:
				embed.add_field(name="Badges", value="<:BetaTester:885084426818687026>", inline=False)
			elif user.id == 783314693086380032:
				embed.add_field(name="Badges", value="<:retar:819137093258838017>", inline=False)
			elif user.bot:
				embed.add_field(name="Badges", value="<:bot:885186066812899328>", inline=False)
		embed.add_field(name='Status', value=str(user.status).title())
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


	@commands.command(aliases=['si', 'sinfo'])
	@commands.guild_only()
	async def serverinfo(self, ctx, gid:int=None):
		if gid is not None:
			guild = self.bot.get_guild(gid)
		else:
			guild = ctx.guild
		date_format = "%a, %d %b %Y %I:%M %p"
		s1 = ""
		s2 = ""
		embed = discord.Embed(title=f"{guild.name} info",
							colour=guild.owner.colour,
							timestamp=datetime.utcnow())
		embed.set_thumbnail(url=guild.icon_url)
		embed.add_field(name='Owner', value=guild.owner)
		embed.add_field(name='Region', value=str(guild.region).title())
		embed.add_field(name='Server created on',
						value=guild.created_at.strftime(date_format))
		embed.add_field(name='Humans',
						value=len(
							list(filter(lambda m: not m.bot, guild.members))))
		embed.add_field(name='Bots',
						value=len(list(filter(lambda m: m.bot,
											guild.members))))
		online = 0
		for i in guild.members:
			if str(i.status) == 'online' or str(i.status) == 'dnd' or str(i.status) == "idle":
				online += 1
		embed.add_field(name="Online", value=online)
		for i in guild.text_channels:
			s1 += f"<#{i.id}>\n"
		embed.add_field(name='Text channels', value=s1, inline=False)
		for i in guild.voice_channels:
			s2 += f"<#{i.id}>\n"
		embed.add_field(name='Voice channels', value=s2, inline=True)
		embed.add_field(name='Roles', value=(len(guild.roles) - 1))
		embed.add_field(name="Emojis", value=len(guild.emojis))
		embed.set_footer(text='ID: ' + str(guild.id))
		await ctx.send(embed=embed)


	@commands.command()
	async def encrypt(self, ctx, *, s: str):
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

			reaction, user = await self.bot.wait_for("reaction_add", check=check)
			await message.delete()
			await ctx.message.delete()


	@commands.command()
	async def decrypt(self, ctx, *, s2: str):
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

			reaction2, user2 = await self.bot.wait_for("reaction_add", check=check)
			await message2.delete()
			await ctx.message.delete()


	@commands.command(name="kick", pass_context=True)
	@commands.guild_only()
	@commands.has_permissions(manage_roles=True, kick_members=True)
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _kick(self, ctx, member: discord.Member = None, *, reason=None):
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
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.reply("I'm sorry but peasants are not allowed to kick",
							mention_author=False)


	@commands.command(name="ban", pass_context=True)
	@commands.guild_only()
	@commands.has_permissions(manage_roles=True, kick_members=True)
	@commands.cooldown(1, 20, commands.BucketType.user)
	async def _ban(self, ctx, member: discord.Member = None, *, reason=None):
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
			elif str(member) == "SkullBlazer#9339":
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

			reaction, user = await self.bot.wait_for('reaction_add', check=check2)

			await msg.delete()
			if str(reaction) == "✅":
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

			reaction, user = await self.bot.wait_for('reaction_add', check=check2)

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
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			text = "The AUDACITY of this peasant to try and ban someone"
			await ctx.reply(text, mention_author=False)


	@commands.command(name='unban')
	@commands.guild_only()
	async def _unban(self, ctx, uid: int):
		user = await self.bot.fetch_user(uid)
		await ctx.guild.unban(user)
		await ctx.reply(f"Unbanned <!@{uid}>", mention_author=False)


	# @commands.command()
	# async def ping(self, ctx):
	# 	e = discord.Embed(title="Pong!",
	# 					  description=("Latency: " +
	# 								   str(round(self.bot.latency, 3) * 1000) + "ms"),
	# 					  color=discord.Colour.teal(),
	# 					  timestamp=datetime.utcnow())
	# 	await ctx.reply(embed=e, mention_author=False)


	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def ping(self, ctx):
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
						value=f"{round(self.bot.latency * 1000)}ms",
						inline=True)
		embed.add_field(
			name="Average speed",
			value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
		embed.set_footer(
			text=f"Estimated total time elapsed: {round(sum(times))}ms")
		await msg.edit(
			content=
			f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**",
			embed=embed)


	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def nick(self, ctx, member: Optional[discord.Member], *, name: str = None):
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


	@commands.command(aliases=['changeprefix'])
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def prefix(self, ctx, prefx='>>'):
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

				reaction, user = await self.bot.wait_for('reaction_add', check=check2)

				await msg.clear_reactions()
				if str(reaction) == "✅":
					db[str(ctx.guild.id)][1] = prefx
					await ctx.reply(f"Prefix changed to {prefx}",
									mention_author=False)
			else:
				db[str(ctx.guild.id)][1] = prefx
				await ctx.reply(f"Prefix changed to {prefx}", mention_author=False)


	@commands.command(aliases=['autoresponse'])
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def stalkermode(self, ctx, flag: str = None):
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


	@commands.command()
	async def snipe(self, ctx, cid: int = None):
		if cid:
			channel = await self.bot.fetch_channel(cid)
		else:
			channel = ctx.channel
			cid = channel.id
		try:
			if not self.flag:
				em = discord.Embed(title=f"Last deleted message in {channel.name}",
									description=self.d_content[cid])
			elif not self.flag2:
				self.flag = False
				self.flag2 = True
				if ('title' in self.d_content[cid]) and ('description' in self.d_content[cid]) and ('fields' not in self.d_content[cid]):
					em = discord.Embed(title=self.d_content[cid]['title'], description=self.d_content[cid]['description'], colour=self.d_content[cid]['color'])
				elif ('title' not in self.d_content[cid]) and ('description' in self.d_content[cid]) and ('fields' not in self.d_content[cid]):
					em = discord.Embed(description=self.d_content[cid]['description'], colour=self.d_content[cid]['color'])
				elif ('title' in self.d_content[cid]) and ('description' in self.d_content[cid]) and ('fields' in self.d_content[cid]):
					em = discord.Embed(title=self.d_content[cid]['title'], description=self.d_content[cid]['description'], colour=self.d_content[cid]['color'])
					for field in self.d_content[cid]['fields']:
						em.add_field(value=field['value'], name=field['name'], inline=field['inline'])
				elif ('title' not in self.d_content[cid]) and ('description' in self.d_content[cid]) and ('fields' in self.d_content[cid]):
					em = discord.Embed(description=self.d_content[cid]['description'], colour=self.d_content[cid]['color'])
					for field in self.d_content[cid]['fields']:
						em.add_field(value=field['value'], name=field['name'], inline=field['inline'])
				elif ('title' in self.d_content[cid]) and ('description' not in self.d_content[cid]) and ('fields' in self.d_content[cid]):
					em = discord.Embed(title=self.d_content[cid]['title'], colour=self.d_content[cid]['color'])
					for field in self.d_content[cid]['fields']:
						em.add_field(value=field['value'], name=field['name'], inline=field['inline'])
				elif ('title' not in self.d_content[cid]) and ('description' not in self.d_content[cid]) and ('fields' in self.d_content[cid]):
					em = discord.Embed(colour=self.d_content[cid]['color'])
					for field in self.d_content[cid]['fields']:
						em.add_field(value=field['value'], name=field['name'], inline=field['inline'])
				if 'name' in self.d_content[cid]:
					em.set_author(name=self.d_content[cid]['name'])
				em.set_footer(text=f"Author: {self.d_author[cid]}")
				await ctx.send(embed=em)
				return
			else:
				em = discord.Embed(title=f"Last deleted image in {channel.name}")
				em.set_image(url=self.d_content[cid])
				self.flag = False
			em.set_footer(text=f"Author: {self.d_author[cid]}")
			await ctx.send(embed=em)
		except KeyError:
			await ctx.send(f"There are no recently deleted messages in <#{cid}>")


	@commands.command(aliases=['esnipe'])
	async def editsnipe(self, ctx, cid: int = None):
		if cid:
			channel = await self.bot.fetch_channel(cid)
		else:
			channel = ctx.channel
			cid = channel.id
		try:
			em = discord.Embed(
				title=f"Last edited message in {channel.name}",
				description=f"**Original message:** {self.e_content1[cid]}\n \n \
			**Edited message:** {self.e_content2[cid]}")
			em.set_footer(text=f"Author: {self.e_author[cid]}")
			await ctx.send(embed=em)
			
		except KeyError:
			await ctx.send(f"There are no recently edited messages in <#{cid}>")


	# @commands.command()
	# async def delete(self, ctx, mid:int=None):
	#	 if mid is None:
	#		 await ctx.send(f"Deleting {ctx.author.name}'s account...")
	#		 return
	#	 else:
	#		 message = await ctx.fetch_message(mid)
	#		 if message:
	#			 await message.delete()
	#			 await ctx.message.delete()


	@commands.command(aliases=['ut'])
	async def uptime(self, ctx):
		second = time() - self.start_time
		minute, second = divmod(second, 60)
		hour, minute = divmod(minute, 60)
		day, hour = divmod(hour, 24)
		dplur = "days"
		hplur = "hours"
		mplur = "minutes"
		splur = "seconds"
		if int(day) == 1:
			dplur = "day"
		if int(hour) == 1:
			hplur = "hour"
		if int(minute) == 1:
			mplur = "minute"
		if float(second) == 1.0:
			splur = "second"
		await ctx.reply(("Bot has been alive ~~since the beginning of time~~ for " +
					str(int(day)) + f" {dplur}, " + str(int(hour)) + f" {hplur}, " +
					str(int(minute)) + f" {mplur} and %.2f {splur}" % second), mention_author=False)


	@commands.command(aliases=['pn'])
	async def patchnotes(self, ctx):
		if ctx.guild:
			p = db[str(ctx.guild.id)][1]
		else:
			p = ">>"
		e = discord.Embed(title="Updates for SlaveBot v2.0.2",
						description=f"\
		**1. IMPORTANT ANNOUNCEMENT**: CHANGED PROBABILITIES OF JACKPOT!\n \
		Getting the `100,000x` multiplier has a `0.1%` chance, `10,000x` is `0.25%`, and `1,000x` is `0.5%`.\n \
		**2.** Added more music commands, `{p}volume`, `{p}now`, `{p}skip`, `{p}queue`, `{p}shuffle`, `{p}remove`, `{p}loop`\n \
		**3.** Added an **Action**, `{p}yeet`\n \
		**4.** Added a **Utility**, `{p}suggest`\n \
		**5.** Major backend changes, i.e. lots of bugs. Same deal as before, real bugs found get prizes.\n \
		**6.** Removed Herobrine.",
						colour=discord.Color.dark_grey())
		await ctx.send(embed=e)

	@commands.command()
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def suggest(self, ctx):
		msg = await ctx.send("Select 1 if you're reporting a bug, 2 if you want to suggest a command to be added, 3 for other, or 4 to cancel")
		await msg.add_reaction("1⃣")
		await msg.add_reaction("2⃣")
		await msg.add_reaction("3⃣")
		await msg.add_reaction("4⃣")
		def check(reaction, user):
			return str(reaction.emoji) in ['1⃣', '2⃣', "3⃣", "4⃣"] and user == ctx.author and msg == reaction.message
		try:
			reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
			await msg.delete()
			user = self.bot.get_user(305341210443382785)
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
				message = await self.bot.wait_for('message', check=check2, timeout=60)
				try:
					await user.send(message.content)
				except discord.errors.HTTPException:
					await user.send(message.attachments[0].proxy_url)
				await ctx.send("Message sent!")
			except asyncio.TimeoutError:
				await ctx.send("Message sent to my master that you're stupid")	
		except asyncio.TimeoutError:
			await ctx.send("Message sent to my master that you're stupid")

def setup(bot):
	bot.add_cog(Utilities(bot))