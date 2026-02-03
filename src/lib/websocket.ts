import { useEffect, useRef, useCallback, useState } from 'react'
import { getWebSocketUrl, getSSEUrl } from './api'
import type { WebSocketEvent } from './types'

interface UseWebSocketOptions {
    onOpen?: () => void
    onClose?: () => void
    onError?: (error: Event) => void
    reconnectAttempts?: number
    reconnectInterval?: number
}

export function useWebSocket(sessionId: string, options: UseWebSocketOptions = {}) {
    const {
        onOpen,
        onClose,
        onError,
        reconnectAttempts = 3,
        reconnectInterval = 3000,
    } = options

    const wsRef = useRef<WebSocket | null>(null)
    const reconnectCountRef = useRef(0)
    const listenersRef = useRef<Map<string, Set<(data: any) => void>>>(new Map())
    const isConnectedRef = useRef(false) // Added for checking connection status in connect

    const [isConnected, setIsConnected] = useState(false)
    const [connectionError, setConnectionError] = useState<string | null>(null)

    // Connect to WebSocket
    const connect = useCallback(() => {
        if (!sessionId || isConnectedRef.current) {
            return
        }

        try {
            const wsUrl = getWebSocketUrl()
            console.log('Connecting to WebSocket:', wsUrl)

            const ws = new WebSocket(wsUrl)

            ws.onopen = () => {
                console.log('WebSocket connected')
                setIsConnected(true)
                setConnectionError(null)
                reconnectCountRef.current = 0
                onOpen?.()
            }

            ws.onmessage = (event) => {
                try {
                    const message: WebSocketEvent = JSON.parse(event.data)
                    console.log('WebSocket message:', message)

                    // Notify all listeners for this event type
                    const listeners = listenersRef.current.get(message.type)
                    if (listeners) {
                        listeners.forEach(callback => callback(message.data))
                    }

                    // Also notify wildcard listeners
                    const wildcardListeners = listenersRef.current.get('*')
                    if (wildcardListeners) {
                        wildcardListeners.forEach(callback => callback(message))
                    }
                } catch (error) {
                    console.error('Failed to parse WebSocket message:', error)
                }
            }

            ws.onerror = (error) => {
                console.error('WebSocket error:', error)
                setConnectionError('Connection error occurred')
                onError?.(error)
            }

            ws.onclose = () => {
                console.log('WebSocket disconnected')
                setIsConnected(false)

                // Attempt reconnection
                if (reconnectCountRef.current < reconnectAttempts) {
                    reconnectCountRef.current++
                    console.log(`Reconnecting... Attempt ${reconnectCountRef.current}/${reconnectAttempts}`)
                    setTimeout(connect, reconnectInterval)
                } else {
                    setConnectionError('Failed to connect after multiple attempts')
                }

                onClose?.()
            }

            wsRef.current = ws
        } catch (error) {
            console.error('Failed to create WebSocket:', error)
            setConnectionError('Failed to create connection')
        }
    }, [sessionId, onOpen, onClose, onError, reconnectAttempts, reconnectInterval])

    // Disconnect from WebSocket
    const disconnect = useCallback(() => {
        if (wsRef.current) {
            wsRef.current.close()
            wsRef.current = null
            setIsConnected(false)
        }
    }, [])

    // Send message
    const send = useCallback((data: any) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(data))
        } else {
            console.warn('WebSocket not connected, cannot send message')
        }
    }, [])

    // Subscribe to event type
    const on = useCallback((eventType: string, callback: (data: any) => void) => {
        if (!listenersRef.current.has(eventType)) {
            listenersRef.current.set(eventType, new Set())
        }
        listenersRef.current.get(eventType)!.add(callback)

        // Return unsubscribe function
        return () => {
            listenersRef.current.get(eventType)?.delete(callback)
        }
    }, [])

    // Unsubscribe from event type
    const off = useCallback((eventType: string, callback?: (data: any) => void) => {
        if (callback) {
            listenersRef.current.get(eventType)?.delete(callback)
        } else {
            listenersRef.current.delete(eventType)
        }
    }, [])

    // Auto-connect on mount
    useEffect(() => {
        if (sessionId) {
            connect()
        }

        return () => {
            disconnect()
        }
    }, [sessionId, connect, disconnect])

    return {
        isConnected,
        connectionError,
        connect,
        disconnect,
        send,
        on,
        off,
    }
}

// ========================================
// SSE Fallback Hook (for environments without WebSocket support)
// ========================================

export function useSSE(sessionId: string, options: UseWebSocketOptions = {}) {
    const { onOpen, onClose, onError } = options
    const eventSourceRef = useRef<EventSource | null>(null)
    const listenersRef = useRef<Map<string, Set<(data: any) => void>>>(new Map())

    const [isConnected, setIsConnected] = useState(false)
    const [connectionError, setConnectionError] = useState<string | null>(null)

    const connect = useCallback(() => {
        if (!sessionId) return

        try {
            const sseUrl = getSSEUrl(sessionId)
            console.log('Connecting to SSE:', sseUrl)

            const eventSource = new EventSource(sseUrl)

            eventSource.onopen = () => {
                console.log('SSE connected')
                setIsConnected(true)
                setConnectionError(null)
                onOpen?.()
            }

            eventSource.onmessage = (event) => {
                try {
                    const message: WebSocketEvent = JSON.parse(event.data)

                    const listeners = listenersRef.current.get(message.type)
                    if (listeners) {
                        listeners.forEach(callback => callback(message.data))
                    }
                } catch (error) {
                    console.error('Failed to parse SSE message:', error)
                }
            }

            eventSource.onerror = (error) => {
                console.error('SSE error:', error)
                setConnectionError('Connection error occurred')
                setIsConnected(false)
                onError?.(error)
            }

            eventSourceRef.current = eventSource
        } catch (error) {
            console.error('Failed to create SSE connection:', error)
            setConnectionError('Failed to create connection')
        }
    }, [sessionId, onOpen, onError])

    const disconnect = useCallback(() => {
        if (eventSourceRef.current) {
            eventSourceRef.current.close()
            eventSourceRef.current = null
            setIsConnected(false)
            onClose?.()
        }
    }, [onClose])

    const on = useCallback((eventType: string, callback: (data: any) => void) => {
        if (!listenersRef.current.has(eventType)) {
            listenersRef.current.set(eventType, new Set())
        }
        listenersRef.current.get(eventType)!.add(callback)

        return () => {
            listenersRef.current.get(eventType)?.delete(callback)
        }
    }, [])

    useEffect(() => {
        if (sessionId) {
            connect()
        }

        return () => {
            disconnect()
        }
    }, [sessionId, connect, disconnect])

    return {
        isConnected,
        connectionError,
        connect,
        disconnect,
        on,
    }
}
