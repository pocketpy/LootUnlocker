import os
import sys

print(os.getcwd())
sys.path.append(os.getcwd())

from loot_unlocker.models import db

db.init_db(drop_old=True)

print('Database initialized')