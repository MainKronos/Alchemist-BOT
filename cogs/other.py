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
		# self.printer.start()

	async def get_last_chapter(self):
		regex = re.compile(r'https:\/\/mangadex\.org\/chapter\/.*')
		ch = self.channel
		message = discord.utils.find(lambda message: regex.search(message.content), await ch.history(limit=10).flatten())
		return int(re.search(r"https:\/\/mangadex\.org\/chapter\/(\d+)", message.content).group(1))

	def chapters(self):
		res = requests.get("https://mangadex.org/api/v2/group/8588", params = {'include':'chapters'})
		return res.json()["data"]["chapters"]

	@tasks.loop(seconds=1800)
	async def printer(self):
		try:
			chapterID= await self.get_last_chapter()
			mychapters = self.chapters()
			messaggi = []
			for chapter in mychapters:
				if chapter["id"] == chapterID:
					break
				else:
					messaggi.append(f'Nuovo capitolo di {chapter["mangaTitle"]} Vol.{chapter["volume"]} Ch.{chapter["chapter"]}\n\nhttps://mangadex.org/chapter/{chapter["id"]}')

			messaggi.reverse()

			for msg in messaggi:
				print(msg)
				await self.channel.send(msg)
		except Exception as e:
			print(f"ERRORE PRINTER: {e}")
			return

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


def setup(bot):
	bot.add_cog(manga(bot))
	bot.add_cog(hospitality(bot))
	# bot.add_cog(MessageControl(bot))