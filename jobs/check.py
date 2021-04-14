import config
from discord.ext import commands

##### CHECK ######

def is_owner(ctx): # Se è lo sviluppatore
	owners = [520593633808875571, 173063242187276288] # Krónos, Teletta🌱
	return ctx.message.author.id in owners

def is_admin(ctx): # Se è amministratore
	if is_owner(ctx):
		return True

	return ctx.author.guild_permissions.administrator

def is_in_guild(guild_id): # Controlla se è nella gilda

	async def predicate(ctx):
		if is_owner(ctx):
			return True

		if ctx.guild and ctx.guild.id == guild_id:
			return True

		raise commands.CommandError("Questa Server non ha i permessi per eseguire questo comando.")
	return commands.check(predicate)

def has_role(role_id):
	async def predicate(ctx):
		if is_owner(ctx):
			return True

		if role_id in [x.id for x in ctx.author.roles]:
			return True

		raise commands.CommandError("Non hai il ruolo necessario per eseguire questo comando..")
	return commands.check(predicate)


def is_banned(ctx):
	return ctx.message.author.id in config.BANNED

################################ OTHER ##################################

def need_censura(ctx):
	# if is_admin(ctx):
	# 	return False

	if ctx.guild.id == 792523466040803368: # ⛩| Holy Quindecimᴵᵗᵃ
		whitelist = [781533713267163156] # SCIPOLA
		
		return ctx.author.id not in whitelist

	return False 

def is_alive(ctx): # Se è vivo
	guild_id = ctx.message.guild.id
	member_id = ctx.message.author.id

	if guild_id in config.KILLED and member_id in config.KILLED[guild_id]:
		return False
	else:
		return True