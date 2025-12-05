'use client'

import { ChatMessage as ChatMessageType } from '@/types'
import ReactMarkdown from 'react-markdown'
import { User } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ChatMessageProps {
  message: ChatMessageType
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className="group w-full">
      <div className="flex gap-4">
        {/* Avatar */}
        <div className="flex h-8 w-8 shrink-0 items-center justify-center">
          {isUser ? (
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground">
              <User className="h-4 w-4" />
            </div>
          ) : (
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
              <div className="h-4 w-4 rounded-full bg-primary" />
            </div>
          )}
        </div>

        {/* Message Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-sm font-medium">
              {isUser ? 'You' : 'Investor Match'}
            </span>
          </div>
          
          <div
            className={cn(
              'prose prose-sm max-w-none dark:prose-invert',
              'prose-headings:mt-4 prose-headings:mb-2',
              'prose-p:my-2 prose-p:leading-7',
              'prose-ul:my-2 prose-ol:my-2',
              'prose-li:my-1',
              'prose-code:text-sm prose-code:bg-muted prose-code:px-1 prose-code:py-0.5 prose-code:rounded',
              'prose-pre:bg-muted prose-pre:p-4 prose-pre:rounded-lg',
              'prose-a:text-primary prose-a:underline',
              'prose-strong:font-semibold',
              'text-foreground'
            )}
          >
            {isUser ? (
              <div className="whitespace-pre-wrap break-words leading-7">
                {message.content}
              </div>
            ) : (
              <ReactMarkdown
                components={{
                  h1: ({ children }) => (
                    <h1 className="text-xl font-semibold mb-3 mt-6 first:mt-0">{children}</h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="text-lg font-semibold mb-2 mt-5">{children}</h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="text-base font-semibold mb-2 mt-4">{children}</h3>
                  ),
                  p: ({ children }) => (
                    <p className="mb-3 leading-7 last:mb-0">{children}</p>
                  ),
                  ul: ({ children }) => (
                    <ul className="list-disc list-inside mb-3 space-y-1 ml-1">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="list-decimal list-inside mb-3 space-y-1 ml-1">{children}</ol>
                  ),
                  li: ({ children }) => (
                    <li className="leading-7">{children}</li>
                  ),
                  strong: ({ children }) => (
                    <strong className="font-semibold">{children}</strong>
                  ),
                  em: ({ children }) => (
                    <em className="italic">{children}</em>
                  ),
                  code: ({ children }) => (
                    <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono">
                      {children}
                    </code>
                  ),
                  pre: ({ children }) => (
                    <pre className="bg-muted p-4 rounded-lg overflow-x-auto my-3">
                      {children}
                    </pre>
                  ),
                  a: ({ href, children }) => (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary underline hover:text-primary/80"
                    >
                      {children}
                    </a>
                  ),
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-muted-foreground/20 pl-4 my-3 italic">
                      {children}
                    </blockquote>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
