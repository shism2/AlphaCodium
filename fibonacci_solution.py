def fibonacci_base_cases(n):
    """
    Handles the base cases for the Fibonacci sequence (n=0 or n=1).
    """
    if n <= 1:
        return n
    return None

def fibonacci_iterative(n):
    """
    Calculates the nth Fibonacci number iteratively.
    """
    a = 0
    b = 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci(n):
    """
    Calculates the nth Fibonacci number.
    """
    base_case_result = fibonacci_base_cases(n)
    if base_case_result is not None:
        return base_case_result
    return fibonacci_iterative(n)

if __name__ == "__main__":
    n = int(input())
    result = fibonacci(n)
    print(result)