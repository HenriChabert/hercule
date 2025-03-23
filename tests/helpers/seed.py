from src.app.seeders.user import UserSeeder, UserFields
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast

def get_test_admin_user_fields():
    return cast(UserFields, {
        "email": "admin@test.com",
        "role": "admin",
        "password": "admin"
    })

def get_test_user_fields():
    return cast(UserFields, {
        "email": "user@test.com",
        "role": "user",
        "password": "user"
    })

async def seed_db(db: AsyncSession):
    user_seeder = UserSeeder(db)

    test_user = get_test_admin_user_fields()
    user = await user_seeder.seed(n=1, fields=test_user)

    test_user = get_test_user_fields()
    user = await user_seeder.seed(n=1, fields=test_user)

    return user
