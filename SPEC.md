# SPEC.md — mcp-rpn

## Purpose

An MCP server that exposes a Reverse Polish Notation (RPN) calculator. The server accepts expressions in RPN format (e.g., `3 4 +`) and returns the computed result. It maintains a stack per session, allowing sequential operations.

## Scope

### What IS in scope
- RPN expression evaluation with basic arithmetic operators: `+`, `-`, `*`, `/`, `**` (power), `%` (modulo)
- Stack management (push, clear)
- Per-session stack state
- MCP protocol compliance (stdio transport)
- Error handling for invalid expressions, division by zero, empty stack

### What is NOT in scope
- Floating-point precision control
- Scientific functions (sin, cos, log, etc.)
- Complex numbers
- GUI or CLI interface (server-only)

## Public API / Interface

### MCP Tools

#### `evaluate`
Evaluate an RPN expression and optionally return the full stack state.

- **Input**: `expression` (string) - Space-separated RPN expression (e.g., "3 4 +")
- **Input**: `show_stack` (boolean, optional, default: false) - Return full stack after evaluation
- **Returns**: Object with:
  - `result` (number) - The computed result
  - `stack` (array of numbers, optional) - Full stack if `show_stack` is true
  - `error` (string, null) - Error message if evaluation failed

### RPN Operations

| Operator | Symbol | Arity | Description |
|----------|--------|-------|-------------|
| Add | `+` | 2 | Pop a, b; push b + a |
| Subtract | `-` | 2 | Pop a, b; push b - a |
| Multiply | `*` | 2 | Pop a, b; push b * a |
| Divide | `/` | 2 | Pop a, b; push b / a |
| Power | `**` | 2 | Pop a, b; push b ** a |
| Modulo | `%` | 2 | Pop a, b; push b % a |
| Clear | `clear` | 0 | Clear entire stack |
| Dup | `dup` | 1 | Duplicate top of stack |
| Swap | `swap` | 2 | Swap top two elements |

## Edge Cases

1. **Empty expression**: Return 0 or empty stack
2. **Insufficient operands**: Return error "Insufficient operands for operation"
3. **Division by zero**: Return error "Division by zero"
4. **Invalid token**: Return error "Invalid token: {token}"
5. **Stack underflow on clear/dup/swap**: Return appropriate error
6. **Large numbers**: Handle Python's arbitrary precision integers
7. **Non-integer division**: Return float result (e.g., `3 2 /` → 1.5)
8. **Negative numbers**: Support leading minus (e.g., `-5 3 +` → -2)
9. **Decimal numbers**: Support float literals (e.g., `3.5 2 *` → 7.0)

## Performance & Constraints

- O(n) evaluation where n is the number of tokens
- No external dependencies beyond MCP SDK
- Memory usage proportional to stack depth
