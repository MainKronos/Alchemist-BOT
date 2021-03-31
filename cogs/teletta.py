import os, sys, discord
from discord.ext import commands
from jobs import check
import config
import json, random, requests


class Teletta(commands.Cog, name="teletta"):
	def __init__(self, bot):
		self.bot = bot
		self.gitFolder = f"{config.GIT_FOLDER}/teletta"
		self.localFolder = "./img/teletta"

	@commands.command(name='teletta', help="", aliases=['guido'])
	@check.is_in_guild(698597723451949076) # Bullet Club
	async def teletta(self, ctx, gif=None):
		"""
		Invia la lista dei comandi per le gif di teletta.
		"""

		imgs_name = [x.split('.')[0].lower() for x in os.listdir(self.localFolder)]

		if gif == None: # manda le gif possibili

			txtdesc = '\n'.join(imgs_name) # Decrizione subcomandi

			embed = discord.Embed(
				title="Teletta GIF",
				description=f'```{txtdesc}```',
				color=0xa8c0ff
			)
			await context.send(embed=embed)
		else:
			if gif.lower() in imgs_name:
				embed = discord.Embed(
					title=title,
					color=0xa8c0ff
				)

				url = f"{self.gitFolder}/{gif.title()+'.gif'}"
				embed.set_image(url=url)
				embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
				await ctx.channel.send(embed=embed)
			else:
				raise commands.BadArgument(f"La gif Teletta {gif} non esiste.")

	@commands.command(name='teletta', help="", aliases=['guido'])
	@check.is_in_guild(698597723451949076) # Bullet Club
	async def teletta(self, ctx):
		"""
		Manda una gif di Teletta.
		"""

		thisDir = "teletta"

		localDir = f"{self.localFolder}/{thisDir}"
		image = random.choice(os.listdir(localDir))

		title = "Teletta " + image.split('.')[0]

		embed = discord.Embed(
			title=title,
			color=0xa8c0ff
		)

		url = f"{self.gitFolder}/{thisDir}/{image}"
		embed.set_image(url=url)
		embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
		await ctx.channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Teletta(bot))