import os, sys, discord
from discord.ext.commands import Cog
from discord import app_commands
import config

@app_commands.context_menu(name="warn")
# @app_commands.checks.has_permissions(**dict(discord.Permissions.elevated()))
async def warn(interaction: discord.Interaction, message: discord.Message):
	"""
	Allerta un utente.

	Parameters
	----------
	message: Message
		Messaggio da segnalare
	"""

	embed = discord.Embed(
		title="User Warned!",
		description=f"**{message.author.mention}** è stato warnato da **{interaction.user.mention}**!",
		color=0x00FF00
	)
	embed.add_field(
		name="Motivo:",
		value=message.jump_url
	)
	await interaction.response.send_message(embed=embed)
	# try:
	# 	await user.send(f"Sei stato warnato da **{context.message.author}**!\nMotivo: {reason}")
	# except:
	# 	pass

async def setup(bot):
	bot.tree.add_command(warn)
	pass