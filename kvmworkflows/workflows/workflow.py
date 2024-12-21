from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from kvmworkflows.activities.get_tags import get_tags
    from kvmworkflows.activities.insert_tags import insert_tags
    

@workflow.defn
class Workflow:

    @workflow.run
    async def run(self):
        tags = await workflow.execute_activity(
            get_tags,
            start_to_close_timeout=timedelta(seconds=300),
        )
        await workflow.execute_activity(
            insert_tags,
            tags,
            start_to_close_timeout=timedelta(seconds=300),
        )