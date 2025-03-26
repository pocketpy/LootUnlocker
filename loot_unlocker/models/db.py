from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Player(SQLModel, table=True):
    id: str = Field(primary_key=True)
    platform: str = Field(index=True)
    nickname: str = Field(index=True, max_length=32)
    avatar: str = Field()
    is_admin: bool = Field(default=False)
    access_token: str = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Project(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    description: str = Field()
    latest_version: int = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ProjectVersion(SQLModel, table=True):
    version: int = Field(primary_key=True)
    comment: str = Field(default="")
    data: str = Field()

    project_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CloudSave(SQLModel, table=True):
    id: str = Field(primary_key=True)
    data: str = Field()
    index: int = Field()

    version: int = Field()
    project_id: str = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class CloudLog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str = Field()
    data: str = Field()

    version: int = Field()
    project_id: str = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class Ugc(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str = Field()
    data: str = Field()

    version: int = Field()
    project_id: str = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class Image(SQLModel, table=True):
    id: str = Field(primary_key=True)
    base64: str = Field()
    base64_thumbnail: str = Field(default="")
    project_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class File(SQLModel, table=True):
    id: str = Field(primary_key=True)
    filename: str = Field()
    size: int = Field()
    project_id: str = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql
    print(CreateTable(Player.__table__).compile(dialect=postgresql.dialect()))