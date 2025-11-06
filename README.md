# Trend App MCP Server

A Model Context Protocol (MCP) server that aggregates and processes trending content from various sources including HuggingFace, Reddit, YouTube, and more.

## Features

- Content crawling from multiple sources:
  - HuggingFace
  - Reddit
  - YouTube
  - SERP (Search Engine Results)

- Tag-based content filtering and organization
- Asynchronous API client support

## Quick Start

1. Install dependencies:

```bash
uv init
uv install

uv run main.py
```

2. Run the client example:
```python
from fastmcp import Client
import asyncio

client = Client("your-server-url")

async def fetch_trending_content(tags=None, user_query=None):
    async with client:
        response = await client.call_tool(
            "process_interest",
            {"tags": tags}
        )
        print(response)

asyncio.run(fetch_trending_content(tags=["dataset"]))
```

## Project Structure

```
app/
├── crawlers/       # Content crawlers for different platforms
├── llm/           # LLM integration implementations
├── schemas/       # Data models and schemas
├── tools/         # Tool definitions and routers
└── const/         # Constants and configuration
```
