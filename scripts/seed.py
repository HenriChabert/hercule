import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.seeders.webhook import WebhookSeeder
from src.app.seeders.trigger import TriggerSeeder
from src.app.core.db.database import sync_get_db, reinit_db

def seed_database() -> None:
    reinit_db()

    session = sync_get_db()

    trigger_seeder = TriggerSeeder(session)
    webhook_seeder = WebhookSeeder(session)

    webhooks = webhook_seeder.seed(fields={
        "url": "https://n8n.andover.ai/webhook-test/test-on-trigger-clicked"
    })

    triggers = trigger_seeder.seed(fields={
        "name": "n8n Webhook Test",
        "webhook_id": webhooks[-1].id
    })

    trigger_seeder.seed(n=9)

    session.close()

if __name__ == "__main__":
    seed_database()
