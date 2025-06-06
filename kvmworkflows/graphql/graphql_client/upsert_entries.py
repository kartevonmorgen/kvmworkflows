# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Optional

from .base_model import BaseModel


class UpsertEntries(BaseModel):
    insert_entries: Optional["UpsertEntriesInsertEntries"]


class UpsertEntriesInsertEntries(BaseModel):
    affected_rows: int


UpsertEntries.model_rebuild()
