import os, sys, discord, asyncio
from discord.ext.commands import Cog
from discord import app_commands
import config
import json, random, requests

from PIL import Image
from io import BytesIO

class fun(Cog, name="fun"):
	def __init__(self, bot):
		self.bot = bot
		self.gitFolder = f"{config.GIT_FOLDER}/fun"
		self.localFolder = "./img/fun"

	@app_commands.command(name='padoru')
	async def padoru(self, interaction: discord.Interaction):
		"""
		Invia 280 volte la scritta padoru.
		"""
		await interaction.response.send_message("padoru "*280)

	# @commands.command(name='teletta', aliases=['guido'])
	# @check.is_in_guild(698597723451949076) # Bullet Club
	# async def teletta(self, ctx, gif=None):
	# 	"""
	# 	Invia la lista dei comandi per le gif di teletta.
	# 	"""

	# 	thisDir = "teletta"

	# 	localDir = f"{self.localFolder}/{thisDir}"

	# 	imgs_name = [x.split('.')[0].lower() for x in os.listdir(localDir)]

	# 	if gif == None: # manda le gif possibili

	# 		txtdesc = '\n'.join(imgs_name) # Decrizione subcomandi

	# 		embed = discord.Embed(
	# 			title="Teletta GIF",
	# 			description=f'```{txtdesc}```',
	# 			color=0xa8c0ff
	# 		)
	# 		await ctx.send(embed=embed)
	# 	else:
	# 		if gif.lower() in imgs_name:
	# 			embed = discord.Embed(
	# 				title=f"Teletta {gif.title()}",
	# 				color=0xa8c0ff
	# 			)

	# 			url = f"{self.gitFolder}/{thisDir}/{gif.title()+'.gif'}"
	# 			embed.set_image(url=url)
	# 			embed.set_footer(text=f"messaggio inviato da {ctx.message.author.name}")
	# 			await ctx.channel.send(embed=embed)
	# 		else:
	# 			raise commands.BadArgument(f"La gif Teletta {gif} non esiste.")

	@app_commands.command(name='bestemmia')
	async def bestemmia(self, interaction: discord.Interaction):
		"""
		Invia una bestemmia.
		"""

		f=open('json/bestList.json', 'r')
		bestemmieList = json.loads(f.read())
		f.close()

		response = random.choice(bestemmieList)

		await interaction.response.send_message(response)

	@app_commands.command(name='stura')
	async def stura(self, interaction: discord.Interaction, user:discord.User=None):
		"""
		Stura qualcuno.

		Parameters
		----------
		user: User
			Utente da sturare
		"""

		if user == self.bot.user:
			raise discord.ext.commands.BadArgument(f"Impossibile sturare {self.bot.user.mention}")	

		if user==None:
			user = random.choice([x for x in interaction.guild.members if x.status != discord.Status.offline])

		embed = discord.Embed(
			title="Stura",
			colour = discord.Colour.blue(),
			description=f"**{interaction.user.mention}** sta sturando **{user.mention}**"
		)

		embed.set_thumbnail(url=f"{self.gitFolder}/stura/stura.gif")

		print(f"{interaction.user.name} sta sturando {user.name}")
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="8ball")
	async def eight_ball(self, interaction: discord.Interaction, question: str):
		"""
		Chiedi qualsiasi cosa al BOT.

		Parameters
		----------
		question: str
			Domanda da fare al BOT
		"""
		answers = ['È certo.', 'È decisamente così.', 'Ci puoi scommettere!.', 'Senza dubbio.',
				   'Sì, sicuramente.', 'Da quel che vedo, si.', 'Probabilmente si.', 'Parebbe di si.', 'Si.',
				   'Le carte mi indicano sì.', 'Risposta confusa, riprova.', 'Riprova più tardi.', 'Meglio che non te lo dica.',
				   'Non posso risponderti ora come ora.', 'Concentrati e chiedi di nuovo più tardi.', 'Non contarci.', 'La mia risposta è no.',
				   'Le mie fonti dicono di no.', 'Parebbe di no.', 'Sono molto dubbioso.']
		embed = discord.Embed(
			title="**La mia risposta:**",
			description=f"{random.choice(answers)}",
			color=0x00FF00
		)
		embed.add_field(name=f"Alla domanda:", value=f"{question}", inline=False)
		embed.set_footer(
			text=f"Domanda richiesta da: {interaction.user}"
		)
		embed.set_thumbnail(url=f"{self.gitFolder}/8ball/8ball.png")
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="dice")
	async def dice(self, interaction: discord.Interaction, face:int=6):
		"""
		Tira un dado.

		Parameters
		----------
		face: int
			Numero di facce del dado
		"""

		embed = discord.Embed(
			title="**Il dado è tratto!**",
			description=f"{random.randint(1, face)}",
			color=0x00FF00
		)
		embed.set_thumbnail(url=f"https://media.tenor.com/images/73659ccb799438fa79e9c9a876194f1d/tenor.gif")
		await interaction.response.send_message(embed=embed)


	HentaiGroup = app_commands.Group(name="hentai", nsfw=True, description="Hentai")

	@HentaiGroup.command(name="tags", nsfw=True)
	async def tags(self, interaction: discord.Interaction):
		"""
	 	Invia i tags più popolari.
	 	"""

		embed = discord.Embed(
			title="TAGS POPOLARI",
			colour = discord.Colour.blurple()
		)

		res = requests.get(f'https://danbooru.donmai.us/tags?search[order]=count&limit=24', params={'format':'json'}, timeout=3).json()
		response = " ".join([x["name"] for x in res])
		ordinal = 1
		for tag in res:
			embed.add_field(name=f"{ordinal}° Posto", value=f"``{tag['name']}``", inline=True)
			ordinal += 1
		embed.add_field(name=f"({ordinal}° Posto)", value=f"``socks``", inline=True)

		await interaction.response.send_message(embed=embed)

	@HentaiGroup.command(name="find", nsfw=True)
	async def find(self, interaction: discord.Interaction, tag: str):
		"""
	 	Invia un immagine hentai relativa al tag inserito.

		Parameters
		----------
		tag: str
			Nome del tag
	 	"""

		tag = tag.lower().replace(" ", "_")

		while True:
			try:
				res = requests.get(f'https://danbooru.donmai.us/posts/random?tags=score%3A>50+rating%3Aexplicit+{tag}', params={'format':'json'}, timeout=3).json()

				image = res["file_url"]
				break
			except KeyError:
				pass
			except Exception as e:
				print(e)
				return

		embed = discord.Embed()
		embed.set_image(url=image)
		text =  ", ".join([f"{x}" for x in res["tag_string"].split(' ')])
		embed.set_footer(text=f"Tags: {text}")

		await interaction.response.send_message(embed=embed, ephemeral=True)

	@app_commands.command(name='quiz')
	async def quiz(self, interaction: discord.Interaction):
		"""
		Richiedi un quiz su un anime.
		"""


		f=open('json/quiz.json', 'r')
		domande = json.loads(f.read())
		f.close()

		quiz = random.choice(domande)
		# quiz['domanda']			


		class InputQuiz(discord.ui.Select):
			async def callback(self, *s):
				self.view.stop()
				

		modal = discord.ui.View(timeout=20)
		select = InputQuiz(options=[
			discord.SelectOption(label="Vero"),
			discord.SelectOption(label="Falso")
		])
		modal.add_item(select)

		embed = discord.Embed(
			title="QUIZ",
			colour=discord.Colour.dark_grey(),
			description="Hai 20 secondi per rispondere."
		)
		embed.add_field(name="Domanda", value=f"``{quiz['domanda']}``", inline=False)
		embed.add_field(name="Per", value=f"{interaction.user.mention}", inline=True)
		embed.add_field(name="Penalità", value=f"**Morte**", inline=True)
		embed.set_thumbnail(url=f"{self.gitFolder}/quiz/quiz.png")

		await interaction.response.send_message(embed=embed, view=modal)

		

		await modal.wait()
		modal.clear_items()
		
		if len(select.values):
			res = select.values[0]
			if (res == "Vero") == quiz["risposta"]:
				await interaction.edit_original_response(content ="Corretto", view=None, embed=None)
				return

		await interaction.edit_original_response(content ="Sbagliato", view=None, embed=None)
		


async def setup(bot):
	await bot.add_cog(fun(bot))