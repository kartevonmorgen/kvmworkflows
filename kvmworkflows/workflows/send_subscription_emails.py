from datetime import timedelta
from temporalio import workflow
from typing import List

from kvmworkflows.models.subscription_types import EntrySubscriptionType


with workflow.unsafe.imports_passed_through():
    from kvmworkflows.activities.create_entries_email_messages import create_entries_email_messages
    from kvmworkflows.activities.create_subscription_digest_email import create_subscription_digest_email
    from kvmworkflows.activities.fetch_entries import fetch_created_entries_by_filters
    from kvmworkflows.activities.fetch_subscriptions import fetch_subscriptions_by_interval
    from kvmworkflows.activities.send_emails import send_emails
    from kvmworkflows.config.config import config
    from kvmworkflows.mail.mailngun import EmailMessage
    from kvmworkflows.models.subscription_interval import SubscriptionInterval


@workflow.defn
class Workflow:
    
    @workflow.run
    async def run(
        self,
        interval: SubscriptionInterval,
        subscription_type: EntrySubscriptionType,
    ):
        subscriptions = await workflow.execute_activity(
            fetch_subscriptions_by_interval,
            args=(interval, subscription_type),
            start_to_close_timeout=timedelta(seconds=300),
        )

        email_messages: List[EmailMessage] = []
        for subscription in subscriptions:
            entries = await workflow.execute_activity(
                fetch_created_entries_by_filters,
                args=(
                    interval,
                    subscription.lat_min,
                    subscription.lon_min,
                    subscription.lat_max,
                    subscription.lon_max,
                ),
                start_to_close_timeout=timedelta(seconds=300),
            )

            subscription_email_messages = await workflow.execute_activity(
                create_entries_email_messages,
                args=(subscription, entries),
                start_to_close_timeout=timedelta(seconds=300),
            )
            
            email_messages.extend(subscription_email_messages)

        await workflow.execute_activity(
            send_emails,
            args=(email_messages,),
            start_to_close_timeout=timedelta(
                seconds=config.email.area_subscription_creates.start_to_close_timeout_seconds
            ),
        )


@workflow.defn 
class SubscriptionDigestWorkflow:
    """Workflow that sends digest emails (one email per subscription with multiple entries)"""
    
    @workflow.run
    async def run(
        self,
        interval: SubscriptionInterval,
        subscription_type: EntrySubscriptionType,
    ):
        subscriptions = await workflow.execute_activity(
            fetch_subscriptions_by_interval,
            args=(interval, subscription_type),
            start_to_close_timeout=timedelta(seconds=300),
        )

        email_messages: List[EmailMessage] = []
        for subscription in subscriptions:
            entries = await workflow.execute_activity(
                fetch_created_entries_by_filters,
                args=(
                    interval,
                    subscription.lat_min,
                    subscription.lon_min,
                    subscription.lat_max,
                    subscription.lon_max,
                ),
                start_to_close_timeout=timedelta(seconds=300),
            )

            # Create single digest email for all entries in this subscription
            digest_email = await workflow.execute_activity(
                create_subscription_digest_email,
                args=(subscription, entries, interval),
                start_to_close_timeout=timedelta(seconds=300),
            )
            
            if digest_email:
                email_messages.append(digest_email)

        await workflow.execute_activity(
            send_emails,
            args=(email_messages,),
            start_to_close_timeout=timedelta(
                seconds=config.email.area_subscription_creates.start_to_close_timeout_seconds
            ),
        )
