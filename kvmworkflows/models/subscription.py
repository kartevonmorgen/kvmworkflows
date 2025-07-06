from pydantic import BaseModel, EmailStr, computed_field
from typing import List, TypeAlias

from kvmworkflows.models.subscription_types import EntrySubscriptionType
from kvmworkflows.config.config import config


class Subscription(BaseModel):
    id: str
    title: str
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: str
    subscription_type: EntrySubscriptionType

    @computed_field
    @property
    def unsubscribe_url(self) -> str:
        return f"{config.email.unsubscribe_url}/{self.id}"


Subscriptions: TypeAlias = List[Subscription]
