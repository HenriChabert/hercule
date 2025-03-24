from src.app.models.user import User
from src.app.seeders.base import BaseSeeder
from tests.helpers.fakers.user import UserFaker, UserFields


class UserSeeder(BaseSeeder):
    async def seed(self, n: int = 1, fields: UserFields | None = None) -> list[User]:
        fakes: list[User] = []

        user_faker = UserFaker()

        for _ in range(n):
            fake = await user_faker.create_fake(self.session, fields)
            fakes.append(fake)

        return fakes
