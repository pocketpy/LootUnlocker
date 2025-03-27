from fastapi import HTTPException, Request
from sqlmodel import select

from loot_unlocker.models.db import Player, new_session
from loot_unlocker.utils import salted_passwd_md5

def get_current_player(request: Request):
    req_player_id = request.headers['x-player-id']
    req_player_passwd = request.headers['x-player-passwd']
    req_project_id = request.headers['x-project-id']
    req_project_version = request.headers['x-project-version']

    with new_session() as session:
        sql = select(Player).where(Player.id == int(req_player_id))
        player = session.exec(sql).first()
        if player is None or player.hash_passwd != salted_passwd_md5(req_player_passwd):
            raise HTTPException(401, detail="Invalid player id or password")
        if player.project_id != req_project_id:
            raise HTTPException(403, detail="Mismatched project id")
        if req_project_version != player.project_version:
            if req_project_version > player.project_version:
                player.project_version = req_project_version
                session.commit()
            else:
                raise HTTPException(400, detail="Invalid project version")
        request.state.player = player
        return player

