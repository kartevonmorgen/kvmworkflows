import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from kvmworkflows.workflows.workflow import Workflow
from kvmworkflows.activities.get_tags import get_tags
from kvmworkflows.activities.insert_tags import insert_tags
from kvmworkflows.activities.get_search_entries import get_search
from kvmworkflows.activities.insert_search_entries import insert_search_entries



async def main():
    client = await Client.connect("95.217.222.28:7233")

    worker = Worker(
        client,
        task_queue="kvmworkflows",
        workflows=[Workflow],
        activities=[get_tags, insert_tags, get_search, insert_search_entries],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
