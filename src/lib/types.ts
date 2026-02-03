import { z } from "zod"

// ========================================
// Form Schemas
// ========================================

export const ResearchFormSchema = z.object({
    query: z.string().min(10, "Query must be at least 10 characters"),
    maxIterations: z.number().min(1).max(5),
    includeAnalysis: z.boolean(),
})

export type ResearchFormData = z.infer<typeof ResearchFormSchema>

// ========================================
// Agent Types
// ========================================

export type AgentType = 'planner' | 'researcher' | 'analyst' | 'synthesizer' | 'critic'
export type AgentStatus = 'idle' | 'running' | 'success' | 'error'

export interface AgentActivity {
    agent: AgentType
    action: string
    timestamp: string
    status: AgentStatus
    output?: string
    metrics?: Record<string, number>
    iteration?: number
}

// ========================================
// Research Types
// ========================================

export interface Citation {
    id: string
    url: string
    title: string
    snippet: string
    relevanceScore?: number
}

export interface ResearchMetrics {
    contextRelevance: number
    groundedness: number
    answerRelevance: number
    overallScore: number
    tokenUsage?: {
        totalTokens: number
        promptTokens: number
        completionTokens: number
    }
    costEstimate?: number
}

export interface ResearchResult {
    sessionId: string
    query: string
    finalReport: string
    citations: Citation[]
    metrics: ResearchMetrics
    agentActivities: AgentActivity[]
    createdAt: string
    completedAt: string
}

// ========================================
// WebSocket Event Types
// ========================================

export type WebSocketEventType =
    | 'agent_update'
    | 'report_chunk'
    | 'metrics_update'
    | 'complete'
    | 'error'

export interface WebSocketEvent<T = any> {
    type: WebSocketEventType
    data: T
    timestamp: string
}

export interface AgentUpdateEvent {
    agent: AgentType
    action: string
    status: AgentStatus
    output?: string
    metrics?: Record<string, number>
}

export interface ReportChunkEvent {
    content: string
    isComplete: boolean
}

export interface MetricsUpdateEvent {
    metrics: Partial<ResearchMetrics>
}

export interface CompleteEvent {
    result: ResearchResult
}

export interface ErrorEvent {
    message: string
    code?: string
    details?: any
}

// ========================================
// API Response Types
// ========================================

export interface ApiResponse<T> {
    success: boolean
    data?: T
    error?: {
        message: string
        code: string
        details?: any
    }
}

export interface ResearchSession {
    sessionId: string
    query: string
    status: 'pending' | 'running' | 'completed' | 'failed'
    createdAt: string
    updatedAt: string
    result?: ResearchResult
}

// ========================================
// Preset Templates
// ========================================

export interface ResearchPreset {
    id: string
    title: string
    description: string
    query: string
    category: 'business' | 'academic' | 'technical' | 'general'
    icon: string
}
