from typing import List, Optional
from datetime import datetime
from weather_entry import WeatherEntry

class WeatherDiary:
    """Collection of weather entries with business logic"""
    
    def __init__(self):
        self._entries: List[WeatherEntry] = []
    
    def add_entry(self, entry: WeatherEntry) -> bool:
        """Add weather entry, prevent duplicates for same date"""
        if self.has_entry_on_date(entry.date):
            return False
        
        self._entries.append(entry)
        self._entries.sort(key=lambda x: x.date)
        return True
    
    def remove_entry(self, date: datetime) -> bool:
        """Remove entry by date"""
        for i, entry in enumerate(self._entries):
            if entry.date.date() == date.date():
                del self._entries[i]
                return True
        return False
    
    def get_all_entries(self) -> List[WeatherEntry]:
        """Return all entries sorted by date"""
        return self._entries.copy()
    
    def get_entry_by_date(self, date: datetime) -> Optional[WeatherEntry]:
        """Find entry by exact date"""
        for entry in self._entries:
            if entry.date.date() == date.date():
                return entry
        return None
    
    def has_entry_on_date(self, date: datetime) -> bool:
        """Check if entry exists for date"""
        return self.get_entry_by_date(date) is not None
    
    def filter_by_date_range(self, start_date: datetime, 
                              end_date: datetime) -> List[WeatherEntry]:
        """Filter entries between two dates"""
        return [e for e in self._entries 
                if start_date.date() <= e.date.date() <= end_date.date()]
    
    def filter_by_temperature_range(self, min_temp: float, 
                                     max_temp: float) -> List[WeatherEntry]:
        """Filter entries by temperature range"""
        return [e for e in self._entries 
                if min_temp <= e.temperature <= max_temp]
    
    def get_temperature_data(self) -> tuple:
        """Get dates and temperatures for plotting"""
        dates = [e.date.strftime("%Y-%m-%d") for e in self._entries]
        temperatures = [e.temperature for e in self._entries]
        return dates, temperatures
    
    def clear(self):
        """Remove all entries"""
        self._entries.clear()
    
    def count(self) -> int:
        return len(self._entries)
    
    def to_dict_list(self) -> List[dict]:
        """Convert all entries to dict list for JSON"""
        return [entry.to_dict() for entry in self._entries]
    
    @classmethod
    def from_dict_list(cls, data_list: List[dict]):
        """Create diary from dict list"""
        diary = cls()
        for data in data_list:
            entry = WeatherEntry.from_dict(data)
            diary._entries.append(entry)
        diary._entries.sort(key=lambda x: x.date)
        return diary