from __future__ import annotations

from typing import Iterable

from sympy import E, Symbol, diff, sympify


def _prepare_expression(equation: str, variable: str = 'x'):
    equation = str(equation).strip().replace('^', '**')
    symbol = Symbol(variable)
    locals_map = {variable: symbol, 'e': E}

    if '=' in equation:
        left, right = equation.split('=', 1)
        expression = sympify(left, locals=locals_map) - sympify(right, locals=locals_map)
    else:
        expression = sympify(equation, locals=locals_map)

    return expression, symbol


def _as_real_number(value) -> float:
    numeric = complex(sympify(value).evalf())
    if abs(numeric.imag) > 1e-9:
        raise ValueError('Newton\'s method produced a non-real value.')
    return float(numeric.real)


def newton_method(
    equation: str,
    initial_guess,
    variable: str = 'x',
    tolerance: float = 1e-7,
    max_iterations: int = 50,
):
    expression, symbol = _prepare_expression(equation, variable)
    derivative = diff(expression, symbol)
    current = float(initial_guess)

    for iteration in range(1, max_iterations + 1):
        function_value = _as_real_number(expression.subs(symbol, current))
        derivative_value = _as_real_number(derivative.subs(symbol, current))
        if abs(derivative_value) < 1e-12:
            raise ZeroDivisionError('Derivative was too close to zero for Newton\'s method.')

        next_value = current - function_value / derivative_value
        if abs(next_value - current) <= tolerance:
            return next_value, iteration
        current = next_value

    return current, max_iterations


def find_roots(
    equation: str,
    guesses: Iterable | None = None,
    variable: str = 'x',
    tolerance: float = 1e-7,
    max_iterations: int = 50,
):
    if guesses is None:
        guesses = (-5, -2, 0, 2, 5)

    roots = []
    for guess in guesses:
        try:
            root, iterations = newton_method(
                equation,
                guess,
                variable=variable,
                tolerance=tolerance,
                max_iterations=max_iterations,
            )
        except Exception:
            continue

        if all(abs(root - existing_root) > tolerance * 10 for existing_root, _, _ in roots):
            roots.append((root, guess, iterations))

    return roots
