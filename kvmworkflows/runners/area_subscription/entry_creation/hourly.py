import asyncio

from datetime import datetime
from temporalio.client import Client
from loguru import logger

from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.models.subscription_types import EntrySubscriptionType
from kvmworkflows.workflows.send_subscription_emails import Workflow
from kvmworkflows.config.config import config


async def main():
    logger.info("Starting hourly subscriptions workflow")
    client = await Client.connect(config.temporal.uri)

    stories = await client.execute_workflow(
        Workflow.run,
        args=(SubscriptionInterval.HOURLY, EntrySubscriptionType.CREATES),
        id=f"config.temporal.workflows.area_subscription.entry_creation.hourly.name-{datetime.now().isoformat()}",
        task_queue=config.temporal.workflows.area_subscription.entry_creation.hourly.task_queue,
        cron_schedule=config.temporal.workflows.area_subscription.entry_creation.hourly.cron_schedule,
    )


if __name__ == "__main__":
    asyncio.run(main())
