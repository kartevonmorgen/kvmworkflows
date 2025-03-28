# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, Optional

from .base_model import BaseModel


class InsertSubscriptionsOne(BaseModel):
    insert_subscriptions_one: Optional["InsertSubscriptionsOneInsertSubscriptionsOne"]


class InsertSubscriptionsOneInsertSubscriptionsOne(BaseModel):
    id: Any
    title: str
    email: str
    interval: str
    lat_min: Any
    lon_min: Any
    lat_max: Any
    lon_max: Any
    subscription_type: Any
    language: Optional[str]
    is_active: bool


InsertSubscriptionsOne.model_rebuild()
