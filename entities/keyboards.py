from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.database import Database
from i18n import i18n

def settings(db: Database, group_id: int, lang: str = "en"):
  group_settings = db.get_group_settings(group_id)
  t = i18n(lang)

  builder = InlineKeyboardBuilder()
  builder.row(
    InlineKeyboardButton(text=f"{('✅' if group_settings.accept_only_messages else '❌') + ' ' + t.get('bot.settings.accept_only_messages')}", callback_data=f"settings:update:accept_only_messages"),
    InlineKeyboardButton(text=f"{('✅' if group_settings.accept_only_commands else '❌') + ' ' + t.get('bot.settings.accept_only_commands')}", callback_data=f"settings:update:accept_only_commands"),
  )
  builder.row(
    InlineKeyboardButton(text=t.get("bot.settings.default_quality") + f' ({group_settings.default_quality}p)', callback_data=f"settings:update:default_quality"),
  )
  
  return builder.as_markup()