from typing import Iterable
from temporalio import activity
from kvmworkflows.graphql.client import client
from kvmworkflows.graphql.graphql_client.input_types import tags_insert_input


@activity.defn
async def insert_tags(tags: Iterable[str]) -> None:
    inputs = list(map(lambda tag: tags_insert_input(id=tag), tags))
    
    await client.insert_tags(inputs)
