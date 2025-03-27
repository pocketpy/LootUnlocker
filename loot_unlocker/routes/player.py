from fastapi import APIRouter
from pydantic import BaseModel

from loot_unlocker.models.db import Player, new_session
from loot_unlocker.utils import random_hex_string, salted_passwd_md5

router = APIRouter(
    prefix="/api/player",
)

class CreatePlayerInput(BaseModel):
    project_id: int
    channel: str
    project_version: int
    extras: dict = {}

class CreatePlayerOutput(BaseModel):
    id: int
    passwd: str

@router.post("/")
async def create_player(params: CreatePlayerInput):
    passwd = random_hex_string(64)
    player = Player(
        project_id=params.project_id,
        hash_passwd=salted_passwd_md5(passwd),
        channel=params.channel,
        project_version=params.project_version,
        extras=params.extras,
    )
    with new_session() as session:
        session.add(player)
        session.commit()
    return CreatePlayerOutput(id=player.id, passwd=passwd)
