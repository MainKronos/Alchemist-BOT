import os, sys, discord
from datetime import datetime, timedelta
from discord.ext import commands
from jobs import check
import config

class rip(commands.Cog, name="rip"):
	def __init__(self, bot):
		self.bot = bot
		# config.KILLED = {
		# 	# Guild.id : {
		# 	# 	Member.id : {
		# 	# 		"time" : time,
		# 	# 		"delta" : delta,
		#	#		"channel": channel_id
		# 	# 	},
		# 	# 	...
		# 	# },
		# 	# ...
		# }

	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author == self.bot.user:
			return

		# await self.check_death()

		ctx = await self.bot.get_context(message)

		if not check.is_alive(ctx):
			await message.delete()

	@commands.command(name="kill")
	@commands.check(check.has_role)
	async def kill(self, context, member: discord.Member, delta:int=1):
		"""
		Uccide un membro di questo Server Discord
		"""
		

		### errors ###
		if delta <= 0:
			raise discord.ext.commands.BadArgument(f"`{delta}` non è un numero valido.")
		if delta > 5:
			delta = 5
			member = context.message.author

		if member == self.bot.user:
			raise discord.ext.commands.BadArgument(f"Non è possibile uccidere {member.mention}.")

		guild_id = context.guild.id
		member_id = member.id

		if context.guild.id == 792523466040803368: # ⛩| Holy Quindecimᴵᵗᵃ
			if await self.bot.is_owner(member):
				raise discord.ext.commands.BadArgument(f"Non è possibile uccidere {member.mention}.")

		if guild_id in config.KILLED and member_id in config.KILLED[guild_id]:
			raise discord.ext.commands.BadArgument(f"L'utente {member.mention} è già morto.")
		###############

		if guild_id not in config.KILLED:
			config.KILLED[guild_id] = {}

		config.KILLED[guild_id][member_id] = {
			"time": datetime.now(),
			"delta": timedelta(minutes=delta),
			"channel": context.channel.id
		}

		embed = discord.Embed(
			colour = discord.Colour.darker_gray()
		)
		embed.add_field(name="KILL", value=f"L'utente {member.mention} è morto e non potrà parlare per {delta*60} secondi.", inline=False)
		embed.set_footer(text=f"Kill eseguita da {context.message.author}")
		embed.set_thumbnail(url="https://media.tenor.com/images/1cb732f34c3b3f90d526fee50288912c/tenor.gif")
		await context.channel.send(embed=embed)

	@commands.command(name="suicide", aliases=["suicidio"])
	async def suicide(self, context):
		await self.kill(context, context.message.author)

	@commands.command(name="killinfo", aliases=["kinfo", "kill_info", "kinf"])
	@commands.check(check.has_role)
	async def killinfo(self, context):
		"""
		Restituisce le informazioni di chi è stato ucciso
		"""

		# guild_id = context.guild.id

		if len(config.KILLED) == 0:
			raise discord.ext.commands.BadArgument(f"Ancora nessun utente è morto.")

		embed = discord.Embed(
			title = "R.I.P.",
			colour = discord.Colour.darker_gray()
		)
		embed.set_thumbnail(url="https://media.tenor.com/images/1cb732f34c3b3f90d526fee50288912c/tenor.gif")

		for guild_id in config.KILLED:

			text = ""
			for member_id in config.KILLED[guild_id]:
				member = context.guild.get_member(member_id)
				las = datetime.now() - config.KILLED[guild_id][member_id]["time"]
				nex = config.KILLED[guild_id][member_id]["delta"] - las

				text += f"**\n{member.name}** | *{member.nick}*\n```Tempo trascorso: {str(las)}\nTempo rimasto: {str(nex)}```"

			embed.add_field(name=self.bot.get_guild(guild_id).name, value=text, inline=False)

		await context.channel.send(embed=embed)

	@commands.command(name='revive')
	async def revive(self, context, member:discord.User, sacrifice:discord.User=None):
		"""
		Fà risorgere una vita al prezzo di una vita.
		"""

		if sacrifice == None: sacrifice = context.message.author
		if not check.is_owner(context): sacrifice = context.message.author 

		guild_id = context.guild.id
		member_id = member.id


		if guild_id not in config.KILLED or member_id not in config.KILLED[guild_id]:
			raise discord.ext.commands.BadArgument(f"L'utente non {member.mention} è morto.")

		config.KILLED[guild_id][sacrifice.id] = config.KILLED[guild_id][member_id].copy()
		config.KILLED[guild_id].pop(member_id)

		embed = discord.Embed(
			colour = discord.Colour.teal()
		)
		embed.add_field(name="REVIVE", value=f"L'utente {sacrifice.mention} si è sacrificato per {member.mention}.", inline=False)
		# embed.set_thumbnail(url="https://media.tenor.com/images/096adb7ce60f35aa4d2ceb4243de0530/tenor.gif")
		await context.channel.send(embed=embed)

	@commands.command(name='killedit', aliases=['kedit', 'ked'])
	@commands.check(check.is_admin)
	async def killedit(self, context, member:discord.User, delta:int, guild_id:int=None):
		"""
		Modifica una morte.
		"""

		if guild_id==None:
			guild_id = context.guild.id
		member_id = member.id


		if guild_id not in config.KILLED or member_id not in config.KILLED[guild_id]:
			raise discord.ext.commands.BadArgument(f"L'utente non {member.mention} è morto.")

		config.KILLED[guild_id][member_id]["delta"]=timedelta(minutes=delta)

		embed = discord.Embed(
			colour = discord.Colour.teal()
		)
		embed.add_field(name="killedit", value=f"Il tempo di morte dell'utente {member.mention} è stato modificato a {delta*60} secondi.", inline=False)
		# embed.set_thumbnail(url="https://media.tenor.com/images/096adb7ce60f35aa4d2ceb4243de0530/tenor.gif")
		await context.channel.send(embed=embed)

def setup(bot):
	bot.add_cog(rip(bot))