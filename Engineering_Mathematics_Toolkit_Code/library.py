from sympy import Abs, E, diff, integrate, solve, sympify, symbols


def _prepare_expression(function, variable='x'):
    x = symbols(variable)
    return sympify(function).subs('e', E), x


def valid_function(function):
    if '=' in str(function):
        raise ValueError('Enter a valid function (no "=" allowed).')
    return sympify(function).subs('e', E)


def definite_integral(function, x1, x2, variable='x'):
    function, x = _prepare_expression(function, variable)
    lower = float(sympify(x1).evalf())
    upper = float(sympify(x2).evalf())
    integral = integrate(function, x)
    upper_value = float(sympify(integral.subs(x, upper)).evalf())
    lower_value = float(sympify(integral.subs(x, lower)).evalf())
    return upper_value - lower_value


def area_between_2functions(function1, function2, x1, x2, variable='x'):
    function1, x = _prepare_expression(function1, variable)
    function2 = sympify(function2).subs('e', E)
    lower = float(sympify(x1).evalf())
    upper = float(sympify(x2).evalf())
    if lower > upper:
        lower, upper = upper, lower

    intersections = []
    for point in solve(function1 - function2, x):
        try:
            numeric_point = float(point.evalf())
        except TypeError:
            continue
        if lower <= numeric_point <= upper:
            intersections.append(numeric_point)

    intervals = [lower] + sorted(set(intersections)) + [upper]
    total_area = 0.0
    for start, end in zip(intervals, intervals[1:]):
        area = float(sympify(integrate(Abs(function1 - function2), (x, start, end))).evalf())
        total_area += area
    return total_area


def Tangent_Line(function, point, variable='x'):
    function, x = _prepare_expression(function, variable)
    point = float(sympify(point).evalf())
    derivative = float(sympify(diff(function, x).subs(x, point)).evalf())
    y_val = float(sympify(function.subs(x, point)).evalf())

    if abs(derivative) < 1e-12:
        return f'y = {y_val}'

    intercept = y_val - derivative * point
    if abs(intercept) < 1e-12:
        return f'y = {derivative}x'
    if intercept > 0:
        return f'y = {derivative}x + {intercept}'
    return f'y = {derivative}x - {abs(intercept)}'


def Normal_line(function, point, variable='x'):
    function, x = _prepare_expression(function, variable)
    point = float(sympify(point).evalf())
    derivative = float(sympify(diff(function, x).subs(x, point)).evalf())
    y_val = float(sympify(function.subs(x, point)).evalf())

    if abs(derivative) < 1e-12:
        return f'x = {point}'

    slope = -1 / derivative
    intercept = y_val - slope * point
    if abs(intercept) < 1e-12:
        return f'y = {slope}x'
    if intercept > 0:
        return f'y = {slope}x + {intercept}'
    return f'y = {slope}x - {abs(intercept)}'


def area_between_functions(function1, function2, x1, x2, variable='x'):
    return area_between_2functions(function1, function2, x1, x2, variable)


def tangent_line(function, point, variable='x'):
    return Tangent_Line(function, point, variable)


def normal_line(function, point, variable='x'):
    return Normal_line(function, point, variable)