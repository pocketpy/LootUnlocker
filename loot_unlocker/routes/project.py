from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/project",
)

class CreateProjectInput(BaseModel):
    name: str
    description: str
    extras: dict = {}

class CreateProjectOutput(BaseModel):
    id: int

@router.post("/")
async def create_project(params: CreateProjectInput):
    project = db.Project(
        name=params.name,
        description=params.description,
        extras=params.extras,
    )
    with db.new_session() as session:
        session.add(project)
        session.commit()
    return CreateProjectOutput(id=project.id)


