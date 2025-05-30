from src.app.models.trigger import Trigger
from src.app.seeders.base import BaseSeeder
from tests.helpers.fakers.trigger import TriggerFaker, TriggerFields


class TriggerSeeder(BaseSeeder):
    async def seed(
        self, n: int = 1, fields: TriggerFields | None = None
    ) -> list[Trigger]:
        fakes: list[Trigger] = []

        trigger_faker = TriggerFaker()

        for _ in range(n):
            fake = await trigger_faker.create_fake(self.session, fields)
            fakes.append(fake)

        return fakes
