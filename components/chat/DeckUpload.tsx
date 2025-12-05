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
      <Card className="border-2 border-primary/50">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                <File className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="font-medium">{currentPitchDeck.name}</p>
                <p className="text-sm text-muted-foreground">
                  Uploaded {formatDate(currentPitchDeck.uploadedAt)}
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={removeDeck}
              disabled={uploading}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card
      {...getRootProps()}
      className={`cursor-pointer border-2 border-dashed transition-colors ${
        isDragActive
          ? 'border-primary bg-primary/5'
          : 'border-muted-foreground/25 hover:border-primary/50'
      }`}
    >
      <CardContent className="p-8">
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center gap-4 text-center">
          {uploading ? (
            <>
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
              <div>
                <p className="font-medium">Uploading pitch deck...</p>
                <p className="text-sm text-muted-foreground">
                  Please wait while we process your PDF
                </p>
              </div>
            </>
          ) : (
            <>
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <Upload className="h-8 w-8 text-primary" />
              </div>
              <div>
                <p className="font-medium">
                  {isDragActive
                    ? 'Drop your pitch deck here'
                    : 'Drag & drop your pitch deck here'}
                </p>
                <p className="text-sm text-muted-foreground">
                  or click to browse (PDF, max 10MB)
                </p>
              </div>
            </>
          )}
        </div>
      </CardContent>
    </Card>
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
