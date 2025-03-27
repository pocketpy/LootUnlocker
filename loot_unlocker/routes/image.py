from fastapi import APIRouter, HTTPException, Request, Depends, Response, File
from pydantic import BaseModel
import uuid

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/image",
    dependencies=[Depends(get_current_player)]
)

class UploadImageOutput(BaseModel):
    token: str

@router.post("/")
async def upload_image(request: Request, file: bytes = File(...)):
    player: db.Player = request.state.player
    token = uuid.uuid4().hex
    with db.new_session() as session:
        image = db.Image(
            token=token,
            player_id=player.id,
            data=file,
            data_thumbnail=NotImplemented
        )
        session.add(image)
        session.commit()
    return UploadImageOutput(token=token)


@router.get("/{token}")
async def download_image(request: Request, token: str):
    player: db.Player = request.state.player
    with db.new_session() as session:
        image = session.get(db.Image, token)
        if image is None:
            raise HTTPException(404)
        return Response(content=image.data, media_type="image/png")


@router.get("/thumbnail/{token}")
async def download_thumbnail(request: Request, token: str):
    player: db.Player = request.state.player
    with db.new_session() as session:
        image = session.get(db.Image, token)
        if image is None:
            raise HTTPException(404)
        return Response(content=image.data_thumbnail, media_type="image/png")