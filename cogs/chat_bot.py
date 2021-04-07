import os, sys, discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from jobs import check
import config
import requests, random, re

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer



class MyChatBot(commands.Cog, name="MyChatBot"): # MyChatBot
	def __init__(self, bot):
		self.bot = bot

		self.chat_bot = ChatBot(
			'Norman',
			storage_adapter='chatterbot.storage.SQLStorageAdapter',
			database_uri='sqlite:///database.sqlite3',
			logic_adapters=[
				'chatterbot.logic.MathematicalEvaluation',
				'chatterbot.logic.BestMatch']

			# read_only=True
		)
		# self.StartTrainer()

	def StartTrainer(self):
		trainer = ChatterBotCorpusTrainer(self.chat_bot)
		trainer.train(
			# "./CorpusTrainer/health.yml",
			# "./CorpusTrainer/history.yml",
			# "./CorpusTrainer/literature.yml",
			# "./CorpusTrainer/trivia.yml",
			"./CorpusTrainer/conversations.yml"
			# "./CorpusTrainer/food.yml",
			# "./CorpusTrainer/greetings.yml",
			# "./CorpusTrainer/ChatData.json"
		)

	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author == self.bot.user: return
		if message.channel.id != 829023211748327474: return
		if message.content.startswith(">"): return

		response = self.chat_bot.get_response(message.clean_content)
		await message.channel.send(response)


def setup(bot):
	bot.add_cog(MyChatBot(bot))