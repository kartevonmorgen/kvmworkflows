import httpx

from temporalio import activity
from kvmworkflows.graphql.graphql_client.client import Client
from kvmworkflows.graphql.graphql_client.input_types import tags_insert_input


@activity.defn
async def insert_tags(tags: list[str]) -> None:
    inputs = list(map(lambda tag: tags_insert_input(id=tag), tags))

    http_client = httpx.AsyncClient(headers={"x-hasura-admin-secret": "HFyp3TNzjiwmNFt7TfxTcXsNbGbg5Jrd"}, timeout=300)

    client = Client('http://95.217.222.28:8787/v1/graphql', http_client=http_client)
    await client.insert_tags(inputs)
