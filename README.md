# AI Agent with Web Search

A simple AI agent built with FastAPI that can search the web using Exa search API. Available in two modes: REST API and MCP Server.

## Features

- 🤖 AI-powered agent using OpenAI (GPT-4o-mini)
- 🔍 Web search capabilities via Exa
- 🌐 REST API for standard HTTP requests
- 🔌 MCP (Model Context Protocol) server support
- 📝 Automatic tool calling for web searches
- 💬 Conversation context management

## Setup

### 1. Clone and Install Dependencies

```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Exa API Key (required for web search)
EXA_API_KEY=your_exa_api_key_here
```

Get your API keys:
- OpenAI: https://platform.openai.com/api-keys
- Exa: https://exa.ai

## Usage

### REST API Mode

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

#### Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the latest developments in AI?",
    "conversation_history": []
  }'
```

Response:
```json
{
  "response": "Here are some latest developments...",
  "used_tools": ["search_web"],
  "messages": [
    {"role": "user", "content": "What are the latest developments in AI?"},
    {"role": "assistant", "content": "Here are some latest developments..."}
  ]
}
```

### MCP Server Mode

Run the MCP server:

```bash
python mcp_server.py
```

The MCP server communicates via stdio and can be integrated with MCP-compatible clients.

## Architecture

```
User Request
    ↓
FastAPI / MCP Server
    ↓
AIAgent (agent.py)
    ↓
OpenAI API (decides if web search needed)
    ↓
Tools Layer (tools.py) - Exa Search
    ↓
Formatted Response
```

## Project Structure

```
agent-one/
├── main.py              # FastAPI REST API
├── mcp_server.py        # MCP Protocol Server
├── agent.py             # Core AI agent logic
├── tools.py             # Tool implementations (web search)
├── models.py            # Pydantic models
├── requirements.txt     # Dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## Features Explained

### Web Search Tool

The agent automatically decides when to search the web:
- Questions about current events
- Recent news or developments
- Information not in training data

### Conversation Context

The agent maintains full conversation history:
- Client sends history with each request
- Agent returns complete updated history
- Stateless design for scalability

### Tool Calling

Multi-step reasoning:
1. User asks question
2. Agent decides if search needed
3. Executes search tool automatically
4. Integrates results into response
5. Returns final answer

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openai` - OpenAI API client
- `exa-py` - Exa search API
- `mcp` - Model Context Protocol
- `python-dotenv` - Environment management

## License

MIT
