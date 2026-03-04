from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class InteractionLog(SQLModel, table=True):
    __tablename__ = "interacts"  # ✅ ИСПРАВЛЕНО

    id: int | None = Field(default=None, primary_key=True)
    learner_id: int = Field(...)
    item_id: int = Field(...)
    kind: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class InteractionLogCreate(BaseModel):
    learner_id: int
    item_id: int
    kind: str


class InteractionModel(BaseModel):
    id: int
    learner_id: int
    item_id: int
    kind: str
    created_at: datetime  # ✅