from fastapi import APIRouter
from pydantic import BaseModel

from loot_unlocker.models import db
from loot_unlocker.utils import hash_passwd, random_passwd

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
    passwd = random_passwd()
    with db.new_session() as session:
        player = db.Player(
            hash_passwd=hash_passwd(passwd),
            channel=params.channel,
            project_id=params.project_id,
            project_version=params.project_version,
            extras=params.extras,
        )
        session.add(player)
        session.commit()
        return CreatePlayerOutput(id=player.id, passwd=passwd)
