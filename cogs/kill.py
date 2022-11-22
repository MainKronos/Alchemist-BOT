import os, sys, discord, json, time
from typing import Dict
from discord.ext.commands import Cog
from discord import app_commands
from jobs.bot import bot

class Kill(Cog, name="Kill"):
	def __init__(self, bot):
		self.bot = bot
		self.killed: Dict[discord.Member, float] = {}
	
	@Cog.listener()
	async def on_message(self, message: discord.Message):

		if message.author == self.bot.user:
			return

		if self.isDead(message.author):
			await message.delete()
	
	def isDead(self, user: discord.Member):
		if user in self.killed:
			remain_time = self.killed[user] - time.time()
			if remain_time > 0:
				return remain_time
			else:
				del self.killed[user]
		
		return False

	@app_commands.command(name="kill")
	async def kill(self, interaction: discord.Interaction, user: discord.Member, delta: app_commands.Range[int, 1, 5]):
		"""
		Uccidi qualcuno.

		Parameters
		----------
		user: Member
			Persona da uccidere
		delta: Range[int, 1, 5]
			Numero di minuti
		"""

		if self.isDead(interaction.user): 
			raise app_commands.AppCommandError("Non puoi uccidere da morto.")
			return

		self.killed[user] = time.time() + delta*60

		embed = discord.Embed(
			color=discord.Colour.darker_gray()
		)

		embed.add_field(name="KILL", value=f"L'utente {user.mention} è morto e non potrà parlare per {delta} minuti.", inline=False)
		embed.set_footer(text=f"Kill eseguita da {interaction.user}")
		embed.set_thumbnail(url="https://media.tenor.com/images/1cb732f34c3b3f90d526fee50288912c/tenor.gif")

		
		await interaction.response.send_message(embed=embed)

		
	@app_commands.command(name="kinfo")
	async def kinfo(self, interaction: discord.Interaction, user: discord.Member = None):
		"""
		Controlla se un utente è morto.

		Parameters
		----------
		user: Member
			Persona da controllare
		"""

		if user == None: user = interaction.user

		embed = discord.Embed(
			title = "R.I.P.",
			colour = discord.Colour.darker_gray(),
			description=f"Tempo rimasto di {user}: {round(self.isDead(user))} secondi."
		)
		embed.set_thumbnail(url="https://media.tenor.com/images/1cb732f34c3b3f90d526fee50288912c/tenor.gif")

		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
	await bot.add_cog(Kill(bot))