from fastmcp import Client
import asyncio

client = Client("http://localhost:8000/mcp")

async def fetch_trending_content(tags=None, user_query=None):
    async with client:
        response = await client.call_tool(
            "process_interest",
            {"tags": tags}
        )
        with open("trending_content.json", "w") as f:
            import json
            json.dump(response, f, indent=4)

asyncio.run(fetch_trending_content(tags=["discussion", "ai"], user_query=None))
