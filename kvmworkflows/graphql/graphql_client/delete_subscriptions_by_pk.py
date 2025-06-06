# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, Optional

from .base_model import BaseModel


class DeleteSubscriptionsByPk(BaseModel):
    delete_subscriptions_by_pk: Optional[
        "DeleteSubscriptionsByPkDeleteSubscriptionsByPk"
    ]


class DeleteSubscriptionsByPkDeleteSubscriptionsByPk(BaseModel):
    id: Any
    title: str
    email: str
    interval: str
    lat_min: Any
    lon_min: Any
    lat_max: Any
    lon_max: Any
    subscription_type: Any
    last_email_sent_at: Optional[Any]
    n_emails_sent: int
    language: Optional[str]
    is_active: bool


DeleteSubscriptionsByPk.model_rebuild()
