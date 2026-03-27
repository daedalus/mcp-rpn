from __future__ import annotations

import pytest

from mcp_rpn._core import CalculatorSession, RPNCalculator


@pytest.fixture
def calculator() -> RPNCalculator:
    return RPNCalculator()


@pytest.fixture
def session() -> CalculatorSession:
    return CalculatorSession()
