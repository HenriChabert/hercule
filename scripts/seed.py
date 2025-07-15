import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.seeders.trigger import TriggerFields, TriggerSeeder
from src.app.seeders.user import UserFields, UserSeeder
from src.app.seeders.webhook import WebhookFields, WebhookSeeder


async def seed_users(session: AsyncSession) -> None:
    user_seeder = UserSeeder(session)
    await user_seeder.seed(
        fields=UserFields(
            email="admin@hercule.com",
            role="admin",
            password="admin",
        )
    )

    await user_seeder.seed(
        fields=UserFields(
            email="user@hercule.com",
            role="user",
            password="user",
        )
    )


async def seed_webhooks(session: AsyncSession) -> None:
    webhook_seeder = WebhookSeeder(session)
    await webhook_seeder.seed(
        fields=WebhookFields(
            id="webhook-1",
            name="Webhook 1",
            url="https://webhook.site/1234567890",
        )
    )

    await webhook_seeder.seed(
        fields=WebhookFields(
            id="webhook-2",
            name="Webhook 2",
            url="https://webhook.site/1234567890",
        )
    )


async def seed_triggers(session: AsyncSession) -> None:
    trigger_seeder = TriggerSeeder(session)
    await trigger_seeder.seed(
        fields=TriggerFields(
            id="trigger-1",
            name="Page opened",
            webhook_id="webhook-1",
            event="page_opened",
        )
    )

    await trigger_seeder.seed(
        fields=TriggerFields(
            id="trigger-2",
            name="Button clicked",
            webhook_id="webhook-2",
            event="button_clicked",
        )
    )

    await trigger_seeder.seed(
        fields=TriggerFields(
            id="trigger-3",
            name="Manual trigger in popup",
            webhook_id="webhook-3",
            event="manual_trigger_in_popup",
        )
    )


async def seed_database(session: AsyncSession) -> None:
    await seed_users(session)
    await seed_webhooks(session)
    await seed_triggers(session)
