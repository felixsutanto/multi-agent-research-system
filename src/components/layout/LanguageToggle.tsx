"use client"

import { Globe } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useLanguage } from "@/components/shared/language-provider"

export function LanguageToggle() {
    const { locale, setLocale } = useLanguage()

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="relative">
                    <Globe className="h-5 w-5" />
                    <span className="sr-only">Toggle language</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem
                    onClick={() => setLocale("en")}
                    className={locale === "en" ? "bg-accent" : ""}
                >
                    <span className="mr-2">🇺🇸</span>
                    English
                </DropdownMenuItem>
                <DropdownMenuItem
                    onClick={() => setLocale("id")}
                    className={locale === "id" ? "bg-accent" : ""}
                >
                    <span className="mr-2">🇮🇩</span>
                    Indonesia
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}
