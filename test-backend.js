// Quick test script to verify Railway backend is accessible
// Run with: node test-backend.js

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://deal-fit-production.up.railway.app'

async function testBackend() {
  console.log('Testing backend at:', API_URL)
  
  // Test 1: Health check
  try {
    console.log('\n1. Testing /health endpoint...')
    const healthRes = await fetch(`${API_URL}/health`)
    const healthData = await healthRes.json()
    console.log('✓ Health check:', healthData)
  } catch (error) {
    console.error('✗ Health check failed:', error.message)
  }
  
  // Test 2: Root endpoint
  try {
    console.log('\n2. Testing / endpoint...')
    const rootRes = await fetch(`${API_URL}/`)
    const rootData = await rootRes.json()
    console.log('✓ Root endpoint:', rootData)
  } catch (error) {
    console.error('✗ Root endpoint failed:', error.message)
  }
  
  // Test 3: Chat endpoint
  try {
    console.log('\n3. Testing /api/chat endpoint...')
    const chatRes = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: 'Test query',
        pitch_deck_text: null,
      }),
    })
    
    if (!chatRes.ok) {
      const errorText = await chatRes.text()
      console.error('✗ Chat endpoint failed:', chatRes.status, errorText)
    } else {
      const chatData = await chatRes.json()
      console.log('✓ Chat endpoint response:', chatData)
    }
  } catch (error) {
    console.error('✗ Chat endpoint failed:', error.message)
  }
}

testBackend()
