from aiogram import Router, filters, types, enums

from i18n import i18n

router = Router()

@router.message(filters.Command("start"))
async def start(message: types.Message):
  t = i18n(message.from_user.language_code)

  return await message.reply_photo(types.FSInputFile("assets/ctb_banner.png"), t.get("bot.start"), parse_mode=enums.ParseMode.HTML)