from fastapi import HTTPException, Request
from sqlmodel import select

from loot_unlocker.models.db import Player, new_session
from loot_unlocker.utils import hash_passwd

def get_current_player(request: Request):
    try:
        req_player_id = int(request.headers['x-player-id'])
        req_player_passwd = str(request.headers['x-player-passwd'])
        req_project_id = int(request.headers['x-project-id'])
        req_project_version = int(request.headers['x-project-version'])
    except (KeyError, ValueError):
        raise HTTPException(400, detail="Invalid headers")

    with new_session() as session:
        player = session.get(Player, req_player_id)
        if player is None or player.hash_passwd != hash_passwd(req_player_passwd):
            raise HTTPException(401, detail="Invalid player id or passwd")
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

