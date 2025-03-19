from temporalio import activity
from rich import print
from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.graphql.client import graphql_client
from kvmworkflows.models.subscription import Subscriptions, Subscription


@activity.defn
async def fetch_subscriptions_by_interval(interval: SubscriptionInterval) -> Subscriptions:
    subscriptions_response = await graphql_client.get_subscriptions_by_interval(interval=interval.value)
    db_subscriptions = subscriptions_response.subscriptions
    subscriptions: Subscriptions = list(
        map(
            lambda db_subscription: Subscription(
                email=db_subscription.email,
                lat_min=db_subscription.lat_min,
                lon_min=db_subscription.lon_min,
                lat_max=db_subscription.lat_max,
                lon_max=db_subscription.lon_max,
                interval=SubscriptionInterval(db_subscription.interval),
            ),
            db_subscriptions,
        )
    )

    return subscriptions


async def test_fetch_subscriptions_by_interval():
    subscriptions = await fetch_subscriptions_by_interval(SubscriptionInterval.DAILY)
    print(subscriptions[:2])


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_fetch_subscriptions_by_interval())