import os, sys, discord
from discord.ext import commands
from jobs import check
import config

class moderation(commands.Cog, name="moderation"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='kick', pass_context=True)
	@commands.check(check.is_admin)
	async def kick(self, context, member: discord.Member, *args):
		"""
		Espelle un utente fuori dal server.
		"""
		if context.message.author.guild_permissions.kick_members:
			if member.guild_permissions.administrator:
				raise discord.ext.commands.BadArgument("L'utente è amministratore.")
			else:
				reason = " ".join(args)
				embed = discord.Embed(
					title="User Kicked!",
					description=f"**{member}** was kicked by **{context.message.author}**!",
					color=0x00FF00
				)
				embed.add_field(
					name="Reason:",
					value=reason
				)
				await context.send(embed=embed)
				try:
					await member.send(
						f"You were kicked by **{context.message.author}**!\nReason: {reason}"
					)
				except:
					pass
		else:
			raise discord.ext.commands.CheckFailure()

	@commands.command(name="nick")
	@commands.check(check.is_admin)
	async def nick(self, context, member: discord.Member, *, name: str):
		"""
		Cambia il nickname di un Membro del Server.
		"""
		if context.message.author.guild_permissions.administrator:
			if name.lower() == "None":
				name = None
			embed = discord.Embed(
				title="Nickname Cambiato!",
				description=f"Il nuovo nickname di **{member}** è **{name}**!",
				color=0x00FF00
			)
			await context.send(embed=embed)
			await member.change_nickname(name)
		else:
			raise discord.ext.commands.CheckFailure()

	@commands.command(name="warn")
	@commands.check(check.is_admin)
	async def warn(self, context, member: discord.Member, *args):
		"""
		Allerta un utente.
		"""

		if await self.bot.is_owner(member):
			raise discord.ext.commands.BadArgument(f"Non è possibile warnare {member.mention}.")

		reason = " ".join(args)
		embed = discord.Embed(
			title="User Warned!",
			description=f"**{member}** was warned by **{context.message.author}**!",
			color=0x00FF00
		)
		embed.add_field(
			name="Reason:",
			value=reason
		)
		await context.send(embed=embed)
		try:
			await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
		except:
			pass

	@commands.command(name="purge")
	@commands.check(check.is_admin)
	async def purge(self, context, number):
		"""
		Cancella un numero finito di messaggi.
		"""
		try:
			number = int(number)
		except:
			raise discord.ext.commands.BadArgument(f"`{number}` non è un numero valido.")
		if number < 1:
			embed = discord.Embed(
				title="Error!",
				description=f"`{number}` is not a valid number.",
				color=0xFF0000
			)
			await context.send(embed=embed)
			return
		purged_messages = await context.message.channel.purge(limit=number)
		embed = discord.Embed(
			title="Chat Cleared!",
			description=f"**{context.message.author}** cleared **{len(purged_messages)}** messages!",
			color=0x00FF00
		)
		await context.send(embed=embed)

def setup(bot):
	bot.add_cog(moderation(bot))