from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .file import router as file_router
from .image import router as image_router
from .log import router as log_router
from .player import router as player_router
from .save import router as save_router
from .ugc import router as ugc_router
from .admin import include_admin_routes

app = FastAPI(
    title="LootUnlocker API",
    docs_url="/api/docs",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    )

app.include_router(file_router)
app.include_router(image_router)
app.include_router(log_router)
app.include_router(player_router)
app.include_router(save_router)
app.include_router(ugc_router)
include_admin_routes(app)
