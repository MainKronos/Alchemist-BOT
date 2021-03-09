import os
# from importlib import import_module
from jobs.bot import *
from jobs.error import *
from jobs import check, task


# Carica tutti i moduli in jobs
# for job in os.listdir("jobs"):
# 	if job.endswith(".py") and job != "__init__.py":
# 		myjob = job.replace(".py", "")

# 		# import_module(f"jobs.{myjob}")
# 		module = __import__(f"{myjob}", locals(), globals(), fromlist=["*"], level=1)

# 		for k in dir(module):
# 			locals()[k] = getattr(module, k)
