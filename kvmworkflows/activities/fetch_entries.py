from datetime import date
from rich import print
from temporalio import activity
from typing import List

from kvmworkflows.config.config import config
from kvmworkflows.graphql.client import graphql_client
from kvmworkflows.models.entries import EntryDict
from kvmworkflows.models.subscription_interval import SubscriptionInterval


@activity.defn
async def fetch_created_entries_by_filters(
    interval: SubscriptionInterval,
    lat_min: float,
    lon_min: float,
    lat_max: float,
    lon_max: float,
) -> List[EntryDict]:
    # start, end = interval.passed_interval_dates.start_date, interval.passed_interval_dates.end_date

    start, end = date(2025, 3, 23), date(2025, 3, 27)

    # the entries before the skip date are skipped
    # if start < config.start_date:
    #     start = config.start_date

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
            lambda db_entry: EntryDict(
                id=db_entry.id,
                created_at=db_entry.created_at,
                updated_at=db_entry.updated_at,
                title=db_entry.title,
                description=db_entry.description,
                status=db_entry.status,
                lat=db_entry.lat,
                lng=db_entry.lng,
            ),
            db_entries,
        )
    )

    return entries


async def test_fetch_entries_by_create_interval():
    entries = await fetch_created_entries_by_filters(
        interval=SubscriptionInterval.DAILY,
        lat_max=45.61,
        lat_min=45.5,
        lon_max=8.07,
        lon_min=8,
    )
    print(entries)
    print(len(entries))


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_fetch_entries_by_create_interval())
