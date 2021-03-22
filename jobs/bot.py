import discord
from discord.ext.commands import Bot
from discord.ext import commands
import config
import locale

class MyHelpCommand(commands.DefaultHelpCommand):
	async def send_command_help(self, command):
		embed = discord.Embed(
			title = f">{command.name}",
			colour = discord.Colour.orange(),
			description = f"```{command.help}```"
		)
		embed.add_field(name=f"Utilizzo", value=f"```dust\n{command.usage}\n```", inline=False)
		destination = self.get_destination()
		await destination.send(embed=embed)

	async def send_pages(self):

		embed = discord.Embed(
			title = "HELP",
			colour = discord.Colour.orange()
		)

		destination = self.get_destination()
		prefix = config.BOT_PREFIX[0]
		for i in bot.cogs:
			cog = bot.get_cog(i.lower())
			if cog == None: continue
			commands = cog.get_commands()
			if len(commands) == 0: continue
			command_list = [command.name for command in commands]
			command_description = [command.help for command in commands]
			help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
			embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)

		await destination.send(embed=embed)

	async def send_error_message(self, error):
		raise discord.ext.commands.BadArgument(error)

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

intents = discord.Intents.all()

bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents, help_command=MyHelpCommand())