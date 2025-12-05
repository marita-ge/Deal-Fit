'use client'

import { useEffect, useRef } from 'react'
import { useChatStore } from '@/lib/store'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import DeckUpload from './DeckUpload'
import { AlertCircle, Sparkles } from 'lucide-react'

export default function ChatInterface() {
  const { messages, isLoading, error, currentPitchDeck } = useChatStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  return (
    <div className="flex h-screen flex-col bg-background">
      {/* Minimal Header */}
      <div className="border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="mx-auto flex h-14 max-w-3xl items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <h1 className="text-lg font-semibold">Investor Match</h1>
          </div>
          {currentPitchDeck && (
            <div className="text-xs text-muted-foreground">
              Pitch deck loaded
            </div>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="border-b border-destructive/20 bg-destructive/5 px-4 py-3">
          <div className="mx-auto flex max-w-3xl items-center gap-2 text-sm text-destructive">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <p>{error}</p>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto w-full max-w-3xl px-4">
          {messages.length === 0 && (
            <div className="flex h-full flex-col items-center justify-center py-12">
              <div className="mb-8 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <Sparkles className="h-8 w-8 text-primary" />
              </div>
              <h2 className="mb-2 text-2xl font-semibold">
                How can I help you find investors?
              </h2>
              <p className="mb-8 text-center text-muted-foreground">
                {currentPitchDeck
                  ? 'Ask me questions about finding the perfect investors for your startup.'
                  : 'Upload your pitch deck to get started, or ask general questions about investors.'}
              </p>
              
              {!currentPitchDeck && (
                <div className="mb-8 w-full max-w-md">
                  <DeckUpload />
                </div>
              )}

              <div className="grid w-full max-w-2xl grid-cols-1 gap-3 sm:grid-cols-2">
                <button
                  onClick={() => {
                    const textarea = document.querySelector('textarea') as HTMLTextAreaElement
                    if (textarea) {
                      textarea.focus()
                      textarea.value = 'Find investors interested in fintech startups'
                      const event = new Event('input', { bubbles: true })
                      textarea.dispatchEvent(event)
                    }
                  }}
                  className="group rounded-lg border border-border bg-card p-4 text-left text-sm transition-colors hover:bg-accent"
                >
                  <div className="font-medium">Find investors by industry</div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    "Find investors interested in fintech startups"
                  </div>
                </button>
                <button
                  onClick={() => {
                    const textarea = document.querySelector('textarea') as HTMLTextAreaElement
                    if (textarea) {
                      textarea.focus()
                      textarea.value = 'Who invests in Series A rounds?'
                      const event = new Event('input', { bubbles: true })
                      textarea.dispatchEvent(event)
                    }
                  }}
                  className="group rounded-lg border border-border bg-card p-4 text-left text-sm transition-colors hover:bg-accent"
                >
                  <div className="font-medium">Search by funding stage</div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    "Who invests in Series A rounds?"
                  </div>
                </button>
                <button
                  onClick={() => {
                    const textarea = document.querySelector('textarea') as HTMLTextAreaElement
                    if (textarea) {
                      textarea.focus()
                      textarea.value = 'Show me investors in San Francisco'
                      const event = new Event('input', { bubbles: true })
                      textarea.dispatchEvent(event)
                    }
                  }}
                  className="group rounded-lg border border-border bg-card p-4 text-left text-sm transition-colors hover:bg-accent"
                >
                  <div className="font-medium">Find by location</div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    "Show me investors in San Francisco"
                  </div>
                </button>
                <button
                  onClick={() => {
                    const textarea = document.querySelector('textarea') as HTMLTextAreaElement
                    if (textarea) {
                      textarea.focus()
                      textarea.value = 'Find investors matching my pitch deck'
                      const event = new Event('input', { bubbles: true })
                      textarea.dispatchEvent(event)
                    }
                  }}
                  className="group rounded-lg border border-border bg-card p-4 text-left text-sm transition-colors hover:bg-accent"
                >
                  <div className="font-medium">Match with my pitch deck</div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    "Find investors matching my pitch deck"
                  </div>
                </button>
              </div>
            </div>
          )}

          {messages.length > 0 && (
            <div className="py-6">
              {messages.map((message, index) => (
                <ChatMessage key={message.id} message={message} />
              ))}

              {isLoading && (
                <div className="group w-full py-6">
                  <div className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center">
                      <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center">
                        <div className="h-3 w-3 animate-pulse rounded-full bg-primary" />
                      </div>
                    </div>
                    <div className="flex-1 pt-1">
                      <div className="flex gap-1">
                        <div className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/40 [animation-delay:-0.3s]" />
                        <div className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/40 [animation-delay:-0.15s]" />
                        <div className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/40" />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        {!currentPitchDeck && messages.length === 0 && (
          <div className="mx-auto max-w-3xl px-4 pt-4">
            <DeckUpload />
          </div>
        )}
        <ChatInput />
      </div>
    </div>
  )
}
