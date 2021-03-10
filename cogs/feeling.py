import os, sys, discord
from discord.ext import commands
from jobs import check
import config
import json, random, requests


class feeling(commands.Cog, name="feeling"):
	def __init__(self, bot):
		self.bot = bot
		self.gitFolder = f"{config.GIT_FOLDER}/feeling"
		self.localFolder = "./img/feeling"

	@commands.group(name="ex", invoke_without_command=True)
	async def ex(self, context):
		"""
		Invia la lista dei subcomandi per le azioni/sentimenti.
		"""

		exCommand = self.bot.get_command("ex") # Questo comando
		subcommands = [sub for sub in self.bot.walk_commands() if sub.parent == exCommand]

		sub_list = [sub.name for sub in subcommands]
		sub_description = [sub.help for sub in subcommands]

		txtdesc = '\n'.join(f'{n} - {h}' for n, h in zip(sub_list, sub_description)) # Decrizione subcomandi

		embed = discord.Embed(
			title="FEELING",
			description=f'```{txtdesc}```',
			color=0x212121
		)
		await context.send(embed=embed)

	@ex.command(name="kiss")
	async def kiss(self, ctx, user:discord.User):
		"""
		Bacia qualcuno.
		"""
		thisDir = "kiss"

		localDir = f"{self.localFolder}/{thisDir}"
		image = random.choice(os.listdir(localDir))

		embed = discord.Embed(
			title="FEELING",
			description=f'{user.mention}, 💕❤️',
			color=0xff758c
		)

		url = f"{self.gitFolder}/{thisDir}/{image}"
		embed.set_image(url=url)
		embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
		await ctx.channel.send(embed=embed)

	@ex.command(name="pat")
	async def pat(self, ctx, user:discord.User):
		"""
		Fai pat pat a qualcuno.
		"""
		thisDir = "pat"

		localDir = f"{self.localFolder}/{thisDir}"
		image = random.choice(os.listdir(localDir))

		embed = discord.Embed(
			title="FEELING",
			description=f'{user.mention}, pat pat.',
			color=0xff758c
		)

		url = f"{self.gitFolder}/{thisDir}/{image}"
		embed.set_image(url=url)
		embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
		await ctx.channel.send(embed=embed)

	@ex.command(name="hug")
	async def hug(self, ctx, user:discord.User):
		"""
		Abbraccia qualcuno.
		"""
		thisDir = "hug"

		localDir = f"{self.localFolder}/{thisDir}"
		image = random.choice(os.listdir(localDir))

		embed = discord.Embed(
			title="FEELING",
			description=f'{user.mention}, 🫂❤️',
			color=0xff758c
		)

		url = f"{self.gitFolder}/{thisDir}/{image}"
		embed.set_image(url=url)
		embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
		await ctx.channel.send(embed=embed)

	@ex.command(name='baka')
	async def baka(self, ctx, user:discord.User):
		"""
		Invia un baka a qualcuno.
		"""
		thisDir = "baka"

		localDir = f"{self.localFolder}/{thisDir}"
		images = os.listdir(localDir)
		AnimePict = [x for x in images if x.split('.')[0]==f'{user.id}']
		if len(AnimePict) == 0: AnimePict = 'default.gif'
		else: AnimePict = AnimePict[0]

		embed = discord.Embed(
			title="FEELING",
			description=f'{user.mention}, BAKA!',
			color=0xff758c
		)

		url = f"{self.gitFolder}/{thisDir}/{AnimePict}"
		embed.set_image(url=url)
		embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
		await ctx.channel.send(embed=embed)

def setup(bot):
	bot.add_cog(feeling(bot))