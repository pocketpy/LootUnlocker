import os
import sys

print(os.getcwd())
sys.path.append(os.getcwd())

from loot_unlocker.models import db
from loot_unlocker.utils import hash_passwd, random_passwd

db.init_db(drop_old=True)

# insert a default admin user
passwd = random_passwd()
with db.new_session() as session:
    admin = db.Admin(
        username='admin',
        hash_passwd=hash_passwd(passwd),
    )
    session.add(admin)
    session.commit()

    print('username:', admin.username)
    print('passwd', passwd)

print('Database initialized')

with open('tests/admin_passwd.txt', 'w') as f:
    f.write(passwd)
