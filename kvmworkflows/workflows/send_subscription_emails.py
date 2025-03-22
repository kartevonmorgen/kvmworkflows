import asyncio

from datetime import timedelta
from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    from kvmworkflows.models.subscription_interval import SubscriptionInterval
    from kvmworkflows.activities.fetch_entries import fetch_entries_by_filters
    from kvmworkflows.activities.send_subscription_emails import send_subscription_email
    from kvmworkflows.activities.fetch_subscriptions import (
        fetch_subscriptions_by_interval,
    )


@workflow.defn
class Workflow:
    @workflow.run
    async def run(self, interval: SubscriptionInterval):
        subscriptions = await workflow.execute_activity(
            fetch_subscriptions_by_interval,
            interval,
            start_to_close_timeout=timedelta(seconds=300),
        )

        tasks = []
        start, end = interval.passed_interval_dates
        for subscription in subscriptions:
            entries = await workflow.execute_activity(
                fetch_entries_by_filters,
                args=(
                    start,
                    end,
                    subscription.lat_min,
                    subscription.lon_min,
                    subscription.lat_max,
                    subscription.lon_max,
                ),
                start_to_close_timeout=timedelta(seconds=300),
            )

            for entry in entries:
                task = await workflow.execute_activity(
                    send_subscription_email,
                    args=(
                        subscription.email,
                        entry,
                    ),
                    start_to_close_timeout=timedelta(seconds=300),
                )
                tasks.append(task)

        asyncio.gather(*tasks)
