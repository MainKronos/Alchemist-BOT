import discord, asyncio, os, platform, sys
from discord.ext import commands
from jobs import *
import config


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	bot.loop.create_task(task.status_task())
	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
	print("-------------------")
	load_cogs() # Carica i cogs
	utils.load_banned() # Carica gli tenti bannati

	bot.loop.create_task(task.check_death_task())

# Setup the game status task of the bot


def load_cogs():
	cogs = [f'cogs.{c.replace(".py", "")}' for c in os.listdir("cogs") if c.endswith(".py")]

	for extension in cogs:
		try:
			bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
	ctx = await bot.get_context(message)

	# Ignores if a command is being executed by a bot or by the bot itself
	if message.author is bot.user: return
	elif check.is_banned(ctx): return
	elif check.is_alive(ctx):
		await bot.process_commands(message)
		# Process the command if the user is not blacklisted

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	print(f"Executed {executedCommand} command in {ctx.guild.name} by {ctx.message.author} (ID: {ctx.message.author.id})")

# Run the bot with the token
bot.run(config.TOKEN)
