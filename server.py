from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import httpx
import json
import os
from dotenv import load_dotenv


load_dotenv()

mcp = FastMCP("docs-mcp-server")

USER_AGENT = "docs-mcp-server-app/1.0"
SERPER_URL = "https://google.serper.dev/search"

# Libraries and their documentation urls
docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "mcp": "modelcontextprotocol.io",
    "openai": "platform.openai.com/docs"
}

# Search through serper api
async def search_web(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}


# Fetch serper results url doc and parse using BeautifulSoup
async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"


@mcp.tool()
async def get_docs(query: str, library: str):
    """
    Search the docs for a given query and library.
    Supports langchain, llama-index, mcp, and openai.

    Args:
        query: The query to search for (e.g. "Chroma DB")
        library: The library to search in (e.g. "langchain")
    
    Returns:
        Text from the docs
    """
    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported by this tool")

    query = f"site:{docs_urls[library]} {query}" # Serper search format for searching in specified site
    results = await search_web(query)

    if len(results["organic"]) == 0:
        return "No results found"
    
    text = ""
    for result in results["organic"]:
        text += await fetch_url(result["link"])
    
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")
