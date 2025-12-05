'use client'

import { useState, KeyboardEvent, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useChatStore } from '@/lib/store'
import { cn } from '@/lib/utils'

export default function ChatInput() {
  const { isLoading, addMessage, setLoading, setError, currentPitchDeck } = useChatStore()
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSubmit = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: input.trim(),
      timestamp: new Date(),
    }

    addMessage(userMessage)
    setInput('')
    setLoading(true)
    setError(null)

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage.content,
          pitchDeckText: currentPitchDeck?.textContent || null,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to get response')
      }

      const data = await response.json()

      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: data.response,
        timestamp: new Date(),
      }

      addMessage(assistantMessage)
    } catch (error) {
      let errorMessage = 'Failed to send message'
      
      if (error instanceof Error) {
        errorMessage = error.message
        // Check if it's a network error
        if (error.message.includes('fetch failed') || error.message.includes('Failed to fetch')) {
          errorMessage = 'Unable to connect to the server. Please check your internet connection and ensure the backend API is running.'
        }
      }
      
      setError(errorMessage)
      
      const assistantErrorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: `⚠️ **Error**: ${errorMessage}\n\nPlease ensure:\n- Your backend API is running\n- The NEXT_PUBLIC_API_URL environment variable is set correctly\n- Your internet connection is stable`,
        timestamp: new Date(),
      }
      addMessage(assistantErrorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="mx-auto w-full max-w-3xl px-4 pb-4 pt-4">
      <div className="relative flex items-end gap-2 rounded-2xl border border-border bg-background shadow-sm transition-shadow focus-within:shadow-md">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message Investor Match..."
          disabled={isLoading}
          rows={1}
          className={cn(
            'max-h-[200px] w-full resize-none rounded-2xl border-0 bg-transparent px-4 py-3',
            'text-sm leading-6 placeholder:text-muted-foreground',
            'focus:outline-none focus:ring-0',
            'disabled:cursor-not-allowed disabled:opacity-50'
          )}
        />
        <div className="flex items-center gap-1 p-2">
          <Button
            onClick={handleSubmit}
            disabled={!input.trim() || isLoading}
            size="sm"
            className="h-8 w-8 rounded-lg p-0"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
      <p className="mt-2 text-center text-xs text-muted-foreground">
        Investor Match can make mistakes. Check important info.
      </p>
    </div>
  )
}
