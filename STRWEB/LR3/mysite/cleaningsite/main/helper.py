# graph/utils.py
from math import pow, log

def power_series(x, eps):
    """Calculating the value of a function by decomposing into a power series."""
    n = 0
    result = 0.0
    sum = 1 / ((2 * n + 1) * pow(x, 2 * n + 1))
    while abs(sum) >= eps:
        result += 2 * sum
        n += 1
        sum = 1 / ((2 * n + 1) * pow(x, 2 * n + 1))

        if n > 500:
            break

    return result, n + 1

def generate_data(x, eps, points=10):
    """Generates data for plotting."""
    x_values = [x + i * 0.1 for i in range(points)]  # Creating x values for plotting
    series_values = []
    math_values = []
    for x_val in x_values:
        series_value, _ = power_series(x_val, eps)
        math_value = log((x_val + 1) / (x_val - 1))  # Using math function for comparison
        series_values.append(series_value)
        math_values.append(math_value)

    return {
        "x_values": x_values,
        "series_values": series_values,
        "math_values": math_values
    }
