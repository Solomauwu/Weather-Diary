import json
import os
from typing import List, Optional
from weather_entry import WeatherEntry
from weather_diary import WeatherDiary

class JsonStorage:
    """Handle JSON file operations"""
    
    def __init__(self, filename: str = "weather_data.json"):
        self.filename = filename
    
    def save(self, diary: WeatherDiary) -> bool:
        """Save all entries to JSON file"""
        try:
            data = {
                "entries": diary.to_dict_list(),
                "count": diary.count()
            }
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def load(self) -> Optional[WeatherDiary]:
        """Load entries from JSON file"""
        if not os.path.exists(self.filename):
            return None
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "entries" in data:
                return WeatherDiary.from_dict_list(data["entries"])
            return None
        except Exception as e:
            print(f"Error loading: {e}")
            return None
    
    def export_to_csv(self, diary: WeatherDiary, filename: str = "weather_export.csv"):
        """Export to CSV format"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Temperature (°C)", "Description", "Precipitation (mm)"])
            
            for entry in diary.get_all_entries():
                writer.writerow([
                    entry.date.strftime("%Y-%m-%d"),
                    entry.temperature,
                    entry.description,
                    entry.precipitation
                ])
        return filename