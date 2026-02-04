"use client"

import { useState, useCallback, useEffect } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { researchApi } from '@/lib/api'
import type {
    ResearchFormData,
    AgentActivity,
    ResearchMetrics,
    Citation,
    ResearchResult,
} from '@/lib/types'

// LocalStorage key for session history
const SESSIONS_STORAGE_KEY = 'research-sessions'

// Helper to get sessions from localStorage
function getStoredSessions(): ResearchResult[] {
    if (typeof window === 'undefined') return []
    try {
        const stored = localStorage.getItem(SESSIONS_STORAGE_KEY)
        return stored ? JSON.parse(stored) : []
    } catch {
        return []
    }
}

// Helper to save session to localStorage
function saveSession(session: ResearchResult): void {
    if (typeof window === 'undefined') return
    try {
        const sessions = getStoredSessions()
        // Add new session at the beginning
        sessions.unshift(session)
        // Keep only last 10 sessions
        const trimmed = sessions.slice(0, 10)
        localStorage.setItem(SESSIONS_STORAGE_KEY, JSON.stringify(trimmed))
    } catch (e) {
        console.error('Failed to save session:', e)
    }
}

// Helper to delete session from localStorage
function deleteStoredSession(sessionId: string): void {
    if (typeof window === 'undefined') return
    try {
        const sessions = getStoredSessions()
        const filtered = sessions.filter((s: ResearchResult) => s.sessionId !== sessionId)
        localStorage.setItem(SESSIONS_STORAGE_KEY, JSON.stringify(filtered))
    } catch (e) {
        console.error('Failed to delete session:', e)
    }
}

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
            setError(null) // Clear any WebSocket errors since research succeeded

            // Save to localStorage for history
            saveSession(result)

            // Invalidate to refresh history
            queryClient.invalidateQueries({ queryKey: ['research-sessions'] })
        },
        onError: (err: Error) => {
            setError(err.message)
            setIsStreaming(false)
        },
    })

    // Get research session details (from localStorage)
    const { data: sessionData, isLoading: isLoadingSession } = useQuery({
        queryKey: ['research', currentSessionId],
        queryFn: async () => {
            if (!currentSessionId) return null
            // Try to find in localStorage
            const sessions = getStoredSessions()
            return sessions.find((s: ResearchResult) => s.sessionId === currentSessionId) || null
        },
        enabled: !!currentSessionId,
    })

    // Get all research sessions (from localStorage)
    const { data: sessions, isLoading: isLoadingSessions } = useQuery({
        queryKey: ['research-sessions'],
        queryFn: async () => {
            return getStoredSessions()
        },
    })

    // Delete a session
    const deleteSession = useMutation({
        mutationFn: async (sessionId: string) => {
            deleteStoredSession(sessionId)
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
    }, [])

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
        isConnected: false, // WebSocket not used since HF doesn't support it
        error, // Only show actual API errors, not WebSocket connection errors
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
