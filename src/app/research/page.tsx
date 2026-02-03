"use client"

import { Suspense } from "react"
import { AlertCircle } from "lucide-react"
import { Navbar } from "@/components/layout/Navbar"
import { ResearchForm } from "@/components/research/ResearchForm"
import { AgentTimeline } from "@/components/research/AgentTimeline"
import { StreamingReport } from "@/components/research/StreamingReport"
import { MetricsDashboard } from "@/components/research/MetricsDashboard"
import { useResearch } from "@/hooks/useResearch"
import { toast } from "sonner"

export default function ResearchPage() {
    const {
        agentActivities,
        reportContent,
        citations,
        metrics,
        isStreaming,
        isConnected,
        error,
        isStarting,
        startResearch,
    } = useResearch()

    const handleStartResearch = async (data: any) => {
        try {
            await startResearch(data)
            toast.success("Research started successfully!")
        } catch (err) {
            console.error("Failed to start research:", err)
            toast.error("Failed to start research. Please try again.")
        }
    }

    const hasContent = agentActivities.length > 0 || reportContent || isStreaming

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30 
                   dark:from-slate-950 dark:via-slate-950/50 dark:to-purple-950/20">
            <Navbar />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
                {/* Hero Section */}
                <section className="py-16 sm:py-20">
                    <div className="text-center mb-12">
                        <h1 className="text-4xl sm:text-5xl md:text-6xl font-black bg-gradient-to-r 
                          from-purple-600 via-indigo-600 to-blue-600 
                          bg-clip-text text-transparent mb-6">
                            Multi-Agent Research
                        </h1>
                        <p className="text-lg sm:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                            Watch AI agents collaborate to conduct comprehensive research,
                            analyze data, and generate professional reports in real-time.
                        </p>
                    </div>

                    {/* Research Form */}
                    <ResearchForm onSubmit={handleStartResearch} isLoading={isStarting || isStreaming} />
                </section>

                {/* Connection Error */}
                {error && (
                    <div className="mb-8 p-4 bg-red-50 dark:bg-red-950/20 border-2 border-red-200 
                        dark:border-red-900 rounded-2xl flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5 flex-shrink-0" />
                        <div>
                            <h3 className="font-semibold text-red-900 dark:text-red-100 mb-1">
                                Connection Error
                            </h3>
                            <p className="text-sm text-red-700 dark:text-red-200">
                                {error}
                            </p>
                            <p className="text-xs text-red-600 dark:text-red-300 mt-2">
                                Please check your backend API connection and try again.
                            </p>
                        </div>
                    </div>
                )}

                {/* Dynamic Content Area */}
                {hasContent && (
                    <div className="space-y-12 animate-in fade-in duration-500">
                        {/* Agent Timeline */}
                        {(agentActivities.length > 0 || isStreaming) && (
                            <Suspense fallback={<LoadingSkeleton />}>
                                <div className="bg-white/70 dark:bg-slate-900/70 backdrop-blur-sm 
                              p-6 sm:p-8 rounded-3xl border-2 border-border/50 shadow-xl">
                                    <AgentTimeline
                                        activities={agentActivities}
                                        isStreaming={isStreaming}
                                    />
                                </div>
                            </Suspense>
                        )}

                        {/* Metrics Dashboard */}
                        {Object.keys(metrics).length > 0 && (
                            <Suspense fallback={<LoadingSkeleton />}>
                                <div className="bg-white/70 dark:bg-slate-900/70 backdrop-blur-sm 
                              p-6 sm:p-8 rounded-3xl border-2 border-border/50 shadow-xl">
                                    <MetricsDashboard metrics={metrics} />
                                </div>
                            </Suspense>
                        )}

                        {/* Streaming Report */}
                        {(reportContent || isStreaming) && (
                            <Suspense fallback={<LoadingSkeleton />}>
                                <div className="bg-white/70 dark:bg-slate-900/70 backdrop-blur-sm 
                              p-6 sm:p-8 rounded-3xl border-2 border-border/50 shadow-xl">
                                    <StreamingReport
                                        report={reportContent}
                                        citations={citations}
                                        isStreaming={isStreaming}
                                    />
                                </div>
                            </Suspense>
                        )}
                    </div>
                )}

                {/* Empty State - Only show when not streaming and no content */}
                {!hasContent && !isStarting && (
                    <div className="text-center py-16 text-muted-foreground">
                        <p className="text-lg">
                            Enter a research query above to get started
                        </p>
                    </div>
                )}
            </div>
        </div>
    )
}

function LoadingSkeleton() {
    return (
        <div className="animate-pulse space-y-4">
            <div className="h-8 bg-muted rounded-lg w-1/3" />
            <div className="space-y-3">
                <div className="h-24 bg-muted rounded-xl" />
                <div className="h-24 bg-muted rounded-xl" />
            </div>
        </div>
    )
}
