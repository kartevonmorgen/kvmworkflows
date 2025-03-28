from temporalio import activity
from typing import List
from loguru import logger

from kvmworkflows.config.config import config
from kvmworkflows.mail.mailngun import EmailMessage, MailgunSender


@activity.defn
async def send_emails(email_messages: List[EmailMessage]):
    n_messages = len(email_messages)
    if n_messages == 0:
        logger.info("No emails to send")
        return None
    
    logger.info("Start sending emails")
    sender = MailgunSender(domain=config.email.domain, api_key=config.email.api_key)
    
    try:
        results = await sender.send_bulk_emails(
            email_messages, concurrency=config.email.concurrency
        )
        n_exceptions = len([r for r in results if isinstance(r, Exception)])
        
        if n_exceptions == n_messages:
            logger.error("Failed to send any emails")
        elif n_exceptions:
            logger.success(
                f"Sent {n_messages - n_exceptions} emails successfully"
            )
            logger.error(f"Failed to send {n_exceptions} emails")
        else:
            logger.success(f"Sent all {n_messages} emails successfully")
        
        return results
    except Exception as e:
        logger.error(f"Error sending emails: {e}")
    finally:
        await sender.close_async()
