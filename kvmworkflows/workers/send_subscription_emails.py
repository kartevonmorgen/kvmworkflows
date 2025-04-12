import asyncio
import typer

from loguru import logger
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter

from kvmworkflows.activities.create_entries_email_messages import create_entries_email_messages
from kvmworkflows.activities.fetch_entries import fetch_created_entries_by_filters
from kvmworkflows.activities.fetch_subscriptions import fetch_subscriptions_by_interval
from kvmworkflows.activities.send_emails import send_emails
from kvmworkflows.config.config import TemporalWorkflowConfig, config
from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.workflows.send_subscription_emails import Workflow


async def run(interval: SubscriptionInterval):
    logger.info("Starting worker: send subscription emails")
    client = await Client.connect(config.temporal.uri, data_converter=pydantic_data_converter)
    logger.success("Connected to Temporal: send subscription emails")

    try:
        conf: TemporalWorkflowConfig = getattr(config.temporal.workflows.area_subscription.entry_creation, interval.value)
    except AttributeError:
        logger.error(f"Subscription interval not implemented yet: {interval.value}")
        raise

    worker = Worker(
        client,
        task_queue=conf.task_queue,
        workflows=[Workflow],
        activities=[
            fetch_created_entries_by_filters,
            send_emails,
            fetch_subscriptions_by_interval,
            create_entries_email_messages,
        ],
    )

    await worker.run()


def main(interval: SubscriptionInterval):
    """
    Run the worker for sending subscription emails.
    """
    asyncio.run(run(interval))


if __name__ == "__main__":
    typer.run(main)
