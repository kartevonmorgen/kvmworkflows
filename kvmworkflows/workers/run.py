import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from kvmworkflows.activities.get_tags import get_tags
from kvmworkflows.activities.insert_tags import insert_tags
from kvmworkflows.workflows.workflow import Workflow


async def main():
    client = await Client.connect("95.217.222.28:7233")

    worker = Worker(
        client,
        task_queue="kvmworkflows",
        workflows=[Workflow],
        activities=[get_tags, insert_tags],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
