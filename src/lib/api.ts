import axios from 'axios'
import type { ResearchFormData, ResearchResult, ResearchSession } from './types'

// Get API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance with default config
export const apiClient = axios.create({
    baseURL: API_URL,
    timeout: 600000, // 10 minutes for long-running research on HF free tier
    headers: {
        'Content-Type': 'application/json',
    },
})


// Request interceptor to add auth tokens if needed in the future
apiClient.interceptors.request.use(
    (config) => {
        // Add auth token here if implementing authentication
        // const token = localStorage.getItem('token')
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`
        // }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // Server responded with error status
            console.error('API Error:', error.response.data)
        } else if (error.request) {
            // Request made but no response
            console.error('Network Error:', error.message)
        } else {
            // Something else happened
            console.error('Error:', error.message)
        }
        return Promise.reject(error)
    }
)

// ========================================
// API Endpoints
// ========================================

// Backend response type (matches what the API actually returns)
interface BackendResearchResponse {
    query: string
    report: string  // Backend uses 'report', not 'finalReport'
    citations: any[]
    metrics: any
    agent_log?: any[]
    iterations: number
    approved: boolean
    errors: string[]
}

export const researchApi = {
    /**
     * Start a new research session
     * Backend returns ResearchResponse directly (not wrapped)
     */
    startResearch: async (data: ResearchFormData): Promise<ResearchResult> => {
        const response = await apiClient.post<BackendResearchResponse>('/research', {
            query: data.query,
            max_iterations: data.maxIterations,
            include_evaluation: data.includeAnalysis,
        })
        // Map backend response to frontend type
        return {
            sessionId: `session-${Date.now()}`, // Generate temp ID since backend doesn't return one
            query: response.data.query,
            finalReport: response.data.report,  // Map 'report' to 'finalReport'
            citations: response.data.citations.map((c: any, i: number) => ({
                id: c.id || `cite-${i}`,
                url: c.url || '',
                title: c.title || '',
                snippet: c.snippet || '',
            })),
            metrics: {
                contextRelevance: response.data.metrics?.context_relevance || 0,
                groundedness: response.data.metrics?.groundedness || 0,
                answerRelevance: response.data.metrics?.answer_relevance || 0,
                overallScore: response.data.metrics?.overall_score || 0,
            },
            agentActivities: response.data.agent_log?.map((log: any) => ({
                agent: log.agent as any,
                action: log.action,
                status: 'success' as any,
                timestamp: log.timestamp,
                output: log.output ? JSON.stringify(log.output) : undefined,
            })) || [],
            createdAt: new Date().toISOString(),
            completedAt: new Date().toISOString(),
        }
    },

    /**
     * Get research session by ID (not implemented in backend yet)
     */
    getSession: async (sessionId: string): Promise<ResearchSession | null> => {
        // Backend doesn't support this yet, return null
        return null
    },

    /**
     * Get all research sessions (not implemented in backend yet)
     */
    getSessions: async (): Promise<ResearchSession[]> => {
        // Backend doesn't support this yet, return empty array
        return []
    },

    /**
     * Delete a research session (not implemented in backend yet)
     */
    deleteSession: async (sessionId: string): Promise<void> => {
        // Backend doesn't support this yet, do nothing
    },

    /**
     * Get health status of the API
     */
    health: async (): Promise<{ status: string; version: string }> => {
        const response = await apiClient.get<{ status: string; version: string }>('/health')
        return response.data
    },
}

/**
 * Get WebSocket URL for real-time updates
 */
export function getWebSocketUrl(): string {
    const wsProtocol = API_URL.startsWith('https') ? 'wss' : 'ws'
    const baseUrl = API_URL.replace(/^https?:\/\//, '')
    return `${wsProtocol}://${baseUrl}/ws/research`
}

/**
 * Get Server-Sent Events URL as fallback
 */
export function getSSEUrl(sessionId: string): string {
    return `${API_URL}/research/${sessionId}/stream`
}
