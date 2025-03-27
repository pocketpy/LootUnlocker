from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .file import router as file_router
from .image import router as image_router
from .log import router as log_router
from .player import router as player_router
from .project import router as project_router
from .save import router as save_router
from .ugc import router as ugc_router
from .version import router as version_router

app = FastAPI(
    middleware=[CORSMiddleware(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )]
)

app.include_router(file_router)
app.include_router(image_router)
app.include_router(log_router)
app.include_router(player_router)
app.include_router(project_router)
app.include_router(save_router)
app.include_router(ugc_router)
app.include_router(version_router)
app.include_router(version_router)
