import asyncio

from loguru import logger
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter

from kvmworkflows.activities.create_entries_email_messages import create_entries_email_messages
from kvmworkflows.activities.fetch_entries import fetch_created_entries_by_filters
from kvmworkflows.activities.fetch_subscriptions import fetch_subscriptions_by_interval
from kvmworkflows.activities.send_emails import send_emails
from kvmworkflows.config.config import config
from kvmworkflows.workflows.send_subscription_emails import Workflow


async def main():
    logger.info("Starting worker: send subscription emails")
    client = await Client.connect(config.temporal.uri, data_converter=pydantic_data_converter)
    logger.success("Connected to Temporal: send subscription emails")

    worker = Worker(
        client,
        task_queue=config.temporal.workflows.area_subscription.entry_creation.daily.task_queue,
        workflows=[Workflow],
        activities=[
            fetch_created_entries_by_filters,
            send_emails,
            fetch_subscriptions_by_interval,
            create_entries_email_messages,
        ],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
