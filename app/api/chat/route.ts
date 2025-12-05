import { NextRequest, NextResponse } from 'next/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { query } = body

    if (!query || typeof query !== 'string') {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      )
    }

    // Get current pitch deck from session/state
    // For now, we'll pass it through the request body
    const { pitchDeckText } = body

    // Call the backend API
    const backendResponse = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        pitch_deck_text: pitchDeckText || null,
      }),
    })

    if (!backendResponse.ok) {
      const error = await backendResponse.json().catch(() => ({
        error: 'Backend request failed',
      }))
      return NextResponse.json(error, { status: backendResponse.status })
    }

    const data = await backendResponse.json()

    return NextResponse.json({
      response: data.response || data.recommendation || 'No response received',
    })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      {
        error:
          error instanceof Error ? error.message : 'Internal server error',
      },
      { status: 500 }
    )
  }
}
