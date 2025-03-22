from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from uuid import UUID

from kvmworkflows.graphql.client import graphql_client
from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.models.subscription_types import SubscriptionType


router = APIRouter()


class CreateSubscriptionRequest(BaseModel):
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: SubscriptionInterval
    subscription_type: SubscriptionType


class SubscriptionResponse(BaseModel):
    id: UUID
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: SubscriptionInterval
    subscription_type: SubscriptionType


@router.post("/subscribe")
async def create_subscription(subscription: CreateSubscriptionRequest) -> SubscriptionResponse:
    subscriptions_response = await graphql_client.get_exact_subscriptions(
        email=subscription.email,
        interval=subscription.interval,
        lat_min=subscription.lat_min,
        lon_min=subscription.lon_min,
        lat_max=subscription.lat_max,
        lon_max=subscription.lon_max,
        subscription_type=subscription.subscription_type,
    )

    if subscriptions_response.subscriptions:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Subscription already exists")
    
    insert_subscription_response = await graphql_client.insert_subscriptions_one(
        email=subscription.email,
        lat_min=subscription.lat_min,
        lon_min=subscription.lon_min,
        lat_max=subscription.lat_max,
        lon_max=subscription.lon_max,
        interval=subscription.interval,
        subscription_type=subscription.subscription_type
    )

    if insert_subscription_response.insert_subscriptions_one is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create subscription")
    
    subscription_id = insert_subscription_response.insert_subscriptions_one.id

    response = SubscriptionResponse(
        id=subscription_id,
        email=subscription.email,
        lat_min=subscription.lat_min,
        lon_min=subscription.lon_min,
        lat_max=subscription.lat_max,
        lon_max=subscription.lon_max,
        interval=subscription.interval,
        subscription_type=subscription.subscription_type,
    )

    return response


@router.get("/unsubscribe/{subscription_id}")
async def delete_subscription(subscription_id: str) -> SubscriptionResponse:
    delete_subscription_response = await graphql_client.delete_subscriptions_by_pk(id=subscription_id)
    if delete_subscription_response.delete_subscriptions_by_pk is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    
    deleted_subscription = delete_subscription_response.delete_subscriptions_by_pk

    response = SubscriptionResponse(
        id=deleted_subscription.id,
        email=deleted_subscription.email,
        lat_min=deleted_subscription.lat_min,
        lon_min=deleted_subscription.lon_min,
        lat_max=deleted_subscription.lat_max,
        lon_max=deleted_subscription.lon_max,
        interval=SubscriptionInterval(deleted_subscription.interval),
        subscription_type=SubscriptionType(deleted_subscription.subscription_type)
    )

    return response
