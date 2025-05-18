def is_non_negative_integer(n):
    """
    Checks if the input is a non-negative integer.
    """
    return isinstance(n, int) and n >= 0

def factorial_base_case(n):
    """
    Handles the base case for factorial calculation (n=0).
    """
    if n == 0:
        return 1
    return None

def factorial_iterative(n):
    """
    Calculates the factorial of a non-negative integer n iteratively.
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def factorial(n):
    """
    Calculates the factorial of a non-negative integer n.
    """
    if not is_non_negative_integer(n):
        raise ValueError("Input must be a non-negative integer.")

    base_case_result = factorial_base_case(n)
    if base_case_result is not None:
        return base_case_result

    return factorial_iterative(n)

if __name__ == "__main__":
    n = int(input())
    print(factorial(n))