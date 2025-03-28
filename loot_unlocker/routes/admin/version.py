from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from loot_unlocker.models import db
from loot_unlocker.middlewares import get_admin_username

router = APIRouter(
    prefix="/api/admin/version",
    tags=["Admin"],
    dependencies=[Depends(get_admin_username)],
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
