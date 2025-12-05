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

    // Check if API URL is configured
    if (!API_URL || API_URL === 'http://localhost:8000') {
      console.warn('Backend API URL not configured. Using fallback response.')
      return NextResponse.json({
        response: `I understand you're asking: "${query}". 

To use the full AI-powered investor matching features, please configure the backend API URL in your environment variables (NEXT_PUBLIC_API_URL).

For now, here's what I can help with:
- Finding investors by industry, stage, or location
- Matching investors to your pitch deck
- Getting contact information for relevant investors

Please ensure your backend API is running and the NEXT_PUBLIC_API_URL environment variable is set correctly.`,
      })
    }

    // Call the backend API with timeout
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 30000) // 30 second timeout

    try {
      const backendResponse = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          pitch_deck_text: pitchDeckText || null,
        }),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!backendResponse.ok) {
        const error = await backendResponse.json().catch(() => ({
          error: `Backend request failed with status ${backendResponse.status}`,
        }))
        return NextResponse.json(error, { status: backendResponse.status })
      }

      const data = await backendResponse.json()

      return NextResponse.json({
        response: data.response || data.recommendation || 'No response received',
      })
    } catch (fetchError) {
      clearTimeout(timeoutId)
      
      if (fetchError instanceof Error && fetchError.name === 'AbortError') {
        return NextResponse.json(
          { error: 'Request timeout: The backend API took too long to respond. Please try again.' },
          { status: 504 }
        )
      }

      // Network error or connection refused
      if (fetchError instanceof Error) {
        console.error('Backend fetch error:', fetchError.message)
        return NextResponse.json(
          { 
            error: `Unable to connect to backend API at ${API_URL}. Please ensure the backend is running and accessible. Error: ${fetchError.message}` 
          },
          { status: 503 }
        )
      }

      throw fetchError
    }
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
