from pydantic import BaseModel, EmailStr
from typing import List, TypeAlias

from kvmworkflows.models.subscription_types import SubscriptionType


class Subscription(BaseModel):
    id: str
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: str
    subscription_type: SubscriptionType


Subscriptions: TypeAlias = List[Subscription]
