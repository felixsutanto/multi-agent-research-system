"use client"

import { useMemo } from "react"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    ResponsiveContainer,
    Tooltip,
    Cell,
} from "recharts"
import { TrendingUp, Zap, DollarSign, Target } from "lucide-react"
import type { ResearchMetrics } from "@/lib/types"
import { formatNumber, formatCurrency } from "@/lib/utils"

interface MetricsDashboardProps {
    metrics: Partial<ResearchMetrics>
}

export function MetricsDashboard({ metrics }: MetricsDashboardProps) {
    const {
        contextRelevance = 0,
        groundedness = 0,
        answerRelevance = 0,
        overallScore = 0,
        tokenUsage,
        costEstimate = 0,
    } = metrics

    // Chart data for RAG Triad
    const chartData = useMemo(() => [
        {
            name: "Context Relevance",
            value: contextRelevance,
            color: "#8B5CF6", // purple-500
            description: "How relevant the retrieved context is",
        },
        {
            name: "Groundedness",
            value: groundedness,
            color: "#10B981", // green-500
            description: "How well the answer is grounded in facts",
        },
        {
            name: "Answer Relevance",
            value: answerRelevance,
            color: "#F59E0B", // amber-500
            description: "How relevant the answer is to the query",
        },
    ], [contextRelevance, groundedness, answerRelevance])

    const overallPercentage = Math.round(overallScore * 100)
    const qualityLevel = overallPercentage >= 90 ? 'Excellent'
        : overallPercentage >= 80 ? 'Good'
            : overallPercentage >= 70 ? 'Fair'
                : 'Needs Improvement'

    const qualityColor = overallPercentage >= 90 ? 'text-green-600 dark:text-green-400'
        : overallPercentage >= 80 ? 'text-blue-600 dark:text-blue-400'
            : overallPercentage >= 70 ? 'text-amber-600 dark:text-amber-400'
                : 'text-red-600 dark:text-red-400'

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Overall Quality Score */}
            <Card className="border-2">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Target className="w-5 h-5 text-purple-600" />
                        Overall Quality Score
                    </CardTitle>
                    <CardDescription>
                        Aggregate performance across all metrics
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="relative w-full h-40 bg-gradient-to-br from-purple-50 to-indigo-50 
                        dark:from-purple-950/30 dark:to-indigo-950/30 
                        rounded-2xl flex items-center justify-center overflow-hidden">
                        {/* Animated background circles */}
                        <div className="absolute inset-0 opacity-20">
                            <div className="absolute top-0 left-0 w-32 h-32 bg-purple-400 rounded-full blur-3xl animate-pulse" />
                            <div className="absolute bottom-0 right-0 w-32 h-32 bg-indigo-400 rounded-full blur-3xl animate-pulse delay-75" />
                        </div>

                        <div className="relative text-center z-10">
                            <div className={`text-6xl font-black mb-2 bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent`}>
                                {overallPercentage}%
                            </div>
                            <Badge className={qualityColor}>
                                {qualityLevel}
                            </Badge>
                            <p className="text-xs text-muted-foreground mt-2">
                                {overallPercentage >= 85 && "Above industry benchmark"}
                                {overallPercentage >= 70 && overallPercentage < 85 && "Meets expectations"}
                                {overallPercentage < 70 && "Below threshold"}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* RAG Triad Chart */}
            <Card className="border-2">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-purple-600" />
                        RAG Triad Metrics
                    </CardTitle>
                    <CardDescription>
                        Retrieval-Augmented Generation quality indicators
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <ResponsiveContainer width="100%" height={200}>
                        <BarChart data={chartData} layout="vertical">
                            <XAxis
                                type="number"
                                domain={[0, 1]}
                                tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                                axisLine={false}
                                tickLine={false}
                                tick={{ fontSize: 12 }}
                            />
                            <YAxis
                                type="category"
                                dataKey="name"
                                width={140}
                                axisLine={false}
                                tickLine={false}
                                tick={{ fontSize: 12 }}
                            />
                            <Tooltip
                                formatter={(value: number, name: string, props: any) => [
                                    `${(value * 100).toFixed(1)}%`,
                                    props.payload.description
                                ]}
                                contentStyle={{
                                    backgroundColor: 'hsl(var(--background))',
                                    border: '1px solid hsl(var(--border))',
                                    borderRadius: '8px',
                                    fontSize: '12px',
                                }}
                            />
                            <Bar
                                dataKey="value"
                                radius={[0, 8, 8, 0]}
                            >
                                {chartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>

            {/* Token Usage */}
            {tokenUsage && (
                <Card className="border-2">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Zap className="w-5 h-5 text-amber-600" />
                            Token Usage
                        </CardTitle>
                        <CardDescription>
                            API consumption for this research session
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid grid-cols-3 gap-4">
                            <div className="text-center p-3 bg-muted/50 rounded-xl">
                                <div className="text-2xl font-bold text-foreground">
                                    {formatNumber(tokenUsage.totalTokens)}
                                </div>
                                <div className="text-xs text-muted-foreground mt-1">Total</div>
                            </div>
                            <div className="text-center p-3 bg-muted/50 rounded-xl">
                                <div className="text-2xl font-bold text-foreground">
                                    {formatNumber(tokenUsage.promptTokens)}
                                </div>
                                <div className="text-xs text-muted-foreground mt-1">Prompt</div>
                            </div>
                            <div className="text-center p-3 bg-muted/50 rounded-xl">
                                <div className="text-2xl font-bold text-foreground">
                                    {formatNumber(tokenUsage.completionTokens)}
                                </div>
                                <div className="text-xs text-muted-foreground mt-1">Completion</div>
                            </div>
                        </div>

                        {/* Progress bar */}
                        <div className="space-y-2">
                            <div className="flex justify-between text-xs text-muted-foreground">
                                <span>Prompt vs Completion</span>
                                <span>
                                    {Math.round((tokenUsage.promptTokens / tokenUsage.totalTokens) * 100)}% /
                                    {Math.round((tokenUsage.completionTokens / tokenUsage.totalTokens) * 100)}%
                                </span>
                            </div>
                            <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                                    style={{ width: `${(tokenUsage.promptTokens / tokenUsage.totalTokens) * 100}%` }}
                                />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Cost Estimate */}
            {costEstimate > 0 && (
                <Card className="border-2">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <DollarSign className="w-5 h-5 text-green-600" />
                            Cost Estimate
                        </CardTitle>
                        <CardDescription>
                            Approximate research cost
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="text-center p-6 bg-gradient-to-br from-green-50 to-emerald-50 
                          dark:from-green-950/30 dark:to-emerald-950/30 rounded-2xl">
                            <div className="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">
                                {formatCurrency(costEstimate)}
                            </div>
                            <p className="text-sm text-muted-foreground">
                                Based on current API pricing
                            </p>
                            <div className="mt-4 pt-4 border-t border-border/50">
                                <div className="flex justify-between text-xs text-muted-foreground">
                                    <span>Per 1K tokens</span>
                                    <span className="font-mono">
                                        {tokenUsage ? formatCurrency(costEstimate / (tokenUsage.totalTokens / 1000)) : '-'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    )
}
