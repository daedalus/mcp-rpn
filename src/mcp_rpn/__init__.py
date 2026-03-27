from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from ._core import CalculatorSession

__version__ = "0.1.0"
__all__ = ["__version__"]

server = Server("mcp-rpn")
session = CalculatorSession()


@server.list_tools()  # type: ignore[no-untyped-call,untyped-decorator]
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="evaluate",
            description="Evaluate an RPN (Reverse Polish Notation) expression. "
            "Operators: +, -, *, /, **, % (add, subtract, multiply, divide, power, modulo). "
            "Commands: clear (clear stack), dup (duplicate top), swap (swap top two). "
            "Example: '3 4 +' returns 7",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Space-separated RPN expression (e.g., '3 4 +')",
                    },
                    "show_stack": {
                        "type": "boolean",
                        "description": "Return full stack after evaluation",
                        "default": False,
                    },
                },
                "required": ["expression"],
            },
        ),
        Tool(
            name="clear",
            description="Clear the RPN calculator stack",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()  # type: ignore[untyped-decorator]
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "evaluate":
        expression = arguments.get("expression", "")
        show_stack = arguments.get("show_stack", False)
        result = session.evaluate(expression, show_stack)
        if result["error"]:
            return [TextContent(type="text", text=f"Error: {result['error']}")]
        output = f"Result: {result['result']}"
        if show_stack and result["stack"]:
            output += f"\nStack: {result['stack']}"
        return [TextContent(type="text", text=output)]

    elif name == "clear":
        session.clear()
        return [TextContent(type="text", text="Stack cleared")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )
