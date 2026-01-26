"""
AI Agent with Retrieval Capabilities

This script creates an AI agent using the OpenAI Assistants API that can answer questions
about book content using retrieval-augmented generation. The agent integrates with the
existing Qdrant search logic through the retrieval system in backend/retrieve.py.
"""
import os
import sys
import json
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv




# Add the backend directory to the path so we can import the retrieval system
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from retrieve import retrieve_content

# Load environment variables
load_dotenv()

# Initialize OpenAI client with modern approach
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY environment variable is not set.")
    print("💡 Solution: Add 'OPENAI_API_KEY=your_openai_api_key' to your .env file")
    print("     or set it as an environment variable before running this script.")
    print("     Get your API key from: https://platform.openai.com/api-keys")
    sys.exit(1)

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"❌ Error initializing OpenAI client: {str(e)}")
    print("💡 Solution: Verify your API key is correct and has proper permissions.")
    sys.exit(1)

def create_retrieval_tool():
    """
    Create a retrieval tool that wraps the existing retrieve_content function.
    This tool will be available to the AI agent to search the vector database.
    """
    return {
        "type": "function",
        "function": {
            "name": "retrieve_content",
            "description": "Retrieve relevant content from the book knowledge base based on a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant content"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }

def execute_retrieve_content(query: str, top_k: int = 5) -> str:
    """
    Execute the retrieval function and format results for the agent.
    """
    try:
        results = retrieve_content(query, top_k)

        if not results:
            return json.dumps({
                "error": "No relevant content found for the query",
                "query": query
            })

        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result.get('payload', {}).get('original_text', '')[:500] + "..." if len(result.get('payload', {}).get('original_text', '')) > 500 else result.get('payload', {}).get('original_text', ''),
                "source_url": result.get('payload', {}).get('source_url', 'N/A'),
                "relevance_score": result.get('score', 0.0)
            })

        return json.dumps(formatted_results)
    except Exception as e:
        return json.dumps({
            "error": f"Error retrieving content: {str(e)}",
            "query": query
        })

def create_agent():
    """
    Create an OpenAI assistant with the retrieval tool.
    """
    # List of preferred models in order of preference
    preferred_models = [
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-4o-mini"
    ]

    selected_model = None

    # Try to find an available model
    for model in preferred_models:
        try:
            # Test if the model is available by making a simple call
            client.models.retrieve(model)
            selected_model = model
            print(f"✅ Using model: {model}")
            break
        except Exception:
            continue

    if not selected_model:
        # If none of the preferred models are available, try to list available models
        try:
            available_models = client.models.list()
            print("📋 Available models:")
            for model_info in available_models.data:
                if 'gpt' in model_info.id.lower():
                    print(f"  - {model_info.id}")
        except Exception:
            pass

        print("❌ Error: No suitable GPT models found in your OpenAI account.")
        print("💡 Solution: Ensure you have access to GPT models in your OpenAI account.")
        print("     Check: https://platform.openai.com/account/billing/overview")
        print("     You may need to add payment information or upgrade your account.")
        print("     Or use a different model by updating the code.")
        return None

    try:
        assistant = client.beta.assistants.create(
            name="Book Content Assistant",
            description="An AI assistant that answers questions about book content using retrieval-augmented generation",
            model=selected_model,
            tools=[create_retrieval_tool()],
            instructions="You are a helpful assistant that answers questions about book content. Use the retrieve_content tool to find relevant information before responding. Always base your answers on the retrieved content and cite sources when possible. If no relevant content is found, inform the user."
        )
        return assistant
    except Exception as e:
        print(f"❌ Error creating assistant: {str(e)}")
        print("💡 Solution: Check your OpenAI account permissions and ensure you have sufficient quota.")
        print("     Make sure your API key has assistant creation permissions enabled.")
        return None

def run_agent_interaction(assistant_id: str):
    """
    Run an interactive session with the agent.
    """
    print("AI Agent with Retrieval Capabilities - Ready to answer questions about book content!")
    print("Type 'quit' to exit the conversation.\n")

    # Create a thread for the conversation
    thread = client.beta.threads.create()

    while True:
        user_input = input("Your question: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Add user message to thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )

            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )

            # Wait for the run to complete
            import time
            while run.status in ['queued', 'in_progress']:
                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Handle tool calls if needed
            if run.status == 'requires_action' and run.required_action:
                # Execute the tool calls
                tool_outputs = []
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "retrieve_content":
                        # Parse the arguments
                        args = json.loads(tool_call.function.arguments)
                        query = args.get("query")
                        top_k = args.get("top_k", 5)

                        # Execute the function
                        result = execute_retrieve_content(query, top_k)

                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": result
                        })

                # Submit tool outputs
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

                # Wait for the run to complete after tool outputs
                while run.status in ['queued', 'in_progress']:
                    time.sleep(0.5)
                    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Get the assistant's response
            messages = client.beta.threads.messages.list(
                thread_id=thread.id,
                order="desc"
            )

            if messages.data:
                assistant_response = messages.data[0].content[0].text.value
                print(f"\nAgent: {assistant_response}\n")
            else:
                print("\nAgent: I couldn't generate a response for your query.\n")

        except Exception as e:
            print(f"\nError during interaction: {str(e)}\n")

def main():
    """
    Main function to initialize and run the AI agent.
    """
    print("Initializing AI Agent with Retrieval Capabilities...")

    try:
        # Create the assistant
        assistant = create_agent()
        if assistant is None:
            print("❌ Failed to create assistant. Exiting.")
            sys.exit(1)

        print(f"✅ Assistant created with ID: {assistant.id}")

        # Run the interactive session
        run_agent_interaction(assistant.id)

    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        print("💡 Solution: Check the error message above for specific guidance.")
        print("     Common issues:")
        print("     - Invalid API key or insufficient permissions")
        print("     - No available GPT models in your account")
        print("     - Network connectivity issues")
        print("     - Rate limits exceeded")
        sys.exit(1)

if __name__ == "__main__":
    main()