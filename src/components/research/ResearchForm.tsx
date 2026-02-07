"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import {
    ArrowRight, Sparkles, Loader2,
    Car, Brain, Leaf, Landmark, Atom, HeartPulse, Shield, Shirt,
    type LucideIcon
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { ResearchFormSchema, type ResearchFormData } from "@/lib/types"
import { RESEARCH_PRESETS } from "@/data/presets"
import { toast } from "sonner"

// Icon mapping for preset icons
const iconMap: Record<string, LucideIcon> = {
    Car, Brain, Leaf, Landmark, Atom, HeartPulse, Shield, Shirt,
}

function PresetIcon({ name }: { name: string }) {
    const IconComponent = iconMap[name]
    if (!IconComponent) return <span className="text-2xl">{name}</span>
    return <IconComponent className="h-7 w-7 text-purple-500" />
}

interface ResearchFormProps {
    onSubmit: (data: ResearchFormData) => Promise<void>
    isLoading?: boolean
}

export function ResearchForm({ onSubmit, isLoading = false }: ResearchFormProps) {
    const [isFocused, setIsFocused] = useState(false)
    const [presetsOpen, setPresetsOpen] = useState(false)

    const form = useForm<ResearchFormData>({
        resolver: zodResolver(ResearchFormSchema),
        defaultValues: {
            query: "",
            maxIterations: 1, // Reduced from 3 for faster results on HF free tier
            includeAnalysis: true,
        },
        mode: "onChange",
    })


    const handleSubmit = async (data: ResearchFormData) => {
        try {
            await onSubmit(data)
        } catch (error) {
            toast.error("Failed to start research. Please try again.")
        }
    }

    const handlePresetSelect = (query: string) => {
        form.setValue("query", query)
        setPresetsOpen(false)
        toast.success("Preset loaded!")
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
            e.preventDefault()
            form.handleSubmit(handleSubmit)()
        }
    }

    return (
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6 max-w-3xl mx-auto">
            {/* Main Query Input */}
            <div className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-3xl opacity-20 group-hover:opacity-30 blur transition duration-200" />
                <div className="relative">
                    <div className="absolute left-5 top-5 z-10">
                        <Sparkles className="h-5 w-5 text-purple-500 animate-pulse" />
                    </div>

                    <Textarea
                        {...form.register("query")}
                        placeholder="Ask a complex research question...

Example: Analyze Indonesia's 2026 EV policy impact on automotive industry"
                        className="min-h-[180px] pl-14 pr-6 pt-6 resize-none 
                     bg-white dark:bg-slate-950 
                     border-2 border-purple-200 dark:border-purple-900/50 
                     focus:border-purple-400 focus:ring-4 focus:ring-purple-500/10 
                     rounded-2xl text-base leading-relaxed
                     transition-all duration-200"
                        onFocus={() => setIsFocused(true)}
                        onBlur={() => setIsFocused(false)}
                        onKeyDown={handleKeyDown}
                        disabled={isLoading}
                    />

                    {isFocused && !isLoading && (
                        <div className="absolute bottom-4 right-4 text-xs text-muted-foreground flex items-center gap-2 animate-in fade-in duration-200">
                            <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                                <span className="text-xs">Ctrl</span>↵
                            </kbd>
                            <span>to submit</span>
                        </div>
                    )}
                </div>

                {form.formState.errors.query && (
                    <p className="mt-2 text-sm text-red-500 flex items-center gap-1">
                        {form.formState.errors.query.message}
                    </p>
                )}
            </div>

            {/* Options Row */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                {/* Left side: Options */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                    <div className="flex items-center gap-2">
                        <input
                            type="checkbox"
                            id="includeAnalysis"
                            {...form.register("includeAnalysis")}
                            className="w-4 h-4 rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                            disabled={isLoading}
                        />
                        <Label
                            htmlFor="includeAnalysis"
                            className="text-sm text-muted-foreground cursor-pointer select-none"
                        >
                            Include data analysis & charts
                        </Label>
                    </div>

                    {/* Preset Templates Dialog */}
                    <Dialog open={presetsOpen} onOpenChange={setPresetsOpen}>
                        <DialogTrigger asChild>
                            <Button
                                type="button"
                                variant="outline"
                                size="sm"
                                className="text-xs"
                                disabled={isLoading}
                            >
                                <Sparkles className="h-3 w-3 mr-1" />
                                Browse Presets
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
                            <DialogHeader>
                                <DialogTitle>Research Presets</DialogTitle>
                                <DialogDescription>
                                    Choose from popular research templates to get started quickly
                                </DialogDescription>
                            </DialogHeader>

                            <div className="grid gap-3 mt-4">
                                {RESEARCH_PRESETS.map((preset) => (
                                    <button
                                        key={preset.id}
                                        onClick={() => handlePresetSelect(preset.query)}
                                        className="flex items-start gap-4 p-4 rounded-xl border-2 border-border 
                             hover:border-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/20 
                             transition-all text-left group"
                                    >
                                        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
                                            <PresetIcon name={preset.icon} />
                                        </div>
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <h4 className="font-semibold text-sm group-hover:text-purple-600 dark:group-hover:text-purple-400">
                                                    {preset.title}
                                                </h4>
                                                <Badge variant="secondary" className="text-xs capitalize">
                                                    {preset.category}
                                                </Badge>
                                            </div>
                                            <p className="text-xs text-muted-foreground line-clamp-2">
                                                {preset.description}
                                            </p>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </DialogContent>
                    </Dialog>
                </div>

                {/* Right side: Submit Button */}
                <Button
                    type="submit"
                    size="lg"
                    disabled={isLoading || !form.watch("query").trim()}
                    className="group bg-gradient-to-r from-purple-600 to-indigo-600 
                   hover:from-purple-700 hover:to-indigo-700 
                   px-8 h-12 rounded-xl shadow-lg 
                   hover:shadow-xl transition-all duration-300
                   disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                            Researching...
                        </>
                    ) : (
                        <>
                            Start Research
                            <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                        </>
                    )}
                </Button>
            </div>
        </form>
    )
}
