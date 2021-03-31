import os, sys, discord, asyncio
from discord.ext import commands
from jobs import check
import config
import json, random, requests

from PIL import Image
from io import BytesIO

class fun(commands.Cog, name="fun"):
	def __init__(self, bot):
		self.bot = bot
		self.gitFolder = f"{config.GIT_FOLDER}/fun"
		self.localFolder = "./img/fun"

	@commands.command(name='nhug', help="", aliases=['tatsu'])
	async def tatsu(self, ctx, user:discord.User=None):
		"""
		Richiede un abbraccio a qualcuno.
		"""

		if user == None:
			desc = "Ti prego... **abbracciami**!"
		else:
			desc = f"{user.mention}, ti prego... **abbracciami**!"

		embed = discord.Embed(
			description=desc
		)
		embed.set_image(url="https://media1.tenor.com/images/5b2bbfcbc1724a0bdc1b48dcf89274d6/tenor.gif")
		embed.set_footer(text=f"Abbraccio necessario a {ctx.message.author.name}")

		await ctx.channel.send(embed=embed)

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


	@commands.command(name='bestemmia', help="", aliases=["unicorno","porcone","porco","best"], usage=r'>bestemmia (add {BESTEMMIA})/(list)')
	async def bestemmia(self, ctx, arg=None, * ,best=None):
		"""
		Scrive una bestemmia.
		"""
		# Scrive una bestemmia (con 'list' le scrive tutte, con 'add' ne aggiunge una)

		f=open('json/bestList.json', 'r')
		bestemmieList = json.loads(f.read())
		f.close()

		response = random.choice(bestemmieList)

		if check.need_censura(ctx): 
			response = f"||{response}||"

		await ctx.channel.send(response)

	@commands.command(name='stura', usage=r'>stura ({USER})')
	async def stura(self, ctx, user:discord.User=None):
		"""
		Stura qualcuno (se non è specificato chi, ne prende uno a caso)
		"""

		if user == self.bot.user:
			raise discord.ext.commands.BadArgument(f"Impossibile sturare {bot.user.mention}")	

		if user==None:
			user = random.choice([x for x in ctx.guild.members if x.status != discord.Status.offline])

		embed = discord.Embed(
			title="Stura",
			colour = discord.Colour.blue(),
			description=f"**{ctx.message.author.name}** sta sturando **{user.name}**"
		)

		embed.set_thumbnail(url=f"{self.gitFolder}/stura/stura.gif")

		print(f"{ctx.author.name} sta sturando {user.name}")
		await ctx.channel.send(embed=embed)

	@commands.command(name="8ball")
	@commands.cooldown(1, 5, commands.BucketType.guild)
	async def eight_ball(self, context, *, args):
		"""
		Chiedi qualsiasi cosa al BOT.
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
		embed.add_field(name=f"Alla domanda:", value=f"{args}", inline=False)
		embed.set_footer(
			text=f"Domanda richiesta da: {context.message.author}"
		)
		embed.set_thumbnail(url=f"{self.gitFolder}/8ball/8ball.png")
		await context.send(embed=embed)

	@commands.command(name='hentai', usage=r'>hentai ({TAG})')
	# @commands.cooldown(1, 1, commands.BucketType.user)
	async def hentai(self, ctx, *, tag=""):
		"""
		Invia hentai (tags scrive i tags più popolari)
		"""

		params = {
			'format':'json'
		}

		embed = None

		warningEmbed = discord.Embed(
			title="WARNING",
			colour = discord.Colour.blurple()
		)

		channel = None
		if not ctx.channel.is_nsfw():
			channel = discord.utils.find(lambda channel: channel.is_nsfw(), ctx.guild.text_channels)
			warningEmbed.add_field(name=f"Messaggi inviato in", value=f"{channel.mention}", inline=False)
		else:
			channel = ctx.channel

		if tag == 'tags':

			embed = discord.Embed(
				title="TAGS POPOLARI",
				colour = discord.Colour.blurple()
			)


			res = requests.get(f'https://danbooru.donmai.us/tags?search[order]=count&limit=24', params=params, timeout=3).json()
			response = " ".join([x["name"] for x in res])
			ordinal = 1
			for tag in res:
				embed.add_field(name=f"{ordinal}° Posto", value=f"``{tag['name']}``", inline=True)
				ordinal += 1
			embed.add_field(name=f"({ordinal}° Posto)", value=f"``socks``", inline=True)

		else:	
			await ctx.message.delete()

			tag = tag.lower().replace(" ", "_")

			print("HENTAI")

			try:
				res = requests.get(f'https://danbooru.donmai.us/posts/random?tags=score%3A>50+rating%3Aexplicit+{tag}', params=params, timeout=3).json()

				image = res["file_url"]
			except Exception as e:
				print(e)
				return

			embed = discord.Embed()
			embed.set_image(url=image)
			text =  ", ".join([f"{x}" for x in res["tag_string"].split(' ')])
			embed.set_footer(text=f"Tags: {text}")

		await channel.send(embed=embed)
		
		if not ctx.channel.is_nsfw():
			await ctx.channel.send(embed=warningEmbed)

	@commands.command(name='quiz', help='quiz', usage=r'>quiz')
	async def quiz(self, ctx, user:discord.User=None):

		res = {True:'👍', False:'👎'}

		f=open('json/quiz.json', 'r')
		domande = json.loads(f.read())
		f.close()

		if user==None:
			user = ctx.message.author


		channel = ctx.message.channel
		Quiz = random.choice(domande)

		embed = discord.Embed(
			title="QUIZ",
			colour=discord.Colour.dark_grey(),
			description="Hai 20 secondi per rispondere vero (👍) o falso (👎)."
		)
		embed.add_field(name="Domanda", value=f"``{Quiz['domanda']}``", inline=False)
		embed.add_field(name="Per", value=f"{user.mention}", inline=True)
		embed.add_field(name="Penalità", value=f"**Morte**", inline=True)
		embed.set_thumbnail(url=f"{self.gitFolder}/quiz/quiz.png")

		message = await channel.send(embed=embed)
		await message.add_reaction('👍')
		await message.add_reaction('👎')

		def check(reaction, userx):
			return userx == user and reaction.message == message

		try:
			reaction, userx = await self.bot.wait_for('reaction_add', timeout=20, check=check)

			if str(reaction.emoji) != res[Quiz["risposta"]]: raise
		except Exception:
			await self.bot.get_command('kill').callback(self, ctx, user)
		else:
			await channel.send('👍')

	@commands.command(name='tag', usage=r'>tag {USER}')
	async def tag(self, ctx, user:discord.User):
		"""
		Tagga qualcuno.
		"""
		await ctx.channel.send(f"{user.name} ATTACK!!!")
		
		for x in range(5):
			await ctx.channel.send(user.mention)
			await asyncio.sleep(1)

	@commands.command(name='hentai', usage=r'>hentai ({TAG})')
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def hentai(self, ctx, *, tag=""):
		"""
		Invia hentai (tags scive i tags più popolari)
		"""

		params = {
			'format':'json'
		}

		embed = None

		warningEmbed = discord.Embed(
			title="WARNING",
			colour = discord.Colour.blurple()
		)

		channel = None
		if not ctx.channel.is_nsfw():
			channel = discord.utils.find(lambda channel: channel.is_nsfw(), ctx.guild.text_channels)
			warningEmbed.add_field(name=f"Messaggi inviato in", value=f"{channel.mention}", inline=False)
		else:
			channel = ctx.channel

		if tag == 'tags':
			embed = discord.Embed(
				title="TAGS POPOLARI",
				colour = discord.Colour.blurple()
			)

			res = requests.get(f'https://danbooru.donmai.us/tags?search[order]=count&limit=24', params=params, timeout=3).json()
			response = " ".join([x["name"] for x in res])
			ordinal = 1
			for tag in res:
				embed.add_field(name=f"{ordinal}° Posto", value=f"``{tag['name']}``", inline=True)
				ordinal += 1
			embed.add_field(name=f"({ordinal}° Posto)", value=f"``socks``", inline=True)
		else:	
			await ctx.message.delete()

			tag = tag.lower().replace(" ", "_")
			try:
				res = requests.get(f'https://danbooru.donmai.us/posts/random?tags=score%3A>50+rating%3Aexplicit+{tag}', params=params, timeout=3).json()

				image = res["file_url"]
			except Exception as e:
				print(e)
				return

			embed = discord.Embed()
			embed.set_image(url=image)
			text =  ", ".join([f"{x}" for x in res["tag_string"].split(' ')])
			embed.set_footer(text=f"Tags: {text}")

		await channel.send(embed=embed)
		
		if not ctx.channel.is_nsfw():
			await ctx.channel.send(embed=warningEmbed)

def setup(bot):
	bot.add_cog(fun(bot))