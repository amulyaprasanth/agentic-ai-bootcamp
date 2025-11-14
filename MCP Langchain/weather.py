from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather at the location

    Args:
        location (str): location where you want to get weather

    Returns:
        str: weather
    """
    return f"It's always sunny in {location}"

if __name__ == "__main__":
    # streamable-http transport runs an fastapi application
    mcp.run(transport="streamable-http")