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

    // Check if API URL is configured (only block localhost in production)
    const isProduction = process.env.NODE_ENV === 'production' || process.env.VERCEL === '1'
    const isLocalhost = API_URL.includes('localhost') || API_URL.includes('127.0.0.1')
    
    if (isProduction && (!API_URL || isLocalhost)) {
      console.warn('Backend API URL not configured in production. Using fallback response.')
      return NextResponse.json({
        response: `**Backend API Not Configured**

To enable AI-powered investor matching on Vercel, you need to:

1. **Deploy your FastAPI backend** to a hosting service:
   - Railway (railway.app) - Recommended
   - Render (render.com)
   - Fly.io (fly.io)
   - Or any Python hosting service

2. **Set the environment variable in Vercel:**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: \`NEXT_PUBLIC_API_URL\` = your deployed backend URL (e.g., https://your-app.railway.app)
   - Select all environments (Production, Preview, Development)
   - Click Save and redeploy

3. **Ensure your backend has:**
   - Access to the investor database files
   - \`ANTHROPIC_API_KEY\` configured
   - All Python dependencies installed

Once configured, I'll be able to provide real investor recommendations based on your pitch deck and query.`,
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
