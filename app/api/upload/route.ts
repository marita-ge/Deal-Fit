import { NextRequest, NextResponse } from 'next/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File | null

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 })
    }

    if (file.type !== 'application/pdf') {
      return NextResponse.json(
        { error: 'Only PDF files are allowed' },
        { status: 400 }
      )
    }

    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File size must be less than 10MB' },
        { status: 400 }
      )
    }

    // Forward file directly to backend API (no local storage needed in serverless)
    const backendFormData = new FormData()
    backendFormData.append('file', file)

    const backendResponse = await fetch(`${API_URL}/api/upload`, {
      method: 'POST',
      body: backendFormData,
    })

    if (!backendResponse.ok) {
      const error = await backendResponse.json().catch(() => ({
        error: 'Backend upload failed',
      }))
      return NextResponse.json(error, { status: backendResponse.status })
    }

    const backendData = await backendResponse.json()
    const filename = `${Date.now()}-${file.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`

    return NextResponse.json({
      id: backendData.id || filename,
      name: file.name,
      uploadedAt: new Date().toISOString(),
      textContent: backendData.text_content || backendData.textContent,
    })
  } catch (error) {
    console.error('Upload API error:', error)
    return NextResponse.json(
      {
        error:
          error instanceof Error ? error.message : 'Internal server error',
      },
      { status: 500 }
    )
  }
}
