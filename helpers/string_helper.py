"""Helper methods for string"""


def is_null_or_whitespace(input_str: str):
    """Check if the input string is null or whitespace"""
    return not input_str or input_str.isspace()
