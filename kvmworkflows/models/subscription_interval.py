from enum import StrEnum
from datetime import date, timedelta
from pydantic import BaseModel


class IntervalDates(BaseModel):
    start_date: date
    end_date: date


class SubscriptionInterval(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    @property
    def passed_interval_dates(self) -> IntervalDates:
        today = date.today()
        if self == SubscriptionInterval.DAILY:
            return IntervalDates(start_date=today - timedelta(days=1), end_date=today)
        elif self == SubscriptionInterval.WEEKLY:
            return IntervalDates(start_date=today - timedelta(days=today.weekday()), end_date=today)
        elif self == SubscriptionInterval.MONTHLY:
            return IntervalDates(start_date=date(today.year, today.month, 1), end_date=today)
        elif self == SubscriptionInterval.YEARLY:
            return IntervalDates(start_date=date(today.year, 1, 1), end_date=today)
        else:
            raise ValueError(f"Invalid interval: {self}")
