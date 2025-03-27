from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.dialects.postgresql import JSONB, JSON

ImageToken = str

def new_session():
    engine = create_engine(...)
    return Session(engine)


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
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    id: int | None = Field(default=None, primary_key=True)

    hash_passwd: str = Field()
    channel: str = Field(index=True)
    is_ugc_admin: bool = Field(default=False)
    
    nickname: str | None = Field(index=True, max_length=32, default=None)
    avatar: ImageToken | None = Field(default=None)

    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Save(SQLModel, table=True):
    player_id: int = Field(foreign_key="player.id", primary_key=True)
    key: str = Field(primary_key=True)

    data: bytes = Field()

    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Log(SQLModel, table=True):
    player_id: int = Field(foreign_key="player.id", primary_key=True)
    id: int | None = Field(default=None, primary_key=True)

    text: str = Field()

    project_version: int = Field(default=0)
    extras: dict = Field(default={}, sa_type=JSONB)
    created_at: datetime = Field(default_factory=datetime.now)


class Ugc(SQLModel, table=True):
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    id: int | None = Field(default=None, primary_key=True)

    type: str = Field()
    data: bytes = Field()
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

    player_id: str = Field(foreign_key="player.id")
    created_at: datetime = Field(default_factory=datetime.now)


class File(SQLModel, table=True):
    token: ImageToken = Field(primary_key=True)

    data: bytes = Field()
    size: int = Field()
    filename: str | None = Field(default=None)

    player_id: str = Field(foreign_key="player.id")
    created_at: datetime = Field(default_factory=datetime.now)


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql
    print(CreateTable(Ugc.__table__).compile(dialect=postgresql.dialect()))