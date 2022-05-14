import os, sys, discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from jobs import check
import config
import requests, random, re

class manga(commands.Cog, name="manga"): # Posta i manga usciti
	def __init__(self, bot):
		self.bot = bot
		self.channel = self.bot.get_channel(717091489557250099)
		self.printer.start()

	async def get_last_chapter(self):
		regex = re.compile(r'https:\/\/mangadex\.org\/chapter\/(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)')
		ch = self.channel
		message = discord.utils.find(lambda message: regex.search(message.content), await ch.history(limit=50).flatten())
		return regex.search(message.content).group(1)

	def chapters(self, chapterID):
		res = requests.get("https://api.mangadex.org/chapter", params = {
			"groups[]":"80efffac-a5bc-4fc1-8725-a3542dc76092",
			"limit":10,
			"order[publishAt]":"desc",
			"includes[]":"user"
		})

		mychapters = []
		for raw in res.json()["data"]:

			if raw["id"] == chapterID: break

			mychapters.append({
				"chapterID": raw["id"],
				"mangaID": [x for x in raw["relationships"] if x["type"] == "manga"][0]["id"],
				"title": None,
				"cover": None,
				"volume": raw["attributes"]["volume"] if raw["attributes"]["volume"] is not None else "",
				"chapter": raw["attributes"]["chapter"] if raw["attributes"]["chapter"] is not None else "",
				"author": [x for x in raw["relationships"] if x["type"] == "user"][0]["attributes"]["username"]
			})
		
		mychapters = self.add_info(mychapters)
		mychapters.reverse()
		return mychapters

		# [x for x in raw["relationships"] if x["type"] == "manga"][0]["attributes"]["title"]["en"]


	def add_info(self, mychapters):

		for chapter in mychapters:
			res = requests.get(f"https://api.mangadex.org/manga/{chapter['mangaID']}", params = {"includes[]":"cover_art"}).json()
			chapter["title"] = list(res["data"]["attributes"]["title"].values())[0]
			chapter["cover"] = [x for x in res["data"]["relationships"] if x["type"] == "cover_art"][0]["attributes"]["fileName"]

		return mychapters

	@tasks.loop(seconds=1800)
	async def printer(self):
		
		try:
			chapterID = await self.get_last_chapter()
			mychapters = self.chapters(chapterID)

		except Exception as e:
			print(f"Errore mangadex API: {e}")
		else:
			for chapter in mychapters:

				msg = f'Nuovo capitolo di {chapter["title"]} Vol.{chapter["volume"]} Ch.{chapter["chapter"]}\nhttps://mangadex.org/chapter/{chapter["chapterID"]}\n\n'

				embed = discord.Embed()
				embed.set_image(url=f"https://uploads.mangadex.org/covers/{chapter['mangaID']}/{chapter['cover']}")
				embed.set_footer(text=f"Capitolo gentilmente offerto da {chapter['author']}.")

				await self.channel.send(msg, embed=embed)





class hospitality(commands.Cog, name="hospitality"): # hospitality
	def __init__(self, bot):
		self.bot = bot
		self.channel = self.bot.get_channel(717089928567193690)
		# self.godmorning.start()

	def get_Bullet_Club(self):
		res = requests.get("https://mangadex.org/api/v2/group/8588")
		return res.json()["data"]

	def get_manga(self):
		page = random.randint(1, 5)
		res = requests.get(f"https://api.jikan.moe/v3/top/manga/{page}/oneshots")
		return random.choice(res.json()["top"])

	def get_embed(self, now):
		bullet = self.get_Bullet_Club()
		manga = self.get_manga()

		desc = f"""
		Buongiorno,
		oggi è **%A %d %B %Y**, ore **%H:%M**.

		Il livello attuale di produttività del **{bullet['name']}** è:
		> `{bullet['likes']}` _likes_.
		> `{bullet['follows']}` _followers_.
		> `{bullet['views']}` _visualizzazioni_.
		> `{bullet['chapters']}` _capitoli pubblicati_.
		> `{len(bullet['members'])}` _membri_.

		Il manga consigliato oggi è **{manga['title']}**:
		> Tipologia: `Oneshot`
		> Valutazione: `{manga['score']}`
		> Pubblicazione: `{manga['start_date']}`
		> Link: `{manga['url']}`

		**Che anche oggi sia una giornata produttiva!**
		"""

		desc = now.strftime(desc)

		embed = discord.Embed(
			title= "**HOSPITALITY**",
			description=desc,
			colour = 0x4169E1
		)
		embed.set_thumbnail(url=manga["image_url"])
		embed.set_footer(text=f"Messaggio gentilmente offerto da {self.bot.user.name}.")

		return embed

	@commands.command(name="hospitality", aliases=["hos"])
	@commands.check(check.is_owner)
	async def hospitality(self, context):
		"""
		Hospitality
		"""

		now = datetime.now()

		embed = self.get_embed(now)
		await context.channel.send(embed=embed)

	@tasks.loop(seconds=3600)
	async def godmorning(self):	

		now = datetime.now()

		if now.hour == 7: # Se è mattina
			embed = self.get_embed(now)
			await self.channel.send(embed=embed)


class MessageControl(commands.Cog, name="MessageControl"): # MessageControl
	def __init__(self, bot):
		self.bot = bot		

	async def getData(self, guild):
		tempo = datetime.now() - timedelta(seconds=10)

		async for entry in guild.audit_logs(action=discord.AuditLogAction.message_delete, oldest_first=False, limit=1):
			# print('{0.user} ha cancellato il messaggio di {0.target}'.format(entry))
			# return "{0.user}".format(entry)
			return entry.user

	@commands.Cog.listener()
	async def on_message_delete(self, message):

		if message.author == self.bot.user:

			user = await self.getData(message.guild)

			if user != self.bot.user:

				ctx = await self.bot.get_context(message)
				txt = f"Hai eliminato un messaggio di {self.bot.user.mention}."

				await self.bot.get_command('warn').callback(self, ctx, user, txt)
				# await message.channel.send(user)

class Moderazione(commands.Cog, name="Moderazione"):
	def __init__(self, bot):
		self.bot = bot
		self.wordList = ["."]

	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author == self.bot.user: return

		msg = message.content.lower()

		if len(msg) == 1:
			if message.channel.id in [835137512657387520, 717089928567193690]:
				await message.delete()





class Reazioni(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.REAZIONI = True

	@commands.Cog.listener()
	async def on_message(self, message):

		if self.REAZIONI:

			if message.author == self.bot.user:
				return

			if message.content == ".":

				if message.author.id == 583627239128825857:

					coltello = self.bot.get_emoji(760586805236989982)  # coltello

					await message.channel.send(coltello)




				# if rand > 70:
				# 	await message.reply("BAKA")


				# if rand > 97:
				# 	await message.delete()
			# if rand > 1:

			# 	# if message.channel.id != 717089928567193690:
			# 	# 	return
					
			# 	# USERS = ["Krónos#9268", ""]
			# 	if message.author.id == 759761676139757588:

			# 		reactions = []
			# 		# reactions.append(self.bot.get_emoji(760586805236989982)) # coltello
			# 		# reactions.append(self.bot.get_emoji(760911496178827334)) # frusta
			# 		reactions.append(self.bot.get_emoji(806558724877189130)) # No
			# 		# reactions.append(self.bot.get_emoji(806558202887536650)) # popcorn
			# 		reactions.append(self.bot.get_emoji(812753805690535987)) # dance
			# 		# reactions.append("🔥")
			# 		# reactions.append("‼️")
			# 		# reactions.append("🖤")

			# 		for reac in reactions:
			# 			await message.add_reaction(reac)

			# 		print("Aggiunti emoji al messaggio di {}".format(message.author))

			

				# else:
				# 	frusta = bot.get_emoji(760911496178827334)
				# 	await message.add_reaction(frusta)
				# 	print("> Aggiunto frusta al messaggio di {}".format(message.author))

def setup(bot):
	bot.add_cog(manga(bot))
	bot.add_cog(hospitality(bot))
	# bot.add_cog(Reazioni(bot))
	# bot.add_cog(Moderazione(bot))
	# bot.add_cog(MessageControl(bot))
	# bot.add_cog(RandomKill(bot))
