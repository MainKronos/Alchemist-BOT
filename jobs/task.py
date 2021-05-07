import asyncio, discord
import config
from jobs.bot import bot
from jobs import utils

async def status_task():
	while True:
		await bot.change_presence(activity=discord.Activity(name="video ecchi", type=discord.ActivityType.watching))
		await asyncio.sleep(30)
		await bot.change_presence(activity=discord.Activity(name="manga hentai", type=discord.ActivityType.watching))
		await asyncio.sleep(30)

async def check_death_task():
	while True:
		await utils.check_death()
		await asyncio.sleep(10)