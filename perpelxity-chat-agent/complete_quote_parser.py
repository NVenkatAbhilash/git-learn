
"""
Complete Quote Request Parser with Error Handling

This is the final, production-ready implementation that handles all error scenarios
and provides helpful user prompts when information is missing or invalid.

Key Features:
- Detects missing effective date or quote ID
- Validates formats and provides specific suggestions  
- Returns structured JSON for successful requests
- User-friendly error messages and correction examples

Usage:
    parser = CompleteQuoteParser()
    result = parser.parse_user_input("Get quote for id 3653")
    if result['success']:
        # Process the quote: result['data'] = {'id': 3653, 'effective_date': '202409'}
    else:
        # Show user the error message and suggestions
        print(result['user_message'])
"""

import re
import json
from datetime import datetime
from dateutil.parser import parse as dateutil_parse
from typing import Dict, Optional, Union, List, Tuple


class CompleteQuoteParser:
    """
    Production-ready quote parser with comprehensive error handling.
    """

    def __init__(self):
        # Core patterns for valid requests
        self.valid_patterns = [
            r"get\s+quote\s+for\s+(?:id\s+)?(\d+)\s+(?:on\s+date\s+|on\s+|for\s+effective\s+date\s+)([a-zA-Z]+\s+\d{4}|\d{4}-\d{1,2}-\d{1,2})",
            r"quote\s+for\s+(?:id\s*[:\s]+)?(\d+)[,\s]+(?:(?:date\s*[:\s]+)|(?:on\s+))([a-zA-Z]+\s+\d{4}|\d{4}-\d{1,2}-\d{1,2})"
        ]

        # Valid month names for validation
        self.valid_months = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'jan', 'feb', 'mar', 'apr', 'may', 'jun',
            'jul', 'aug', 'sep', 'sept', 'oct', 'nov', 'dec'
        ]

        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.valid_patterns]

    def parse_user_input(self, user_input: str) -> Dict[str, any]:
        """
        Main method to parse user input with comprehensive error handling.

        Returns:
            {
                'success': bool,
                'data': {'id': int, 'effective_date': str} or None,
                'error_type': str or None,
                'error_message': str,
                'user_message': str,  # Ready-to-show message for user
                'suggestions': [str]
            }
        """
        user_input = user_input.strip()

        # Check if it's a quote request
        if not self._has_quote_intent(user_input):
            return {
                'success': False,
                'data': None,
                'error_type': 'NO_QUOTE_INTENT',
                'error_message': 'Not a quote request',
                'user_message': self._get_no_quote_intent_message(),
                'suggestions': [
                    "Start with 'Get quote for...' or 'Quote for...'",
                    "Example: 'Get quote for id 3653 on date Sept 2024'"
                ]
            }

        # Try to parse complete request
        for pattern in self.compiled_patterns:
            match = pattern.search(user_input)
            if match:
                id_str, date_str = match.groups()
                return self._validate_and_process(id_str, date_str, user_input)

        # Check for partial information
        return self._handle_partial_request(user_input)

    def _has_quote_intent(self, user_input: str) -> bool:
        """Check if user has quote intent"""
        quote_keywords = ['quote', 'quotation', 'pricing', 'get quote']
        return any(keyword in user_input.lower() for keyword in quote_keywords)

    def _validate_and_process(self, id_str: str, date_str: str, original_input: str) -> Dict[str, any]:
        """Validate ID and date, return appropriate response"""

        # Validate ID
        id_valid, id_error = self._validate_id(id_str)
        if not id_valid:
            return {
                'success': False,
                'data': None,
                'error_type': 'INVALID_ID',
                'error_message': id_error,
                'user_message': self._get_invalid_id_message(id_error),
                'suggestions': self._get_id_suggestions()
            }

        # Validate date
        date_valid, date_error, yyyymm = self._validate_date(date_str)
        if not date_valid:
            return {
                'success': False,
                'data': None,
                'error_type': 'INVALID_DATE', 
                'error_message': date_error,
                'user_message': self._get_invalid_date_message(date_error),
                'suggestions': self._get_date_suggestions()
            }

        # Success!
        return {
            'success': True,
            'data': {
                'id': int(id_str),
                'effective_date': yyyymm
            },
            'error_type': None,
            'error_message': '',
            'user_message': self._get_success_message(int(id_str), yyyymm),
            'suggestions': []
        }

    def _validate_id(self, id_str: str) -> Tuple[bool, str]:
        """Validate quote ID"""
        try:
            id_num = int(id_str)
            if id_num < 1000:
                return False, f"Quote ID {id_num} is too short (minimum 4 digits required)"
            if id_num > 999999:
                return False, f"Quote ID {id_num} is too long (maximum 6 digits allowed)"
            return True, ""
        except ValueError:
            return False, f"'{id_str}' is not a valid number"

    def _validate_date(self, date_str: str) -> Tuple[bool, str, Optional[str]]:
        """Validate and parse date"""
        date_str = date_str.strip()

        # Check month name validity for month/year format
        month_year_match = re.match(r'^([a-zA-Z]+)\s+(\d{4})$', date_str, re.IGNORECASE)
        if month_year_match:
            month_name, year = month_year_match.groups()
            if month_name.lower() not in self.valid_months:
                return False, f"'{month_name}' is not a valid month name", None

        try:
            parsed_date = dateutil_parse(date_str, fuzzy=False)
            yyyymm = parsed_date.strftime("%Y%m")

            # Check date reasonableness
            current_date = datetime.now()
            min_date = current_date.replace(year=current_date.year - 2)
            max_date = current_date.replace(year=current_date.year + 3)

            if parsed_date < min_date:
                return False, f"Date {date_str} is too far in the past", None
            if parsed_date > max_date:
                return False, f"Date {date_str} is too far in the future", None

            return True, "", yyyymm
        except:
            return False, f"'{date_str}' is not a valid date format", None

    def _handle_partial_request(self, user_input: str) -> Dict[str, any]:
        """Handle requests with missing information"""

        # Extract potential ID and date
        potential_id = self._extract_id(user_input)
        potential_date = self._extract_date(user_input)

        if potential_id and not potential_date:
            # Has ID, missing date
            id_valid, id_error = self._validate_id(potential_id)
            if not id_valid:
                return {
                    'success': False,
                    'data': None,
                    'error_type': 'INVALID_ID',
                    'error_message': id_error,
                    'user_message': self._get_invalid_id_message(id_error),
                    'suggestions': self._get_id_suggestions()
                }

            return {
                'success': False,
                'data': None,
                'error_type': 'MISSING_DATE',
                'error_message': 'Effective date is missing',
                'user_message': self._get_missing_date_message(potential_id),
                'suggestions': self._get_missing_date_suggestions(potential_id)
            }

        elif potential_date and not potential_id:
            # Has date, missing ID
            return {
                'success': False,
                'data': None,
                'error_type': 'MISSING_ID',
                'error_message': 'Quote ID is missing',
                'user_message': self._get_missing_id_message(potential_date),
                'suggestions': self._get_missing_id_suggestions(potential_date)
            }

        else:
            # Missing both or unclear
            return {
                'success': False,
                'data': None,
                'error_type': 'INCOMPLETE_REQUEST',
                'error_message': 'Missing both quote ID and effective date',
                'user_message': self._get_incomplete_request_message(),
                'suggestions': self._get_complete_format_suggestions()
            }

    def _extract_id(self, text: str) -> Optional[str]:
        """Extract potential ID from text"""
        match = re.search(r'\b(\d{3,6})\b', text)
        return match.group(1) if match else None

    def _extract_date(self, text: str) -> Optional[str]:
        """Extract potential date from text"""
        patterns = [
            r'\b(\d{4}-\d{1,2}-\d{1,2})\b',
            r'\b([a-zA-Z]{3,9}\s+\d{4})\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    # User message generators
    def _get_success_message(self, quote_id: int, effective_date: str) -> str:
        formatted_date = f"{effective_date[:4]}-{effective_date[4:]}"
        return f"Perfect! Quote request received for ID {quote_id} with effective date {formatted_date}. Processing now..."

    def _get_missing_date_message(self, quote_id: str) -> str:
        return f"I found your quote ID {quote_id}, but you forgot to specify the effective date. Please add the date to your request."

    def _get_missing_id_message(self, date_str: str) -> str:
        return f"I found the date {date_str}, but you forgot to specify the quote ID. Please add the quote ID to your request."

    def _get_invalid_id_message(self, error: str) -> str:
        return f"There's an issue with the quote ID: {error}. Please provide a valid quote ID."

    def _get_invalid_date_message(self, error: str) -> str:
        return f"There's an issue with the date: {error}. Please provide a valid date."

    def _get_incomplete_request_message(self) -> str:
        return "I can see you want a quote, but I need both the quote ID and effective date. Please provide both pieces of information."

    def _get_no_quote_intent_message(self) -> str:
        return "This doesn't appear to be a quote request. If you need a quote, please specify the quote ID and effective date."

    # Suggestion generators
    def _get_missing_date_suggestions(self, quote_id: str) -> List[str]:
        return [
            f"Try: 'Get quote for id {quote_id} on date Sept 2024'",
            f"Or: 'Quote for {quote_id} for effective date 2024-09-01'",
            f"Or: 'Quote for {quote_id} on October 2024'"
        ]

    def _get_missing_id_suggestions(self, date_str: str) -> List[str]:
        return [
            f"Try: 'Get quote for id 3653 on {date_str}'",
            f"Or: 'Quote for 4567 on {date_str}'",
            "Quote IDs should be 4-6 digits long"
        ]

    def _get_id_suggestions(self) -> List[str]:
        return [
            "Quote IDs must be 4-6 digits (e.g., 1234, 53267, 123456)",
            "Try: 'Get quote for id 3653 on date Sept 2024'",
            "Or: 'Quote for 12345 for effective date 2024-09-01'"
        ]

    def _get_date_suggestions(self) -> List[str]:
        return [
            "Use month/year format: 'Sept 2024', 'October 2024'",
            "Or full date: '2024-09-01', '2024-10-15'",
            "Try: 'Get quote for id 3653 on date Sept 2024'"
        ]

    def _get_complete_format_suggestions(self) -> List[str]:
        return [
            "Format 1: 'Get quote for id [ID] on date [MONTH YEAR]'",
            "Example: 'Get quote for id 3653 on date Sept 2024'",
            "",
            "Format 2: 'Get quote for [ID] for effective date [YYYY-MM-DD]'",
            "Example: 'Get quote for 3653 for effective date 2024-09-01'",
            "",
            "Quote IDs: 4-6 digits | Dates: Month/Year or YYYY-MM-DD"
        ]


def demonstrate_error_handling():
    """Demonstrate all error handling scenarios"""

    parser = CompleteQuoteParser()

    test_cases = [
        # Valid cases
        ("Get quote for id 3653 on date Sept 2024", "✅ VALID"),
        ("Quote for 4567 for effective date 2024-09-01", "✅ VALID"),

        # Missing information
        ("Get quote for id 3653", "❌ MISSING DATE"),
        ("Quote for October 2024", "❌ MISSING ID"),
        ("I need a quote", "❌ INCOMPLETE"),

        # Invalid formats
        ("Get quote for id 123 on Sept 2024", "❌ INVALID ID (too short)"),
        ("Quote for 3653 on Blah 2024", "❌ INVALID DATE (bad month)"),
        ("Quote for 3653 on Sept 2020", "❌ INVALID DATE (too old)"),

        # No quote intent
        ("Hello there", "❌ NOT A QUOTE REQUEST")
    ]

    print("🧪 COMPREHENSIVE ERROR HANDLING DEMONSTRATION")
    print("=" * 55)

    for i, (test_input, expected_type) in enumerate(test_cases, 1):
        print(f"\n{i:2d}. {expected_type}")
        print(f"    Input: '{test_input}'")

        result = parser.parse_user_input(test_input)

        if result['success']:
            print(f"    ✅ SUCCESS: {json.dumps(result['data'])}")
        else:
            print(f"    ❌ ERROR: {result['error_type']}")
            print(f"    💬 Message: {result['user_message']}")
            if result['suggestions']:
                print(f"    💡 Suggestions:")
                for suggestion in result['suggestions'][:2]:  # Show first 2
                    print(f"       • {suggestion}")
        print("-" * 50)


if __name__ == "__main__":
    demonstrate_error_handling()
