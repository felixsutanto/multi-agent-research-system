import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format a date string to a readable format
 */
export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d)
}

/**
 * Format a relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diff = now.getTime() - d.getTime()

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`
  if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
  return 'Just now'
}

/**
 * Truncate text to a specific length
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

/**
 * Format number with commas
 */
export function formatNumber(num: number): string {
  return new Intl.NumberFormat('en-US').format(num)
}

/**
 * Format currency
 */
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}

/**
 * Calculate reading time for text
 */
export function calculateReadingTime(text: string): string {
  const wordsPerMinute = 200
  const wordCount = text.split(/\s+/).length
  const minutes = Math.ceil(wordCount / wordsPerMinute)
  return `${minutes} min read`
}

/**
 * Parse markdown-like headers (simple implementation)
 */
export function parseMarkdownHeaders(text: string): Array<{ level: number; text: string; id: string }> {
  const headerRegex = /^(#{1,6})\s+(.+)$/gm
  const headers: Array<{ level: number; text: string; id: string }> = []

  let match
  while ((match = headerRegex.exec(text)) !== null) {
    const level = match[1].length
    const text = match[2]
    const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-')
    headers.push({ level, text, id })
  }

  return headers
}

/**
 * Generate a random ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 11)
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null
      func(...args)
    }

    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
    return false
  }
}

/**
 * Export content to PDF
 */
export async function exportToPDF(content: string, filename: string = 'research-report'): Promise<boolean> {
  try {
    // Dynamic import to reduce bundle size
    const { jsPDF } = await import('jspdf')

    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
    })

    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 20
    const maxWidth = pageWidth - (margin * 2)
    let currentY = margin

    // Add title
    doc.setFontSize(20)
    doc.setFont('helvetica', 'bold')
    doc.text('Research Report', margin, currentY)
    currentY += 15

    // Add date
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.text(formatDate(new Date()), margin, currentY)
    currentY += 10

    // Process content
    doc.setFontSize(11)
    const lines = content.split('\n')

    for (const line of lines) {
      // Check if we need a new page
      if (currentY > pageHeight - margin) {
        doc.addPage()
        currentY = margin
      }

      // Handle headers
      if (line.startsWith('# ')) {
        currentY += 5
        doc.setFontSize(16)
        doc.setFont('helvetica', 'bold')
        const text = line.replace('# ', '')
        doc.text(text, margin, currentY, { maxWidth })
        currentY += 10
        doc.setFontSize(11)
        doc.setFont('helvetica', 'normal')
      } else if (line.startsWith('## ')) {
        currentY += 3
        doc.setFontSize(14)
        doc.setFont('helvetica', 'bold')
        const text = line.replace('## ', '')
        doc.text(text, margin, currentY, { maxWidth })
        currentY += 8
        doc.setFontSize(11)
        doc.setFont('helvetica', 'normal')
      } else if (line.trim()) {
        // Regular text
        const splitText = doc.splitTextToSize(line, maxWidth)
        doc.text(splitText, margin, currentY)
        currentY += splitText.length * 6
      } else {
        currentY += 4
      }
    }

    // Save the PDF
    doc.save(`${filename}.pdf`)
    return true
  } catch (error) {
    console.error('Failed to export PDF:', error)
    return false
  }
}
