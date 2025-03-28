from datetime import datetime
from pydantic import BaseModel, computed_field
from typing import TypeAlias, List, TypedDict
from rich import print

from kvmworkflows.config.config import config
from kvmworkflows.models.review_status import ReviewStatus
from kvmworkflows.models.supported_languages import SupportedLanguages
from kvmworkflows.liquid_utils.render import render_template


class EntryDict(TypedDict):
    id: str
    created_at: str
    updated_at: str
    title: str
    description: str
    status: str
    lat: float
    lng: float


class Entry(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    status: ReviewStatus
    lat: float
    lng: float

    @computed_field
    @property
    def unsubscribe_link(self) -> str:
        return f"{config.email.area_subscription_creates.unsubscribe_url}/{self.id}"
    
    def to_dict(self) -> EntryDict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "lat": self.lat,
            "lng": self.lng,
        }
    
    @classmethod
    def from_dict(cls, data: EntryDict) -> "Entry":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            title=data["title"],
            description=data["description"],
            status=ReviewStatus(data["status"]),
            lat=data["lat"],
            lng=data["lng"],
        )


def get_unsubscribe_link(entry: EntryDict) -> str:
    return f"{config.email.area_subscription_creates.unsubscribe_url}/{entry['id']}"


# todo: maybe move this to a separate module like the template
def to_creates_html(entry: EntryDict, language: SupportedLanguages = SupportedLanguages.de) -> str:
    rendered = render_template(
        config.email.area_subscription_creates.template.format(language=language),
        entry=entry,
        domain=config.email.domain,
    )
    
    return rendered


Entries: TypeAlias = List[Entry]


if __name__ == "__main__":
    entry = Entry(
        id="b0b2b0d1-4e4d-4e4d-8e8d-4e4d4e4d4e4d",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        title="Test Title",
        description="Test Description",
        status=ReviewStatus.CREATED,
        lat=15,
        lng=16,
    )
    
    # print(entry.to_dict())
    
    entry_dict = entry.to_dict()
    print(entry_dict)

    # print(json.dumps(entry))
    rendered = to_creates_html(entry_dict)
    print(rendered)
