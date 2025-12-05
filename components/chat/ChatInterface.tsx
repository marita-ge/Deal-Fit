'use client'

import { useEffect, useRef } from 'react'
import { useChatStore } from '@/lib/store'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import DeckUpload from './DeckUpload'
import { AlertCircle } from 'lucide-react'
import { Card } from '@/components/ui/card'

export default function ChatInterface() {
  const { messages, isLoading, error } = useChatStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <div className="border-b bg-background p-4">
        <h1 className="text-2xl font-bold">Investor Match Chat</h1>
        <p className="text-sm text-muted-foreground">
          Upload your pitch deck and ask questions to find the perfect investors
        </p>
      </div>

      {/* Pitch Deck Upload */}
      <div className="border-b bg-muted/30 p-4">
        <DeckUpload />
      </div>

      {/* Error Display */}
      {error && (
        <div className="border-b border-destructive/50 bg-destructive/10 p-4">
          <div className="flex items-center gap-2 text-destructive">
            <AlertCircle className="h-4 w-4" />
            <p className="text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="mx-auto max-w-3xl">
          {messages.length === 0 && (
            <Card className="border-dashed p-12 text-center">
              <p className="text-muted-foreground">
                Start by uploading your pitch deck above, then ask questions like:
              </p>
              <ul className="mt-4 space-y-2 text-left text-sm text-muted-foreground">
                <li>• "Find investors interested in fintech startups"</li>
                <li>• "Who invests in Series A rounds?"</li>
                <li>• "Show me investors in San Francisco"</li>
                <li>• "Find investors matching my pitch deck"</li>
              </ul>
            </Card>
          )}

          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {isLoading && (
            <div className="flex gap-4 py-6">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
              </div>
              <div className="rounded-lg bg-muted px-4 py-3">
                <p className="text-muted-foreground">Thinking...</p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput />
    </div>
  )
}
