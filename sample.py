from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def is_format1_in_range(format1_str, format2_str):
    # Parse format1 (e.g., "2024-05-17 14:05:56.333000 UTC")
    format1 = datetime.strptime(format1_str, "%Y-%m-%d %H:%M:%S.%f UTC")
    
    # Parse format2 (e.g., "4/1/2023")
    format2 = datetime.strptime(format2_str, "%m/%d/%Y")
    
    # Calculate the range:
    # 11 months before format2 (start of range)
    start_range = format2 - relativedelta(months=11)
    
    # End of range is the last day of the month of format2
    end_range = format2.replace(day=1) + relativedelta(months=1) - timedelta(days=1)
    
    # Check if format1 is within the range
    return start_range <= format1 <= end_range

# Test the function
format1_str = "2024-05-17 14:05:56.333000 UTC"
format2_str = "4/1/2023"  # month/day/year
result = is_format1_in_range(format1_str, format2_str)

print("Is format1 in range:", result)
