import asyncio, discord
import config
from datetime import datetime, timedelta
from jobs.bot import bot

async def check_death(): # Controlla se il tempo di attesa di tutte le persone morte è finito
	member_chace = []

	for guild_id in config.KILLED:
		for member_id in config.KILLED[guild_id]:
			killData = check_death_member(guild_id, member_id)
			if isinstance(killData, dict):
				member_chace.append(killData)
	else:
		for killData in member_chace:
			guild_id = killData["guild_id"]
			member_id = killData["member_id"]
			channel_id = killData["channel_id"]

			remove_member_killed(guild_id, member_id)
			await send_respawn(member_id, channel_id)

def remove_member_killed(guild_id, member_id): # Rimuove un membro da dalla lista dei morti
	config.KILLED[guild_id].pop(member_id)

async def send_respawn(member_id, channel_id): # Invia la notifica di respawn
	channel = bot.get_channel(channel_id)

	embed = discord.Embed(
		colour = discord.Colour.teal()
	)
	embed.add_field(name="RESPAWN", value=f"L'utente <@{member_id}> è rinato.", inline=False)
	await channel.send(embed=embed)

def check_death_member(guild_id, member_id): # Controlla se una persona è morta

	if guild_id not in config.KILLED:
		return

	if member_id not in config.KILLED[guild_id]:
		return

	time = config.KILLED[guild_id][member_id]["time"]
	delta = config.KILLED[guild_id][member_id]["delta"]

	if datetime.now() >= (time + delta):
		channel_id = config.KILLED[guild_id][member_id]["channel"]

		return {
			"guild_id": guild_id,
			"member_id": member_id,
			"channel_id": channel_id
		}