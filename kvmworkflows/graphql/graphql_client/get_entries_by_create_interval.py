# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, List

from .base_model import BaseModel


class GetEntriesByCreateInterval(BaseModel):
    entries: List["GetEntriesByCreateIntervalEntries"]


class GetEntriesByCreateIntervalEntries(BaseModel):
    created_at: Any
    description: str
    lat: Any
    id: str
    lng: Any
    status: str
    title: str
    updated_at: Any


GetEntriesByCreateInterval.model_rebuild()
