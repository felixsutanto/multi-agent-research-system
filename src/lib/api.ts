import axios from 'axios'
import type { ApiResponse, ResearchFormData, ResearchResult, ResearchSession } from './types'

// Get API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance with default config
export const apiClient = axios.create({
    baseURL: API_URL,
    timeout: 300000, // 5 minutes for long-running research
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

export const researchApi = {
    /**
     * Start a new research session
     */
    startResearch: async (data: ResearchFormData): Promise<ApiResponse<ResearchSession>> => {
        const response = await apiClient.post<ApiResponse<ResearchSession>>('/api/research', {
            query: data.query,
            max_iterations: data.maxIterations,
            include_analysis: data.includeAnalysis,
        })
        return response.data
    },

    /**
     * Get research session by ID
     */
    getSession: async (sessionId: string): Promise<ApiResponse<ResearchSession>> => {
        const response = await apiClient.get<ApiResponse<ResearchSession>>(`/api/research/${sessionId}`)
        return response.data
    },

    /**
     * Get all research sessions (for history)
     */
    getSessions: async (): Promise<ApiResponse<ResearchSession[]>> => {
        const response = await apiClient.get<ApiResponse<ResearchSession[]>>('/api/research')
        return response.data
    },

    /**
     * Delete a research session
     */
    deleteSession: async (sessionId: string): Promise<ApiResponse<void>> => {
        const response = await apiClient.delete<ApiResponse<void>>(`/api/research/${sessionId}`)
        return response.data
    },

    /**
     * Get health status of the API
     */
    health: async (): Promise<ApiResponse<{ status: string; version: string }>> => {
        const response = await apiClient.get<ApiResponse<{ status: string; version: string }>>('/health')
        return response.data
    },
}

/**
 * Get WebSocket URL for real-time updates
 */
export function getWebSocketUrl(sessionId: string): string {
    const wsProtocol = API_URL.startsWith('https') ? 'wss' : 'ws'
    const baseUrl = API_URL.replace(/^https?:\/\//, '')
    return `${wsProtocol}://${baseUrl}/ws/research/${sessionId}`
}

/**
 * Get Server-Sent Events URL as fallback
 */
export function getSSEUrl(sessionId: string): string {
    return `${API_URL}/api/research/${sessionId}/stream`
}
