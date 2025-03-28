import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from loguru import logger

from kvmworkflows.workflows.sync_bbox import Workflow
from kvmworkflows.activities.get_tags import get_tags
from kvmworkflows.activities.insert_tags import insert_tags
from kvmworkflows.activities.get_search_entries import get_search
from kvmworkflows.activities.insert_search_entries import upsert_search_entries
from kvmworkflows.config.config import config



async def main():
    logger.info("Starting worker: sync bbox")
    client = await Client.connect(config.temporal.uri)
    logger.success("Connected to Temporal: sync bbox")

    worker = Worker(
        client,
        task_queue=config.temporal.workflows.sync_bbox.task_queue,
        workflows=[Workflow],
        activities=[get_tags, insert_tags, get_search, upsert_search_entries],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
