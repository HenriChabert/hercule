import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.seeders.webhook import WebhookSeeder
from src.app.seeders.trigger import TriggerSeeder
from src.app.seeders.user import UserSeeder

from sqlalchemy.ext.asyncio import AsyncSession

async def seed_database(session: AsyncSession) -> None:
    trigger_seeder = TriggerSeeder(session)
    webhook_seeder = WebhookSeeder(session)

    webhooks = await webhook_seeder.seed(fields={
        "url": "https://n8n.andover.ai/webhook-test/test-on-trigger-clicked"
    })

    _ = await trigger_seeder.seed(fields={
        "name": "n8n Webhook Test",
        "webhook_id": webhooks[-1].id
    })

    await trigger_seeder.seed(n=9)

    user_seeder = UserSeeder(session)
    await user_seeder.seed(n=1, fields={
        "email": "test@test.com",
        "password": "test"
    })