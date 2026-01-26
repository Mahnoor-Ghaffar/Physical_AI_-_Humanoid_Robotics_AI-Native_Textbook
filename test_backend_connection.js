const fetch = require('node-fetch');

async function testBackendConnection() {
  const backendUrl = 'https://mahnoor09-deploy-hack.hf.space';

  console.log('Testing connection to backend:', backendUrl);

  try {
    // Test the root endpoint
    const response = await fetch(backendUrl);
    console.log('Status:', response.status);
    console.log('Response type:', response.headers.get('content-type'));

    if (response.ok) {
      console.log('✅ Successfully connected to the backend!');

      // Try to get the response text to see what we get
      const text = await response.text();
      console.log('Response preview (first 200 chars):', text.substring(0, 200));
    } else {
      console.log('❌ Backend responded with error:', response.status);
    }
  } catch (error) {
    console.error('❌ Error connecting to backend:', error.message);
  }

  // Test the /chat endpoint
  console.log('\nTesting /chat endpoint...');
  try {
    const chatResponse = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [{ role: 'user', content: 'Hello' }],
        model: 'gpt-3.5-turbo',
        temperature: 0.7,
        max_tokens: 50
      })
    });

    console.log('/chat endpoint status:', chatResponse.status);

    if (chatResponse.ok) {
      const data = await chatResponse.json();
      console.log('✅ /chat endpoint is working!');
      console.log('Response preview:', JSON.stringify(data, null, 2).substring(0, 200));
    } else {
      console.log('❌ /chat endpoint returned error:', chatResponse.status);
    }
  } catch (error) {
    console.error('❌ Error testing /chat endpoint:', error.message);
  }
}

testBackendConnection();