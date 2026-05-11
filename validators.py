from datetime import datetime
from typing import Tuple, Optional

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_date(date_str: str) -> Optional[datetime]:
        """Validate and parse date string (YYYY-MM-DD)"""
        try:
            date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            # Check if date is not in future
            if date.date() > datetime.now().date():
                return None
            return date
        except ValueError:
            return None
    
    @staticmethod
    def validate_temperature(temp_str: str) -> Optional[float]:
        """Validate temperature value"""
        try:
            temp = float(temp_str.strip())
            if -100 <= temp <= 60:
                return temp
            return None
        except ValueError:
            return None
    
    @staticmethod
    def validate_precipitation(precip_str: str) -> Optional[float]:
        """Validate precipitation value"""
        try:
            precip = float(precip_str.strip())
            if 0 <= precip <= 500:
                return precip
            return None
        except ValueError:
            return None
    
    @staticmethod
    def validate_description(desc_str: str) -> Optional[str]:
        """Validate description"""
        desc = desc_str.strip()
        if desc and len(desc) <= 200:
            return desc
        return None
    
    @staticmethod
    def parse_date_range(range_str: str) -> Tuple[Optional[datetime], Optional[datetime]]:
        """Parse date range input (YYYY-MM-DD to YYYY-MM-DD)"""
        parts = range_str.split("to")
        if len(parts) != 2:
            return None, None
        
        start = Validators.validate_date(parts[0])
        end = Validators.validate_date(parts[1])
        
        if start and end and start <= end:
            return start, end
        return None, None