import os, sys, discord
from discord.ext import commands
from jobs import check
import config
import json, random, requests

from PIL import *
from PIL import ImageFilter, ImageDraw, Image, ImageSequence
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

		process_img = "fire.gif"

		burnfile=f"{self.localFolder}/{process_img}"
		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()


		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		fire = Image.open(burnfile)

		avatar = avatar.resize((500, 500))
		# fire = fire.resize((500, 500))

		frames = []

		for frame in ImageSequence.Iterator(fire):
			frame = frame.convert("RGBA").resize((500, 500))
			burninate = Image.blend(avatar.copy(), frame, alpha=0.7)
			frames.append(burninate)


		final_buffer = BytesIO()
		frames[0].save(final_buffer, format="GIF", save_all=True, append_images=frames[1:], optimize=False, loop=0)
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="burn.gif"))

	@im.command(name='salt')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def salt(self, ctx, user:discord.User):
		"""
		Metti un po' di sale.
		"""

		process_img = "salt.gif"

		saltfile=f"{self.localFolder}/{process_img}"
		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()


		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		salt = Image.open(saltfile)

		avatar = avatar.resize((500, 500))

		frames = []

		for frame in ImageSequence.Iterator(salt):
			frame = frame.convert("RGBA").resize((500, 500))

			new_frame = avatar.copy()
			
			new_frame.paste(frame, mask=frame) 
			frames.append(new_frame)


		final_buffer = BytesIO()
		frames[0].save(final_buffer, format="GIF", save_all=True, append_images=frames[1:], optimize=False, loop=0)
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="burn.gif"))

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

	@im.command(name='bed')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def bed(self, ctx, user1:discord.User, user2:discord.User):
		"""
		bed
		"""

		process_img = "bed.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes1 = await user1.avatar_url_as(format="png", size=1024).read()
		avatar_bytes2 = await user2.avatar_url_as(format="png", size=1024).read()

		avatar1 = Image.open(BytesIO(avatar_bytes1)).convert("RGBA")
		avatar2 = Image.open(BytesIO(avatar_bytes2)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask1 = Image.new("L", (100, 100), 0)
		mask2 = Image.new("L", (70, 70), 0)

		draw = ImageDraw.Draw(mask1)
		draw.ellipse((0, 0, 100, 100), fill=255)
		draw = ImageDraw.Draw(mask2)
		draw.ellipse((0, 0, 70, 70), fill=255)

		avatar1 = avatar1.resize((100, 100))
		avatar1_2 = avatar1.resize((70, 70))
		avatar2 = avatar2.resize((70, 70))

		process_img.paste(avatar1, (25, 100), mask1)
		process_img.paste(avatar1, (25, 300), mask1)
		process_img.paste(avatar1_2, (53, 450), mask2)
		process_img.paste(avatar2, (53, 575), mask2)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="bed.png"))

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

	@im.command(name='affect')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def affect(self, ctx, user:discord.User):
		"""
		affect
		"""

		process_img = "affect.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		avatar = avatar.resize((200, 200)).crop((0, 21.5, 200, 178.5))

		process_img.paste(avatar, (180, 383))

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="affect.png"))

	@im.command(name='beautiful')
	@commands.cooldown(1, 2, commands.BucketType.guild)
	async def beautiful(self, ctx, user:discord.User):
		"""
		beautiful
		"""

		process_img = "beautiful.png"
		process_img=f"{self.localFolder}/{process_img}"

		avatar_bytes = await user.avatar_url_as(format="png", size=1024).read()

		avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
		process_img = Image.open(process_img).convert("RGBA").copy()

		mask = Image.new("RGBA", (376, 400), 0)

		avatar = avatar.resize((95, 95))
		mask.paste(avatar, (258, 28))
		mask.paste(avatar, (258, 229))

		process_img = Image.alpha_composite(mask, process_img)

		final_buffer = BytesIO()
		process_img.save(final_buffer, "png")
		final_buffer.seek(0)

		await ctx.channel.send(file=discord.File(fp=final_buffer, filename="beautiful.png"))

def setup(bot):
	bot.add_cog(image_processing(bot))