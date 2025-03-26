# Library Docs MCP Server

This is an MCP (Model Context Protocol) server that allows you to search and fetch documentation for popular libraries like Langchain, Llama-Index, MCP, and OpenAI using the Serper API.

## Features

- Search library documentation using a natural language query.
- Supports Langchain, Llama-Index, MCP, and OpenAI (Update the code to add other libraries).
- Uses the `Serper API` to perform site-specific searches.
- Parses and returns the documentation using `BeautifulSoup`.
- **Provides updated documentation** – useful for LLM models with knowledge cut-off dates.

## Why Use This Server with LLMs?

Many LLM models, including those used in **Anthropic Desktop** and similar platforms, have a knowledge cut-off date and may not have access to the latest library documentation. This MCP server solves that problem by:

- Fetching **real-time documentation** from official sources.
- Providing **up-to-date information** for development and troubleshooting.
- Improving the accuracy and relevance of responses when working with new library updates.

### Setting Up with Anthropic Desktop

To use this server with **Anthropic Desktop**, update the `claude_desktop_config.json` file with the following configuration:

```json
{
  "mcpServers": {
    "docs-mcp-server": {
      "command": "C:\\Users\\Vikram\\.local\\bin\\uv.exe",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "F:\\My Projects\\AI\\docs-mcp-server\\server.py"
      ]
    }
  }
}
```
