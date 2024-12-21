import asyncio


from temporalio.client import Client
from kvmworkflows.workflows.workflow import Workflow



async def main():
    client = await Client.connect("95.217.222.28:7233")

    stories = await client.execute_workflow(
        Workflow.run,
        id="navid-kvm-sync",
        task_queue="kvmworkflows",
    )
    


if __name__ == "__main__":
    asyncio.run(main())