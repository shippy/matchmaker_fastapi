from datetime import datetime
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel
from typing import Any, Mapping, Optional

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    message: Mapping[str, Any] = Field(..., sa_column=Column(JSON))
    created_at: datetime