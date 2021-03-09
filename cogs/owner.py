import os, sys, discord
from discord.ext import commands
from jobs import check, utils
import config

class owner(commands.Cog, name="owner"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="shutdown", aliases=["close", "turnoff", "quit", "exit"])
	@commands.check(check.is_owner)
	async def shutdown(self, context):
		"""
		Spegne il Bot.
		"""

		embed = discord.Embed(
			description="Shutting down. Bye! :wave:",
			color=0x00FF00
		)
		await context.send(embed=embed)
		self.bot.clear()
		await self.bot.logout()
		await self.bot.close()

	@commands.group(name="end", invoke_without_command=True)
	@commands.check(check.is_owner)
	async def end(self, context, user:discord.User):
		"""
		Rimuove la possibilità ad un utente di usare il bot.
		"""
		utils.add_banned(user.id)

		embed = discord.Embed(
			title="THE END",
			description=f"L'utente {user.mention} non potrà MAI più usare i comandi di {self.bot.user.mention}.",
			color=0x212121
		)
		await context.send(embed=embed)

	@end.command(name="list")
	async def list(self, context):
		embed = discord.Embed(
			color=0x212121
		)
		ll = "\t".join([self.bot.get_user(m).mention for m in config.BANNED])
		embed.add_field(name="THE END", value=f"{ll}", inline=False)
		await context.send(embed=embed)


	@commands.command(name="say", aliases=["echo"])
	@commands.check(check.is_owner)
	async def say(self, context, *, args):
		"""
		Bot echo.
		"""

		await context.send(args)

	@commands.command(name="embed")
	@commands.check(check.is_owner)
	async def embed(self, context, *, args):
		"""
		Bot echo in embed.
		"""

		embed = discord.Embed(
			description=args,
			color=0x00FF00
		)
		await context.send(embed=embed)

	@commands.command(name="push")
	@commands.check(check.is_owner)
	async def push(self, context, channel_id:int, *, args):
		"""
		Invia un messaggio come embed al canale indicato.
		"""

		embed = discord.Embed(
			description=args,
			color=0x00FF00
		)
		channel = self.bot.get_channel(channel_id)
		await channel.send(embed=embed)


def setup(bot):
	bot.add_cog(owner(bot))