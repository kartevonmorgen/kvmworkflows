import httpx

from kvmworkflows.graphql.graphql_client.client import Client
from kvmworkflows.config.config import config


http_client = httpx.AsyncClient(headers=config.sinks.graphql.headers, timeout=config.sinks.graphql.timeout)
graphql_client = Client(config.sinks.graphql.url, http_client=http_client)
