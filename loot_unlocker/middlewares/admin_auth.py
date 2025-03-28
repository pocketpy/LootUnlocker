from loot_unlocker.models import db
from loot_unlocker.utils import hash_passwd

from fastapi import HTTPException, Request

def get_admin_username(request: Request):
    req_username = request.headers.get("x-admin-username")
    req_passwd = request.headers.get("x-admin-passwd")
    with db.new_session() as session:
        admin = session.get(db.Admin, req_username)
        if admin is None or admin.hash_passwd != hash_passwd(req_passwd):
            raise HTTPException(401, detail="Invalid admin username or passwd")
        request.state.admin = admin
    return admin.username

