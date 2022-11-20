import discord
from discord import app_commands
from jobs.bot import bot

# The code in this event is executed every time a valid commands catches an error
@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
	print(f"ERRORE in {interaction.guild.name} by {interaction.user}: {error} ")

	embed = discord.Embed(
		title = "ERROR",
		colour = discord.Colour.red()
	)

	if isinstance(error, app_commands.CommandNotFound):
		embed.add_field(name=f"Comando '{interaction.command}' inesistente.", value="Controllare meglio.", inline=False)
		await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)
		return

	if isinstance(error, app_commands.CheckFailure):
		embed.add_field(name=f"{interaction.user.mention}", value="Non hai i permessi necessari per usare questo comando.", inline=False)
		await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)
		return

	if isinstance(error, app_commands.CommandOnCooldown):
		embed.add_field(name=f"{interaction.user.mention}", value="Riprova fra %.2fs" % error.retry_after, inline=False)
		await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)
		return

	try:
		embed.add_field(name=f"{interaction.user.mention}", value=f"{error}", inline=False)
		await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)
	except Exception as e:
		pass