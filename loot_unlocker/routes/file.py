import uuid
from fastapi import APIRouter, Depends, Request, HTTPException, Response, UploadFile
from pydantic import BaseModel

from loot_unlocker.middlewares import get_current_player
from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/file",
    dependencies=[Depends(get_current_player)],
    tags=["File"],
)

class UploadFileOutput(BaseModel):
    token: str

@router.post("/", response_model=UploadFileOutput)
async def upload_file(request: Request, file: UploadFile):
    player: db.Player = request.state.player
    token = uuid.uuid4().hex
    data = await file.read()
    size = len(data)

    if size > 1024 * 1024 * 16:
        raise HTTPException(400, "File too large")
    
    with db.new_session() as session:
        file = db.File(
            token=token,
            data=data,
            filename=file.filename,
            size=size,
            player_id=player.id,
        )
        session.add(file)
        session.commit()
    return UploadFileOutput(token=token)


@router.get("/{token}")
async def download_file(token: str):
    with db.new_session() as session:
        file = session.get(db.File, token)
        if file is None:
            raise HTTPException(404)
        return Response(content=file.data, media_type="application/octet-stream")