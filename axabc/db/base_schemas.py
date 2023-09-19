from datetime import datetime
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

