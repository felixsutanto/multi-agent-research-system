"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { en } from "@/locales/en"
import { id } from "@/locales/id"
import type { Translations } from "@/locales/en"

type Locale = "en" | "id"

interface LanguageContextType {
    locale: Locale
    t: Translations
    setLocale: (locale: Locale) => void
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

const translations = { en, id }

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [locale, setLocaleState] = useState<Locale>("en")

    useEffect(() => {
        // Load saved locale from localStorage
        const saved = localStorage.getItem("locale") as Locale | null
        if (saved && (saved === "en" || saved === "id")) {
            setLocaleState(saved)
        }
    }, [])

    const setLocale = (newLocale: Locale) => {
        setLocaleState(newLocale)
        localStorage.setItem("locale", newLocale)
    }

    const value = {
        locale,
        t: translations[locale],
        setLocale,
    }

    return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>
}

export function useLanguage() {
    const context = useContext(LanguageContext)
    if (!context) {
        throw new Error("useLanguage must be used within LanguageProvider")
    }
    return context
}
