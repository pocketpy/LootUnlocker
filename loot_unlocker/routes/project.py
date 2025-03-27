from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from loot_unlocker.models.db import Project, new_session

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
    project = Project(
        name=params.name,
        description=params.description,
        extras=params.extras,
    )
    with new_session() as session:
        session.add(project)
        session.commit()
    return CreateProjectOutput(id=project.id)


