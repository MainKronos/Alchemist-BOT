import config

##### CHECK ######

def is_owner(ctx): # Se è lo sviluppatore
	owners = [173063242187276288]
	return ctx.message.author.id in owners

def is_admin(ctx): # Se è amministratore
	if is_owner(ctx):
		return True

	return ctx.author.guild_permissions.administrator

def has_role(ctx): # Settaggi particolari per gilda
	if is_admin(ctx):
		return True

	if ctx.guild.id == 792523466040803368: # ⛩| Holy Quindecimᴵᵗᵃ
		# return False # EVENTO
		return 795782994740379718 in [x.id for x in ctx.author.roles] # 795782994740379718 = 💎| Membro dello Staff •

	return True

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