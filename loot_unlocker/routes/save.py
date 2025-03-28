from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import select

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/save",
    dependencies=[Depends(get_current_player)],
    tags=["Save"],
)

class UploadSaveInput(BaseModel):
    key: str
    text: str
    extras: dict = {}

@router.post("/")
async def upload_save(request: Request, params: UploadSaveInput):
    player: db.Player = request.state.player
    with db.new_session() as session:
        sql = select(db.Save).where(db.Save.player_id == player.id, db.Save.key == params.key)
        save = session.exec(sql).first()
        if save is not None:
            # update
            save.text = params.text
            save.extras = params.extras
        else:
            # insert
            save = db.Save(
                player_id=player.id,
                key=params.key,
                text=params.text,
                project_version=player.project_version,
                extras=params.extras
            )
            session.add(save)
        session.commit()


@router.get("/{key}", response_model=db.Save)
async def download_save(request: Request, key: str):
    player: db.Player = request.state.player
    with db.new_session() as session:
        sql = select(db.Save).where(db.Save.player_id == player.id, db.Save.key == key)
        save = session.exec(sql).first()
        if save is None:
            raise HTTPException(404)
        if save.player_id != player.id:
            raise HTTPException(403)
        return save


class ListSaveOutputItem(BaseModel):
    key: str
    project_version: int
    extras: dict
    created_at: datetime
    updated_at: datetime

class ListSaveOutput(BaseModel):
    items: list[ListSaveOutputItem]

@router.get("/", response_model=ListSaveOutput)
async def list_save(request: Request, limit: int = 20, offset: int = 0):
    player: db.Player = request.state.player
    with db.new_session() as session:
        sql = select(db.Save).where(db.Save.player_id == player.id).limit(limit).offset(offset)
        saves = session.exec(sql).all()
        items = [ListSaveOutputItem(
                    key=save.key,
                    project_version=save.project_version,
                    extras=save.extras,
                    created_at=save.created_at,
                    updated_at=save.updated_at
                    ) for save in saves]
        return ListSaveOutput(items=items)


@router.delete("/{key}")
async def delete_save(request: Request, key: str):
    player: db.Player = request.state.player
    with db.new_session() as session:
        sql = select(db.Save).where(db.Save.player_id == player.id, db.Save.key == key)
        save = session.exec(sql).first()
        if save is None:
            raise HTTPException(404)
        session.delete(save)
        session.commit()