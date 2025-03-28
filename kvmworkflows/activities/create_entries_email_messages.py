import asyncio

from rich import print
from temporalio import activity
from typing import List

from kvmworkflows.config.config import config
from kvmworkflows.models.entries import get_unsubscribe_link, to_creates_html
from kvmworkflows.models.subscription import Subscription
from kvmworkflows.models.entries import EntryDict
from kvmworkflows.mail.mailngun import EmailMessage
from kvmworkflows.models.subscription_types import EntrySubscriptionType


@activity.defn
async def create_entries_email_messages(
    subscription: Subscription, entries: List[EntryDict]
) -> List[EmailMessage]:
    email_messages: List[EmailMessage] = []
    for entry in entries:
        email_message: EmailMessage = EmailMessage(
            sender=config.email.area_subscription_creates.sender,
            to=subscription.email,
            subject=config.email.area_subscription_creates.subject,
            html=to_creates_html(entry),
            unsubscribe_link=get_unsubscribe_link(entry),
        )
        email_messages.append(email_message)

    return email_messages


if __name__ == "__main__":
    subscription = Subscription(
        id="19b8fe6e-9302-4b3c-a455-5b4ef048645b",
        email="navidkalaei@gmail.com",
        lat_min=45.5,
        lon_min=8.0,
        lat_max=45.61,
        lon_max=8.07,
        interval="daily",
        subscription_type=EntrySubscriptionType.CREATES,
    )

    entries: List[EntryDict] = [
        {
            "created_at": "2025-03-24T13:18:15.572111+00:00",
            "description": "unterstützt die Erforschung und Gestaltung von Architektur nach den Prinzipien der Bioarchitektur mit der Untersuchung von Produkten und Technologien für ein „Durchbruch“",
            "id": "42c5f152e9294540bf695c0dba11315a",
            "lat": 45.60543431695804,
            "lng": 8.055843789156453,
            "status": "created",
            "title": "Tiziana Monterisi Architetto Studio",
            "updated_at": "2025-03-26T14:19:09.846601+00:00",
        },
        {
            "created_at": "2025-03-24T13:18:15.572111+00:00",
            "description": "Die Organisation der Lieferkette von Sekundärmaterialien für den Reisanbau wird zu neuen Materialien für ein gesundes Bauen und zu einem neuen ethischen und technologisch fortschrittlichen Weg, um das Haus wieder zu einem zu machen\n\n",
            "id": "3b16b8d9f3f543b5a8980573e0653424",
            "lat": 45.60543431695804,
            "lng": 8.055843789156453,
            "status": "created",
            "title": "RiceHouse",
            "updated_at": "2025-03-26T14:19:09.846601+00:00",
        },
    ]

    rendered = asyncio.run(create_entries_email_messages(subscription, entries))
    print(rendered)
