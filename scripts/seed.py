import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.seeders.webhook import WebhookSeeder
from src.app.seeders.trigger import TriggerSeeder
from src.app.seeders.user import UserSeeder

from sqlalchemy.ext.asyncio import AsyncSession


async def seed_database(session: AsyncSession) -> None:
    user_seeder = UserSeeder(session)
    await user_seeder.seed(
        fields={"email": "admin@hercule.com", "role": "admin", "password": "admin"}
    )

    await user_seeder.seed(
        fields={"email": "user@hercule.com", "role": "user", "password": "user"}
    )
