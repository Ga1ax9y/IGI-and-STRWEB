from math import pow

def powerSeries(x,eps):
    """Calculating the value of a function by decomposing into a power series.

    Keyword arguments:
    x -- the value of the argument
    eps -- accuracy of calculations

    Return values:
    result -- function value
    n -- iteration number

    """
    n=0
    result = 0.0
    sum = 1/((2*n+1)*pow(x,2*n+1))
    while abs(sum) >= eps:
        result += 2 * sum
        n+=1
        sum = 1/((2*n+1)*pow(x,2*n+1))

        if n > 500:
            break

    return (result, n+1)
