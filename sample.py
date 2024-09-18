from datetime import datetime, timedelta
import calendar

def is_within_range(format1, format2):
    # Parse format1: time with timezone info
    time_format1 = datetime.fromisoformat(format1)
    
    # Parse format2: month/day/year
    date_format2 = datetime.strptime(format2, "%m/%d/%Y")
    
    # Calculate the start of the range: 11 months before format2
    year = date_format2.year
    month = date_format2.month
    start_year = year if month > 11 else year - 1
    start_month = (month - 11) if month > 11 else (month + 1)
    
    # Start range: first day of the start month
    start_range = datetime(start_year, start_month, 1)

    # End range: last day of format2's month
    last_day_of_month = calendar.monthrange(year, month)[1]
    end_range = datetime(year, month, last_day_of_month, 23, 59, 59, 999999)
    
    # Check if format1 is within the range
    return start_range <= time_format1 <= end_range

# Example usage:
format1 = "2022-05-01T10:04:15.520000+00:00"  # ISO format
format2 = "4/1/2023"  # MM/DD/YYYY

print(is_within_range(format1, format2))  # Returns True or False
