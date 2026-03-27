from hypothesis import Verbosity, given, settings
from hypothesis import strategies as st

from mcp_rpn._core import CalculatorSession, RPNCalculator


class TestRPNCalculator:
    def test_add(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("3 4 +")
        assert result.result == 7
        assert result.error is None

    def test_subtract(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("10 3 -")
        assert result.result == 7
        assert result.error is None

    def test_multiply(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("3 4 *")
        assert result.result == 12
        assert result.error is None

    def test_divide(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("10 2 /")
        assert result.result == 5.0
        assert result.error is None

    def test_divide_float_result(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("3 2 /")
        assert result.result == 1.5
        assert result.error is None

    def test_power(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("2 3 **")
        assert result.result == 8
        assert result.error is None

    def test_modulo(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("10 3 %")
        assert result.result == 1
        assert result.error is None

    def test_complex_expression(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("10 5 2 + * 2 -")
        assert result.result == 68
        assert result.error is None

    def test_empty_expression(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("")
        assert result.error is None

    def test_clear(self, calculator: RPNCalculator) -> None:
        calculator.evaluate("3 4 +")
        result = calculator.evaluate("clear")
        assert result.stack == []
        assert result.error is None

    def test_dup(self, calculator: RPNCalculator) -> None:
        calculator.evaluate("5")
        result = calculator.evaluate("dup")
        assert result.stack == [5, 5]
        assert result.result == 5
        assert result.error is None

    def test_swap(self, calculator: RPNCalculator) -> None:
        calculator.evaluate("3 4")
        result = calculator.evaluate("swap")
        assert result.stack == [4, 3]
        assert result.error is None

    def test_insufficient_operands(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("3 +")
        assert result.error == "Insufficient operands for operation '+'"
        assert result.result is None

    def test_division_by_zero(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("5 0 /")
        assert result.error == "Division by zero"
        assert result.result is None

    def test_invalid_token(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("3 4 $")
        assert result.error == "Invalid token: $"
        assert result.result is None

    def test_negative_numbers(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("-5 3 +")
        assert result.result == -2
        assert result.error is None

    def test_decimal_numbers(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("3.5 2 *")
        assert result.result == 7.0
        assert result.error is None

    def test_large_numbers(self, calculator: RPNCalculator) -> None:
        result = calculator.evaluate("999999999999999 999999999999999 *")
        assert result.result == 999999999999998000000000000001
        assert result.error is None

    def test_get_stack(self, calculator: RPNCalculator) -> None:
        calculator.evaluate("3 4 5")
        assert calculator.get_stack() == [3, 4, 5]

    def test_sequential_operations(self, calculator: RPNCalculator) -> None:
        calculator.evaluate("3 4 +")
        result = calculator.evaluate("5 *")
        assert result.result == 35
        assert calculator.get_stack() == [35]


class TestCalculatorSession:
    def test_evaluate_returns_dict(self, session: CalculatorSession) -> None:
        result = session.evaluate("3 4 +")
        assert isinstance(result, dict)
        assert result["result"] == 7
        assert result["error"] is None

    def test_evaluate_with_show_stack(self, session: CalculatorSession) -> None:
        result = session.evaluate("3 4 +", show_stack=True)
        assert result["result"] == 7
        assert result["stack"] == [7]

    def test_evaluate_without_show_stack(self, session: CalculatorSession) -> None:
        result = session.evaluate("3 4 +", show_stack=False)
        assert result["result"] == 7
        assert result["stack"] is None

    def test_error_result(self, session: CalculatorSession) -> None:
        result = session.evaluate("3 +", show_stack=True)
        assert result["result"] is None
        assert result["error"] == "Insufficient operands for operation '+'"
        assert result["stack"] == [3]

    def test_clear_session(self, session: CalculatorSession) -> None:
        session.evaluate("3 4 +")
        result = session.clear()
        assert result["result"] is None
        assert result["stack"] == []
        assert result["error"] is None


@given(
    st.lists(
        st.one_of(
            st.integers(min_value=-1000, max_value=1000),
            st.floats(
                min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False
            ),
        ),
        min_size=1,
        max_size=20,
    )
)
@settings(verbosity=Verbosity.verbose, max_examples=50)
def test_hypothesis_number_sequence(numbers: list[float | int]) -> None:
    calc = RPNCalculator()
    for num in numbers:
        token = repr(num)
        if token in {"inf", "-inf", "nan"}:
            continue
        result = calc.evaluate(token)
        assert result.error is None
        assert result.result is not None
