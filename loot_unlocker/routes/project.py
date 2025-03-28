from fastapi import APIRouter
from pydantic import BaseModel

from loot_unlocker.models import db

router = APIRouter(
    prefix="/api/project",
    tags=["Project"],
)

class CreateProjectInput(BaseModel):
    name: str
    description: str
    extras: dict = {}

class CreateProjectOutput(BaseModel):
    id: int

@router.post("/", response_model=CreateProjectOutput)
async def create_project(params: CreateProjectInput):
    with db.new_session() as session:
        project = db.Project(
            name=params.name,
            description=params.description,
            extras=params.extras,
        )
        session.add(project)
        session.commit()

        version = db.Version(
            project_id=project.id,
            version=0,
        )
        session.add(version)
        session.commit()
        return CreateProjectOutput(id=project.id)


