def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def simple_factorial(n):
    if n == 0:
        return 1
    else:
        return n * simple_factorial(n-1)
