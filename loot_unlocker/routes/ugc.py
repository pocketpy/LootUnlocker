from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from sqlmodel import select

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models.db import Player, Ugc, new_session

router = APIRouter(
    prefix="/api/ugc",
    dependencies=[Depends(get_current_player)]
)

class UploadUgcInput(BaseModel):
    type: str
    data: bytes
    extras: dict = {}

@router.post("/")
async def upload_ugc(request: Request, params: UploadUgcInput):
    player: Player = request.state.player
    with new_session() as session:
        ugc = Ugc(
            player_id=player.id,
            project_id=player.project_id,
            type=params.type,
            data=params.data,
            extras=params.extras
        )
        session.add(ugc)
        session.commit()


class UpdateUgcInput(BaseModel):
    data: bytes
    extras: dict = {}

@router.put("/{ugc_id}")
async def update_ugc(request: Request, ugc_id: int, params: UpdateUgcInput):
    player: Player = request.state.player
    with new_session() as session:
        sql = select(Ugc).where(Ugc.id == ugc_id)
        ugc = session.exec(sql).first()
        if ugc is None:
            raise HTTPException(404)
        if not player.is_ugc_admin:
            if ugc.player_id != player.id:
                raise HTTPException(403)
        ugc.data = params.data
        ugc.extras = params.extras
        session.commit()


@router.get("/{ugc_id}")
async def download_ugc(request: Request, ugc_id: int):
    player: Player = request.state.player
    with new_session() as session:
        sql = select(Ugc).where(Ugc.id == ugc_id)
        ugc = session.exec(sql).first()
        if ugc is None:
            raise HTTPException(404)
        if not player.is_ugc_admin:
            if not ugc.is_public and ugc.player_id != player.id:
                raise HTTPException(403)
        return ugc
    

@router.delete("/{ugc_id}")
async def delete_ugc(request: Request, ugc_id: int):
    player: Player = request.state.player
    with new_session() as session:
        sql = select(Ugc).where(Ugc.id == ugc_id)
        ugc = session.exec(sql).first()
        if ugc is None:
            raise HTTPException(status_code=404)
        if not player.is_ugc_admin:
            if ugc.player_id != player.id:
                raise HTTPException(status_code=403)
        session.delete(ugc)
        session.commit()


@router.get("/")
async def list_ugc(request: Request, limit: int = 20, offset: int = 0):
    player: Player = request.state.player
    with new_session() as session:
        sql = select(Ugc).where(Ugc.player_id == player.id).limit(limit).offset(offset)
        return session.exec(sql).all()
