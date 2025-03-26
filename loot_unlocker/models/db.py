from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Player(SQLModel, table=True):
    id: str = Field(primary_key=True)
    platform: str = Field(index=True)
    nickname: str = Field(index=True)
    is_admin: bool = Field(default=False)
    access_token: str = Field()

class Project(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    description: str = Field()

class CloudSave(SQLModel, table=True):
    project_id: str = Field(foreign_key="project.id")
    player_id: str = Field(foreign_key="player.id")
    data: str = Field()
    version: str = Field()
    created_at: datetime = Field(default=datetime.now)

class CloudLog(SQLModel, table=True):
    project_id: str = Field(foreign_key="project.id")
    player_id: str = Field(foreign_key="player.id")
    data: str = Field()
    created_at: datetime = Field(default=datetime.now)

class Ugc(SQLModel, table=True):
    project_id: str = Field(foreign_key="project.id")
    player_id: str = Field(foreign_key="player.id")
    type: str = Field()
    data: str = Field()
    created_at: datetime = Field(default=datetime.now)
