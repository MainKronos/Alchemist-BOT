import asyncio, discord
import config
from jobs.bot import bot

async def status_task():
	while True:
		try:
			await bot.change_presence(activity=discord.Activity(name="video ecchi", type=discord.ActivityType.watching))
			await asyncio.sleep(30)
			await bot.change_presence(activity=discord.Activity(name="manga hentai", type=discord.ActivityType.watching))
			await asyncio.sleep(30)
		except Exception:
			pass
