from typing import List
from temporalio import activity
from kvmworkflows.ofdb.tags import get_tags as get_tags_ofdb


@activity.defn
async def get_tags() -> List[str]:
    tags = await get_tags_ofdb()

    return tags
