import httpx

from pydantic import StrictStr, BaseModel
from typing import List
from rich import print
from kvmworkflows.models.search_entry import SearchEntry
from kvmworkflows.config.config import config


class SearchResult(BaseModel):
    visible: List[SearchEntry] = []
    invisible: List[SearchEntry] = []


async def search(
    bbox: StrictStr,
    # org_tag: Optional[StrictStr] = None,
    # categories: Optional[StrictStr] = None,
    # text: Optional[StrictStr] = None,
    # ids: Optional[StrictStr] = None,
    # tags: Optional[StrictStr] = None,
    # status: Optional[StrictStr] = None,
    # limit: Optional[StrictInt] = None,
) -> SearchResult:
    transport = httpx.AsyncHTTPTransport(retries=10)
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(
            f"{config.sources.ofdb.url}/search",
            params={
                "bbox": bbox,
                # "org_tag": org_tag,
                # "categories": categories,
                # "text": text,
                # "ids": ids,
                # "tags": tags,
                # "status": status,
                "limit": 2000,
            },
        )

    return SearchResult.model_validate_json(response.content)


async def test_search():
    bbox = "43.9137,-5.8227,55.3666,20.1489"
    result = await search(
        bbox=bbox,
    )   
    print(len(result.visible))


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_search())
