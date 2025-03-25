import hydra

from datetime import date
from omegaconf import OmegaConf
from pydantic import BaseModel
from typing import cast, Any, List, Tuple, Mapping, Optional
from rich import print


class SourceOfdb(BaseModel):
    url: str

class Sources(BaseModel):
    ofdb: SourceOfdb


class SinkGraphql(BaseModel):
    url: str
    headers: Mapping[str, str]
    timeout: int


class Sinks(BaseModel):
    graphql: SinkGraphql


class Area(BaseModel):
    name: str
    lats: Tuple[float, float]
    lngs: Tuple[float, float]
    lat_n_chunks: int
    lng_n_chunks: int


class TemporalWorkflowConfig(BaseModel):
    name: str
    task_queue: str
    cron_schedule: str


class TemporalWorkflowsConfig(BaseModel):
    sync_bbox: TemporalWorkflowConfig


class TemporalConfig(BaseModel):
    uri: str
    workflows: TemporalWorkflowsConfig


class AppConfig(BaseModel):
    title: str
    host: str
    port: int


class EmailMetadataConfig(BaseModel):
    sender: str
    subject: str
    template: str
    unsubscribe_url: Optional[str] = None
    start_to_close_timeout_seconds: int


class EmailConfig(BaseModel):
    domain: str
    api_key: str
    url: str
    rate_limit: int
    max_retries: int
    retry_delay: int
    concurrency: int
    test_email_recipient: Optional[str] = None
    area_subscription_creates: EmailMetadataConfig


class Config(BaseModel):
    start_date: date
    app: AppConfig
    temporal: TemporalConfig
    email: EmailConfig
    sources: Sources
    sinks: Sinks
    areas: List[Area]


hydra.initialize(version_base=None, config_path="../..")
config_container = cast(dict[str, Any], OmegaConf.to_container(hydra.compose("config")))
config = Config(**config_container)


if __name__ == "__main__":
    print(config)
