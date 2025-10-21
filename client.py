from fastmcp import Client
import asyncio

client = Client("http://localhost:8000/mcp")

async def fetch_trending_content(tags=None, user_query=None):
    async with client:
        response = await client.call_tool(
            "process_interest",
            {"tags": tags, "user_query": user_query}
        )
        print(response)

asyncio.run(fetch_trending_content(tags=["AI", 'video', 'news'], user_query=None))
