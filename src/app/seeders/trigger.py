from src.app.seeders.base import BaseSeeder

from tests.helpers.fakers.trigger import TriggerFaker, TriggerFields
from src.app.models.trigger import Trigger

class TriggerSeeder(BaseSeeder):
    def seed(self, n: int = 1, fields: TriggerFields | None = None) -> list[Trigger]:
        fakes: list[Trigger] = []

        trigger_faker = TriggerFaker()

        for _ in range(n):
            fake = trigger_faker.create_fake(self.session, fields)
            fakes.append(fake)

        return fakes
