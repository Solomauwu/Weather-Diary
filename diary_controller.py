from weather_diary import WeatherDiary
from weather_entry import WeatherEntry
from weather_types import WeatherClassifier
from json_storage import JsonStorage
from console_view import ConsoleView
from datetime import datetime

class DiaryController:
    """Main controller for the application"""
    
    def __init__(self):
        self.diary = WeatherDiary()
        self.storage = JsonStorage()
        self.view = ConsoleView()
    
    def run(self):
        """Main application loop"""
        self.view.show_message("Welcome to Weather Diary! 🌤️")
        
        # Try to load existing data
        self._load_auto()
        
        while True:
            self.view.show_menu()
            choice = input("\nYour choice: ").strip()
            
            if choice == "1":
                self._add_record()
            elif choice == "2":
                self._view_records()
            elif choice == "3":
                self._delete_record()
            elif choice == "4":
                self._filter_by_date()
            elif choice == "5":
                self._filter_by_temperature()
            elif choice == "6":
                self._show_chart()
            elif choice == "7":
                self._save_data()
            elif choice == "8":
                self._load_data()
            elif choice == "9":
                self._show_statistics()
            elif choice == "0":
                self._exit_program()
                break
            else:
                self.view.show_message("Invalid choice! Please try again.", True)
    
    def _add_record(self):
        """Add new weather record"""
        date, temp, description, precip = self.view.get_weather_input()
        
        # Check for existing record on same date
        if self.diary.has_entry_on_date(date):
            self.view.show_message(f"Record for {date.strftime('%Y-%m-%d')} already exists!", True)
            return
        
        # Create and add entry
        entry = WeatherEntry(date, temp, description, precip)
        
        # Get AI-generated weather condition
        condition = WeatherClassifier.get_condition_description(temp, precip)
        icon = WeatherClassifier.get_icon(temp, precip)
        
        if self.diary.add_entry(entry):
            self.view.show_message(f"Record added! {icon} {condition}")
            # Auto-save after adding
            self._save_auto()
        else:
            self.view.show_message("Failed to add record!", True)
    
    def _view_records(self):
        """Display all records"""
        entries = self.diary.get_all_entries()
        self.view.show_records(entries, "All Weather Records")
    
    def _delete_record(self):
        """Delete a record by date"""
        if self.diary.count() == 0:
            self.view.show_message("No records to delete!", True)
            return
        
        date = self.view.get_delete_date()
        
        if self.diary.remove_entry(date):
            self.view.show_message(f"Record for {date.strftime('%Y-%m-%d')} deleted")
            self._save_auto()
        else:
            self.view.show_message(f"No record found for {date.strftime('%Y-%m-%d')}", True)
    
    def _filter_by_date(self):
        """Filter records by date range"""
        start, end = self.view.get_filter_date_range()
        
        if not start or not end:
            self.view.show_message("Invalid date range! Use: YYYY-MM-DD to YYYY-MM-DD", True)
            return
        
        filtered = self.diary.filter_by_date_range(start, end)
        self.view.show_records(filtered, f"Records from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    
    def _filter_by_temperature(self):
        """Filter records by temperature range"""
        min_temp, max_temp = self.view.get_temperature_range()
        
        filtered = self.diary.filter_by_temperature_range(min_temp, max_temp)
        self.view.show_records(filtered, f"Records with temperature {min_temp}°C to {max_temp}°C")
    
    def _show_chart(self):
        """Display temperature chart"""
        entries = self.diary.get_all_entries()
        
        if len(entries) < 2:
            self.view.show_message("Need at least 2 records to create a chart!", True)
            return
        
        dates, temps = self.diary.get_temperature_data()
        self.view.show_chart(dates, temps)
    
    def _show_statistics(self):
        """Display weather statistics"""
        entries = self.diary.get_all_entries()
        self.view.show_statistics(entries)
    
    def _save_data(self):
        """Save data to JSON"""
        if self.storage.save(self.diary):
            self.view.show_message(f"Data saved to {self.storage.filename}")
        else:
            self.view.show_message("Failed to save data!", True)
    
    def _load_data(self):
        """Load data from JSON"""
        loaded = self.storage.load()
        if loaded:
            self.diary = loaded
            self.view.show_message(f"Loaded {self.diary.count()} records from {self.storage.filename}")
        else:
            self.view.show_message("No saved data found!", True)
    
    def _save_auto(self):
        """Auto-save after changes"""
        self.storage.save(self.diary)
    
    def _load_auto(self):
        """Auto-load on startup"""
        loaded = self.storage.load()
        if loaded:
            self.diary = loaded
            print(f"\n📂 Auto-loaded {self.diary.count()} existing records")
    
    def _exit_program(self):
        """Exit the application"""
        if self.diary.count() > 0:
            self._save_auto()
            self.view.show_message("Data saved. Goodbye! 👋")
        else:
            self.view.show_message("Goodbye! 👋")