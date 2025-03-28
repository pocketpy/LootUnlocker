from .project import router as project_router
from .version import router as version_router

def include_admin_routes(app):
    app.include_router(project_router)
    app.include_router(version_router)