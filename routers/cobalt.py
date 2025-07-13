from urllib.parse import urlparse
import pathlib
import uuid

from aiogram import Router, F, types, filters
import validators

from i18n import i18n
from services.database import Database
from services.cobalt import Error, PickerResponse, TunnelRedirectResponse, download
import utilities

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

@router.inline_query()
async def download_from_inline(query: types.InlineQuery):
  mime_type = { 
    ".opus": "audio/opus", ".mp3": "audio/mpeg", ".ogg": "audio/ogg",
    ".mp4": "video/mp4", ".webm": "video/webm"
  }

  url = query.query.strip()
  if not "https://" in url:
    return

  t = i18n(query.from_user.language_code)

  response = await download(query.from_user.id, url)
  results = []

  if isinstance(response, Error):
    await query.answer([], switch_pm_text=t.get(response.code), switch_pm_parameter="error")
    return

  if isinstance(response, PickerResponse):
    for item in response.picker:
      if item.type == "photo":
        results.append(types.InlineQueryResultPhoto(id=str(uuid.uuid4()), photo_url=item.url, title=url, thumbnail_url=item.thumb))
      if item.type == "gif":
        results.append(types.InlineQueryResultGif(id=str(uuid.uuid4()), gif_url=item.url, title=url, thumbnail_url=item.thumb))
      if item.type == "video":
        results.append(types.InlineQueryResultVideo(id=str(uuid.uuid4()), video_url=item.url, title=url, thumbnail_url=item.thumb))
  if isinstance(response, TunnelRedirectResponse):
    media_type = pathlib.Path(response.filename).suffix

    if media_type in (".opus", ".mp3", ".ogg"):
      results.append(types.InlineQueryResultAudio(id=str(uuid.uuid4()), audio_url=response.url, title=url, mime_type=mime_type.get(media_type), thumbnail_url=response.url))
    if media_type == ".gif":
      results.append(types.InlineQueryResultGif(id=str(uuid.uuid4()), gif_url=response.url, title=url, thumbnail_url=response.url))
    if media_type in (".mp4", ".webm"):
      results.append(types.InlineQueryResultVideo(id=str(uuid.uuid4()), video_url=response.url, title=url, mime_type=mime_type.get(media_type), thumbnail_url=response.url))
    if media_type in (".png", ".jpg", ".jpeg", ".webp"):
      results.append(types.InlineQueryResultPhoto(id=str(uuid.uuid4()), photo_url=response.url, title=url, thumbnail_url=response.url))

  await query.answer(results, cache_time=1)

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