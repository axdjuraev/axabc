from datetime import datetime
from pydantic import BaseModel, Field


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class BaseSchema(BaseModel):
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

    def jdict(self):
        res = self.dict()
        res['created_at'] = self.created_at and self.created_at.strftime(DATETIME_FORMAT)
        res['updated_at'] = self.updated_at and self.updated_at.strftime(DATETIME_FORMAT)
        return res

