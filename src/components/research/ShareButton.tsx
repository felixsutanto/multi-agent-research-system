import { Share2, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { useState } from "react"

interface ShareButtonProps {
    query: string
    sessionId?: string
}

export function ShareButton({ query, sessionId }: ShareButtonProps) {
    const [copied, setCopied] = useState(false)

    const handleShare = async () => {
        const url = new URL(window.location.href)

        if (sessionId) {
            url.searchParams.set('session', sessionId)
        } else if (query) {
            url.searchParams.set('q', encodeURIComponent(query))
        }

        const shareUrl = url.toString()

        // Try native share first (mobile)
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'Research Query',
                    text: query,
                    url: shareUrl,
                })
                toast.success("Shared successfully!")
                return
            } catch (error) {
                // User cancelled or error occurred, fall back to clipboard
            }
        }

        // Fallback to clipboard
        try {
            await navigator.clipboard.writeText(shareUrl)
            setCopied(true)
            toast.success("Link copied to clipboard!")
            setTimeout(() => setCopied(false), 2000)
        } catch (error) {
            toast.error("Failed to copy link")
        }
    }

    return (
        <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
            className="group"
        >
            {copied ? (
                <>
                    <Check className="w-4 h-4 mr-1 text-green-500" />
                    Copied!
                </>
            ) : (
                <>
                    <Share2 className="w-4 h-4 mr-1 group-hover:scale-110 transition-transform" />
                    Share
                </>
            )}
        </Button>
    )
}
