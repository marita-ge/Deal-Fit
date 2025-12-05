'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, X, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { validatePDF, formatFileSize } from '@/lib/utils'
import { useChatStore } from '@/lib/store'
import { PitchDeck } from '@/types'

export default function DeckUpload() {
  const { currentPitchDeck, setPitchDeck, setError } = useChatStore()
  const [uploading, setUploading] = useState(false)

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0]
      if (!file) return

      const validation = validatePDF(file)
      if (!validation.valid) {
        setError(validation.error || 'Invalid file')
        return
      }

      setUploading(true)
      setError(null)

      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData,
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.error || 'Upload failed')
        }

        const data = await response.json()
        
        const deck: PitchDeck = {
          id: data.id,
          name: file.name,
          uploadedAt: new Date(data.uploadedAt),
          textContent: data.textContent,
        }

        setPitchDeck(deck)
      } catch (error) {
        setError(
          error instanceof Error ? error.message : 'Failed to upload pitch deck'
        )
      } finally {
        setUploading(false)
      }
    },
    [setPitchDeck, setError]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    disabled: uploading,
  })

  const removeDeck = () => {
    setPitchDeck(null)
  }

  if (currentPitchDeck) {
    return (
      <div className="mb-4 rounded-lg border border-border bg-card p-3">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 min-w-0 flex-1">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded bg-primary/10">
              <File className="h-4 w-4 text-primary" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium">{currentPitchDeck.name}</p>
              <p className="text-xs text-muted-foreground">
                Ready to use
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={removeDeck}
            disabled={uploading}
            className="h-8 w-8 shrink-0 p-0"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div
      {...getRootProps()}
      className={`cursor-pointer rounded-lg border-2 border-dashed transition-colors ${
        isDragActive
          ? 'border-primary bg-primary/5'
          : 'border-border hover:border-primary/50 hover:bg-accent/50'
      }`}
    >
      <input {...getInputProps()} />
      <div className="p-6">
        <div className="flex flex-col items-center justify-center gap-3 text-center">
          {uploading ? (
            <>
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
              <div>
                <p className="text-sm font-medium">Uploading pitch deck...</p>
                <p className="text-xs text-muted-foreground">
                  Please wait while we process your PDF
                </p>
              </div>
            </>
          ) : (
            <>
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <Upload className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium">
                  {isDragActive
                    ? 'Drop your pitch deck here'
                    : 'Upload your pitch deck'}
                </p>
                <p className="text-xs text-muted-foreground">
                  PDF files up to 10MB
                </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}
