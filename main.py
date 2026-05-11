#!/usr/bin/env python3
"""
Weather Diary - Console Application for Weather Tracking
Author: Alexey Kuznetsov

A comprehensive weather diary application that allows users to:
- Record daily weather data (temperature, precipitation, description)
- View, filter, and analyze weather records
- Generate temperature trend charts
- Save/load data to JSON format
"""

from diary_controller import DiaryController

def main():
    """Application entry point"""
    print("\n" + "🌸" * 25)
    print("    WEATHER DIARY APPLICATION")
    print("    Track, Analyze, and Visualize Weather Data")
    print("🌸" * 25)
    
    controller = DiaryController()
    controller.run()

if __name__ == "__main__":
    main()