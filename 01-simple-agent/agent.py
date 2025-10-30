"""
Agent core module - handles conversation and tool execution
"""

import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from models import ChatMessage
from tools import get_all_tools_schema, TOOL_FUNCTIONS


class AIAgent:
    """AI Agent with tool support"""

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the AI agent

        Args:
            model: OpenAI model to use (default: gpt-4o-mini)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.tools = get_all_tools_schema()

    def _convert_messages(self, conversation_history: List[ChatMessage]) -> List[Dict[str, str]]:
        """
        Convert Pydantic messages to OpenAI format

        Args:
            conversation_history: List of ChatMessage objects

        Returns:
            List of message dictionaries for OpenAI API
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history
        ]

    def chat(self, user_message: str, conversation_history: List[ChatMessage] = None) -> Dict[str, Any]:
        """
        Process a chat message with the agent, handling tool calls automatically

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages

        Returns:
            Dictionary containing response, tool usage info, and updated messages
        """
        if conversation_history is None:
            conversation_history = []

        # Add user message to conversation
        messages = self._convert_messages(conversation_history)
        messages.append({"role": "user", "content": user_message})

        used_tools = []
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        # Main conversation loop with tool calling
        while iteration < max_iterations:
            iteration += 1

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if self.tools else None,
                tool_choice="auto" if self.tools else None
            )

            assistant_message = response.choices[0].message

            # Check if the model wants to call a tool
            if assistant_message.tool_calls:
                # Add assistant's message with tool calls to history
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Execute tool calls
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Track tool usage
                    if function_name not in used_tools:
                        used_tools.append(function_name)

                    # Execute the tool
                    tool_function = TOOL_FUNCTIONS.get(function_name)
                    if tool_function:
                        tool_result = tool_function(**function_args)

                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result
                        })
                    else:
                        # Tool not found
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": f"Error: Tool {function_name} not found"
                        })

                # Continue loop to get final response from model
                continue
            else:
                # No tool calls, return the response
                final_response = assistant_message.content

                # Convert back to our format
                response_messages = []
                for msg in conversation_history:
                    response_messages.append(ChatMessage(role=msg.role, content=msg.content))

                # Add user message
                response_messages.append(ChatMessage(role="user", content=user_message))

                # Add assistant response
                response_messages.append(ChatMessage(role="assistant", content=final_response))

                return {
                    "response": final_response,
                    "used_tools": used_tools,
                    "messages": response_messages
                }

        # If we hit max iterations, return error
        return {
            "response": "Sorry, I encountered an issue processing your request. Please try again.",
            "used_tools": used_tools,
            "messages": []
        }
