# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, List

from .base_model import BaseModel


class GetEntriesByFilters(BaseModel):
    entries: List["GetEntriesByFiltersEntries"]


class GetEntriesByFiltersEntries(BaseModel):
    created_at: Any
    description: str
    id: str
    lat: Any
    lng: Any
    status: str
    title: str
    title: str
    updated_at: Any


GetEntriesByFilters.model_rebuild()
