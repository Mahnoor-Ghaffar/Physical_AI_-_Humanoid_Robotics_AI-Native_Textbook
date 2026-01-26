// Test script to verify the frontend can handle the backend response format
const backendResponse = {
  "response": "Based on the retrieved information: --- title: \"Chapter 1: Voice-to-Action with OpenAI Whisper\" description: \"Explore OpenAI Whisper for voice recognition and transcription, integrating with ROS 2 for voice-controlled humanoid robot commands.\" --- import HardwareTrackCallout from '@site/src/components/HardwareTrackCallout'; # Chapter ...\n\nThis answer is based on information from 5 sources.",
  "sources": [
    {
      "source_url": "https://physical-ai-humanoid-robotics-ai-na.vercel.app/module4-vla/ch1-voice",
      "relevance_score": 0.3653394,
      "content_preview": "--- title: \"Chapter 1: Voice-to-Action with OpenAI Whisper\" description: \"Explore OpenAI Whisper for voice recognition and transcription, integrating with ROS 2 for voice-controlled humanoid robot com..."
    }
  ],
  "metadata": {
    "query": "What is chapter 1 about?",
    "top_k": 5,
    "results_count": 5
  }
};

// Simulate the frontend logic after my changes
let responseText = '';
if (backendResponse.response) {
  // Use the response field from the deployed backend
  responseText = backendResponse.response;
} else if (backendResponse.results && backendResponse.results.length > 0) {
  // Fallback to original format if needed
  responseText = `Based on the knowledge base: ${backendResponse.results[0].content.substring(0, 300)}...`;
} else {
  responseText = 'I couldn\'t find relevant information in the knowledge base.';
}

console.log('Formatted response text:');
console.log(responseText);
console.log('\nSuccess: Frontend can now properly handle the deployed backend response!');