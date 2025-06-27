import logging
import os

from aiogram import Router, types, filters

from services.database import Database
from i18n import i18n

logger = logging.getLogger("cobalt")
router = Router()
database = Database()

@router.message(filters.Command("stats"))
async def telemetry_statistics(message: types.Message):
  t = i18n(message.from_user.language_code)
  
  if message.from_user.id != int(os.getenv("BOT_ADMIN")):
    return await message.reply(t.get("bot.errors.permissions.insufficient"))

  daily, daily_total     = database.get_daily_statistics()
  weekly, weekly_total   = database.get_weekly_statistics()
  monthly, monthly_total = database.get_monthly_statistics()

  return await message.reply(
    "🐱 statistics\n\n"
    f"daily: {daily} / {daily_total}\n"
    f"weekly: {weekly} / {weekly_total}\n"
    f"monthly: {monthly} / {monthly_total}",
  )