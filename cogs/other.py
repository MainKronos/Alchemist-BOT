import os, sys, discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
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
		message = discord.utils.find(lambda message: regex.search(message.content), [x async for x in ch.history(limit=50)])
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


async def setup(bot):
	await bot.add_cog(manga(bot))
	# bot.add_cog(Reazioni(bot))
	# bot.add_cog(Moderazione(bot))
	# bot.add_cog(MessageControl(bot))
	# bot.add_cog(RandomKill(bot))
