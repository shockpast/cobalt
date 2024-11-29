//
import i18next from "https://deno.land/x/i18next@v23.16.4/index.js"

//
import english from "./locales/en.json" with { type: "json" }
import russian from "./locales/ru.json" with { type: "json" }

//
const systemLocale = Intl.DateTimeFormat().resolvedOptions().locale

//
i18next
  .init({
    fallbackLng: "en",
    resources: {
      en: { translation: english },
      ru: { translation: russian }
    }
  })

//
export default (language: string | undefined | null) => i18next.getFixedT(language || systemLocale)