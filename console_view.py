from datetime import datetime
from typing import List, Optional
from weather_entry import WeatherEntry
from weather_types import WeatherClassifier

class ConsoleView:
    """Handle all user interface interactions"""
    
    @staticmethod
    def show_menu():
        print("\n" + "=" * 50)
        print("        🌤️  WEATHER DIARY  🌧️")
        print("=" * 50)
        print("1. ➕ Add weather record")
        print("2. 📋 View all records")
        print("3. 🗑️  Delete record")
        print("4. 🔍 Filter by date range")
        print("5. 🌡️  Filter by temperature")
        print("6. 📊 Show temperature chart")
        print("7. 💾 Save to file")
        print("8. 📂 Load from file")
        print("9. 📈 Show statistics")
        print("0. 🚪 Exit")
        print("-" * 50)
    
    @staticmethod
    def get_weather_input():
        """Get weather data from user with validation"""
        from validators import Validators
        
        print("\n--- New Weather Record ---")
        
        # Date input
        while True:
            date_str = input("Date (YYYY-MM-DD): ")
            date = Validators.validate_date(date_str)
            if date:
                break
            print("❌ Invalid date! Use YYYY-MM-DD format, not in future")
        
        # Temperature input
        while True:
            temp_str = input("Temperature (°C, -100 to +60): ")
            temp = Validators.validate_temperature(temp_str)
            if temp is not None:
                break
            print("❌ Invalid temperature! Must be between -100°C and +60°C")
        
        # Description input
        while True:
            desc = input("Weather description: ")
            description = Validators.validate_description(desc)
            if description:
                break
            print("❌ Description cannot be empty and must be ≤ 200 characters")
        
        # Precipitation input
        while True:
            precip_str = input("Precipitation (mm, 0-500): ")
            precip = Validators.validate_precipitation(precip_str)
            if precip is not None:
                break
            print("❌ Invalid precipitation! Must be between 0 and 500 mm")
        
        return date, temp, description, precip
    
    @staticmethod
    def show_records(entries: List[WeatherEntry], title: str = "Weather Records"):
        """Display list of weather records"""
        if not entries:
            print("\n📭 No records found")
            return
        
        print(f"\n📋 {title}:")
        print("-" * 70)
        
        for i, entry in enumerate(entries, 1):
            # Get weather icon
            icon = WeatherClassifier.get_icon(entry.temperature, entry.precipitation)
            print(f"{i:2}. {icon} {entry}")
        
        print("-" * 70)
        print(f"Total: {len(entries)} records")
    
    @staticmethod
    def show_statistics(entries: List[WeatherEntry]):
        """Display weather statistics"""
        if not entries:
            print("\n📭 No data for statistics")
            return
        
        temps = [e.temperature for e in entries]
        precips = [e.precipitation for e in entries]
        
        print("\n📊 WEATHER STATISTICS")
        print("=" * 40)
        print(f"📅 Period: {entries[0].date.strftime('%Y-%m-%d')} - {entries[-1].date.strftime('%Y-%m-%d')}")
        print(f"📝 Total records: {len(entries)}")
        print(f"🌡️  Average temperature: {sum(temps)/len(temps):.1f}°C")
        print(f"🔥 Highest temperature: {max(temps):.1f}°C")
        print(f"❄️  Lowest temperature: {min(temps):.1f}°C")
        print(f"💧 Average precipitation: {sum(precips)/len(precips):.1f} mm")
        print(f"☔ Total precipitation: {sum(precips):.1f} mm")
    
    @staticmethod
    def show_chart(dates: List[str], temperatures: List[float]):
        """Display temperature chart using matplotlib"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from datetime import datetime
            
            plt.figure(figsize=(12, 6))
            
            # Convert string dates to datetime objects
            date_objects = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
            
            # Create the plot
            plt.plot(date_objects, temperatures, marker='o', linewidth=2, 
                    markersize=8, color='#FF6B6B', label='Temperature')
            
            # Customize the chart
            plt.title('🌡️ Temperature Trend Over Time', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Temperature (°C)', fontsize=12)
            plt.grid(True, alpha=0.3, linestyle='--')
            plt.legend()
            
            # Format x-axis
            plt.gcf().autofmt_xdate()
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            
            # Add horizontal line at 0°C
            plt.axhline(y=0, color='blue', linestyle='--', alpha=0.5, label='Freezing point')
            
            # Fill area under curve
            plt.fill_between(date_objects, temperatures, alpha=0.2, color='#FF6B6B')
            
            # Add value labels
            for i, (date, temp) in enumerate(zip(date_objects, temperatures)):
                plt.annotate(f'{temp}°C', (date, temp), 
                            textcoords="offset points", 
                            xytext=(0, 10), 
                            ha='center',
                            fontsize=9,
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("\n❌ Matplotlib not installed. Install with: pip install matplotlib")
        except Exception as e:
            print(f"\n❌ Error creating chart: {e}")
    
    @staticmethod
    def show_message(message: str, is_error: bool = False):
        """Display message to user"""
        prefix = "❌ ERROR:" if is_error else "✅"
        print(f"\n{prefix} {message}")
    
    @staticmethod
    def get_delete_date():
        """Get date for deletion"""
        from validators import Validators
        
        while True:
            date_str = input("Enter date to delete (YYYY-MM-DD): ")
            date = Validators.validate_date(date_str)
            if date:
                return date
            print("❌ Invalid date format!")
    
    @staticmethod
    def get_filter_date_range():
        """Get date range for filtering"""
        from validators import Validators
        
        print("Enter date range (format: YYYY-MM-DD to YYYY-MM-DD)")
        range_str = input("Example: 2024-01-01 to 2024-12-31\n> ")
        return Validators.parse_date_range(range_str)
    
    @staticmethod
    def get_temperature_range():
        """Get temperature range for filtering"""
        from validators import Validators
        
        while True:
            min_str = input("Min temperature (°C): ")
            min_temp = Validators.validate_temperature(min_str)
            if min_temp is not None:
                break
            print("❌ Invalid temperature!")
        
        while True:
            max_str = input("Max temperature (°C): ")
            max_temp = Validators.validate_temperature(max_str)
            if max_temp is not None and max_temp >= min_temp:
                break
            print(f"❌ Invalid temperature! Must be >= {min_temp}")
        
        return min_temp, max_temp
    
    @staticmethod
    def get_confirmation(prompt: str) -> bool:
        """Get yes/no confirmation"""
        response = input(f"{prompt} (y/n): ").lower().strip()
        return response == 'y' or response == 'yes'