import os, sys, discord
from discord.ext.commands import Cog
from discord import app_commands
import photomaker
from io import BytesIO

# @commands.cooldown(1, 600, commands.BucketType.category)

class image_processing(Cog, name="image processing"):
	def __init__(self, bot):
		self.bot = bot
		self.localFolder = "./img/image_processing"

	ImgGroup = app_commands.Group(name="img", description="Image")

	@ImgGroup.command(name="burn")
	async def burn(self, interaction: discord.Interaction, user:discord.User):
		"""
		Brucia sul rogo qualcuno.
		"""

		final_img = photomaker.burn(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="burn.gif"))

	@ImgGroup.command(name="salt")
	async def salt(self, interaction: discord.Interaction, user:discord.User):
		"""
		Metti un po' di sale.
		"""

		final_img = photomaker.salt(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="salt.gif"))

	@ImgGroup.command(name="trash")
	async def trash(self, interaction: discord.Interaction, user:discord.User):
		"""
		Trash
		"""

		final_img = photomaker.trash(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="trash.png"))

	@ImgGroup.command(name="delete")
	async def delete(self, interaction: discord.Interaction, user:discord.User):
		"""
		delete
		"""

		final_img = photomaker.delete(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="delete.png"))

	@ImgGroup.command(name="hitler")
	async def hitler(self, interaction: discord.Interaction, user:discord.User):
		"""
		hitler
		"""

		final_img = photomaker.hitler(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="hitler.png"))

	@ImgGroup.command(name="rip")
	async def rip(self, interaction: discord.Interaction, user:discord.User):
		"""
		rip
		"""

		final_img = photomaker.rip(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="rip.png"))

	@ImgGroup.command(name="facepalm")
	async def facepalm(self, interaction: discord.Interaction, user:discord.User):
		"""
		facepalm
		"""

		final_img = photomaker.facepalm(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="facepalm.png"))

	@ImgGroup.command(name="kiss")
	async def kiss(self, interaction: discord.Interaction, user1:discord.User, user2:discord.User):
		"""
		kiss
		"""

		final_img = photomaker.kiss(await user1.display_avatar.read(), await user2.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="kiss.png"))

	@ImgGroup.command(name="bed")
	async def bed(self, interaction: discord.Interaction, user1:discord.User, user2:discord.User):
		"""
		bed
		"""

		final_img = photomaker.bed(await user1.display_avatar.read(), await user2.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="bed.png"))

	@ImgGroup.command(name="spank")
	async def spank(self, interaction: discord.Interaction, user1:discord.User, user2:discord.User):
		"""
		spank
		"""

		final_img = photomaker.spank(await user1.display_avatar.read(), await user2.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="spank.png"))

	@ImgGroup.command(name="leader")
	async def leader(self, interaction: discord.Interaction, user:discord.User):
		"""
		leader
		"""

		final_img = photomaker.leader(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="leader.png"))

	@ImgGroup.command(name="affect")
	async def affect(self, interaction: discord.Interaction, user:discord.User):
		"""
		affect
		"""

		final_img = photomaker.affect(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="affect.png"))

	@ImgGroup.command(name="beautiful")
	async def beautiful(self, interaction: discord.Interaction, user:discord.User):
		"""
		beautiful
		"""

		final_img = photomaker.beautiful(await user.display_avatar.read())

		await interaction.response.send_message(file=discord.File(fp=BytesIO(final_img), filename="beautiful.png"))

async def setup(bot):
	await bot.add_cog(image_processing(bot))