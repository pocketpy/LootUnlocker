from fastapi import APIRouter, HTTPException, Request, Depends, Response, File
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import uuid

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/image",
    dependencies=[Depends(get_current_player)],
    tags=["Image"],
)

class UploadImageOutput(BaseModel):
    token: str

@router.post("/", response_model=UploadImageOutput)
async def upload_image(request: Request, file: bytes = File(...)):
    player: db.Player = request.state.player
    token = uuid.uuid4().hex
    try:
        pil_image = Image.open(BytesIO(file))
    except:
        raise HTTPException(400)
    
    data = pil_image.tobytes('png')
    with db.new_session() as session:
        image = db.Image(
            token=token,
            player_id=player.id,
            data=data,
            data_thumbnail=None
        )
        session.add(image)
        session.commit()
    return UploadImageOutput(token=token)


@router.get("/{token}")
async def download_image(token: str):
    with db.new_session() as session:
        image = session.get(db.Image, token)
        if image is None:
            raise HTTPException(404)
        return Response(content=image.data, media_type="image/png")


@router.get("/thumbnail/{token}")
async def download_thumbnail(token: str):
    with db.new_session() as session:
        image = session.get(db.Image, token)
        if image is None:
            raise HTTPException(404)
        
        if image.data_thumbnail is None:
            pil_image = Image.open(BytesIO(image.data))
            pil_image.thumbnail((64, 64))
            image.data_thumbnail = pil_image.tobytes('png')
            session.commit()
        return Response(content=image.data_thumbnail, media_type="image/png")