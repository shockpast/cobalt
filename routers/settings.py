from aiogram import Router, F, types, filters, enums
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from i18n import i18n
from services.database import Database
from entities.keyboards import settings as SettingsKeyboard

class SettingsState(StatesGroup):
  value = State()

router = Router()

@router.callback_query(F.data.contains("settings:update"))
async def update_settings(callback: types.CallbackQuery, state: FSMContext):
  message = callback.message
  data = callback.data

  chat = message.chat
  user = message.from_user

  db = Database()
  t = i18n(user.language_code)

  group_id = chat.id if user.id != chat.id else user.id
  group_settings = db.get_group_settings(group_id)

  settings_key = data.split(":")[2]
  settings_value = group_settings[settings_key]

  match settings_key:
    case "accept_only_messages":
      db.update_group_settings(group_id, settings_key, not bool(settings_value))
    case "accept_only_commands":
      db.update_group_settings(group_id, settings_key, not bool(settings_value))
    case "default_quality":
      await state.set_state(SettingsState.value)
      return await message.reply(t.get("messages.settings.quality_options"), parse_mode="Markdown")

  return await message.edit_reply_markup(reply_markup=SettingsKeyboard(db, group_id))

@router.message(SettingsState.value)
async def update_settings_state(message: types.Message, state: FSMContext):
  chat = message.chat
  user = message.from_user

  db = Database()
  t = i18n(user.language_code)

  group_id = chat.id if user.id != chat.id else user.id
  quality = message.text.replace("p", "")

  if not quality in ["480", "720", "1080"]:
    await state.clear()
    return await message.reply(t.get("messages.settings.quality_invalid").format(quality=quality), parse_mode=enums.ParseMode.HTML)

  db.update_group_settings(group_id, "default_quality", quality)

  await state.clear()
  return await message.reply(t.get("messages.settings.updated_settings"))

@router.message(filters.Command("settings"))
async def settings(message: types.Message):
  chat = message.chat
  user = message.from_user

  db = Database()
  t = i18n(user.language_code)

  group_id = chat.id if user.id != chat.id else user.id
  user_status = await message.bot.get_chat_member(chat.id, user.id)

  has_permissions = False
  
  if chat.id == user.id:
    has_permissions = True
  if user_status.status == enums.ChatMemberStatus.ADMINISTRATOR or user_status.status == enums.ChatMemberStatus.CREATOR:
    has_permissions = True

  if not has_permissions:
    return await message.reply(t.get("bot.errors.permissions.insufficient"))

  return await message.reply("you can change this group's settings here", reply_markup=SettingsKeyboard(db, group_id))