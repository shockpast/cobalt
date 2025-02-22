import process from "node:process"
import { randomUUID } from "node:crypto"

import "jsr:@std/dotenv/load" // load .env

import { message } from "npm:telegraf/filters"
import { Input, Telegraf, TelegramError } from "npm:telegraf"
import type { InputMediaAudio, InputMediaPhoto, InputMediaVideo } from "npm:telegraf/types"

import i18n from "./i18n.ts"
import { getFiles } from "./main_utils.ts"
import { services } from "./main_data.ts"

///

const URL_REGEX = /(audio:|mute:)?(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/gi

///

const bot = new Telegraf(Deno.env.get("TELEGRAF_TOKEN")!)

///

bot.start((ctx) => {
  const t = i18n(ctx.message.from.language_code)

  ctx.replyWithPhoto(Input.fromLocalFile(".github/assets/ctb_banner.png"), {
    caption: t("bot.start"),
    parse_mode: "HTML"
  }).catch(() => {})
})

// todo: fetch from instance and cache it for hour
bot.hears(/\/(services)/, async (ctx) => {
  return await ctx.reply(services.join(", "), { parse_mode: "HTML", link_preview_options: { is_disabled: true } })
})

bot.hears(/\/(donate)/, async (ctx) => {
  const t = i18n(ctx.message.from.language_code)

  return await ctx.reply(t("bot.donate"), { parse_mode: "HTML", link_preview_options: { is_disabled: true } })
})

bot.on(message("text"), async (ctx) => {
  const t = i18n(ctx.message.from.language_code)

  //
  const urls = ctx.message.text.matchAll(URL_REGEX)
  if (urls == null) return

  const { files, source, error } = await getFiles(urls)
  if (error)
    return await ctx.reply(`${t(error.code)}\n\n<span class="tg-spoiler">🙀 ${error.code}</span>`, { reply_parameters: { message_id: ctx.message.message_id }, parse_mode: "HTML", link_preview_options: { is_disabled: true } })

  const mediaGroup: (InputMediaPhoto | InputMediaAudio | InputMediaVideo)[] = []

  files.filter(url => url.match(/(jpg|jpeg|png|webp|svg)/gi))
    .map((file) => mediaGroup.push({ type: "photo", media: file }))
  files.filter((url, index) => url.match(/(mp4|webm|mkv)/gi) || (url.includes("/tunnel?id=") && (source[index] && !source[index].includes("soundcloud") && !source[index].includes("audio:"))))
    .map((file) => mediaGroup.push({ type: "video", media: Input.fromURLStream(file, randomUUID().replaceAll("-", "").slice(0, 11)) }))
  files.filter((url, index) => url.match(/(mp3|ogg|wav)/gi) || (source[index] && source[index].includes("soundcloud") || source[index].includes("audio:")))
    .map((file) => mediaGroup.push({ type: "audio", media: Input.fromURLStream(file, randomUUID().replaceAll("-", "").slice(0, 11)) }))

  if (mediaGroup.length < 1) return

  // @ts-ignore: deno-ts(2345)
  ctx.replyWithMediaGroup(mediaGroup, { reply_parameters: { message_id: ctx.message.message_id } })
    .catch(async (err: TelegramError) => {
      const createMessage = (message: string, code: string) => `${message}\n\n<span class="tg-spoiler">🙀 ${code}</span>`

      if (err.description.includes("audio can't be mixed with other media types"))
        return await ctx.reply(createMessage(t("error.telegram.send.mixed"), "error.telegram.send.mixed"), { parse_mode: "HTML" })
    })
})

///

bot.catch(() => {})
bot.launch()

///

process.once("SIGINT", () => bot.stop("SIGINT"))
process.once("SIGTERM", () => bot.stop("SIGTERM"))