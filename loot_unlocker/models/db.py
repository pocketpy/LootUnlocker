from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

ImageToken = str


class Player(SQLModel, table=True):
    id: str = Field(primary_key=True)
    platform: str = Field(index=True)
    is_admin: bool = Field(default=False)
    
    nickname: str | None = Field(index=True, max_length=32, default=None)
    avatar: ImageToken | None = Field(default=None)
    access_token: str | None = Field(index=True, default=None)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Project(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    description: str = Field(default="")
    latest_version: int = Field(default=0)
    
    logo: ImageToken | None = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ProjectVersion(SQLModel, table=True):
    project_id: str = Field(primary_key=True)
    version: int = Field(primary_key=True)
    
    comment: str = Field(default="")
    data: str = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CloudSave(SQLModel, table=True):
    id: str = Field(primary_key=True)
    data: str = Field()
    index: int = Field()

    project_id: str = Field()
    project_version: int = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class CloudLog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    tags: str = Field()
    data: str = Field()

    project_id: str = Field()
    project_version: int = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class Ugc(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str = Field()
    data: str = Field()

    project_id: str = Field()
    project_version: int = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Image(SQLModel, table=True):
    token: ImageToken = Field(primary_key=True)
    base64: str = Field()
    base64_thumbnail: str | None = Field(default=None)
    project_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


class File(SQLModel, table=True):
    token: str = Field(primary_key=True)
    filename: str = Field()
    size: int = Field()
    project_id: str = Field()
    player_id: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)


if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql
    print(CreateTable(Player.__table__).compile(dialect=postgresql.dialect()))