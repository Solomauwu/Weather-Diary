from datetime import datetime
from typing import Optional

class WeatherEntry:
    """Model class for weather record"""
    
    def __init__(self, date: datetime, temperature: float, 
                 description: str, precipitation: float):
        self._date = date
        self._temperature = temperature
        self._description = description
        self._precipitation = precipitation
    
    # Properties with encapsulation
    @property
    def date(self) -> datetime:
        return self._date
    
    @property
    def temperature(self) -> float:
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float):
        if value < -100 or value > 60:
            raise ValueError("Temperature must be between -100°C and +60°C")
        self._temperature = value
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Description cannot be empty")
        self._description = value.strip()
    
    @property
    def precipitation(self) -> float:
        return self._precipitation
    
    @precipitation.setter
    def precipitation(self, value: float):
        if value < 0 or value > 500:
            raise ValueError("Precipitation must be between 0 and 500 mm")
        self._precipitation = value
    
    def to_dict(self) -> dict:
        """Convert entry to dictionary for JSON serialization"""
        return {
            "date": self._date.strftime("%Y-%m-%d"),
            "temperature": self._temperature,
            "description": self._description,
            "precipitation": self._precipitation
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create entry from dictionary"""
        date = datetime.strptime(data["date"], "%Y-%m-%d")
        return cls(date, data["temperature"], data["description"], data["precipitation"])
    
    def __str__(self) -> str:
        return (f"{self._date.strftime('%Y-%m-%d')} | "
                f"Temp: {self._temperature}°C | "
                f"Precip: {self._precipitation}mm | "
                f"{self._description}")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, WeatherEntry):
            return False
        return self._date.date() == other._date.date()