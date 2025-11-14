from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds  two number

    Args:
        a (int): first integer
        b (int): second integer

    Returns:
        int: sum of two numbers
    """
    return a + b

@mcp.tool()
def multiply(a: int, b: int)-> int:
    """Multiplies two number

    Args:
        a (int): first integer
        b (int): second integer

    Returns:
        int: product of a and b
    """
    return a * b

if __name__ == "__main__":
    # The transport = "stdio" tellls the server to 
    # use the standard input/output (stdin and stdout) to receive to tool function calls.
    mcp.run(transport="stdio")
    