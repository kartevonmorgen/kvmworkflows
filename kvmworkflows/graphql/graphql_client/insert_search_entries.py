# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Optional

from .base_model import BaseModel


class InsertSearchEntries(BaseModel):
    insert_entries: Optional["InsertSearchEntriesInsertEntries"]


class InsertSearchEntriesInsertEntries(BaseModel):
    affected_rows: int


InsertSearchEntries.model_rebuild()
