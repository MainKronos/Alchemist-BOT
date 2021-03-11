import os, sys, discord
from discord.ext import commands
from jobs import check
import config
import json, random, requests

from PIL import *
from PIL import ImageFilter
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

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="burn.png"))

	@im.command(name='trash')
	async def trash(self, ctx, user:discord.User):
		"""
		Trash
		"""

		process_img = "trash.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		avatar = avatar.resize((309, 309))
		avatar = avatar.filter(ImageFilter.BLUR)

		process_img.paste(avatar, (309, 0))

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="trash.png"))

	@im.command(name='delete')
	async def delete(self, ctx, user:discord.User):
		"""
		delete
		"""

		process_img = "delete.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		avatar = avatar.resize((195, 195))

		process_img.paste(avatar, (120, 135))

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="delete.png"))

	@im.command(name='hitler')
	async def hitler(self, ctx, user:discord.User):
		"""
		hitler
		"""

		process_img = "hitler.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		avatar = avatar.resize((140, 140))

		process_img.paste(avatar, (46, 43))

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="hitler.png"))

def setup(bot):
	bot.add_cog(image_processing(bot))