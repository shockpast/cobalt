export type FunctionResult = {
  /**
   * mainly provided from cobalt.tools
   */
  error?: {
    /**
     * humanly readable code string
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
  /**
   * url to file array
   */
  files: string[]
  /**
   * url to url array
   */
  source: string[]
}

export type TelegramChat = {
  id: number
  /**
   * exists only in telegram groups
   */
  title?: string
  /**
   * `channel` is a wild guess
   */
  type: "supergroup" | "private" | "channel"
  username?: string
  first_name?: string
  last_name?: string
}