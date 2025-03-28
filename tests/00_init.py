import os
import sys

print(os.getcwd())
sys.path.append(os.getcwd())

from loot_unlocker.models import db

admin = db.init_db()

print('admin.username:', admin[0])
print('admin.password:', admin[1])

print('Database initialized')

with open('tests/admin_passwd.txt', 'w') as f:
    f.write(admin[1])
