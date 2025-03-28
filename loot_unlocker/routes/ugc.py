from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from sqlmodel import select

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models.db import Player, Ugc, new_session

router = APIRouter(
    prefix="/api/ugc",
    dependencies=[Depends(get_current_player)],
    tags=["Ugc"],
)

class UploadUgcInput(BaseModel):
    type: str
    text: str
    extras: dict = {}
    
class UploadUgcOutput(BaseModel):
    id: int

@router.post("/", response_model=UploadUgcOutput)
async def upload_ugc(request: Request, params: UploadUgcInput):
    player: Player = request.state.player
    with new_session() as session:
        ugc = Ugc(
            type=params.type,
            text=params.text,
            player_id=player.id,
            project_id=player.project_id,
            project_version=player.project_version,
            extras=params.extras
        )
        session.add(ugc)
        session.commit()
        return UploadUgcOutput(id=ugc.id)


class UpdateUgcInput(BaseModel):
    type: str
    text: str
    extras: dict = {}

@router.put("/{ugc_id}")
async def update_ugc(request: Request, ugc_id: int, params: UpdateUgcInput):
    player: Player = request.state.player
    with new_session() as session:
        ugc = session.get(Ugc, ugc_id)
        if ugc is None:
            raise HTTPException(404)
        if ugc.player_id != player.id:
            raise HTTPException(403)
        ugc.type = params.type
        ugc.text = params.text
        ugc.extras = params.extras
        session.commit()


@router.get("/{ugc_id}", response_model=Ugc)
async def download_ugc(request: Request, ugc_id: int):
    player: Player = request.state.player
    with new_session() as session:
        ugc = session.get(Ugc, ugc_id)
        if ugc is None:
            raise HTTPException(404)
        if player.project_id != ugc.project_id:
            raise HTTPException(403)
        if not ugc.is_public and ugc.player_id != player.id:
            raise HTTPException(403)
        return ugc
    

@router.delete("/{ugc_id}")
async def delete_ugc(request: Request, ugc_id: int):
    player: Player = request.state.player
    with new_session() as session:
        ugc = session.get(Ugc, ugc_id)
        if ugc is None:
            raise HTTPException(status_code=404)
        if ugc.player_id != player.id:
            raise HTTPException(status_code=403)
        session.delete(ugc)
        session.commit()


class ListUgcOutput(BaseModel):
    items: list[Ugc]

@router.get("/", response_model=ListUgcOutput)
async def list_ugc(request: Request, limit: int = 20, offset: int = 0):
    player: Player = request.state.player
    with new_session() as session:
        sql = select(Ugc).where(Ugc.player_id == player.id).limit(limit).offset(offset)
        items = session.exec(sql).all()
        return ListUgcOutput(items=items)
