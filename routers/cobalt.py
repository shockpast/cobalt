from urllib.parse import urlparse
import pathlib

from aiogram import Router, F, types, filters
import validators

from services.database import Database
from i18n import i18n
from services.cobalt import Error, PickerResponse, TunnelRedirectResponse, download

router = Router()

async def _download(message: types.Message):
  group_id = message.chat.id if message.from_user.id != message.chat.id else message.from_user.id

  db = Database()
  t = i18n(message.from_user.language_code)

  db.log_activity(group_id)
  db.create_group(group_id)

  urls = []
  for url in message.text.split(" "):
    url_str = urlparse(url)._replace(fragment="").geturl()
    if validators.url(url_str):
      urls.append(url_str)

  media_group = []
  for url in urls:
    response = await download(group_id, url)

    if isinstance(response, Error):
      return await message.reply(t.get(response.code), parse_mode="HTML", link_preview_options=types.LinkPreviewOptions(is_disabled=True))
    if isinstance(response, TunnelRedirectResponse):
      media_type = pathlib.Path(response.filename).suffix
      file = types.URLInputFile(url=response.url, filename=response.filename)

      match media_type:
        case ".opus" | ".mp3" | ".ogg":
          media_group.append(types.InputMediaAudio(media=file))
        case ".gif":
          media_group.append(types.InputMediaDocument(media=file))
        case ".mp4" | ".webm":
          media_group.append(types.InputMediaVideo(media=file))
        case ".png" | ".jpg" | ".jpeg" | ".webp":
          media_group.append(types.InputMediaPhoto(media=file))
    if isinstance(response, PickerResponse):
      for media in response.picker:
        file = types.URLInputFile(url=media.url)

        match media.type:
          case "photo":
            media_group.append(types.InputMediaPhoto(media=file))
          case "gif":
            media_group.append(types.InputMediaAnimation(media=file))
          case "video":
            media_group.append(types.InputMediaVideo(media=file))

  if len(media_group) >= 1:
    return await message.reply_media_group(media_group)

@router.message(F.text.startswith("https://") | F.text.startswith("http://"))
async def download_from_text(message: types.Message):
  chat = message.chat
  user = message.from_user

  db = Database()

  group_id = chat.id if user.id != chat.id else user.id
  group_settings = db.get_group_settings(group_id)

  if group_settings.accept_only_messages:
    return await _download(message)

@router.message(filters.Command("download"))
async def download_from_command(message: types.Message):
  chat = message.chat
  user = message.from_user

  db = Database()

  group_id = chat.id if user.id != chat.id else user.id
  group_settings = db.get_group_settings(group_id)

  if group_settings.accept_only_commands:
    return await _download(message)