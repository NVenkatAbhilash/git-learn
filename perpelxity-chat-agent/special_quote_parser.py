
"""
Special Quote Request Parser

Detects special quote request scenarios and extracts ID and date as JSON.

Usage:
    parser = QuoteRequestParser()
    result = parser.parse_quote_request("Get quote for id 3653 on date Sept 2024")
    # Returns: {'id': 3653, 'effective_date': '202409'}
"""

import re
import json
from datetime import datetime
from dateutil.parser import parse as dateutil_parse
from typing import Dict, Optional, Union


class QuoteRequestParser:
    """
    Parser for special quote request scenarios.

    Handles inputs like:
    - "Get quote for id 3653 on date Sept 2024"
    - "Get quote for 3653 for effective date 2024-09-01"

    Returns JSON format: {'id': 3653, 'effective_date': '202409'}
    """

    def __init__(self):
        # Regex patterns for the special scenarios
        self.special_patterns = [
            # "Get quote for id 3653 on date Sept 2024"
            r"get\s+quote\s+for\s+id\s+(\d+)\s+on\s+date\s+([a-zA-Z]+\s+\d{4}|\d{4}-\d{1,2}-\d{1,2})",

            # "Get quote for 3653 for effective date 2024-09-01"
            r"get\s+quote\s+for\s+(\d+)\s+for\s+effective\s+date\s+(\d{4}-\d{1,2}-\d{1,2})",

            # Additional flexible patterns for similar requests
            r"quote\s+for\s+(?:id\s+)?(\d+)\s+(?:on\s+date\s+|for\s+effective\s+date\s+|on\s+)([a-zA-Z]+\s+\d{4}|\d{4}-\d{1,2}-\d{1,2})"
        ]

        # Compile patterns for case-insensitive matching
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.special_patterns]

    def is_special_quote_scenario(self, user_input: str) -> bool:
        """
        Check if the input matches a special quote scenario.

        Args:
            user_input: User's input string

        Returns:
            True if it's a special quote scenario, False otherwise
        """
        for pattern in self.compiled_patterns:
            if pattern.search(user_input.strip()):
                return True
        return False

    def parse_date_to_yyyymm(self, date_string: str) -> Optional[str]:
        """
        Convert date string to YYYYMM format.

        Args:
            date_string: Date in various formats (e.g., "Sept 2024", "2024-09-01")

        Returns:
            Date in YYYYMM format (e.g., "202409") or None if parsing fails
        """
        try:
            # Use dateutil for flexible date parsing
            parsed_date = dateutil_parse(date_string, fuzzy=True)
            return parsed_date.strftime("%Y%m")
        except:
            return None

    def extract_id_and_date(self, user_input: str) -> Optional[Dict[str, Union[int, str]]]:
        """
        Extract ID and date from special quote scenarios.

        Args:
            user_input: User's input string

        Returns:
            Dictionary with 'id' and 'effective_date' or None if extraction fails
        """
        user_input = user_input.strip()

        # Try each pattern
        for pattern in self.compiled_patterns:
            match = pattern.search(user_input)
            if match:
                id_str, date_str = match.groups()

                # Parse the date to YYYYMM format
                effective_date = self.parse_date_to_yyyymm(date_str)
                if effective_date:
                    return {
                        'id': int(id_str),
                        'effective_date': effective_date
                    }

        return None

    def parse_quote_request(self, user_input: str) -> Optional[Dict[str, Union[int, str]]]:
        """
        Main method to parse quote requests.

        Args:
            user_input: User's natural language input

        Returns:
            Dictionary with extracted info or None if not a special scenario
            Format: {'id': 3653, 'effective_date': '202409'}
        """
        if self.is_special_quote_scenario(user_input):
            return self.extract_id_and_date(user_input)
        return None

    def parse_quote_request_json(self, user_input: str) -> Optional[str]:
        """
        Parse quote request and return as JSON string.

        Args:
            user_input: User's natural language input

        Returns:
            JSON string with extracted info or None if not a special scenario
        """
        result = self.parse_quote_request(user_input)
        if result:
            return json.dumps(result)
        return None


# Example usage and testing
def main():
    """Demonstrate the parser with the user's specific examples."""

    parser = QuoteRequestParser()

    # Test cases from user's request
    test_cases = [
        "Get quote for id 3653 on date Sept 2024",
        "Get quote for 3653 for effective date 2024-09-01",
        "Quote for id 1234 on October 2024",
        "This is not a quote request",  # Should return None
        "Get pricing information"  # Should return None
    ]

    print("Testing Special Quote Request Parser:")
    print("=" * 50)

    for i, test_input in enumerate(test_cases, 1):
        print(f"Test {i}: {test_input}")

        # Check if it's a special scenario
        is_special = parser.is_special_quote_scenario(test_input)
        print(f"Special scenario: {is_special}")

        if is_special:
            # Extract the information
            result = parser.parse_quote_request(test_input)
            if result:
                print(f"Extracted JSON: {json.dumps(result)}")
                print(f"ID: {result['id']}")
                print(f"Effective Date: {result['effective_date']}")
            else:
                print("Failed to extract information")
        else:
            print("Not a special quote scenario")

        print("-" * 30)


# Integration example
def handle_user_message(user_input: str) -> str:
    """
    Example of how to integrate this into your existing system.

    Args:
        user_input: User's message

    Returns:
        Response message
    """
    parser = QuoteRequestParser()

    # Check for special quote scenarios
    if parser.is_special_quote_scenario(user_input):
        quote_data = parser.parse_quote_request(user_input)

        if quote_data:
            # Process the special scenario
            response = f"Special quote scenario detected!\n"
            response += f"ID: {quote_data['id']}\n" 
            response += f"Effective Date: {quote_data['effective_date']}\n"
            response += f"JSON: {json.dumps(quote_data)}"

            # Here you would call your quote processing system
            # e.g., process_quote(quote_data['id'], quote_data['effective_date'])

            return response
        else:
            return "Quote scenario detected but failed to extract details."
    else:
        # Handle as regular message
        return "This is not a special quote scenario."


if __name__ == "__main__":
    main()
