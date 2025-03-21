import asyncio

from temporalio.client import Client
from kvmworkflows.workflows.sync_bbox import Workflow
from kvmworkflows.config.config import config


async def main():
    client = await Client.connect(config.temporal.uri)

    stories = await client.execute_workflow(
        Workflow.run,
        id=config.temporal.workflows.sync_bbox.name,
        task_queue=config.temporal.workflows.sync_bbox.task_queue,
        cron_schedule=config.temporal.workflows.sync_bbox.cron_schedule,
    )
    


if __name__ == "__main__":
    asyncio.run(main())
