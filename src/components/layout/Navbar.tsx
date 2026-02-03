"use client"

import Link from "next/link"
import { Brain } from "lucide-react"
import { ThemeToggle } from "./ThemeToggle"
import { LanguageToggle } from "./LanguageToggle"
import { useLanguage } from "@/components/shared/language-provider"

export function Navbar() {
    const { t } = useLanguage()

    return (
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 max-w-screen-2xl items-center">
                <Link href="/" className="flex items-center gap-2 mr-6 hover:opacity-80 transition">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-indigo-600">
                        <Brain className="h-5 w-5 text-white" />
                    </div>
                    <span className="hidden font-bold sm:inline-block bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                        Multi-Agent Research
                    </span>
                </Link>

                <nav className="flex flex-1 items-center gap-6 text-sm">
                    <Link
                        href="/research"
                        className="transition-colors hover:text-foreground/80 text-foreground/60 font-medium"
                    >
                        {t.nav.research}
                    </Link>
                    <Link
                        href="/history"
                        className="transition-colors hover:text-foreground/80 text-foreground/60 font-medium"
                    >
                        {t.nav.history}
                    </Link>
                </nav>

                <div className="flex items-center gap-2">
                    <LanguageToggle />
                    <ThemeToggle />
                </div>
            </div>
        </header>
    )
}
