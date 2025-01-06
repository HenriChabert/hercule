from webpush import WebPush, WebPushSubscription  # type: ignore
from src.app.core.config import Settings
import requests
import aiohttp

from typing import Any, cast, Mapping
from src.app.core.logger import logging

logger = logging.getLogger(__name__)

settings = Settings()

wp = WebPush(
  public_key=settings.PUBLIC_KEY_PATH,
  private_key=settings.PRIVATE_KEY_PATH,
  subscriber="admin@mail.com",
)


async def send_webpush(subscription_data: dict[str, Any], payload: dict[str, Any]) -> bool:
  try:
    subscription = WebPushSubscription.model_validate(subscription_data)
    message = wp.get(message=payload, subscription=subscription)
  except Exception as e:
    logger.error(f"Webpush failed to validate subscription data: {e}")
    return False

  try:
    async with aiohttp.ClientSession() as session:
      await session.post(
        url=str(subscription.endpoint),
        data=message.encrypted,
        headers=cast(Mapping[str, str], message.headers),
      )
      logger.info(f"Webpush sent to {subscription.endpoint}")
  except Exception as e:
    logger.error(f"Webpush failed to send to {subscription.endpoint}: {e}")
    return False
  
  return True
