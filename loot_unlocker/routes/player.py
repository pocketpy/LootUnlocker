from fastapi import APIRouter
from pydantic import BaseModel

from loot_unlocker.models import db
from loot_unlocker.utils import random_hex_string, salted_passwd_md5

router = APIRouter(
    prefix="/api/player",
    tags=["Player"],
)

class CreatePlayerInput(BaseModel):
    project_id: int
    channel: str
    project_version: int
    extras: dict = {}

class CreatePlayerOutput(BaseModel):
    id: int
    passwd: str

@router.post("/", response_model=CreatePlayerOutput)
async def create_player(params: CreatePlayerInput):
    passwd = random_hex_string(64)
    with db.new_session() as session:
        player = db.Player(
            hash_passwd=salted_passwd_md5(passwd),
            channel=params.channel,
            project_id=params.project_id,
            project_version=params.project_version,
            extras=params.extras,
        )
        session.add(player)
        session.commit()
        return CreatePlayerOutput(id=player.id, passwd=passwd)
