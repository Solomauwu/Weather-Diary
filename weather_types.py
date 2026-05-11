from abc import ABC, abstractmethod
from weather_entry import WeatherEntry

class WeatherCondition(ABC):
    """Abstract base class for different weather conditions"""
    
    @abstractmethod
    def get_condition(self, temperature: float, precipitation: float) -> str:
        pass
    
    @abstractmethod
    def get_icon(self) -> str:
        pass

class SunnyWeather(WeatherCondition):
    def get_condition(self, temperature: float, precipitation: float) -> str:
        if precipitation > 0:
            return "Sunny with light rain"
        if temperature > 30:
            return "Hot and Sunny"
        return "Sunny"
    
    def get_icon(self) -> str:
        return "☀️"

class RainyWeather(WeatherCondition):
    def get_condition(self, temperature: float, precipitation: float) -> str:
        if temperature < 0:
            return "Freezing rain"
        if precipitation > 20:
            return "Heavy Rain"
        return "Rainy"
    
    def get_icon(self) -> str:
        return "🌧️"

class SnowyWeather(WeatherCondition):
    def get_condition(self, temperature: float, precipitation: float) -> str:
        if temperature > 0:
            return "Wet snow"
        if precipitation > 10:
            return "Heavy Snowfall"
        return "Snowy"
    
    def get_icon(self) -> str:
        return "❄️"

class CloudyWeather(WeatherCondition):
    def get_condition(self, temperature: float, precipitation: float) -> str:
        if precipitation > 0:
            return "Overcast with drizzle"
        return "Cloudy"
    
    def get_icon(self) -> str:
        return "☁️"

class WeatherClassifier:
    """Factory-like class for weather conditions"""
    
    @staticmethod
    def classify(temperature: float, precipitation: float) -> WeatherCondition:
        if precipitation == 0 and temperature > 15:
            return SunnyWeather()
        elif precipitation > 0 and temperature <= 0:
            return SnowyWeather()
        elif precipitation > 0:
            return RainyWeather()
        else:
            return CloudyWeather()
    
    @staticmethod
    def get_condition_description(temperature: float, precipitation: float) -> str:
        weather = WeatherClassifier.classify(temperature, precipitation)
        return weather.get_condition(temperature, precipitation)
    
    @staticmethod
    def get_icon(temperature: float, precipitation: float) -> str:
        weather = WeatherClassifier.classify(temperature, precipitation)
        return weather.get_icon()