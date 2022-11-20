import discord, asyncio, os, platform, sys
from discord.ext import commands
from jobs import *
import config
import random


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	bot.loop.create_task(task.status_task())

	info = await bot.application_info()
	bot.owner_id = info.owner.id

	print("\n╭-------------「on_ready」-------------╮\n")

	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")

	print("\n ------------------------------------\n")

	print(f'{bot.user} è collegato alle seguenti gilde:')
	for guild in bot.guilds:
		print(f'• {guild.name}(id: {guild.id})')

	print("\n ------------------------------------\n")

	print("Caricamneto cogs:")
	await load_cogs() # Carica i cogs
	
	print("\n╰------------------------------------╯\n")	


	MY_GUILD = discord.Object(id=173069024236666880)
	bot.tree.copy_global_to(guild=MY_GUILD)
	await bot.tree.sync(guild=MY_GUILD)

# Setup the game status task of the bot


async def load_cogs():
	cogs = [f'cogs.{c.replace(".py", "")}' for c in os.listdir("cogs") if c.endswith(".py")]

	for extension in cogs:
		try:
			await bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")

@bot.event
async def on_guild_join(guild):
	guild.leave()

# The code in this event is executed every time someone sends a message, with or without the prefix
# @bot.event
# async def on_message(message):
	# ctx = await bot.get_context(message)

	# # Ignores if a command is being executed by a bot or by the bot itself
	# if message.author is bot.user: return
	# elif check.is_banned(ctx): return
	# elif check.is_alive(ctx):
	# 	await bot.process_commands(message)
		# Process the command if the user is not blacklisted


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_app_command_completion(interaction, command):
	# split = fullCommandName.split(" ")
	# executedCommand = str(split[0])
	print(f"Executed {command.qualified_name} command in {interaction.guild.name} by {interaction.user} (ID: {interaction.user.id})")

# Run the bot with the token
bot.run(config.TOKEN)
