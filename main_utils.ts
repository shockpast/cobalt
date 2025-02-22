import type { APIRequest, APIResponse } from "./types/v10.ts"
import type { FunctionResult } from "./types/other.ts"

const httpClient = Deno.createHttpClient({
  poolMaxIdlePerHost: 0,
  poolIdleTimeout: 5
})

export async function getFiles(urls: IterableIterator<RegExpMatchArray>): Promise<FunctionResult> {
  const files: string[] = []
  const source: string[] = []

  for (const url of urls) {
    const capture = url[0]
    const mode = capture.includes("audio:") ? "audio" : capture.includes("mute:") ? "mute" : "auto"

    source.push(capture)

    const response = await fetch(Deno.env.get("API_URL")!, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": `Api-Key ${Deno.env.get("API_KEY")}`,
        "User-Agent": Deno.env.get("USER_AGENT")
      },
      body: JSON.stringify({
        url: capture.replace(`${mode}:`, ""),
        filenameStyle: "pretty",
        downloadMode: mode
      } satisfies APIRequest),
      client: httpClient
    })

    if (response.status != 200)
      return { files: [], source: source }

    const json: APIResponse = await response.json()
    if (json.status == "error")
      return { files: [], source: source, error: json.error }

    switch (json.status) {
      case "picker":
        json.picker.forEach(data => files.push(data.url))
        break
      case "tunnel":
      case "redirect":
        files.push(json.url)
        break
    }
  }

  return { files, source }
}