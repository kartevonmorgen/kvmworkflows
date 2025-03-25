from datetime import timedelta
from temporalio import workflow
from typing import List

from kvmworkflows.config.config import config
from kvmworkflows.models.subscription_types import SubscriptionType
from kvmworkflows.mail.mailngun import EmailMessage


with workflow.unsafe.imports_passed_through():
    from kvmworkflows.models.subscription_interval import SubscriptionInterval
    from kvmworkflows.activities.fetch_entries import fetch_created_entries_by_filters
    from kvmworkflows.activities.send_emails import (
        send_emails,
    )
    from kvmworkflows.activities.fetch_subscriptions import (
        fetch_subscriptions_by_interval,
    )


@workflow.defn
class Workflow:
    @workflow.run
    async def run(
        self,
        interval: SubscriptionInterval,
        subscription_type: SubscriptionType
    ):
        subscriptions = await workflow.execute_activity(
            fetch_subscriptions_by_interval,
            args=(interval, subscription_type),
            start_to_close_timeout=timedelta(seconds=300),
        )

        email_messages: List[EmailMessage] = []
        start, end = interval.passed_interval_dates
        for subscription in subscriptions:
            entries = await workflow.execute_activity(
                fetch_created_entries_by_filters,
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
                email_message: EmailMessage = EmailMessage(
                    sender=config.email.area_subscription_creates.sender,
                    to=subscription.email,
                    subject=config.email.area_subscription_creates.subject,
                    html=entry.to_creates_html(),
                    unsubscribe_link=entry.unsubscribe_link,
                )
                email_messages.append(email_message)

        await workflow.execute_activity(
            send_emails,
            args=(email_messages,),
            start_to_close_timeout=timedelta(
                seconds=config.email.area_subscription_creates.start_to_close_timeout_seconds
            ),
        )
