"""
Tools module for the AI agent

This module contains tool definitions and schemas for available agent tools.
Currently includes a web search tool using Exa.
"""

import os
from exa_py import Exa


def get_web_search_tool_schema():
    """
    Returns the tool schema for web search that will be passed to OpenAI.

    Returns:
        dict: Tool schema with type, name, description, and parameters
    """
    return {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the web for information on a given query. Use this when you need current information about a topic, recent events, or data that may not be in your training data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string"
                    }
                },
                "required": ["query"]
            }
        }
    }


def search_web_tool(query: str) -> str:
    """
    Executes a web search using the provided query.

    Args:
        query (str): The search query string

    Returns:
        str: Formatted search results containing titles, URLs, and snippets
    """
    try:
        # Get Exa API key from environment
        api_key = os.getenv("EXA_API_KEY")
        if not api_key:
            return "Error: EXA_API_KEY not set in environment variables"

        # Initialize Exa client
        exa = Exa(api_key=api_key)

        # Perform search
        results = exa.search(query, num_results=5)

        if not results.results:
            return f"No search results found for query: '{query}'"

        # Format results
        formatted_results = f"Search results for '{query}':\n\n"
        for idx, result in enumerate(results.results, 1):
            formatted_results += f"{idx}. {result.title}\n"
            formatted_results += f"   URL: {result.url}\n"
            if result.text:
                # Truncate long text snippets
                text = result.text[:300] + "..." if len(result.text) > 300 else result.text
                formatted_results += f"   {text}\n\n"

        return formatted_results.strip()

    except Exception as e:
        error_msg = str(e)
        return f"Error performing search: {error_msg}"


def get_all_tools_schema():
    """
    Returns a list of all available tool schemas for the AI agent.

    Returns:
        list: List of tool schema dictionaries
    """
    return [get_web_search_tool_schema()]


# Tool execution mapping
TOOL_FUNCTIONS = {
    "search_web": search_web_tool
}
