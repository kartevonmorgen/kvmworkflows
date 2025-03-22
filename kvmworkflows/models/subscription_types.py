from enum import StrEnum


class SubscriptionType(StrEnum):
    CREATES = "creates"
    UPDATES = "updates"
    TAGS = "tags"
