# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, List

from .base_model import BaseModel


class GetSubscriptionsByFilter(BaseModel):
    subscriptions: List["GetSubscriptionsByFilterSubscriptions"]


class GetSubscriptionsByFilterSubscriptions(BaseModel):
    id: Any


GetSubscriptionsByFilter.model_rebuild()
