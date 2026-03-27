from dataclasses import dataclass
from typing import Any


@dataclass
class EvaluationResult:
    result: float | int | None
    stack: list[float | int]
    error: str | None


class RPNCalculator:
    def __init__(self) -> None:
        self._stack: list[float | int] = []

    def clear(self) -> None:
        self._stack.clear()

    def get_stack(self) -> list[float | int]:
        return list(self._stack)

    def evaluate(self, expression: str) -> EvaluationResult:
        if not expression.strip():
            return EvaluationResult(
                result=0 if not self._stack else None,
                stack=self.get_stack(),
                error=None,
            )

        tokens = expression.strip().split()

        for token in tokens:
            if self._is_number(token):
                self._stack.append(self._parse_number(token))
            elif token in {"+", "-", "*", "/", "**", "%"}:
                if not self._check_operands(2):
                    return EvaluationResult(
                        result=None,
                        stack=self.get_stack(),
                        error=f"Insufficient operands for operation '{token}'",
                    )
                try:
                    self._apply_binary_op(token)
                except ZeroDivisionError:
                    return EvaluationResult(
                        result=None,
                        stack=self.get_stack(),
                        error="Division by zero",
                    )
            elif token in {"clear", "swap", "dup"}:
                if token == "clear":
                    self.clear()
                elif token == "dup":
                    if not self._check_operands(1):
                        return EvaluationResult(
                            result=None,
                            stack=self.get_stack(),
                            error="Insufficient operands for operation 'dup'",
                        )
                    self._stack.append(self._stack[-1])
                elif token == "swap":
                    if not self._check_operands(2):
                        return EvaluationResult(
                            result=None,
                            stack=self.get_stack(),
                            error="Insufficient operands for operation 'swap'",
                        )
                    self._stack[-2], self._stack[-1] = self._stack[-1], self._stack[-2]
            else:
                return EvaluationResult(
                    result=None,
                    stack=self.get_stack(),
                    error=f"Invalid token: {token}",
                )

        result = self._stack[-1] if self._stack else None
        return EvaluationResult(result=result, stack=self.get_stack(), error=None)

    def _is_number(self, token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _parse_number(self, token: str) -> float | int:
        try:
            value = float(token)
            if value.is_integer() and "." not in token.lower():
                return int(value)
            return value
        except ValueError:
            return float(token)

    def _check_operands(self, count: int) -> bool:
        return len(self._stack) >= count

    def _apply_binary_op(self, op: str) -> None:
        b = self._stack.pop()
        a = self._stack.pop()
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            result = a / b
        elif op == "**":
            result = a**b
        elif op == "%":
            result = a % b
        else:
            raise ValueError(f"Unknown operator: {op}")
        self._stack.append(result)


class CalculatorSession:
    def __init__(self) -> None:
        self._calculator = RPNCalculator()

    def evaluate(self, expression: str, show_stack: bool = False) -> dict[str, Any]:
        result = self._calculator.evaluate(expression)
        if result.error:
            return {
                "result": None,
                "stack": result.stack if show_stack else None,
                "error": result.error,
            }

        return {
            "result": result.result,
            "stack": result.stack if show_stack else None,
            "error": None,
        }

    def clear(self) -> dict[str, Any]:
        self._calculator.clear()
        return {"result": None, "stack": [], "error": None}
