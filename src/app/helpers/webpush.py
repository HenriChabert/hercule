from typing import Any, Mapping, cast

import aiohttp
from webpush import WebPush, WebPushSubscription  # type: ignore

from src.app.core.config import Settings
from src.app.core.logger import logging

logger = logging.getLogger(__name__)

settings = Settings()

wp = WebPush(
    public_key=settings.PUBLIC_KEY_PATH,
    private_key=settings.PRIVATE_KEY_PATH,
    subscriber="chabhenrib@gmail.com",
)

async def send_webpush(
    subscription_data: dict[str, Any], payload: Mapping[str, Any]
) -> bool:
    try:
        subscription = WebPushSubscription.model_validate(subscription_data)
        message = wp.get(
            message=cast(dict[str, Any], payload), subscription=subscription
        )
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
            curl_equivalent = f"curl -X POST {subscription.endpoint} -d {message.encrypted}"
            for header, value in message.headers.items():
                curl_equivalent += f" -H '{header}: {value}'"

            logger.info(subscription.model_dump_json())
    except Exception as e:
        logger.error(f"Webpush failed to send to {subscription.endpoint}: {e}")
        return False

    return True
