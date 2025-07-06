import asyncio

from rich import print
from temporalio import activity
from typing import List

from kvmworkflows.config.config import config
from kvmworkflows.models.entries import to_subscription_digest_html
from kvmworkflows.models.subscription import Subscription
from kvmworkflows.models.entries import EntryDict
from kvmworkflows.mail.mailngun import EmailMessage
from kvmworkflows.models.subscription_types import EntrySubscriptionType
from kvmworkflows.models.subscription_interval import SubscriptionInterval


@activity.defn
async def create_subscription_digest_email(
    subscription: Subscription, entries: List[EntryDict], interval: SubscriptionInterval
) -> EmailMessage | None:
    """Create a single digest email for a subscription with multiple entries"""
    if not entries:
        return None
    
    count = len(entries)
    subject = f"{count} neue Einträge für dein Abo \"{subscription.title}\""
    
    email_message = EmailMessage(
        sender=config.email.area_subscription_creates.sender,
        to=subscription.email,
        subject=subject,
        html=to_subscription_digest_html(subscription, entries, interval.value),
        unsubscribe_link=f"{config.email.area_subscription_creates.unsubscribe_url}/{subscription.id}",
    )
    
    return email_message


if __name__ == "__main__":
    subscription = Subscription(
        id="19b8fe6e-9302-4b3c-a455-5b4ef048645b",
        title="Test subscription",
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
            "description": "unterstützt die Erforschung und Gestaltung von Architektur nach den Prinzipien der Bioarchitektur mit der Untersuchung von Produkten und Technologien für ein Durchbruch",
            "id": "42c5f152e9294540bf695c0dba11315a",
            "lat": 45.60543431695804,
            "lng": 8.055843789156453,
            "status": "created",
            "title": "Tiziana Monterisi Architetto Studio",
            "updated_at": "2025-03-26T14:19:09.846601+00:00",
            "category": "Nachhaltiges Bauen",
            "tags": "Bioarchitektur, Forschung",
            "address_line": "Via Roma 123, Milano",
            "homepage": "https://tiziana-architetto.it",
            "email": "info@tiziana-architetto.it",
            "phone": "+39 02 1234567",
        },
        {
            "created_at": "2025-03-24T13:18:15.572111+00:00",
            "description": "Die Organisation der Lieferkette von Sekundärmaterialien für den Reisanbau wird zu neuen Materialien für ein gesundes Bauen und zu einem neuen ethischen und technologisch fortschrittlichen Weg, um das Haus wieder zu einem zu machen",
            "id": "3b16b8d9f3f543b5a8980573e0653424",
            "lat": 45.60543431695804,
            "lng": 8.055843789156453,
            "status": "created",
            "title": "RiceHouse",
            "updated_at": "2025-03-26T14:19:09.846601+00:00",
            "category": "Nachhaltiges Material",
            "tags": "Reisbau, Materialien, Innovation",
            "address_line": "Via Verde 456, Milano",
            "homepage": "https://ricehouse.it",
            "email": "contact@ricehouse.it",
            "phone": "+39 02 7654321",
        },
    ]

    interval = SubscriptionInterval.DAILY
    rendered = asyncio.run(create_subscription_digest_email(subscription, entries, interval))
    print(rendered)