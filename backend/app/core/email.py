import logging

logger = logging.getLogger(__name__)

async def send_welcome_email(email_to: str, username: str) -> None:
    """
    Simulates sending an email asynchronously.
    I will integrate with Gmail later
    """
    import asyncio
    
    # Simulating network latency for an external SMTP server
    await asyncio.sleep(2) 
    
    # We log it so you can see it working in the terminal without real email credentials
    logger.info("=========================================")
    logger.info(f"EMAIL DISPATCHED TO: {email_to}")
    logger.info(f"SUBJECT: Welcome to PAPR Study Decks!")
    logger.info(f"BODY: Hi {username}, here are your credentials... Remember to change your password.")
    logger.info("=========================================")
    
    return None