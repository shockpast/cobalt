import os
from dataclasses import dataclass
from typing import List

import aiohttp

from services.database import Database

@dataclass
class TunnelRedirectResponse:
  status: str # tunnel/redirect
  url: str
  filename: str

@dataclass
class PickerObject:
  type: str
  url: str
  thumb: str
@dataclass
class PickerResponse:
  status: str # picker
  audio: str
  audio_filename: str
  picker: List[PickerObject]

@dataclass
class Response:
  status: str # picker/tunnel/redirect
  object: PickerResponse | TunnelRedirectResponse
@dataclass
class Error:
  code: str

async def download(group_id: int, url: str, download_mode: str = "auto"):
  db = Database()
  settings = db.get_group_settings(group_id)

  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {os.getenv("COBALT_TOKEN", "None")}",
    "User-Agent": os.getenv("COBALT_USER_AGENT", "None")
  }

  body = {
    "url": url,
    "audioFormat": "mp3",
    "downloadMode": download_mode,
    "filenameStyle": "nerdy",
    "videoQuality": settings.default_quality
  }

  async with aiohttp.ClientSession() as session:
    async with session.post(os.getenv("COBALT_BASE"), headers=headers, json=body) as response:
      json = await response.json()
      if json["status"] == "error":
        return Error(json["error"]["code"])
      if json["status"] == "tunnel" or json["status"] == "redirect":
        return TunnelRedirectResponse(json["status"], json["url"], json["filename"])
      if json["status"] == "picker":
        media_list = []
        for media in json["picker"]:
          media_list.append(PickerObject(media["type"], media["url"], media["thumb"]))

        return PickerResponse(json["status"], json["audio"], json["audioFilename"], media_list)

      return Error("error.bot.unknown")