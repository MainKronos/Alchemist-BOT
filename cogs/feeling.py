import discord
from discord.ext.commands import Cog
from discord import app_commands
import random, requests


class feeling(Cog, name="feeling"):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name="feel")
	async def feel(self, interaction: discord.Interaction, something: str):
		"""
		Invia una gif riguardante il parametro usato.

		Parameters
		----------
		something: str
			Descrizione del sentimento
		"""

		search_term = f"anime {something}" 

		res = requests.get(f"https://tenor.googleapis.com/v2/search?q={search_term}&key=AIzaSyDzdaVSGfjcpHftJlSfHpOCYF0mVBukf9Q&client_key=tenor&limit=10&media_filter=gif")

		embed = discord.Embed(
			title="FEELING",
			description=f'{search_term.title()}'
		)

		url = random.choice(res.json()["results"])["media_formats"]["gif"]["url"]
		embed.set_image(url=url)
		embed.set_footer(text=f"messaggio inviato da {interaction.user}")
		await interaction.response.send_message(embed=embed)

async def setup(bot):
	await bot.add_cog(feeling(bot))