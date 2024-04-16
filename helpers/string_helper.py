"""Helper methods for string"""

# pylint: disable=too-few-public-methods
class StringHelper():
    """string helper methods"""

    def is_null_or_whitespace(self, input_str: str):
        """Check if the input string is null or whitespace"""
        return not input_str or input_str.isspace()

# pylint: enable=too-few-public-methods
