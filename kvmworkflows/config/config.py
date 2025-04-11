import hydra

from datetime import datetime
from omegaconf import OmegaConf
from pydantic import BaseModel
from typing import List, Tuple, Mapping, Optional
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


class TemporalAreaSubscriptionsEntryCreationConfig(BaseModel):
    hourly: TemporalWorkflowConfig
    daily: TemporalWorkflowConfig
    weekly: TemporalWorkflowConfig
    monthly: TemporalWorkflowConfig


class TemporalAreaSubscriptionsConfig(BaseModel):
    limit: int
    entry_creation: TemporalAreaSubscriptionsEntryCreationConfig


class TemporalWorkflowsConfig(BaseModel):
    sync_bbox: TemporalWorkflowConfig
    area_subscription: TemporalAreaSubscriptionsConfig


class TemporalConfig(BaseModel):
    uri: str
    workflows: TemporalWorkflowsConfig


class AppCorsConfig(BaseModel):
    allowed_origins: List[str]
    allowed_methods: List[str]
    allowed_headers: List[str]
    allow_credentials: bool


class AppConfig(BaseModel):
    title: str
    host: str
    port: int
    cors: AppCorsConfig
    openapi_url: str


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
    start_datetime: datetime
    app: AppConfig
    temporal: TemporalConfig
    email: EmailConfig
    sources: Sources
    sinks: Sinks
    areas: List[Area]


hydra.initialize(version_base=None, config_path="/app/config.yaml")
cfg = hydra.compose("config")
resolved_cfg = OmegaConf.to_container(cfg, resolve=True)
config = Config.model_validate(resolved_cfg)

if __name__ == "__main__":
    print(config)
