def factorial(n):
    """
    Calculate the factorial of a non-negative integer n.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n (n!)
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

# Test cases
if __name__ == "__main__":
    test_cases = [
        (5, 120),
        (0, 1),
        (1, 1),
        (10, 3628800)
    ]
    
    for input_val, expected_output in test_cases:
        result = factorial(input_val)
        print(f"factorial({input_val}) = {result}, Expected: {expected_output}, {'✓' if result == expected_output else '✗'}")