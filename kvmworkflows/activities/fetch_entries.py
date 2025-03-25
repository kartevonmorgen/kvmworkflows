from datetime import date
from temporalio import activity
from rich import print
from kvmworkflows.graphql.client import graphql_client
from kvmworkflows.models.entries import Entries, Entry
from kvmworkflows.models.review_status import ReviewStatus
from kvmworkflows.config.config import config


@activity.defn
async def fetch_created_entries_by_filters(
    start: date,
    end: date,
    lat_min: float,
    lon_min: float,
    lat_max: float,
    lon_max: float,
) -> Entries:
    # the entries before the skip date are skipped
    if start < config.start_date:
        start = config.start_date

    entries_result = await graphql_client.get_entries_by_filters(
        create_at_gte=start,
        create_at_lte=end,
        lat_gte=lat_min,
        lon_gte=lon_min,
        lat_lte=lat_max,
        lon_lte=lon_max,
    )
    db_entries = entries_result.entries
    entries = list(
        map(
            lambda db_entry: Entry(
                id=db_entry.id,
                created_at=db_entry.created_at,
                updated_at=db_entry.updated_at,
                title=db_entry.title,
                description=db_entry.description,
                status=ReviewStatus(db_entry.status),
                lat=db_entry.lat,
                lng=db_entry.lng,
            ),
            db_entries,
        )
    )

    return entries


async def test_fetch_entries_by_create_interval():
    entries = await fetch_created_entries_by_filters(
        date(2024, 12, 21),
        date(2024, 12, 23),
        lat_min=50.74,
        lat_max=50.75,
        lon_min=7.1,
        lon_max=7.2,
    )
    print(entries[:2])
    print(len(entries))


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_fetch_entries_by_create_interval())
