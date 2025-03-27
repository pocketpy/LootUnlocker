from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlmodel import select

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models.db import Player, Save, new_session

router = APIRouter(
    prefix="/api/save",
    dependencies=[Depends(get_current_player)]
)

class UploadSaveInput(BaseModel):
    key: str
    data: bytes
    extras: dict = {}

@router.post("/")
async def upload_save(request: Request, params: UploadSaveInput):
    player: Player = request.state.player
    with new_session() as session:
        sql = select(Save).where(Save.key == params.key)
        save = session.exec(sql).first()
        if save is not None:
            # update
            save.data = params.data
            save.extras = params.extras
        else:
            # insert
            save = Save(
                player_id=player.id,
                key=params.key,
                data=params.data,
                project_version=player.project_version,
                extras=params.extras
            )
            session.add(save)
        session.commit()


def download_save():
    pass


def list_saves():
    pass


def delete_save():
    pass