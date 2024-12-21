# Generated by ariadne-codegen
# Source: http://95.217.222.28:8787/v1/graphql

from enum import Enum


class cursor_ordering(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class entries_constraint(str, Enum):
    entries_pkey = "entries_pkey"


class entries_select_column(str, Enum):
    created_at = "created_at"
    description = "description"
    id = "id"
    lat = "lat"
    long = "long"
    status = "status"
    title = "title"
    updated_at = "updated_at"


class entries_update_column(str, Enum):
    created_at = "created_at"
    description = "description"
    id = "id"
    lat = "lat"
    long = "long"
    status = "status"
    title = "title"
    updated_at = "updated_at"


class entry_links_constraint(str, Enum):
    entry_links_pkey = "entry_links_pkey"


class entry_links_select_column(str, Enum):
    created_at = "created_at"
    entry = "entry"
    link = "link"


class entry_links_update_column(str, Enum):
    created_at = "created_at"
    entry = "entry"
    link = "link"


class entry_tags_constraint(str, Enum):
    entry_tags_pkey = "entry_tags_pkey"


class entry_tags_select_column(str, Enum):
    created_at = "created_at"
    entry = "entry"
    tag = "tag"


class entry_tags_update_column(str, Enum):
    created_at = "created_at"
    entry = "entry"
    tag = "tag"


class link_constraint(str, Enum):
    link_pkey = "link_pkey"


class link_select_column(str, Enum):
    created_at = "created_at"
    description = "description"
    id = "id"
    title = "title"
    updated_at = "updated_at"
    url = "url"


class link_update_column(str, Enum):
    created_at = "created_at"
    description = "description"
    id = "id"
    title = "title"
    updated_at = "updated_at"
    url = "url"


class order_by(str, Enum):
    asc = "asc"
    asc_nulls_first = "asc_nulls_first"
    asc_nulls_last = "asc_nulls_last"
    desc = "desc"
    desc_nulls_first = "desc_nulls_first"
    desc_nulls_last = "desc_nulls_last"


class tags_constraint(str, Enum):
    tags_pkey = "tags_pkey"


class tags_select_column(str, Enum):
    created_at = "created_at"
    id = "id"


class tags_update_column(str, Enum):
    created_at = "created_at"
    id = "id"