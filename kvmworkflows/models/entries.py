from datetime import datetime
from pydantic import BaseModel, computed_field
from typing import TypeAlias, List, TypedDict
from rich import print

from kvmworkflows.config.config import config
from kvmworkflows.models.review_status import ReviewStatus
from kvmworkflows.models.subscription import Subscription
from kvmworkflows.models.subscription_interval import SubscriptionInterval
from kvmworkflows.models.subscription_types import EntrySubscriptionType
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
    tags: List[str]
    link: str


class Entry(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    status: ReviewStatus
    lat: float
    lng: float
    tags: List[str] = []
    
    @computed_field
    @property
    def link(self) -> str:
        return f"{config.kvm.entry_url}/{self.id}"
    
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
            "tags": self.tags,
            "link": self.link, 
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
            tags=data["tags"],
        )

# todo: maybe move this to a separate module like the template
def to_creates_html(subscription: Subscription, entries: List[EntryDict], interval: SubscriptionInterval, language: SupportedLanguages = SupportedLanguages.de) -> str:
    rendered = render_template(
        config.email.area_subscription_creates.template.format(interval=interval, language=language),
        subscription=subscription.model_dump(),
        entries=entries,
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
    
    # entry_dict = entry.to_dict()
    # print(entry_dict)
    entries_dicts : List[EntryDict] = [entry.to_dict() for _ in range(3)]

    subscription = Subscription(
       email="navid@gmail.com",
         id="sub-123",
        title="Test Subscription",
        lat_min=10.0,
        lon_min=10.0,
        lat_max=20.0,
        lon_max=20.0,
        interval=SubscriptionInterval.WEEKLY,
        subscription_type=EntrySubscriptionType.CREATES,
    )

    # print(json.dumps(entry))
    rendered = to_creates_html(subscription, entries_dicts, SubscriptionInterval.WEEKLY, SupportedLanguages.de)
    print(rendered)
