from fastapi import APIRouter
from pydantic import BaseModel

from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/version",
    tags=["Version"],
)

class CreateVersionInput(BaseModel):
    project_id: int
    version: int

@router.post("/")
async def create_version(params: CreateVersionInput):
    version = db.Version(
        project_id=params.project_id,
        version=params.version,
    )
    with db.new_session() as session:
        session.add(version)
        session.commit()



