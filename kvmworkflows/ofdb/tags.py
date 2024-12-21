import httpx

from pydantic import TypeAdapter
from typing import List
from rich import print
from loguru import logger


tags_adapter = TypeAdapter(List[str])


async def get_tags() -> List[str]:
    transport = httpx.AsyncHTTPTransport(retries=10)
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            response = await client.get(
                "https://api.ofdb.io/v0/tags",
                timeout=300,
            )
        except Exception as e:
            logger.error(f"Failed to get tags: {e}")
            raise e

    return tags_adapter.validate_json(response.content)


async def test_get_tags():
    tags = await get_tags()
    print(tags[:10])


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_get_tags())
