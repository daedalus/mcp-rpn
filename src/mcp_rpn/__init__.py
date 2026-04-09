from fastmcp import FastMCP

from mcp_rpn._core import CalculatorSession

__version__ = "0.1.1"
__all__ = ["__version__", "mcp"]

mcp = FastMCP("mcp-rpn")
session = CalculatorSession()


@mcp.tool()
def evaluate(expression: str, show_stack: bool = False) -> str:
    """Evaluate an RPN (Reverse Polish Notation) expression.

    Operators: +, -, *, /, **, % (add, subtract, multiply, divide, power, modulo).
    Commands: clear (clear stack), dup (duplicate top), swap (swap top two).
    Example: '3 4 +' returns 7

    Args:
        expression: Space-separated RPN expression (e.g., "3 4 +").
        show_stack: Whether to return full stack after evaluation (default: False).

    Returns:
        The computed result as a string, or error message if evaluation failed.

    Example:
        >>> evaluate("3 4 +")
        'Result: 7'
    """
    result = session.evaluate(expression, show_stack)
    if result["error"]:
        return f"Error: {result['error']}"
    output = f"Result: {result['result']}"
    if show_stack and result["stack"]:
        output += f"\nStack: {result['stack']}"
    return output


@mcp.tool()
def clear() -> str:
    """Clear the RPN calculator stack.

    Removes all values from the current session stack.

    Returns:
        Confirmation message that stack was cleared.

    Example:
        >>> clear()
        'Stack cleared'
    """
    session.clear()
    return "Stack cleared"


def main() -> None:
    """Entry point for running the MCP server."""
    mcp.run()
