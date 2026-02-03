"use client"

import { useState, useCallback, useEffect } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useWebSocket } from '@/lib/websocket'
import { researchApi } from '@/lib/api'
import type {
    ResearchFormData,
    AgentActivity,
    ResearchMetrics,
    Citation,
    ResearchResult,
    AgentUpdateEvent,
    ReportChunkEvent,
    MetricsUpdateEvent,
    CompleteEvent,
} from '@/lib/types'

export function useResearch(sessionId?: string) {
    const queryClient = useQueryClient()

    // Local state for real-time updates
    const [currentSessionId, setCurrentSessionId] = useState<string | undefined>(sessionId)
    const [agentActivities, setAgentActivities] = useState<AgentActivity[]>([])
    const [reportContent, setReportContent] = useState('')
    const [citations, setCitations] = useState<Citation[]>([])
    const [metrics, setMetrics] = useState<Partial<ResearchMetrics>>({})
    const [isStreaming, setIsStreaming] = useState(false)
    const [error, setError] = useState<string | null>(null)

    // WebSocket connection
    const {
        isConnected,
        connectionError,
        on,
        disconnect,
    } = useWebSocket(currentSessionId || '', {
        onOpen: () => {
            console.log('Research WebSocket connected')
            setError(null)
        },
        onError: (err) => {
            console.error('Research WebSocket error:', err)
            setError('Connection error occurred')
        },
        onClose: () => {
            console.log('Research WebSocket closed')
            setIsStreaming(false)
        },
    })

    // Listen to WebSocket events
    useEffect(() => {
        if (!currentSessionId) return

        // Agent updates
        const unsubscribeAgent = on('agent_update', (data: AgentUpdateEvent) => {
            const activity: AgentActivity = {
                agent: data.agent,
                action: data.action,
                status: data.status,
                timestamp: new Date().toISOString(),
                output: data.output,
                metrics: data.metrics,
            }

            setAgentActivities(prev => [...prev, activity])
        })

        // Report chunks (streaming)
        const unsubscribeReport = on('report_chunk', (data: ReportChunkEvent) => {
            setReportContent(prev => prev + data.content)
            setIsStreaming(!data.isComplete)
        })

        // Metrics updates
        const unsubscribeMetrics = on('metrics_update', (data: MetricsUpdateEvent) => {
            setMetrics(prev => ({ ...prev, ...data.metrics }))
        })

        // Research complete
        const unsubscribeComplete = on('complete', (data: CompleteEvent) => {
            setReportContent(data.result.finalReport)
            setCitations(data.result.citations)
            setMetrics(data.result.metrics)
            setIsStreaming(false)

            // Update query cache
            queryClient.setQueryData(['research', currentSessionId], data.result)
        })

        // Error handling
        const unsubscribeError = on('error', (data: { message: string }) => {
            setError(data.message)
            setIsStreaming(false)
        })

        return () => {
            unsubscribeAgent()
            unsubscribeReport()
            unsubscribeMetrics()
            unsubscribeComplete()
            unsubscribeError()
        }
    }, [currentSessionId, on, queryClient])

    // Start new research session
    const startResearch = useMutation({
        mutationFn: async (data: ResearchFormData) => {
            // Reset state
            setAgentActivities([])
            setReportContent('')
            setCitations([])
            setMetrics({})
            setError(null)
            setIsStreaming(true)

            // Call API to start research
            const result = await researchApi.startResearch(data)

            return result
        },
        onSuccess: (result) => {
            setCurrentSessionId(result.sessionId)
            setReportContent(result.finalReport)
            setCitations(result.citations)
            setMetrics(result.metrics)
            setAgentActivities(result.agentActivities || [])
            setIsStreaming(false)
            queryClient.invalidateQueries({ queryKey: ['research-sessions'] })
        },
        onError: (err: Error) => {
            setError(err.message)
            setIsStreaming(false)
        },
    })

    // Get research session details
    const { data: sessionData, isLoading: isLoadingSession } = useQuery({
        queryKey: ['research', currentSessionId],
        queryFn: async () => {
            if (!currentSessionId) return null
            return await researchApi.getSession(currentSessionId)
        },
        enabled: !!currentSessionId,
        refetchInterval: isStreaming ? 5000 : false, // Poll every 5s while streaming
    })

    // Get all research sessions (for history)
    const { data: sessions, isLoading: isLoadingSessions } = useQuery({
        queryKey: ['research-sessions'],
        queryFn: async () => {
            return await researchApi.getSessions()
        },
    })

    // Delete a session
    const deleteSession = useMutation({
        mutationFn: async (sessionId: string) => {
            await researchApi.deleteSession(sessionId)
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['research-sessions'] })
        },
    })

    // Reset current research
    const resetResearch = useCallback(() => {
        setCurrentSessionId(undefined)
        setAgentActivities([])
        setReportContent('')
        setCitations([])
        setMetrics({})
        setError(null)
        setIsStreaming(false)
        disconnect()
    }, [disconnect])

    // Rerun a previous research
    const rerunResearch = useCallback(async (query: string, maxIterations = 3, includeAnalysis = true) => {
        await startResearch.mutateAsync({
            query,
            maxIterations,
            includeAnalysis,
        })
    }, [startResearch])

    return {
        // Session management
        currentSessionId,
        sessionData,
        sessions,

        // Real-time data
        agentActivities,
        reportContent,
        citations,
        metrics,

        // State
        isStreaming,
        isConnected,
        error: error || connectionError,
        isLoadingSession,
        isLoadingSessions,
        isStarting: startResearch.isPending,

        // Actions
        startResearch: startResearch.mutateAsync,
        deleteSession: deleteSession.mutateAsync,
        resetResearch,
        rerunResearch,
    }
}
