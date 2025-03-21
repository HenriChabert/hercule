#! /usr/bin/env python
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed import seed_database
from src.app.seeders.webhook import WebhookSeeder
from src.app.seeders.trigger import TriggerSeeder
from src.app.core.db.database import session_manager
from src.app.core.config import settings


import click

async def reinit_db() -> None:
    session_manager.init(settings.SQLITE_URI)
    async with session_manager.connect() as connection:
        await session_manager.drop_all(connection)
        await session_manager.create_all(connection)

async def apply_seed() -> None:
    await reinit_db()
    async with session_manager.session() as session:
        await seed_database(session)

@click.group()
def cli():
    pass

@cli.command()
def seed():
    print("Starting database seeding process...")
    asyncio.run(apply_seed())
    print("Database seeding completed successfully!")
    
@cli.command()
def reset():
    print("Resetting database...")
    asyncio.run(reinit_db())
    print("Database reset successfully!")

if __name__ == "__main__":
    cli()
