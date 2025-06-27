import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from services.database import Database
from routers import cobalt, settings, general, telemetry

logging.basicConfig(format='[%(asctime)s] [%(filename)s/%(funcName)s:%(lineno)d] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("cobalt")

load_dotenv()

async def main():
  dp = Dispatcher()
  db = Database("cobalt")
  bot = Bot(os.getenv("BOT_TOKEN"))

  db.initialize()
  dp.include_router(general.router)
  dp.include_router(settings.router)
  dp.include_router(cobalt.router)
  dp.include_router(telemetry.router)

  await dp.start_polling(bot)

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    pass