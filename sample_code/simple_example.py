"""
Sample Python Code: Simple, clean, and low-complexity examples.
Conforms to PEP-8 and clean coding practices.
"""

from typing import List, Optional


def calculate_average(numbers: List[float]) -> float:
    """
    Calculates the arithmetic mean of a list of numbers.
    
    Args:
        numbers: List of numeric values.
        
    Returns:
        The average value or 0.0 if the list is empty.
    """
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def format_user_greeting(username: Optional[str] = None) -> str:
    """
    Generates a personalized welcome message.
    
    Args:
        username: Name of user.
        
    Returns:
        A friendly greeting string.
    """
    if username is None:
        return "Hello, Guest! Welcome to the application."
    cleaned_name = username.strip().capitalize()
    return f"Hello, {cleaned_name}! Welcome back."


class MathUtility:
    """Provides elementary mathematical operations."""

    def __init__(self, precision: int = 2):
        self.precision = precision

    def round_value(self, value: float) -> float:
        """Rounds a float value to the configured precision."""
        return round(value, self.precision)
