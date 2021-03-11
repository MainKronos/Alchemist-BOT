import os, sys, discord
from discord.ext import commands
from jobs import check
import config
import json, random, requests

from PIL import *
from PIL import ImageFilter, ImageDraw 
from io import BytesIO

# @commands.cooldown(1, 600, commands.BucketType.category)

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
	@commands.cooldown(1, 2, commands.BucketType.guild)
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
	@commands.cooldown(1, 2, commands.BucketType.guild)
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
	@commands.cooldown(1, 2, commands.BucketType.guild)
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
	@commands.cooldown(1, 2, commands.BucketType.guild)
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

	@im.command(name='rip')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def rip(self, ctx, user:discord.User):
		"""
		rip
		"""

		process_img = "rip.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask = Image.new("RGBA", (720, 405), 0)

		avatar = avatar.resize((85, 85))
		mask.paste(avatar, (110, 47))

		process_img = Image.alpha_composite(mask, process_img)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="rip.png"))

	@im.command(name='facepalm')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def facepalm(self, ctx, user:discord.User):
		"""
		facepalm
		"""

		process_img = "facepalm.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask = Image.new("RGBA", (632, 357), 0)

		avatar = avatar.resize((255, 255)).crop((10, 10, 245, 245))
		mask.paste(avatar, (199, 112))

		process_img = Image.alpha_composite(mask, process_img)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="facepalm.png"))

	@im.command(name='kiss')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def kiss(self, ctx, user1:discord.User, user2:discord.User):
		"""
		kiss
		"""

		process_img = "kiss.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes1 = await user1.avatar_url_as(format="png", size=1024).read()
		avatar_bytes2 = await user2.avatar_url_as(format="png", size=1024).read()

		avatar1 = Image.open(BytesIO(avatar_bytes1)).convert("RGBA")
		avatar2 = Image.open(BytesIO(avatar_bytes2)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask = Image.new("L", (200, 200), 0)

		draw = ImageDraw.Draw(mask)
		draw.ellipse((0, 0, 200, 200), fill=255)

		avatar1 = avatar1.resize((200, 200))
		avatar2 = avatar2.resize((200, 200))

		process_img.paste(avatar1, (150, 25), mask)
		process_img.paste(avatar2, (350, 25), mask)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="kiss.png"))

	@im.command(name='spank')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def spank(self, ctx, user1:discord.User, user2:discord.User):
		"""
		spank
		"""

		process_img = "spank.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes1 = await user1.avatar_url_as(format="png", size=1024).read()
		avatar_bytes2 = await user2.avatar_url_as(format="png", size=1024).read()

		avatar1 = Image.open(BytesIO(avatar_bytes1)).convert("RGBA")
		avatar2 = Image.open(BytesIO(avatar_bytes2)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask = Image.new("L", (140, 140), 0)

		draw = ImageDraw.Draw(mask)
		draw.ellipse((0, 0, 140, 140), fill=255)

		avatar1 = avatar1.resize((140, 140))
		avatar2 = avatar2.resize((140, 140))

		process_img.paste(avatar1, (350, 220), mask)
		process_img.paste(avatar2, (225, 5), mask)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="spank.png"))

	@im.command(name='leader')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def leader(self, ctx, user:discord.User):
		"""
		leader
		"""

		process_img = "leader.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask = Image.new("RGBA", (600, 539), 0)

		avatar = avatar.resize((135, 135))
		mask.paste(avatar, (350, 20))

		process_img = Image.alpha_composite(mask, process_img)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="leader.png"))


def setup(bot):
	bot.add_cog(image_processing(bot))