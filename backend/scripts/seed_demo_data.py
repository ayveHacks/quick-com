import asyncio

from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database
from app.services.seed_service import seed_demo_data


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    summary = await seed_demo_data(db)
    print("Seed summary:", summary)
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())

