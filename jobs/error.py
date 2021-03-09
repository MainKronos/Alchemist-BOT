import discord
from discord.ext import commands
from jobs.bot import bot

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(ctx, error):
	print(f"ERRORE in {ctx.guild.name} by {ctx.message.author}: {error} ")

	embed = discord.Embed(
		title = "ERROR",
		colour = discord.Colour.red()
	)

	if isinstance(error, commands.CommandNotFound):
		embed.add_field(name=f"Comando '{ctx.invoked_with}' inesistente.", value="Usare >help per maggiori informazioni", inline=False)
		await ctx.channel.send(embed=embed, delete_after=10)
		return
	
	if isinstance(error, commands.DisabledCommand):
		embed.add_field(name=f"{ctx.author.name}", value="Questo comando è stato disabilitato.", inline=False)
		await ctx.channel.send(embed=embed, delete_after=10)
		return

	if isinstance(error, commands.CheckFailure):
		embed.add_field(name=f"{ctx.author.name}", value="Non hai i permessi necessari per usare questo comando.", inline=False)
		await ctx.channel.send(embed=embed, delete_after=10)
		return

	if isinstance(error, commands.CommandOnCooldown):
		embed.add_field(name=f"{ctx.author.name}", value="Riprova fra %.2fs" % error.retry_after, inline=False)
		await ctx.channel.send(embed=embed, delete_after=10)
		return

	if isinstance(error, commands.BadArgument):
		embed.add_field(name=f"{ctx.author.name}", value=f"{error}", inline=False)
		await ctx.channel.send(embed=embed, delete_after=10)
		return

	if isinstance(error, commands.RoleNotFound):
		embed.add_field(name=f"{ctx.author.name}", value=f"{error}", inline=False)
		await ctx.channel.send(embed=embed, delete_after=10)
		return

	# try:
	# 	embed.add_field(name=f"{ctx.author.name}", value=f"{error}", inline=False)
	# 	await ctx.channel.send(embed=embed, delete_after=10)
	# except Exception as e:
	# 	pass
