"""
Tests for subscription digest email functionality.
"""

import asyncio
from typing import List

from kvmworkflows.activities.create_subscription_digest_email import create_subscription_digest_email
from kvmworkflows.models.subscription import Subscription
from kvmworkflows.models.entries import EntryDict
from kvmworkflows.models.subscription_types import EntrySubscriptionType
from kvmworkflows.models.subscription_interval import SubscriptionInterval


def test_subscription_digest_email_creation():
    """Test that subscription digest emails are created correctly."""
    
    async def run_test():
        subscription = Subscription(
            id="test-subscription-id",
            title="Test Subscription",
            email="test@example.com",
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
                "description": "Test entry description",
                "id": "test-entry-1",
                "lat": 45.60543431695804,
                "lng": 8.055843789156453,
                "status": "created",
                "title": "Test Entry 1",
                "updated_at": "2025-03-26T14:19:09.846601+00:00",
                "category": "Test Category",
                "tags": "test, example",
                "address_line": "Test Address 123",
                "homepage": "https://test.example.com",
                "email": "info@test.example.com",
                "phone": "+1 234 567 8900",
            },
            {
                "created_at": "2025-03-24T14:18:15.572111+00:00",
                "description": "Another test entry",
                "id": "test-entry-2",
                "lat": 45.61543431695804,
                "lng": 8.065843789156453,
                "status": "created",
                "title": "Test Entry 2",
                "updated_at": "2025-03-26T15:19:09.846601+00:00",
                "category": None,
                "tags": None,
                "address_line": None,
                "homepage": None,
                "email": None,
                "phone": None,
            }
        ]

        interval = SubscriptionInterval.DAILY
        email = await create_subscription_digest_email(subscription, entries, interval)
        
        # Test email properties
        assert email is not None
        assert email.to == "test@example.com"
        assert "2 neue Einträge" in email.subject
        assert "Test Subscription" in email.subject
        assert "Am letzten Tag gab es 2 neue Einträge" in email.html
        assert "Test Entry 1" in email.html
        assert "Test Entry 2" in email.html
        assert "Test Category" in email.html
        assert "Kategorie nicht verfügbar" in email.html  # For entry 2
        assert "euphorische Grüße" in email.html
        assert "unsubscribe" in email.unsubscribe_link
        
        return email

    # Run the async test
    email = asyncio.run(run_test())
    return email


def test_single_entry_grammar():
    """Test that single entry uses correct German grammar."""
    
    async def run_test():
        subscription = Subscription(
            id="test-subscription-id",
            title="Single Entry Test",
            email="test@example.com",
            lat_min=45.5,
            lon_min=8.0,
            lat_max=45.61,
            lon_max=8.07,
            interval="hourly",
            subscription_type=EntrySubscriptionType.CREATES,
        )

        entries: List[EntryDict] = [
            {
                "created_at": "2025-03-24T13:18:15.572111+00:00",
                "description": "Single test entry",
                "id": "test-entry-single",
                "lat": 45.60543431695804,
                "lng": 8.055843789156453,
                "status": "created",
                "title": "Single Entry",
                "updated_at": "2025-03-26T14:19:09.846601+00:00",
                "category": None,
                "tags": None,
                "address_line": None,
                "homepage": None,
                "email": None,
                "phone": None,
            }
        ]

        interval = SubscriptionInterval.HOURLY
        email = await create_subscription_digest_email(subscription, entries, interval)
        
        # Test correct singular grammar
        assert email is not None
        assert "1 neuer Eintrag" in email.subject
        assert "1 neuen Eintrag" in email.html  # Accusative case
        assert "In der letzten Stunde gab es" in email.html
        
        return email

    # Run the async test
    email = asyncio.run(run_test())
    return email


def test_empty_entries():
    """Test that no email is created for empty entries list."""
    
    async def run_test():
        subscription = Subscription(
            id="test-subscription-id",
            title="Empty Test",
            email="test@example.com",
            lat_min=45.5,
            lon_min=8.0,
            lat_max=45.61,
            lon_max=8.07,
            interval="daily",
            subscription_type=EntrySubscriptionType.CREATES,
        )

        entries: List[EntryDict] = []

        interval = SubscriptionInterval.DAILY
        email = await create_subscription_digest_email(subscription, entries, interval)
        
        # Should return None for empty entries
        assert email is None
        
        return email

    # Run the async test
    email = asyncio.run(run_test())
    return email


if __name__ == "__main__":
    # Run tests directly
    print("Testing subscription digest email creation...")
    email = test_subscription_digest_email_creation()
    print(f"✓ Multiple entries test passed - Subject: {email.subject}")
    
    print("\nTesting single entry grammar...")
    email = test_single_entry_grammar()
    print(f"✓ Single entry grammar test passed - Subject: {email.subject}")
    
    print("\nTesting empty entries...")
    email = test_empty_entries()
    print(f"✓ Empty entries test passed - Email: {email}")
    
    print("\nAll tests passed! ✓")