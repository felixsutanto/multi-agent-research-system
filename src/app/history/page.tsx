"use client"

import { Navbar } from "@/components/layout/Navbar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { useResearch } from "@/hooks/useResearch"
import { formatRelativeTime, truncate } from "@/lib/utils"
import { History, Trash2, RefreshCw, FileText, Clock } from "lucide-react"
import Link from "next/link"

export default function HistoryPage() {
    const { sessions, isLoadingSessions, deleteSession, rerunResearch } = useResearch()

    const handleDelete = async (sessionId: string) => {
        if (confirm("Are you sure you want to delete this research session?")) {
            try {
                await deleteSession(sessionId)
            } catch (error) {
                console.error("Failed to delete session:", error)
            }
        }
    }

    const handleRerun = async (query: string) => {
        try {
            await rerunResearch(query)
        } catch (error) {
            console.error("Failed to rerun research:", error)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30 
                   dark:from-slate-950 dark:via-slate-950/50 dark:to-purple-950/20">
            <Navbar />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
                {/* Header */}
                <div className="mb-12">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-purple-600 to-indigo-600">
                            <History className="h-6 w-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-4xl font-bold text-foreground">
                                Research History
                            </h1>
                            <p className="text-muted-foreground mt-1">
                                View and manage your previous research sessions
                            </p>
                        </div>
                    </div>
                </div>

                {/* Loading State */}
                {isLoadingSessions && (
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="animate-pulse">
                                <div className="h-40 bg-muted rounded-2xl" />
                            </div>
                        ))}
                    </div>
                )}

                {/* Sessions List */}
                {!isLoadingSessions && sessions && sessions.length > 0 && (
                    <div className="grid gap-6">
                        {sessions.map((session: any) => (
                            <Card key={session.sessionId} className="border-2 hover:border-purple-300 dark:hover:border-purple-700 transition-all">
                                <CardHeader>
                                    <div className="flex items-start justify-between gap-4">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-2">
                                                <CardTitle className="text-xl">
                                                    {truncate(session.query, 100)}
                                                </CardTitle>
                                                <StatusBadge status="completed" />
                                            </div>
                                            <CardDescription className="flex items-center gap-4 text-sm">
                                                <span className="flex items-center gap-1">
                                                    <Clock className="w-3 h-3" />
                                                    {formatRelativeTime(session.createdAt)}
                                                </span>
                                                <span>•</span>
                                                <span>ID: {session.sessionId.slice(0, 8)}...</span>
                                            </CardDescription>
                                        </div>

                                        <div className="flex items-center gap-2">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => handleRerun(session.query)}
                                                className="group"
                                            >
                                                <RefreshCw className="w-4 h-4 mr-1 group-hover:rotate-180 transition-transform duration-300" />
                                                Rerun
                                            </Button>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => handleDelete(session.sessionId)}
                                                className="text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-950/20"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                    </div>
                                </CardHeader>

                                {session.result && (
                                    <CardContent>
                                        <div className="space-y-3">
                                            {/* Report Preview */}
                                            {session.result.finalReport && (
                                                <div className="p-4 bg-muted/50 rounded-xl">
                                                    <div className="flex items-center gap-2 mb-2">
                                                        <FileText className="w-4 h-4 text-muted-foreground" />
                                                        <span className="text-sm font-medium">Report Preview</span>
                                                    </div>
                                                    <p className="text-sm text-muted-foreground line-clamp-3">
                                                        {truncate(session.result.finalReport, 200)}
                                                    </p>
                                                </div>
                                            )}

                                            {/* Metrics */}
                                            {session.result.metrics && (
                                                <div className="flex flex-wrap gap-2">
                                                    <Badge variant="outline">
                                                        Quality: {Math.round(session.result.metrics.overallScore * 100)}%
                                                    </Badge>
                                                    {session.result.citations && (
                                                        <Badge variant="outline">
                                                            {session.result.citations.length} Citations
                                                        </Badge>
                                                    )}
                                                    {session.result.agentActivities && (
                                                        <Badge variant="outline">
                                                            {session.result.agentActivities.length} Agent Actions
                                                        </Badge>
                                                    )}
                                                </div>
                                            )}

                                            {/* View Details Link */}
                                            <Link href={`/research?session=${session.sessionId}`}>
                                                <Button variant="link" className="px-0 h-auto">
                                                    View Full Report →
                                                </Button>
                                            </Link>
                                        </div>
                                    </CardContent>
                                )}
                            </Card>
                        ))}
                    </div>
                )}

                {/* Empty State */}
                {!isLoadingSessions && (!sessions || sessions.length === 0) && (
                    <Card className="border-2 border-dashed">
                        <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted mb-4">
                                <History className="h-8 w-8 text-muted-foreground" />
                            </div>
                            <h3 className="text-lg font-semibold text-foreground mb-2">
                                No research history yet
                            </h3>
                            <p className="text-muted-foreground mb-6 max-w-md">
                                Your research sessions will appear here. Start a new research to see your history.
                            </p>
                            <Link href="/research">
                                <Button className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700">
                                    Start Research
                                </Button>
                            </Link>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    )
}

function StatusBadge({ status }: { status: string }) {
    const config = {
        pending: {
            label: 'Pending',
            className: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-950 dark:text-yellow-300',
        },
        running: {
            label: 'Running',
            className: 'bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300 animate-pulse',
        },
        completed: {
            label: 'Completed',
            className: 'bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300',
        },
        failed: {
            label: 'Failed',
            className: 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300',
        },
    }

    const { label, className } = config[status as keyof typeof config] || config.pending

    return (
        <Badge variant="secondary" className={className}>
            {label}
        </Badge>
    )
}
