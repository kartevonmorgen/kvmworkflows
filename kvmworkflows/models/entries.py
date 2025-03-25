from datetime import datetime
from pydantic import BaseModel, computed_field
from typing import TypeAlias, List
from rich import print

from kvmworkflows.config.config import config
from kvmworkflows.liquid.render import render_template
from kvmworkflows.models.review_status import ReviewStatus
from kvmworkflows.models.supported_languages import SupportedLanguages


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
    
    def to_creates_html(self, language: SupportedLanguages = SupportedLanguages.de) -> str:
        rendered = render_template(
            config.email.area_subscription_creates.template.format(language=language),
            entry=self,
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

    rendered = entry.to_creates_html()
    print(rendered)
