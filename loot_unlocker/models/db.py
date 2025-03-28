from datetime import datetime
from sqlmodel import Field, Session, SQLModel
from sqlalchemy.dialects.postgresql import JSONB, JSON

from loot_unlocker.env import get_sql_engine

ImageToken = str


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    logo: ImageToken | None = Field(default=None)
    latest_version: int = Field(default=0)

    description: str = Field(default="")
    config: dict = Field(default={}, sa_type=JSON)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Version(SQLModel, table=True):
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    version: int = Field(primary_key=True)
    
    description: str = Field(default="")
    config: dict = Field(default={}, sa_type=JSON)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    hash_passwd: str = Field()
    channel: str = Field(index=True)
    
    nickname: str | None = Field(index=True, max_length=32, default=None)
    avatar: ImageToken | None = Field(default=None)

    project_id: int = Field(foreign_key="project.id")
    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Save(SQLModel, table=True):
    player_id: int = Field(foreign_key="player.id", primary_key=True)
    key: str = Field(primary_key=True)

    text: str = Field()

    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Log(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    text: str = Field()

    player_id: int = Field(foreign_key="player.id")
    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)


class Ugc(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    type: str = Field(index=True)
    text: str = Field()
    project_id: int = Field(foreign_key="project.id", index=True)

    is_public: bool = Field(default=False)

    player_id: int = Field(foreign_key="player.id")
    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Image(SQLModel, table=True):
    token: ImageToken = Field(primary_key=True)
    
    data: bytes = Field()
    data_thumbnail: bytes | None = Field(default=None)

    player_id: int = Field(foreign_key="player.id")
    created_at: datetime = Field(default_factory=datetime.now)


class File(SQLModel, table=True):
    token: ImageToken = Field(primary_key=True)

    data: bytes = Field()
    size: int = Field()
    filename: str | None = Field(default=None)

    player_id: int = Field(foreign_key="player.id")
    created_at: datetime = Field(default_factory=datetime.now)


def new_session():
    return Session(get_sql_engine())

def init_db(drop_old=False):
    engine = get_sql_engine()
    if drop_old:
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

