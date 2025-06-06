# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, List, Optional

from .base_model import BaseModel


class GetActiveSubscriptionsByInterval(BaseModel):
    subscriptions: List["GetActiveSubscriptionsByIntervalSubscriptions"]


class GetActiveSubscriptionsByIntervalSubscriptions(BaseModel):
    email: str
    id: Any
    interval: str
    language: Optional[str]
    lat_max: Any
    lat_min: Any
    lon_max: Any
    lon_min: Any
    subscription_type: Any
    title: str


GetActiveSubscriptionsByInterval.model_rebuild()
