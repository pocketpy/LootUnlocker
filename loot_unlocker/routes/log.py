from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/log",
    dependencies=[Depends(get_current_player)],
    tags=["Log"],
)

class UploadLogInputItem(BaseModel):
    text: str
    extras: dict = {}

class UploadLogInput(BaseModel):
    items: list[UploadLogInputItem]


@router.post("/")
async def upload_log(request: Request, params: UploadLogInputItem):
    player: db.Player = request.state.player
    with db.new_session() as session:
        log = db.Log(
            player_id=player.id,
            text=params.text,
            project_version=player.project_version,
            extras=params.extras
        )
        session.add(log)
        session.commit()


@router.post("/batch")
async def upload_log_batch(request: Request, params: UploadLogInput):
    player: db.Player = request.state.player
    with db.new_session() as session:
        for item in params.items:
            log = db.Log(
                player_id=player.id,
                text=item.text,
                project_version=player.project_version,
                extras=item.extras
            )
            session.add(log)
        session.commit()

    
