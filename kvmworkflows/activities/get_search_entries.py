from pydantic import StrictStr
from typing import List
from temporalio import activity
from kvmworkflows.models.search_entry import SearchEntry
from kvmworkflows.ofdb.search import search
from rich import print



@activity.defn
async def get_search(bbox: StrictStr) -> List[SearchEntry]:
    search_entries = await search(bbox)
    visible_entries = search_entries.visible

    return visible_entries


async def test_get_search():
    bbox = "43.9137,-5.8227,55.3666,20.1489"
    entries = await get_search(bbox)

    print(len(entries))


if __name__ == '__main__':
    import asyncio

    asyncio.run(test_get_search())
