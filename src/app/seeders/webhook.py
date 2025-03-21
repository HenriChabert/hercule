from src.app.seeders.base import BaseSeeder

from tests.helpers.fakers.webhook import WebhookFaker, WebhookFields
from src.app.models.webhook import Webhook

class WebhookSeeder(BaseSeeder):
    async def seed(self, n: int = 1, fields: WebhookFields | None = None) -> list[Webhook]:
        fakes: list[Webhook] = []
        webhook_faker = WebhookFaker()

        for _ in range(n):
            fake = await webhook_faker.create_fake(self.session, fields)
            fakes.append(fake)

        return fakes
