from mcp.server.fastmcp import FastMCP
from app import get_realtime_info, generate_video_script

# Initialize MCP server with a descriptive name
mcp = FastMCP("Story Forge")


@mcp.tool()
def get_latest_info_mcp(query: str) -> str:
    """
    Fetch real-time information for a given query.

    This tool retrieves up-to-date information (news, trends, or general info)
    based on the user query. It acts as a wrapper over the underlying
    `get_realtime_info` function.

    Args:
        query (str): The user query for which real-time information is required.
                     Example: "latest stock market news", "AI trends 2026"

    Returns:
        str: A text response containing relevant real-time information.
             Returns an error message string if retrieval fails.
    """

    # Call underlying function to fetch real-time information
    return get_realtime_info(query)


@mcp.tool()
def generate_video_script_mcp(query: str) -> str:
    """
    Generate a short-form video script (Instagram Reels / YouTube Shorts).

    This tool performs two steps:
    1. Fetches real-time information using the query
    2. Converts that information into a creative ~200-word video script

    Args:
        query (str): The topic or idea for which the script should be generated.
                     Example: "latest AI trends", "stock market update"

    Returns:
        str: A creative, human-like video script (~200 words) suitable for
             Instagram Reels or YouTube Shorts.
             Returns an error message string if script generation fails.
    """

    # Step 1: Fetch real-time information
    info_text = get_realtime_info(query)

    # Step 2: Generate video script from fetched information
    return generate_video_script(info_text)


# Entry point to start the MCP server
if __name__ == "__main__":
    # Run MCP server using stdio transport (used by MCP clients like Claude)
    mcp.run(transport="stdio")