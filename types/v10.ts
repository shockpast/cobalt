type APIPicker = {
  type: "photo" | "video" | "gif"
  url: string
  /**
   * thumbnail url
   */
  thumb?: string
}

export type APIRequest = {
  /**
   * **must** be included in every request.
   */
  url: string
  /**
   * `720` quality is recommended for phones.
   *
   * default: `1080`
   */
  videoQuality?: "144" | "360" | "480" | "720" | "1080" | "2160" | "4320" | "max"
  /**
   * default: `mp3`
   */
  audioFormat?: "best" | "mp3" | "opus" | "ogg" | "wav"
  /**
   * specifies the bitrate to use for the audio. applies only to audio conversion.
   *
   * default: `128`
   */
  audioBitrate?: "320" | "256" | "128" | "96" | "64" | "8"
  /**
   * changes the way files are named. previews can be seen in the web app.
   *
   * default: `classic`
   */
  filenameStyle?: "classic" | "nerdy" | "pretty" | "basic"
  /**
   * `audio` downloads only the audio, `mute` skips the audio track in videos.
   *
   * default: `auto`
   */
  downloadMode?: "auto" | "audio" | "mute"
  /**
   * `h264` is recommended for phones.
   *
   * default: `h264`
   */
  youtubeVideoCodec?: "h264" | "av1" | "vp9"
  /**
   * specifies the language of audio to download, when the youtube video is dubbed
   */
  youtubeDubLang?: string
  /**
   * uses value from the Accept-Language header for `youtubeDubLang`.
   *
   * default: `false`
   */
  youtubeDubBrowserLang?: boolean
  /**
   * tunnels all downloads through the processing server, even when not necessary.
   *
   * default: `false`
   */
  alwaysProxy?: boolean
  /**
   * disables file metadata when set to `true`.
   *
   * default: `false`
   */
  disableMetadata?: boolean
  /**
   * enables download of original sound used in a tiktok video.
   *
   * default: `false`
   */
  tiktokFullAudio?: boolean
  /**
   * changes whether 1080p h265 videos are preferred or not.
   *
   * default: `false`
   */
  tiktokH265?: boolean
  /**
   * changes whether twitter gifs are converted to .gif
   *
   * default: `true`
   */
  twitterGif?: boolean
}

export type ErrorResponse = {
  /**
   * error
   */
  status: "error"
  /**
   * contains more context about the error
   */
  error: {
    /**
     * machine-readable error code explaining the failure reason
     */
    code: string
    /**
     * container for providing more context
     */
    context: {
      /**
       * stating which service was being downloaded from
       */
      service: string
      /**
       * number providing the ratelimit maximum number of requests, or maximum downloadable video duration
       */
      limit: number
    }
  }
}

export type PickerResponse = {
  status: "picker"
  /**
   * returned when an image slideshow (such as on tiktok) has a general background audio
   */
  audio?: string
  /**
   * cobalt-generated filename, returned if `audio` exists
   */
  audioFilename?: string
  /**
   * array of objects containing the individual media
   */
  picker: APIPicker[]
}

/**
 * `tunnel` or `redirect` Response
 */
export type TunDirResponse = {
  status: "tunnel" | "redirect"
  /**
   * url for the cobalt tunnel, or redirect to an external link
   */
  url: string
  /**
   * cobalt-generated filename for the file being downloaded
   */
  filename: string
}

/**
 * APIResponse is unified collection of all responses (typed)
 */
export type APIResponse = TunDirResponse | PickerResponse | ErrorResponse