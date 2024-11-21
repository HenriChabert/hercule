from src.app.seeders.base import BaseSeeder

from tests.helpers.fakers.trigger import TriggerFaker, TriggerFields

class TriggerSeeder(BaseSeeder):
    def seed(self, n: int = 1, fields: TriggerFields | None = None) -> None:
        trigger_faker = TriggerFaker()

        for _ in range(n):
            trigger_faker.create_fake(self.session, fields)
