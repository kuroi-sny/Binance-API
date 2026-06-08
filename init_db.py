import asyncio
from database import engine 
import models

async def init_models():
    print("Connecting to Postgresql:  ")

    async with engine.begin() as conn: ## websocket
        await conn.run_sync(models.Base.metadata.create_all)
    print("Table created successfuly!")

asyncio.run(init_models())

