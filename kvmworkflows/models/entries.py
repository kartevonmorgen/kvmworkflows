from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import TypeAlias, List
from kvmworkflows.models.review_status import ReviewStatus


class Entry(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    status: ReviewStatus
    lat: float
    lng: float


Entries: TypeAlias = List[Entry]
