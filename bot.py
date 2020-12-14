import os
from discord.ext import commands, tasks
import discord
import random
import time
import requests
import json
import re
import asyncio
from google_trans_new import google_translator  
import datetime as dt

TOKEN = ".."
KILLED = []

startMSG = r"""
┌-----------------------------------┐
|  ____  _                       _  |
| |  _ \(_)___  ___ ___  _ __ __| | |
| | | | | / __|/ __/ _ \| '__/ _` | |
| | |_| | \__ \ (_| (_) | | | (_| | |
| |____/|_|___/\___\___/|_|  \__,_| |
|                                   |
└-----------------------------------┘
"""

intents = intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents, help_command=None)
bot.remove_command('help')

async def leave_guild():
	myGuilds = [173069024236666880, 698597723451949076, 754083217535008962, 768897216844136459] 
	for guild in bot.guilds:
		if guild.id not in myGuilds:
			print(f"Uscendo dalla gilda {guild.name}(id: {guild.id})'")
			await guild.leave()

async def removeGogna(members):
	members_Gogna = []
	channel = None
	gogna = None

	for membro in members:

		if membro.guild.id == 698597723451949076: #Bullet
			channel = membro.guild.get_channel(717089928567193690) #bullet_fun
			gogna = membro.guild.get_role(784386439310868511) #Gogna


		if gogna in membro.roles:
			await membro.remove_roles(gogna)
			print(f"{membro.name} è stato ripristinato")
			members_Gogna.append(membro)

	if len(members_Gogna) > 0:
		txt = " ".join([x.mention for x in members_Gogna])
		embedEnd.add_field(name=f"Ripristinati i membri:", value=f"{txt}", inline=False)
		await channel.send(embed=embedEnd)


### COGS #############################################################################################################

class MyCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.channel = self.bot.get_channel(717091489557250099)
		self.printer.start()
		print("COGS inizializzato")

	async def get_last_chapter(self):
		regex = re.compile(r'https:\/\/mangadex\.org\/chapter\/.*')
		ch = self.channel
		message = discord.utils.find(lambda message: regex.search(message.content), await ch.history(limit=10).flatten())
		return int(re.search(r"https:\/\/mangadex\.org\/chapter\/(\d+)", message.content).group(1))

	def chapters(self):
		cookies = {
			
		}
		res = requests.get("https://mangadex.org/api/v2/group/8588", params = {'include':'chapters'}, cookies=cookies)
		return res.json()["data"]["chapters"]

	@tasks.loop(seconds=1800)
	async def printer(self):
		try:
			chapterID= await self.get_last_chapter()
			chapters = self.chapters()
			messaggi = []
			for chapter in chapters:
				if chapter["id"] == chapterID:
					break
				else:
					messaggi.append(f'Nuovo capitolo di {chapter["mangaTitle"]} Vol.{chapter["volume"]} Ch.{chapter["chapter"]}\n\nhttps://mangadex.org/chapter/{chapter["id"]}')

			messaggi.reverse()

			for msg in messaggi:
				print(msg)
				await self.channel.send(msg)	
		except Exception:
			print("Errore al printer")
			return

class Greeting(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def is_greeting(self, greeting, ora, channel):
		regex = re.compile(f'{greeting}')
		message = discord.utils.find(lambda message: regex.search(message.content), await channel.history(limit=300, after=ora, oldest_first=False).flatten())
		if message == None:
			return False
		else:
			return True

	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author == self.bot.user:
			return

		hour = dt.datetime.now().hour

		stato=None
		greeting=None
		is_greeting=None
		orario=None

		if hour > 6 and hour < 12:
			greeting = f"'Giorno 👋 {message.author.mention}"
			stato = "giorno"
			orario = dt.datetime.today().replace(hour=6, minute=0, second=0, microsecond=0)
		elif hour > 12 and hour < 18:
			greeting = f"'Sera 👋 {message.author.mention}"
			stato ="sera"
			orario = dt.datetime.today().replace(hour=12, minute=0, second=0, microsecond=0)
		else:
			greeting = f"'Notte 👋 {message.author.mention}"
			stato ="notte"
			orario = dt.datetime.today().replace(hour=18, minute=0, second=0, microsecond=0)
			if hour <=0:
				orario -= dt.timedelta(days=1)

		contenuto = message.content.lower()
		if contenuto.find(stato) >=0:
			if not (await self.is_greeting(greeting, orario, message.channel)):
				print(f"L'utente è {message.author.name} stato salutato")
				await message.channel.send(greeting)
			else:
				print(f"L'utente è {message.author.name} gia stato salutato")

class Traduttore(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author == self.bot.user:
			return

		if message.guild.id != 698597723451949076:
			return

		translator = google_translator()

		tr = translator.detect(message.content)
		if len(tr)>0:
			if tr[0] not in ['gl', 'it', 'de', 'en', 'fr', 'nl', 'ro', 'su', 'tl', 'es', 'gu', 'haw', 'zh-CN', 'hmn', 'te', 'pl', 'ca', 'sm', 'eo', 'hi', 'mi', 'jw', 'el', 'so', 'da', 'ha', 'fi', 'ku', 'co', 'pt', 'sk', 'la']:
				tran = translator.translate(message.content, lang_tgt='it')

				# await discord.abc.Messageable.send(content=tran, reference=message)
				print(f"La traduzione per {message.content} è avvenuta\tlang:{tr[0]}")
				await message.channel.send(content=tran)
			else:
				# print(f"La traduzione per {message.content} non è avvenuta\tlang:{tr[0]}")
				pass


class Reazioni(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.REAZIONI = False

	@commands.Cog.listener()
	async def on_message(self, message):

		if self.REAZIONI:

			if message.author == bot.user:
				return

			autore = str()
				
			# USERS = ["Krónos#9268", ""]
			if message.author.id == 520593633808875571:
				await message.add_reaction("👍")
				print("> Aggiunto 👍 al messaggio di {}".format(message.author))
			elif message.author.id == 674259050384326688:
				await message.add_reaction("🤴")
				print("> Aggiunto 🤴 al messaggio di {}".format(message.author))
			elif message.author.id == 706187416175771711:
				await message.add_reaction("✍")
				# await message.channel.send("<@691385177850642483>")

				print("> Aggiunto ✍ al messaggio di {}".format(message.author))

			### per i culti #####


			ruoli = [role.name for role in message.author.roles]

			mutanda = bot.get_emoji(760586805895626832)
			calza = bot.get_emoji(781473890621980673)
			parigine = bot.get_emoji(782292612794023976)

			if "Culto della mutanda" in ruoli:
				await message.add_reaction(mutanda)
				print("> Aggiunto mutanda al messaggio di {}".format(autore))
			elif "Culto della Calza" in ruoli:
				await message.add_reaction(calza)
				print("> Aggiunto Calza al messaggio di {}".format(autore))
			elif "Culto delle parigine" in ruoli:
				await message.add_reaction(parigine)
				print("> Aggiunto parigine al messaggio di {}".format(autore))

	@commands.command(name='toggle', help='Accende/Spegne le reazioni ai mesaggi')
	async def toggle(self, ctx):
		if self.REAZIONI:
			self.REAZIONI = False
			await ctx.channel.send("Reazioni disattivate")
		else:
			self.REAZIONI = True
			await ctx.channel.send("Reazioni attivate")
		print(f"Bot è {self.REAZIONI}")

class WhatAnime(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author == bot.user: return
		if message.channel.id != 787786882138112010: return
		if len(message.attachments) == 0: return

		image = await message.attachments[0].read()
		print(f"L'utente {message.author.name} ha ricercato un'anime.")

		file = {'image': image}
		url = "https://trace.moe/api/search"
		res = requests.post(url, files=file)


		# if bad_r.status_code
		res.raise_for_status()

		res = res.json()["docs"][0]
		embed = discord.Embed(
			title=res["title_romaji"],
			colour = discord.Colour.dark_blue()
		)
		embed.add_field(name=f"Stagione", value=f"``{res['season']}``", inline=False)
		embed.add_field(name=f"Episodio", value=f"``{res['episode']}``", inline=False)
		embed.add_field(name=f"Al Momento", value=f"``{res['at']} secondi``", inline=False)
		embed.add_field(name=f"Accuratezza", value=f"``{res['similarity']*100}%``", inline=False)
		embed.add_field(name=f"Link", value=f"https://myanimelist.net/anime/{res['mal_id']}", inline=False)
		if res['similarity'] < 0.87: 
			embed.add_field(name=f"**POSSIBILE ERRORE**", value=f"⚠️⚠️⚠️⚠️⚠️⚠️", inline=False)

		image = await message.attachments[0].to_file()
		# embed.set_image(url=image_url)

		await message.channel.send(embed=embed, file = image, delete_after=60)
		await message.delete()


### FUNZIONI ############################################################################################################

async def respawn(members):
	global KILLED

	[KILLED.append(user) for user in members]
	await asyncio.sleep(60)
	[KILLED.remove(user) for user in members]

async def Gogna(channel, members, time, ruolo):

	embedEnd = discord.Embed(
		title="GOGNA",
		colour = discord.Colour.teal()
	)

	embedTXT = " ".join([x.mention for x in members])
	embedEnd.add_field(name=f"Ripristinati i membri:", value=f"{embedTXT}", inline=False)

	# gognaDict = {}
	# with open("gogna.json", 'r') as file:
	# 	gognaDict = json.loads(file.read())

	for membro in members:
		await membro.add_roles(ruolo)

	await asyncio.sleep(time*60)
	for membro in members:
		await membro.remove_roles(ruolo)
		# gognaDict.pop(str(membro.id))

	await channel.send(embed=embedEnd)

	# with open("gogna.json", 'w') as file:
	# 	file.write(json.dumps(gognaDict, indent='\t'))

def is_alive(ctx):
	return (not (ctx.author in KILLED))

def is_dev(ctx):
	return ctx.author.id == 173063242187276288

def is_not_excluded(ctx):
	return not ctx.author.id == 621003460787175434

def guild_whitelist(ctx):
	implementedGuild =[173069024236666880, 698597723451949076] 
	return ctx.guild.id in implementedGuild


### EVENTI ##############################################################################################################

@bot.event
async def on_ready():

	print(startMSG)

	print("\n╭-------------「on_ready」-------------╮\n")
	print(f'{bot.user} è collegato alle seguenti gilde:')
	for guild in bot.guilds:
		print(f'• {guild.name}(id: {guild.id})')
		await removeGogna(guild.members)

	print("\n╰------------------------------------╯\n")	
	await leave_guild()
	# await syncGogna()

	bot.add_cog(MyCog(bot))
	bot.add_cog(Greeting(bot))
	bot.add_cog(Reazioni(bot))
	bot.add_cog(Traduttore(bot))
	bot.add_cog(WhatAnime(bot))
	# bot.add_cog(Domande(bot))

	# myActivity = discord.Activity(name="musica natalizia", type=discord.ActivityType.listening)
	# myActivity = discord.Activity(name="i messaggi", type=discord.ActivityType.watching)
	myActivity = discord.Game(name="Minecraft")
	await bot.change_presence(activity=myActivity)


@bot.event
async def on_guild_join(guild):
	print(f"Il bot è appena entrato nella Gilda {guild.name}")
	await leave_guild() # Esce dalla gilde in qui no deve stare

@bot.event
async def on_message(message):

	global KILLED

	if message.author == bot.user:
		return	

	# if message.author.id == 706187416175771711:
	# 	# await message.add_reaction("✍")
	# 	await message.channel.send("<@691385177850642483>")

	if message.author in KILLED:
		user = [x for x in KILLED if message.author == x][0]
		if user.guild == message.guild:
			await message.delete()

	await bot.process_commands(message)

### ERROR

@bot.event
async def on_command_error(ctx, error):
	print(f"ERRORE: {error}")

	embed = discord.Embed(
		title = "ERROR",
		colour = discord.Colour.red()
	)

	if isinstance(error, commands.CommandNotFound):
		embed.add_field(name=f"Comando '{ctx.invoked_with}' inesistente.", value="Usare >help per maggiori informazioni", inline=False)
		await ctx.channel.send(embed=embed)
		return
	
	if isinstance(error, commands.DisabledCommand):
		 
		embed.add_field(name=f"{ctx.author.name}", value="Questo comando è stato disabilitato.", inline=False)
		await ctx.channel.send(embed=embed)
		return

	if isinstance(error, commands.CheckFailure):
		embed.add_field(name=f"{ctx.author.name}", value="Non hai i permessi necessari per usare questo comando.", inline=False)
		await ctx.channel.send(embed=embed)
		return

	if isinstance(error, commands.BadArgument):
		embed.add_field(name=f"{ctx.author.name}", value=f"{error}", inline=False)
		await ctx.channel.send(embed=embed)
		return

	if isinstance(error, commands.RoleNotFound):
		embed.add_field(name=f"{ctx.author.name}", value=f"{error}", inline=False)
		await ctx.channel.send(embed=embed)
		return

	embed.add_field(name=f"{ctx.author.name}", value=f"{error}", inline=False)
	await ctx.channel.send(embed=embed)
	return

### COMMANDS ###################################################################################################

####### HELP #######

@bot.command(name='help', help='Descrive i comandi')
@commands.check(is_alive)
async def help(ctx):

	embed = discord.Embed(
		title = "HELP",
		colour = discord.Colour.orange()
	)
	for command in bot.commands:
		embed.add_field(name=">"+command.name, value=command.help, inline=False)

	await ctx.channel.send(embed=embed)

########################

@bot.command(name='test', help='Messaggio di prova')
@commands.check(is_dev)
async def test(ctx):
	response = "test"
	print(response)
	await ctx.send(response)

@bot.command(name='frase', help="Scrive una frase di un'Anime")
@commands.check(is_alive)
async def frase(ctx):

	f=open('animeFrasi.json', 'r')
	animeFrasi = json.loads(f.read())
	f.close()

	embed = discord.Embed(
		title = "FRASE",
		colour = discord.Colour.green()
	)

	frase=random.choice(animeFrasi)
	
	for part in frase:
		embed.add_field(name=f"{part}", value=f"{frase[part]}", inline=False)

	await ctx.channel.send(embed=embed)

@bot.command(name='bestemmia', help="Scrive una bestemmia (con 'list' le scrive tutte, con 'add' ne aggiunge una)")
@commands.check(is_alive)
@commands.cooldown(1, 5, commands.BucketType.user)
async def bestemmia(ctx, arg=None, * ,best=None):

	f=open('bestList.json', 'r')
	bestemmieList = json.loads(f.read())
	f.close()

	if arg == 'add':
		if best!=None:
			best=best.title()
			if best in bestemmieList:
				await ctx.channel.send(f"La bestemmia '{best}' è già presente")
			else:
				if len(best) > 30:
					await ctx.channel.send("Bestemmia troppo lunga")
				elif (best.find("Dio ") < 0 and best.find("Madonna") < 0 and best.find("Cristo") < 0 and best.find("Padre Pio") < 0 and best.find("San")):
					await ctx.channel.send(f"'{best}' NON è una bestemmia")
				else:
					bestemmieList.append(best)

					f=open("bestList.json", 'w')
					f.write(json.dumps(bestemmieList, indent='\t'))
					f.close()
					print(f"\nLa bestemmia '{best}' è stata aggiunta\n")
					await ctx.channel.send(f"La bestemmia '{best}' è stata aggiunta")
		else:
			await ctx.channel.send("È necessario aggiungere una bestemmia dopo 'add'")
	else:
		if arg == 'list':
			response = "\n".join(bestemmieList)
			for x in range(int(len(response)/2000)+1):
				if x*2000+2000-1 > len(response)-1:
					block = len(response)-1
				else:
					block = x*2000+2000-1 
				await ctx.channel.send(response[x*2000:block])
			return

		else:
			response = random.choice(bestemmieList)
		await ctx.channel.send(response)

@bot.command(name='tag', help='Tagga qualcuno (se non è specificato chi, ne prende uno a caso)')
@commands.check(is_alive)
@commands.cooldown(1, 10, commands.BucketType.user)
async def tag(ctx, user:discord.User=None):

	if user == bot.user:
		raise discord.ext.commands.BadArgument(f"Impossibile taggare {bot.user.mention}")	

	if user==None:
		user = random.choice(ctx.guild.members)

	print(f"Ricvuto arg: {user} name: {user.name}")
	print(f">taggando {user.name}")
	await ctx.channel.send(f"{user.name} ATTACK!!!")
	
	for x in range(5):
		text = str(user.mention)*50
		await ctx.channel.send(text)

@bot.command(name='stura', help='Stura qualcuno (se non è specificato chi, ne prende uno a caso)')
@commands.check(is_alive)
@commands.cooldown(1, 10, commands.BucketType.user)
async def stura(ctx, user:discord.User=None):
	if user == bot.user:
		raise discord.ext.commands.BadArgument(f"Impossibile sturare {bot.user.mention}")	

	if user==None:
		user = random.choice(ctx.guild.members)
	response = f"{ctx.author.mention} sta sturando {user.mention}"
	print(f"{ctx.author.name} sta sturando {user.name}")
	await ctx.channel.send(response)	

@bot.command(name='loda', help='Loda qualcuno (se non è specificato chi, prende Verbal)')
@commands.check(is_alive)
async def loda(ctx, user:discord.User=None):
	if user == bot.user:
		raise discord.ext.commands.BadArgument(f"Impossibile lodare {bot.user.mention}")	

	if user == bot.get_user(621003460787175434):
		raise discord.ext.commands.BadArgument(f"Impossibile lodare {user.mention}")

	complimentiList = [
		"sei il migliore",
		"sei fantastico",
		"bravooooo",
		"menomale che ci sei te",
		"sei strepitoso"
	]

	if user==None:
		user = bot.get_user(674259050384326688) #Verbal

	response = f"{user.mention} {random.choice(complimentiList)}"
	print(f"{ctx.author.name} sta lodando {user.name}")
	await ctx.channel.send(response)

@bot.command(name='offendi', help='Offende qualcuno (se non è specificato chi, prende uno a AksJohn)', aliases=["insulta"])
@commands.check(is_alive)
async def offendi(ctx, user:discord.User=None):
	if user == bot.user:
		raise discord.ext.commands.BadArgument(f"Impossibile offendere {bot.user.mention}")	

	offeseList = [
		"MA VAFFANGUL A CHITEBBIV, CHITEMMURT E CHITESTRAMURT",
		"vafangul a chitebbiv",
		"vafangul a chitemmurt",
		"vafangul a chitestramurt",
		"chitebbiv",
		"vafangul a chitemmurt e stramurt",
		"To mare inferno",
		"To mare orso polare",
		"To mare omo",
		"Lesbico",
		"Rincocitrullito",
		"m'agg rutt u cazz",
		"sei cosi brutto che quando tua madre ti ha fatto si è suicidata",
		"il cesso è più bello di te",
		"fai l'omm anche i merd fai l' omm",
		"testa di clasper",
		"SI' TE PIJO TE SDRUMO",
		"TE DO 'N CARCIO AR CULO CHE TE CE LASCIO DENTRO 'A SCARPA",
		"Sei come la minchia: sempre tra le palle",
		"Sei così spaventoso che quando caghi la tua stessa merda dice di fotterti",
		"sei un AksJohn",
		"quando Dio diede l'intelligenza all'umanità tu dov'eri? Al cesso!?",
		"hai un ego cosi' smisurato che non ti rimane piu' spazio nel cervello",
		"hai un unico difetto: respiri",
		"sei cosi ignorante che pure i tuo amici ti stanno lontano",
		"sei utile quanto un uomo con una gamba sola a una gara di calci in culo",
		"non ti ammazzo perché vorrebbe dire certificare la tua esistenza",
		"perché non sei andato alle paraolimpiadi saresti arrivato primo fra i down",
		"vali quanto un ebreo nel '45",
		"prova a trattenere il respiro cinque minuti così tutti si accorgeranno che l'aria che respiriamo è migliorata",
		"se rompesse il ghiaccio come rompe i coglioni, potrebbe diventare il re delle granite",
		"se Dio ha creato l'ignoranza protesta, perchè ne sei l'unico beneficiario",
		"sei talmente bruh che non ho abbastanza bruh per descriverti",
		"gli animali capiscono senza parlare... tu parli senza capire",
		"mi stai talmente sui maroni che anche insultarti non mi farebbe stare meglio",
		"vedo che ti tieni in forma... c’hai il fisico di chi va tutti i giorni a fanculo, di corsa",
		"è inutile che porti l'orologio se poi il tuo ritardo è mentale",
		"mi fai arrapare il dito medio!",
		"se sei intelligente lo nascondi molto bene"
	]

	if user==None:
		user = bot.get_user(621003460787175434) #AksJohn
	response = f"{user.mention} {random.choice(offeseList)}"

	print(f"{ctx.author.name} sta offendendo {user.name}")

	await ctx.channel.send(response)
	# if ctx.message.guild.me.guild_permissions.manage_nicknames:
	newNick = "Sono un {}".format(random.choice(["AksJohn", "Pirla"]))
	# await ctx.author.edit(nick=newNick)

@bot.command(name='close', help='Spegne il BOT')
@commands.check(is_dev)
async def close(ctx):
	print("Spegnimento Bot")
	bot.clear()
	await bot.close()

@bot.command(name='kill', help='Uccide qualcuno (se non è specificato chi, ne uccide uno a caso)')
@commands.check(is_alive)
@commands.check(is_not_excluded)
@commands.cooldown(1, 30, commands.BucketType.user)
async def kill(ctx, *args):

	global KILLED

	embedKill = discord.Embed(
		colour = discord.Colour.darker_gray()
	)

	embedRespawn = discord.Embed(
		colour = discord.Colour.teal()
	)

	users = []


	if ctx.message.mention_everyone:
		raise discord.ext.commands.BadArgument(f"Non è più possibile uccitere @everyone")
		embedKill.add_field(name="Kill", value="@everyone sono MORTI e non potranno parlare per 60 secondi.", inline=False)
		embedRespawn.add_field(name="RESPAWN", value="@everyone sono RINATI.", inline=False)
		users = ctx.guild.members
		print(f"{ctx.author.name} ha ucciso tutti")
	else:

		errorKiled = [] ##utenti già morti e che non possono rimorire

		if len(args)==0:  # Se non viene passato nessun argomento
			users.append(random.choice(ctx.guild.members))
		else:
			for arg in args:
				try:
					user = await commands.UserConverter().convert(ctx, arg)
				except:
					try:
						ruolo = await commands.RoleConverter().convert(ctx, arg)
					except:
						raise discord.InvalidArgument
					else:
						for membro in ruolo.members:
							if membro == bot.user: raise discord.ext.commands.BadArgument(f"Impossibile uccidere {bot.user.mention}")	
							elif membro not in KILLED: users.append(membro)
							else: errorKiled.append(membro)
				else:
					if user not in ctx.guild.members: raise discord.ext.commands.BadArgument(f"L'utente {user.mention} non fa parte della gilda")
					elif user == bot.user: raise discord.ext.commands.BadArgument(f"Impossibile uccidere {bot.user.mention}")	
					elif user not in KILLED: 
						membro = ctx.guild.get_member(user.id)
						users.append(user)	
					else: errorKiled.append(user)

		embedTXT = " ".join([x.mention for x in users])
		errorTKilled = " ".join([x.mention for x in errorKiled])
		
		if len(users) == 0:
			if len(errorKiled) > 1:
				raise discord.ext.commands.BadArgument(f"Gli utenti {errorTKilled} sono già morti")
			else:
				raise discord.ext.commands.BadArgument(f"L'utente {errorTKilled} è già morto")
		elif len(users) > 1:
			embedTkill = embedTXT +" sono MORTI e non potranno parlare per 60 secondi."
			embedTRespawn = embedTXT +" sono sono RINATI."
		else:
			embedTkill = embedTXT +" è MORTO e non potrà parlare per 60 secondi."
			embedTRespawn = embedTXT +" è RINATO."

		embedKill.add_field(name="Kill", value=embedTkill, inline=False)
		embedRespawn.add_field(name="RESPAWN", value=embedTRespawn, inline=False)	

		print(f"{ctx.author.name} ha ucciso {embedTXT}")

	await ctx.channel.send(embed=embedKill)
	members = [ctx.guild.get_member(x.id) for x in users]
	await respawn(members)
	await ctx.channel.send(embed=embedRespawn)

@bot.command(name='gogna', help='Manda alla gogna (>gogna "tempo" "chi")')
@commands.check(is_alive)
@commands.cooldown(1, 20, commands.BucketType.user)
async def gogna(ctx, tempo=None, *args):

	embed = discord.Embed(
		title="GOGNA",
		colour = discord.Colour.blue()
	)

	embedWarning = discord.Embed(
		title="WARNING",
		colour = discord.Colour.orange()
	)

	if ctx.author.guild.id == 698597723451949076 and 783255213230391296 not in [x.id for x in ctx.author.roles]: #ruolo team_scan
		raise discord.ext.commands.CheckFailure()
		return
	elif ctx.author.guild.id != 698597723451949076 and not ctx.author.guild_permissions.administrator:
		raise discord.ext.commands.CheckFailure()
		return

	if len(args) == 0:
		raise iscord.ext.commands.BadArgument("È necessario aggiungere chi mandare alla gogna (una persona o un ruolo)")
		return

	if tempo == None:
		raise discord.ext.commands.BadArgument("È necessario aggiungere un tempo in minuti")
		return
	else:
		tempo = int(tempo)
		if tempo > 10:
			raise discord.ext.commands.BadArgument("Il tempo massimo è di 10 minuti")
			return

	gogna = None

	if ctx.guild.id == 698597723451949076: #Bullet
		gogna = ctx.guild.get_role(784386439310868511) #Gogna
	elif ctx.guild.id == 754083217535008962: #holy crusade
		gogna = ctx.guild.get_role(785456574884872222) #Gogna
		


	if gogna == None:
		raise discord.ext.commands.RoleNotFound("GOGNA")


	membri=[]
	adminWarning=[]
	userWarning=[]
	for arg in args:
		try:
			user = await commands.UserConverter().convert(ctx, arg)
		except:
			try:
				ruolo = await commands.RoleConverter().convert(ctx, arg)
			except:
				raise discord.InvalidArgument
			else:
				for membro in ruolo.members:
					if membro.guild_permissions.administrator: adminWarning.append(membro)
					elif gogna in membro.roles: userWarning.append(membro)
					else: membri.append(membro)
		else:
			membro = ctx.guild.get_member(user.id)
			if membro.guild_permissions.administrator: adminWarning.append(membro)
			elif gogna in membro.roles: userWarning.append(membro)
			else: membri.append(membro)

	if len(adminWarning) > 0:
		embedTWarning = " ".join([x.mention for x in adminWarning])
		embedWarning.add_field(name=f"I seguenti membri non possono essere mandati alla gogna perchè Amministratori:", value=f"{embedTWarning}", inline=False)
		await ctx.channel.send(embed=embedWarning)

	if len(userWarning) > 0:
		embedWarning.clear_fields()
		embedTWarning = " ".join([x.mention for x in userWarning])
		embedWarning.add_field(name=f"I seguenti membri sono già alla gogna :", value=f"{embedTWarning}", inline=False)
		await ctx.channel.send(embed=embedWarning)


	if len(membri) > 0:

		for membro in membri:
			
			print(f"{membro.name} è stato mandato alla gogna")

		taskGogna = asyncio.create_task(Gogna(ctx.channel, membri, tempo, gogna))

		# with open("gogna.json", 'w') as file:
		# 	file.write(json.dumps(gognaDict, indent='\t'))

		embedTXT = " ".join([x.mention for x in membri])
		embed.add_field(name=f"{ctx.author.name} ha mandato alla gogna:", value=f"{embedTXT} per {tempo} minuti", inline=False)	

		await ctx.channel.send(embed=embed)
		await taskGogna

		for membro in membri:
			print(f"{membro.name} è stato ripristinato")

@bot.command(name='padoru', help='Scrive padoru N volte')
@commands.check(is_alive)
async def paduru(ctx, volte:int=0):
	word = "paduru"
	maxVolte = int(2000/(len(word) + 1))
	if (volte == 0): volte=maxVolte
	elif (volte > maxVolte): volte=maxVolte
	paduruList = [word] * volte
	response = " ".join(paduruList)
	await ctx.channel.send(response)

@bot.command(name='quak', help='Scrive quak N volte')
@commands.check(is_alive)
async def quak(ctx, volte:int=0):

	if ctx.author != bot.get_user(673530180848844820) and ctx.author != bot.get_user(373969182582243329):
		raise discord.ext.commands.CheckFailure()


	word = "quak"
	maxVolte = int(2000/(len(word) + 1))
	if (volte == 0): volte=maxVolte
	elif (volte > maxVolte): volte=maxVolte
	paduruList = [word] * volte
	response = " ".join(paduruList)
	await ctx.channel.send(response)

@bot.command(name='baka', help='Scrive baka a qualcuno')
@commands.check(is_alive)
async def baka(ctx, user:discord.User):

	pictDir = "./BakaPict/"
	images = os.listdir(pictDir)
	AnimePict = [x for x in images if x.split('.')[0]==f'{user.id}']
	if len(AnimePict)  == 0:
		raise discord.ext.commands.BadArgument("Utente non implementato") 
	else:
		AnimePict = AnimePict[0]

	with open(pictDir + AnimePict, 'rb') as fp:
		await ctx.channel.send(file=discord.File(fp, AnimePict), content=user.name)

@bot.command(name='oroscopo', help='oroscopo')
@commands.check(is_alive)
async def oroscopo(ctx, segno=None):
	signs = {
		"ariete":"aries",
		"toro":"taurus",
		"gemelli":"gemini",
		"cancro":"cancer",
		"leone":"leo",
		"vergine":"virgo",
		"bilancia":"libra",
		"scorpione":"scorpio",
		"sagttario":"sagittarius",
		"capricorno":"capricorn",
		"acquario":"aquarius",
		"pesci":"pisces"
	}

	errorTXT = "Aggiungere uno dei seguenti segni: " + ", ".join([x for x in signs])
	if segno == None:
		raise discord.ext.commands.BadArgument(errorTXT)
	elif segno.lower() not in signs:
		raise discord.ext.commands.BadArgument(errorTXT)

	embed = discord.Embed(
		title="OROSCOPO",
		colour = discord.Colour.blurple()
	)

	params = {
		'sign': signs[segno],
		'day':'today'
	}

	translator = google_translator()
	res = requests.post('https://aztro.sameerkumar.website/', params=params)

	tran = translator.translate(res.json()['description'], lang_tgt='it')
	embed.add_field(name=f"{segno.title()}", value=f"{tran}", inline=False)
	print(f"Oroscopo - {segno.title()}")
	await ctx.channel.send(embed=embed)

@bot.command(name='anime', help='Invia un imagine di un anime')
@commands.check(is_alive)
async def anime(ctx):
	pictDir = "./AnimePict/"
	images = os.listdir(pictDir)
	AnimePict = random.choice(images)
	pictName = AnimePict.split('.')[0].replace("_", " ").title()

	with open(pictDir + AnimePict, 'rb') as fp:
		await ctx.channel.send(file=discord.File(fp, AnimePict), content=pictName)

@bot.command(name='hentai', help='Invia hentai (tags scive i tags più popolari)')
@commands.check(is_alive)
async def hentai(ctx, tag=""):

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
		print(response)


	else:	
		await ctx.message.delete()

		tag = tag.lower()

		print("HENTAI")

		try:
			res = requests.get(f'https://danbooru.donmai.us/posts/random?tags=score%3A>50+rating%3Aexplicit+{tag}', params=params, timeout=3).json()

			image = res["file_url"]
		except Exception as e:
			return

		embed = discord.Embed()
		embed.set_image(url=image)

	await channel.send(embed=embed)
	
	if not ctx.channel.is_nsfw():
		await ctx.channel.send(embed=warningEmbed)


@bot.command(name='hug', help='abbraccio')
async def abbraccio(ctx):

	print("HUG")

	# if ctx.author != bot.get_user(520593633808875571) and ctx.author != bot.get_user(173063242187276288):
	# 	raise discord.ext.commands.CheckFailure()

	image = "https://media1.tenor.com/images/325e3807097acda1c7d08737ae89e7c3/tenor.gif"

	embed = discord.Embed()
	embed.set_image(url=image)


	await ctx.channel.send(embed=embed)

###########################################################################################################################
bot.run(TOKEN)