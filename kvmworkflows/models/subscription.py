from pydantic import BaseModel, EmailStr
from typing import List, TypeAlias


class Subscription(BaseModel):
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: str


Subscriptions: TypeAlias = List[Subscription]
