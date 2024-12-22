import hydra

from omegaconf import OmegaConf
from pydantic import BaseModel
from typing import cast, Any, List, Union, Dict, Tuple, Mapping
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


class Config(BaseModel):
    sources: Sources
    sinks: Sinks
    areas: List[Area]


hydra.initialize(version_base=None, config_path="../..")
config_container = cast(dict[str, Any], OmegaConf.to_container(hydra.compose("config")))
config = Config(**config_container)


if __name__ == "__main__":
    print(config)
