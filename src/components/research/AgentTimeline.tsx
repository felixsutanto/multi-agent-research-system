"use client"

import { useMemo } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Badge } from "@/components/ui/badge"
import {
    Brain,
    Search,
    BarChart3,
    FileText,
    ShieldCheck,
    Clock,
    CheckCircle2,
    XCircle,
    Loader2,
} from "lucide-react"
import type { AgentActivity } from "@/lib/types"
import { formatRelativeTime } from "@/lib/utils"

const AGENT_ICONS = {
    planner: Brain,
    researcher: Search,
    analyst: BarChart3,
    synthesizer: FileText,
    critic: ShieldCheck,
} as const

const AGENT_COLORS = {
    planner: "from-purple-500/20 to-indigo-500/20 border-purple-200/50 dark:border-purple-900/50",
    researcher: "from-blue-500/20 to-cyan-500/20 border-blue-200/50 dark:border-blue-900/50",
    analyst: "from-green-500/20 to-emerald-500/20 border-green-200/50 dark:border-green-900/50",
    synthesizer: "from-orange-500/20 to-amber-500/20 border-orange-200/50 dark:border-orange-900/50",
    critic: "from-red-500/20 to-pink-500/20 border-red-200/50 dark:border-red-900/50",
} as const

interface AgentTimelineProps {
    activities: AgentActivity[]
    isStreaming?: boolean
}

export function AgentTimeline({ activities, isStreaming = false }: AgentTimelineProps) {
    const timelineItems = useMemo(() => {
        return activities.map((activity, index) => ({
            ...activity,
            delay: Math.min(index * 0.05, 0.5), // Cap delay at 0.5s
        }))
    }, [activities])

    if (activities.length === 0 && !isStreaming) {
        return null
    }

    return (
        <div className="space-y-4">
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
                <div className="relative flex  items-center">
                    <div className="w-2 h-2 bg-gradient-to-r from-purple-400 to-indigo-500 rounded-full animate-pulse" />
                    <div className="absolute w-2 h-2 bg-gradient-to-r from-purple-400 to-indigo-500 rounded-full animate-ping" />
                </div>
                <h3 className="font-semibold text-lg text-foreground">
                    Agent Activity
                </h3>
                {isStreaming && (
                    <Badge variant="secondary" className="ml-auto animate-pulse">
                        <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                        Live
                    </Badge>
                )}
            </div>

            {/* Timeline Container */}
            <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2 
                     scrollbar-thin scrollbar-thumb-slate-300 dark:scrollbar-thumb-slate-600 
                     scrollbar-track-transparent">
                <AnimatePresence mode="popLayout">
                    {timelineItems.map((activity, index) => {
                        const Icon = AGENT_ICONS[activity.agent] || Brain
                        const colorClass = AGENT_COLORS[activity.agent] || AGENT_COLORS.planner

                        return (
                            <motion.div
                                key={`${activity.agent}-${activity.timestamp}-${index}`}
                                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                                animate={{ opacity: 1, y: 0, scale: 1 }}
                                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                                transition={{
                                    duration: 0.3,
                                    delay: activity.delay,
                                    type: "spring",
                                    stiffness: 300,
                                    damping: 24,
                                }}
                                className="group relative"
                            >
                                <div className={`flex items-start gap-4 p-4 
                               bg-white/50 dark:bg-slate-900/50 
                               backdrop-blur-sm border-2 rounded-2xl 
                               hover:shadow-lg transition-all duration-200
                               hover:bg-white/70 dark:hover:bg-slate-900/70 ${colorClass}`}>

                                    {/* Agent Icon */}
                                    <motion.div
                                        initial={{ scale: 0, rotate: -180 }}
                                        animate={{ scale: 1, rotate: 0 }}
                                        transition={{
                                            type: "spring",
                                            stiffness: 260,
                                            damping: 20,
                                            delay: activity.delay + 0.1,
                                        }}
                                        className={`flex-shrink-0 w-11 h-11 p-2.5 
                               bg-gradient-to-br ${colorClass}
                               rounded-xl border-2 shadow-sm`}
                                    >
                                        <motion.div
                                            animate={{
                                                rotate: activity.status === 'running' ? [0, 360] : 0
                                            }}
                                            transition={{
                                                duration: activity.status === 'running' ? 3 : 0,
                                                repeat: activity.status === 'running' ? Infinity : 0,
                                                ease: "linear"
                                            }}
                                        >
                                            <Icon className="w-full h-full text-foreground" />
                                        </motion.div>
                                    </motion.div>

                                    {/* Activity Details */}
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                                            <span className="font-semibold text-sm capitalize text-foreground">
                                                {activity.agent}
                                            </span>

                                            <StatusBadge status={activity.status} />

                                            {activity.iteration !== undefined && (
                                                <Badge variant="outline" className="text-xs">
                                                    Iteration {activity.iteration}
                                                </Badge>
                                            )}
                                        </div>

                                        <p className="text-sm text-muted-foreground mb-2 leading-relaxed">
                                            {activity.action}
                                        </p>

                                        {activity.output && (
                                            <div className="mt-2 p-2 bg-muted/50 rounded-lg text-xs text-muted-foreground 
                                    border border-border/50 line-clamp-2">
                                                {activity.output}
                                            </div>
                                        )}

                                        {activity.metrics && Object.keys(activity.metrics).length > 0 && (
                                            <div className="flex flex-wrap gap-1.5 mt-2">
                                                {Object.entries(activity.metrics).map(([key, value]) => (
                                                    <Badge
                                                        key={key}
                                                        variant="secondary"
                                                        className="text-xs font-mono"
                                                    >
                                                        {key.replace(/_/g, ' ')}: {Math.round((value as number) * 100)}%
                                                    </Badge>
                                                ))}
                                            </div>
                                        )}

                                        <div className="flex items-center gap-1.5 mt-2 text-xs text-muted-foreground/70">
                                            <Clock className="w-3 h-3" />
                                            {formatRelativeTime(activity.timestamp)}
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )
                    })}
                </AnimatePresence>

                {/* Empty State */}
                {activities.length === 0 && isStreaming && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex flex-col items-center justify-center p-12 text-center"
                    >
                        <Loader2 className="w-8 h-8 text-muted-foreground animate-spin mb-3" />
                        <p className="text-sm text-muted-foreground">
                            Initializing agents...
                        </p>
                    </motion.div>
                )}
            </div>
        </div>
    )
}

function StatusBadge({ status }: { status: AgentActivity['status'] }) {
    const config = {
        idle: {
            icon: Clock,
            label: 'Idle',
            className: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
        },
        running: {
            icon: Loader2,
            label: 'Working',
            className: 'bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300 animate-pulse',
        },
        success: {
            icon: CheckCircle2,
            label: 'Complete',
            className: 'bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300',
        },
        error: {
            icon: XCircle,
            label: 'Failed',
            className: 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300',
        },
    }

    const { icon: Icon, label, className } = config[status] || config.idle

    return (
        <Badge variant="secondary" className={`text-xs flex items-center gap-1 ${className}`}>
            <Icon className={`w-3 h-3 ${status === 'running' ? 'animate-spin' : ''}`} />
            {label}
        </Badge>
    )
}
