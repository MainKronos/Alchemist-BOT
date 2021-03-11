import os, sys, discord, platform, random, aiohttp, json
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

class general(commands.Cog, name="general"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="info", aliases=["botinfo"])
	async def info(self, context):
		"""
		Informazioni sul BOT.
		"""
		embed = discord.Embed(
			description="Alchemist BOT",
			color=0x00FF00
		)
		embed.set_author(
			name="Bot Information"
		)
		embed.add_field(
			name="Owner:",
			value="Krónos#9268",
			inline=True
		)
		embed.add_field(
			name="Python Version:",
			value=f"{platform.python_version()}",
			inline=True
		)
		embed.add_field(
			name="Prefix:",
			value=f"{config.BOT_PREFIX}",
			inline=False
		)
		embed.set_footer(
			text=f"Requested by {context.message.author}"
		)
		await context.send(embed=embed)

	@commands.command(name="serverinfo")
	async def serverinfo(self, context):
		"""
		Informazioni sul Server.
		"""
		server = context.message.guild
		roles = [x.name for x in server.roles]
		role_length = len(roles)
		if role_length > 50:
			roles = roles[:50]
			roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
		roles = ", ".join(roles)
		channels = len(server.channels)
		time = str(server.created_at)
		time = time.split(" ")
		time = time[0]

		embed = discord.Embed(
			title="**Server Name:**",
			description=f"{server}",
			color=0x00FF00
		)
		embed.set_thumbnail(
			url=server.icon_url
		)
		embed.add_field(
			name="Owner",
			value=f"`{server.owner}`"
		)
		embed.add_field(
			name="Server ID",
			value=f"`{server.id}`"
		)
		embed.add_field(
			name="Member Count",
			value=f"`{server.member_count}`"
		)
		embed.add_field(
			name="Text/Voice Channels",
			value=f"`{channels}`"
		)
		embed.add_field(
			name=f"Roles ({role_length})",
			value=f"`{roles}`"
		)
		embed.set_footer(
			text=f"Created at: {time}"
		)
		await context.send(embed=embed)

	@commands.command(name="ping")
	async def ping(self, context):
		"""
		Controlla se il BOT è vivo.
		"""
		embed = discord.Embed(
			color=0x00FF00
		)
		embed.add_field(
			name="Pong!",
			value=":ping_pong:",
			inline=True
		)
		embed.set_footer(
			text=f"Pong request by {context.message.author}"
		)
		await context.send(embed=embed)

	@commands.command(name="poll")
	@commands.cooldown(1, 5, commands.BucketType.guild)
	async def poll(self, context, *args):
		"""
		Crea una poll dove i mambri possono votare.
		"""
		poll_title = " ".join(args)
		embed = discord.Embed(
			title="Una nuova Poll è stata creata!",
			description=f"{poll_title}",
			color=0x00FF00
		)
		embed.set_footer(
			text=f"Poll creata da: {context.message.author} • React per votare!"
		)
		embed_message = await context.send(embed=embed)
		await embed_message.add_reaction("👍")
		await embed_message.add_reaction("👎")
		await embed_message.add_reaction("🤷")

def setup(bot):
	bot.add_cog(general(bot))