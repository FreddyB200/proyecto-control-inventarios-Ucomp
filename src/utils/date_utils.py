"""Date and time utilities."""
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import calendar

class DateUtils:
    """Date and time utilities."""
    
    @staticmethod
    def get_current_date() -> datetime:
        """Get current date and time.
        
        Returns:
            Current datetime object
        """
        return datetime.now()
        
    @staticmethod
    def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
        """Format date to string.
        
        Args:
            date: Datetime object to format
            format_str: Format string
            
        Returns:
            Formatted date string
        """
        return date.strftime(format_str)
        
    @staticmethod
    def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
        """Parse date string to datetime object.
        
        Args:
            date_str: Date string to parse
            format_str: Format string
            
        Returns:
            Parsed datetime object
        """
        return datetime.strptime(date_str, format_str)
        
    @staticmethod
    def get_date_range(
        start_date: datetime,
        end_date: datetime,
        interval: str = "day"
    ) -> List[datetime]:
        """Get list of dates between start and end date.
        
        Args:
            start_date: Start date
            end_date: End date
            interval: Interval type ("day", "week", "month")
            
        Returns:
            List of datetime objects
        """
        dates = []
        current = start_date
        
        while current <= end_date:
            dates.append(current)
            if interval == "day":
                current += timedelta(days=1)
            elif interval == "week":
                current += timedelta(weeks=1)
            elif interval == "month":
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
                    
        return dates
        
    @staticmethod
    def get_month_range(year: int, month: int) -> Tuple[datetime, datetime]:
        """Get start and end dates of a month.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            Tuple of (start_date, end_date)
        """
        start_date = datetime(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        end_date = datetime(year, month, last_day)
        return start_date, end_date
        
    @staticmethod
    def get_quarter_range(year: int, quarter: int) -> Tuple[datetime, datetime]:
        """Get start and end dates of a quarter.
        
        Args:
            year: Year
            quarter: Quarter (1-4)
            
        Returns:
            Tuple of (start_date, end_date)
        """
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2
        start_date = datetime(year, start_month, 1)
        _, last_day = calendar.monthrange(year, end_month)
        end_date = datetime(year, end_month, last_day)
        return start_date, end_date
        
    @staticmethod
    def get_year_range(year: int) -> Tuple[datetime, datetime]:
        """Get start and end dates of a year.
        
        Args:
            year: Year
            
        Returns:
            Tuple of (start_date, end_date)
        """
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        return start_date, end_date
        
    @staticmethod
    def is_weekend(date: datetime) -> bool:
        """Check if date is weekend.
        
        Args:
            date: Date to check
            
        Returns:
            True if weekend, False otherwise
        """
        return date.weekday() >= 5
        
    @staticmethod
    def get_business_days(
        start_date: datetime,
        end_date: datetime
    ) -> List[datetime]:
        """Get list of business days between dates.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            List of business day datetime objects
        """
        dates = []
        current = start_date
        
        while current <= end_date:
            if not DateUtils.is_weekend(current):
                dates.append(current)
            current += timedelta(days=1)
            
        return dates
        
    @staticmethod
    def get_age(birth_date: datetime) -> int:
        """Calculate age from birth date.
        
        Args:
            birth_date: Birth date
            
        Returns:
            Age in years
        """
        today = datetime.now()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (
            today.month == birth_date.month and
            today.day < birth_date.day
        ):
            age -= 1
        return age
        
    @staticmethod
    def get_time_difference(
        start_date: datetime,
        end_date: datetime
    ) -> timedelta:
        """Calculate time difference between dates.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Time difference as timedelta
        """
        return end_date - start_date 