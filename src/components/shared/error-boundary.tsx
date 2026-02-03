"use client"

import { Component, ReactNode } from "react"
import { AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"

interface Props {
    children: ReactNode
    fallback?: ReactNode
}

interface State {
    hasError: boolean
    error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props)
        this.state = { hasError: false, error: null }
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error }
    }

    componentDidCatch(error: Error, errorInfo: any) {
        console.error("Error boundary caught an error:", error, errorInfo)
    }

    render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                return this.props.fallback
            }

            return (
                <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-purple-50/30 dark:from-slate-950 dark:to-purple-950/20 p-4">
                    <div className="max-w-lg w-full bg-white dark:bg-slate-900 rounded-2xl border-2 border-red-200 dark:border-red-900 p-8 shadow-xl">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-red-100 dark:bg-red-950">
                                <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-400" />
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-red-900 dark:text-red-100">
                                    Something went wrong
                                </h2>
                                <p className="text-sm text-red-700 dark:text-red-300">
                                    An unexpected error occurred
                                </p>
                            </div>
                        </div>

                        <div className="bg-red-50 dark:bg-red-950/30 rounded-xl p-4 mb-6">
                            <pre className="text-xs text-red-800 dark:text-red-200 overflow-x-auto">
                                {this.state.error?.message || "Unknown error"}
                            </pre>
                        </div>

                        <div className="flex gap-3">
                            <Button
                                onClick={() => {
                                    this.setState({ hasError: false, error: null })
                                    window.location.reload()
                                }}
                                className="flex-1 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700"
                            >
                                Reload Page
                            </Button>
                            <Button
                                variant="outline"
                                onClick={() => window.location.href = "/"}
                                className="flex-1"
                            >
                                Go Home
                            </Button>
                        </div>

                        <p className="text-xs text-muted-foreground mt-4 text-center">
                            If this problem persists, please contact support
                        </p>
                    </div>
                </div>
            )
        }

        return this.props.children
    }
}
