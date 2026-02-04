"use client"

import { useEffect, useRef, useState, useMemo } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
    Copy,
    Download,
    ExternalLink,
    ChevronDown,
    Check,
    Loader2,
    FileText,
    FileDown,
} from "lucide-react"
import { toast } from "sonner"
import { copyToClipboard, parseMarkdownHeaders, calculateReadingTime, exportToPDF } from "@/lib/utils"
import type { Citation } from "@/lib/types"

interface StreamingReportProps {
    report: string
    citations?: Citation[]
    isStreaming: boolean
}

export function StreamingReport({ report, citations = [], isStreaming }: StreamingReportProps) {
    const [parsedSections, setParsedSections] = useState<
        Array<{ id: string; title: string; content: string; collapsed: boolean }>
    >([])
    const [copied, setCopied] = useState(false)
    const [exporting, setExporting] = useState(false)
    const contentRef = useRef<HTMLDivElement>(null)

    // Parse report into sections based on markdown headers
    useEffect(() => {
        if (!report) return

        const headers = parseMarkdownHeaders(report)
        const sections: typeof parsedSections = []

        if (headers.length === 0) {
            // No headers found, treat entire report as one section
            sections.push({
                id: 'section-0',
                title: 'Research Report',
                content: report,
                collapsed: false,
            })
        } else {
            // Split by headers
            headers.forEach((header, index) => {
                const startIndex = report.indexOf(`${'#'.repeat(header.level)} ${header.text}`)
                const nextHeader = headers[index + 1]
                const endIndex = nextHeader
                    ? report.indexOf(`${'#'.repeat(nextHeader.level)} ${nextHeader.text}`)
                    : report.length

                const content = report.slice(startIndex, endIndex).trim()

                sections.push({
                    id: header.id,
                    title: header.text,
                    content,
                    collapsed: index > 0, // First section expanded by default
                })
            })
        }

        setParsedSections(sections)
    }, [report])

    // Auto-scroll to bottom when streaming
    useEffect(() => {
        if (isStreaming && contentRef.current) {
            contentRef.current.scrollTo({
                top: contentRef.current.scrollHeight,
                behavior: 'smooth',
            })
        }
    }, [report, isStreaming])

    const handleCopy = async () => {
        const success = await copyToClipboard(report)
        if (success) {
            setCopied(true)
            toast.success("Report copied to clipboard!")
            setTimeout(() => setCopied(false), 2000)
        } else {
            toast.error("Failed to copy report")
        }
    }

    const handleDownloadMarkdown = () => {
        // Create a blob and download
        const blob = new Blob([report], { type: 'text/markdown' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `research-report-${new Date().toISOString().slice(0, 10)}.md`
        a.click()
        URL.revokeObjectURL(url)
        toast.success("Markdown downloaded!")
    }

    const handleDownloadPDF = async () => {
        setExporting(true)
        const success = await exportToPDF(report, `research-report-${new Date().toISOString().slice(0, 10)}`)
        setExporting(false)

        if (success) {
            toast.success("PDF exported successfully!")
        } else {
            toast.error("Failed to export PDF")
        }
    }

    const toggleSection = (id: string) => {
        setParsedSections(prev =>
            prev.map(section =>
                section.id === id
                    ? { ...section, collapsed: !section.collapsed }
                    : section
            )
        )
    }

    const readingTime = useMemo(() => {
        return report ? calculateReadingTime(report) : '0 min read'
    }, [report])

    if (!report && !isStreaming) {
        return null
    }

    return (
        <div className="space-y-6">
            {/* Report Header */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-purple-600 to-indigo-600">
                        <FileText className="h-5 w-5 text-white" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                            Research Report
                        </h2>
                        {report && (
                            <p className="text-sm text-muted-foreground">
                                {readingTime} • {report.split(/\s+/).length} words
                            </p>
                        )}
                    </div>
                </div>

                {report && !isStreaming && (
                    <div className="flex items-center gap-2">
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleCopy}
                            className="group"
                        >
                            {copied ? (
                                <Check className="w-4 h-4 mr-1 text-green-500" />
                            ) : (
                                <Copy className="w-4 h-4 mr-1 group-hover:scale-110 transition-transform" />
                            )}
                            {copied ? 'Copied!' : 'Copy'}
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleDownloadMarkdown}
                            className="group"
                        >
                            < Download className="w-4 h-4 mr-1 group-hover:scale-110 transition-transform" />
                            MD
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleDownloadPDF}
                            disabled={exporting}
                            className="group"
                        >
                            {exporting ? (
                                <Loader2 className="w-4 h-4 mr-1 animate-spin" />
                            ) : (
                                <FileDown className="w-4 h-4 mr-1 group-hover:scale-110 transition-transform" />
                            )}
                            PDF
                        </Button>
                    </div>
                )}
            </div>

            {/* Report Content */}
            <div
                ref={contentRef}
                className="max-h-[700px] overflow-y-auto space-y-4 pr-3 
                 scrollbar-thin scrollbar-thumb-slate-300 dark:scrollbar-thumb-slate-600 
                 scrollbar-track-transparent"
            >
                <AnimatePresence mode="popLayout">
                    {parsedSections.map((section, index) => (
                        <motion.section
                            key={section.id}
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                            transition={{ duration: 0.4, ease: "easeOut" }}
                            className="group"
                        >
                            {/* Section Header */}
                            <button
                                onClick={() => toggleSection(section.id)}
                                className="w-full flex items-center justify-between p-5 
                         bg-gradient-to-r from-slate-50/50 to-white/50 
                         dark:from-slate-900/50 dark:to-slate-800/50 
                         rounded-2xl border-2 border-border/50 
                         hover:border-purple-300 dark:hover:border-purple-700
                         hover:shadow-md transition-all cursor-pointer
                         group-hover:bg-white/70 dark:group-hover:bg-slate-900/70"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-1.5 h-10 bg-gradient-to-b from-purple-400 to-indigo-500 rounded-full" />
                                    <span className="font-semibold text-foreground text-lg text-left">
                                        {section.title}
                                    </span>
                                </div>
                                <ChevronDown
                                    className={`w-5 h-5 transition-transform duration-200 text-muted-foreground
                             ${section.collapsed ? 'rotate-0' : 'rotate-180'}`}
                                />
                            </button>

                            {/* Section Content */}
                            <AnimatePresence>
                                {!section.collapsed && (
                                    <motion.div
                                        initial={{ opacity: 0, height: 0 }}
                                        animate={{ opacity: 1, height: "auto" }}
                                        exit={{ opacity: 0, height: 0 }}
                                        transition={{ duration: 0.3 }}
                                        className="mt-3 p-6 bg-white/70 dark:bg-slate-900/70 
                             backdrop-blur-sm rounded-2xl border-2 
                             border-border/50"
                                    >
                                        <div className="prose prose-slate dark:prose-invert max-w-none
                                  prose-headings:font-bold prose-headings:text-foreground
                                  prose-p:text-muted-foreground prose-p:leading-relaxed
                                  prose-a:text-purple-600 prose-a:no-underline hover:prose-a:underline
                                  prose-strong:text-foreground
                                  prose-code:bg-muted prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded
                                  prose-pre:bg-muted prose-pre:border prose-pre:border-border">
                                            <ReactMarkdown content={section.content} citations={citations} />
                                        </div>

                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.section>
                    ))}
                </AnimatePresence>

                {/* Streaming Indicator */}
                {isStreaming && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex items-center justify-center p-8 text-muted-foreground"
                    >
                        <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                        <span className="text-sm">Generating report...</span>
                    </motion.div>
                )}

                {/* Citations */}
                {citations.length > 0 && !isStreaming && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        className="mt-8 p-6 bg-slate-50/50 dark:bg-slate-900/50 rounded-2xl border-2 border-border/50"
                    >
                        <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
                            <ExternalLink className="w-5 h-5 text-purple-600" />
                            Sources & Citations
                        </h3>
                        <div className="space-y-3">
                            {citations.map((citation, index) => (
                                <a
                                    key={citation.id}
                                    href={citation.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block p-4 bg-white dark:bg-slate-950 rounded-xl border border-border
                           hover:border-purple-300 dark:hover:border-purple-700 hover:shadow-md
                           transition-all group"
                                >
                                    <div className="flex items-start gap-3">
                                        <Badge variant="outline" className="mt-0.5">{index + 1}</Badge>
                                        <div className="flex-1">
                                            <h4 className="font-medium text-sm group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                                                {citation.title}
                                            </h4>
                                            <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                                                {citation.snippet}
                                            </p>
                                            <p className="text-xs text-muted-foreground/60 mt-2 truncate">
                                                {citation.url}
                                            </p>
                                        </div>
                                        <ExternalLink className="w-4 h-4 text-muted-foreground group-hover:text-purple-600 transition-colors" />
                                    </div>
                                </a>
                            ))}
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    )
}

// Markdown renderer with IEEE citation support
function ReactMarkdown({ content, citations = [] }: { content: string; citations?: Citation[] }) {
    // Convert [N] citations to clickable links
    const processContent = (text: string): string => {
        let processed = text

        // Convert IEEE citations [1], [2], etc. to clickable links
        processed = processed.replace(
            /\[(\d+)\]/g,
            (match, num) => {
                const citationNum = parseInt(num)
                if (citationNum > 0 && citationNum <= citations.length) {
                    const citation = citations[citationNum - 1]
                    if (citation?.url) {
                        return `<a href="${citation.url}" target="_blank" rel="noopener noreferrer" class="citation-link text-purple-600 hover:text-purple-800 dark:text-purple-400 dark:hover:text-purple-300 font-medium hover:underline" title="${citation.title || 'View source'}">[${num}]</a>`
                    }
                }
                return match
            }
        )

        // Standard markdown processing
        processed = processed
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/gim, '<em>$1</em>')
            .replace(/`(.*?)`/gim, '<code>$1</code>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br />')

        return processed
    }

    const html = processContent(content)

    return <div dangerouslySetInnerHTML={{ __html: `<p>${html}</p>` }} />
}
