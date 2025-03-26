from fastapi import APIRouter

router = APIRouter(
    prefix="/api/project",
)

@router.post("/")
async def create_project():
    pass

@router.get("/")
async def list_projects():
    pass

@router.get("/{project_id}")
async def get_project(project_id: int):
    pass

@router.put("/{project_id}")
async def update_project(project_id: int):
    pass

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    pass

