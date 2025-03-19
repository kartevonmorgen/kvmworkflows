from typing import Iterable
from temporalio import activity
from kvmworkflows.graphql.client import graphql_client
from kvmworkflows.graphql.graphql_client.input_types import entries_insert_input
from kvmworkflows.models.review_status import ReviewStatus
from kvmworkflows.models.search_entry import SearchEntry


@activity.defn
async def insert_search_entries(search_entries: Iterable[SearchEntry]) -> None:
    inputs = list(
        map(
            lambda search_entry: entries_insert_input(
                id=search_entry.id,
                title=search_entry.title,
                description=search_entry.description,
                lat=search_entry.lat,
                lng=search_entry.lng,
                status=search_entry.status,
            ),
            search_entries,
            )
        )
    
    await graphql_client.insert_entries(inputs)


async def test_insert_search_entries():
    search_entries = [
        SearchEntry(
            id="0"*32,
            title="title",
            description="description",
            lat=0.0,
            lng=0.0,
            status=ReviewStatus.CREATED,
        )
    ]
    await insert_search_entries(search_entries)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_insert_search_entries())
