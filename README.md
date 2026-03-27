# mcp-rpn

> MCP server that exposes an RPN calculator

[![PyPI](https://img.shields.io/pypi/v/mcp-rpn.svg)](https://pypi.org/project/mcp-rpn/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-rpn.svg)](https://pypi.org/project/mcp-rpn/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install mcp-rpn
```

## Usage

```bash
mcp-rpn
```

The server uses stdio transport for MCP protocol communication.

## MCP Tools

### evaluate

Evaluate an RPN (Reverse Polish Notation) expression.

```json
{
  "name": "evaluate",
  "arguments": {
    "expression": "3 4 +",
    "show_stack": true
  }
}
```

**Operators:**
- `+` - Add
- `-` - Subtract
- `-` - Multiply
- `/` - Divide
- `**` - Power
- `%` - Modulo

**Commands:**
- `clear` - Clear the stack
- `dup` - Duplicate top of stack
- `swap` - Swap top two elements

**Examples:**
- `3 4 +` returns `7`
- `10 5 2 + * 2 -` returns `32`
- `3 2 /` returns `1.5`

### clear

Clear the calculator stack.

```json
{
  "name": "clear",
  "arguments": {}
}
```

## Development

```bash
git clone https://github.com/daedalus/mcp-rpn.git
cd mcp-rpn
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

## MCP Registry

mcp-name: io.github.daedalus/mcp-rpn
