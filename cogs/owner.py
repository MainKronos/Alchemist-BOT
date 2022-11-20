import os, sys, discord, json
from discord.ext.commands import Cog
from discord import app_commands
from jobs.bot import bot

class owner(Cog, name="owner"):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="poweroff")
	@app_commands.check(lambda i: i.user.id == i.client.owner_id)
	async def poweroff(self, interaction: discord.Interaction):
		"""
		Spegne il Bot.
		"""

		embed = discord.Embed(
			description="Shutting down. Bye! :wave:",
			color=0x00FF00
		)
		await interaction.response.send_message(embed=embed)
		self.bot.clear()
		await self.bot.close()

	@app_commands.command(name="leave")
	@app_commands.check(lambda i: i.user.id == i.client.owner_id)
	@app_commands.choices(guild=[
		app_commands.Choice(name=x.name, value=str(x.id)) for x in bot.guilds
	])
	async def leave(self, interaction: discord.Interaction, guild: str):
		"""
		Esce da una Gilda.

		Parameters
		----------
		guild: str
			Gilda da cui uscire
		"""

		guild = self.bot.get_guild(int(guild))

		embed = discord.Embed(
			description=f"Uscendo dalla Gilda {guild}",
			color=0x00FF00
		)
		await interaction.response.send_message(embed=embed)

		await guild.leave()


async def setup(bot):
	await bot.add_cog(owner(bot))