from temporalio import activity
from pydantic import EmailStr

from kvmworkflows.models.entries import Entry


@activity.defn
async def send_subscription_email(email: EmailStr, entry: Entry):
    # send email to the user
    pass
