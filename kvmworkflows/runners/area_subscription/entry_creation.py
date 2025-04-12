import asyncio
import typer

from datetime import datetime
from temporalio.client import Client
from loguru import logger
from typing import Optional

from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.models.subscription_types import EntrySubscriptionType
from kvmworkflows.workflows.send_subscription_emails import Workflow
from kvmworkflows.config.config import TemporalWorkflowConfig, config




async def run(interval: SubscriptionInterval, subscription_type: EntrySubscriptionType):
    logger.info(f"Starting {interval.value} subscriptions workflow on {subscription_type.value}")
    client = await Client.connect(config.temporal.uri)
    
    try:
        conf: TemporalWorkflowConfig = getattr(config.temporal.workflows.area_subscription.entry_creation, interval.value)
    except AttributeError:
        logger.error(f"Subscription interval not implemented yet: {interval.value}")
        raise

    stories = await client.execute_workflow(
        Workflow.run,
        args=(interval, subscription_type),
        id=f"{conf.name}-{datetime.now().isoformat()}",
        task_queue=conf.task_queue,
        cron_schedule=conf.cron_schedule,
    )


def main(interval: SubscriptionInterval, subscription_type: EntrySubscriptionType = EntrySubscriptionType.CREATES):
    if subscription_type != EntrySubscriptionType.CREATES:
        logger.error(f"Subscription type not implemented yet: {subscription_type.value}")
        raise ValueError(f"Subscription type not implemented yet: {subscription_type.value}")
    
    asyncio.run(run(interval, subscription_type))


if __name__ == "__main__":
    typer.run(main)
