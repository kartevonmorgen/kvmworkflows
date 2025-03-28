from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from uuid import UUID

from kvmworkflows.graphql.client import graphql_client
from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.models.subscription_types import EntrySubscriptionType
from kvmworkflows.models.supported_languages import SupportedLanguages


router = APIRouter()


class CreateSubscriptionRequest(BaseModel):
    title: str
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: SubscriptionInterval
    subscription_type: EntrySubscriptionType
    language: SupportedLanguages


class SubscriptionResponse(BaseModel):
    id: UUID
    title: str
    email: EmailStr
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float
    interval: SubscriptionInterval
    subscription_type: EntrySubscriptionType
    language: SupportedLanguages
    is_active: bool


@router.post("/subscribe", 
    responses={
        status.HTTP_200_OK: {"description": "Subscription created successfully"},
        status.HTTP_409_CONFLICT: {
            "description": "Similar subscription already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "message": "Similar subscription already exists",
                            "subscription": {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Failed to create subscription"}
    }
)
async def create_subscription(
    subscription: CreateSubscriptionRequest,
) -> SubscriptionResponse:
    subscriptions_response = await graphql_client.get_exact_subscriptions(
        email=subscription.email,
        interval=subscription.interval,
        lat_min=subscription.lat_min,
        lon_min=subscription.lon_min,
        lat_max=subscription.lat_max,
        lon_max=subscription.lon_max,
        subscription_type=subscription.subscription_type,
        language=subscription.language,
        is_active=True,
    )

    if subscriptions_response.subscriptions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Similar subscription already exists",
                "subscription": {
                    "id": subscriptions_response.subscriptions[0].id,
                },
            },
        )

    insert_subscription_response = await graphql_client.insert_subscriptions_one(
        title=subscription.title,
        email=subscription.email,
        lat_min=subscription.lat_min,
        lon_min=subscription.lon_min,
        lat_max=subscription.lat_max,
        lon_max=subscription.lon_max,
        interval=subscription.interval,
        subscription_type=subscription.subscription_type,
        language=subscription.language,
    )

    if insert_subscription_response.insert_subscriptions_one is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create subscription",
        )

    subscription_id = insert_subscription_response.insert_subscriptions_one.id

    response = SubscriptionResponse(
        id=subscription_id,
        title=subscription.title,
        email=subscription.email,
        lat_min=subscription.lat_min,
        lon_min=subscription.lon_min,
        lat_max=subscription.lat_max,
        lon_max=subscription.lon_max,
        interval=subscription.interval,
        subscription_type=subscription.subscription_type,
        language=SupportedLanguages(subscription.language),
        is_active=True,
    )

    return response


@router.get("/unsubscribe/{subscription_id}")
async def unsubscribe(subscription_id: str) -> SubscriptionResponse:
    deactivated_subscription_response = await graphql_client.deactivate_subscription(
        id=subscription_id
    )
    if deactivated_subscription_response.update_subscriptions_by_pk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
        )

    deactivated_subscription = (
        deactivated_subscription_response.update_subscriptions_by_pk
    )

    response = SubscriptionResponse(
        id=deactivated_subscription.id,
        title=deactivated_subscription.title,
        email=deactivated_subscription.email,
        lat_min=deactivated_subscription.lat_min,
        lon_min=deactivated_subscription.lon_min,
        lat_max=deactivated_subscription.lat_max,
        lon_max=deactivated_subscription.lon_max,
        interval=SubscriptionInterval(deactivated_subscription.interval),
        subscription_type=EntrySubscriptionType(deactivated_subscription.subscription_type),
        language=SupportedLanguages(deactivated_subscription.language),
        is_active=deactivated_subscription.is_active,
    )

    return response
