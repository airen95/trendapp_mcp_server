from fastmcp import Client
import asyncio

client = Client("https://invisible-plum-panther.fastmcp.app/mcp")

async def fetch_trending_content(tags=None, user_query=None):
    async with client:
        response = await client.call_tool(
            "process_interest",
            {"tags": tags}
        )
        print(response)

asyncio.run(fetch_trending_content(tags=["dataset"], user_query=None))

