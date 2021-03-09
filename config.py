import os

# Can be multiple prefixes, like this: ("!", "?")
BOT_PREFIX = (">")
TOKEN = os.getenv('TOKEN')

KILLED = {} # Persone uccise
BANNED = set() # Persone bannate