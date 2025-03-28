from fastapi import APIRouter, HTTPException, Request, Depends, Response
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
async def upload_image(request: Request, max_width: int = 1024, max_height: int = 1024):
    player: db.Player = request.state.player
    token = uuid.uuid4().hex
    try:
        pil_image = Image.open(BytesIO(await request.body()))
    except:
        raise HTTPException(400)
    
    aspect_ratio = pil_image.width / pil_image.height
    if pil_image.width > max_width:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
        pil_image = pil_image.resize((new_width, new_height))

    if pil_image.height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
        pil_image = pil_image.resize((new_width, new_height))
    
    data = BytesIO()
    pil_image.save(data, format="PNG")
    
    with db.new_session() as session:
        image = db.Image(
            token=token,
            player_id=player.id,
            data=data.getvalue(),
            width=pil_image.width,
            height=pil_image.height
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

