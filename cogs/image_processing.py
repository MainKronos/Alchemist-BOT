import os, sys, discord
from discord.ext import commands
from jobs import check
import config
import json, random, requests

from PIL import Image
from io import BytesIO


class image_processing(commands.Cog, name="image processing"):
	def __init__(self, bot):
		self.bot = bot
		self.localFolder = "./img/image_processing"

	@commands.group(name="im", invoke_without_command=True)
	async def im(self, context):
		"""
		Invia la lista dei subcomandi per le 'image processing'.
		"""

		exCommand = self.bot.get_command("im") # Questo comando
		subcommands = [sub for sub in self.bot.walk_commands() if sub.parent == exCommand]

		sub_list = [sub.name for sub in subcommands]
		sub_description = [sub.help for sub in subcommands]

		txtdesc = '\n'.join(f'{n} - {h}' for n, h in zip(sub_list, sub_description)) # Decrizione subcomandi

		embed = discord.Embed(
			title="IMAGE PROCESSING",
			description=f'```{txtdesc}```',
			color=0x212121
		)
		await context.send(embed=embed)

	@im.command(name='burn')
	async def burn(self, ctx, user:discord.User):
		"""
		Brucia sul rogo qualcuno.
		"""

		process_img = "fire.png"

		burnfile=f"{self.localFolder}/{process_img}"
		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()


		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		fire = Image.open(burnfile).convert("RGBA")

		avatar = avatar.resize((500, 500))
		fire = fire.resize((500, 500))

		burninate = Image.blend(avatar, fire, alpha=0.7)

		final_buffer = BytesIO()
		burninate.save(final_buffer, "png")
		final_buffer.seek(0)

		# burninate.save("burninate.png")
		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="burn.png"))

def setup(bot):
	bot.add_cog(image_processing(bot))