# report.py
# Report generation module for the Battery Performance Tester.
# This module exports test results to both human-readable TXT files and CSV files for further analysis.
# TXT format provides a comprehensive report, while CSV enables data analysis in spreadsheet applications.

import os
import csv
from datetime import datetime
from typing import Dict, List


def generate_report(summary: Dict, score: Dict, readings: Dict) -> str:
    """
    Generate comprehensive test report in both TXT and CSV formats.
    
    Args:
        summary: Summary statistics from BatteryMonitor.get_summary()
        score: Impact scores from scorer.calculate_score()
        readings: Raw data readings with keys 'cpu', 'memory', 'battery', 'timestamps'
        
    Returns:
        Path to the generated TXT report file
    """
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Generate filename with process name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    process_name_safe = _sanitize_filename(summary['process_name'])
    base_filename = f"{process_name_safe}_{timestamp}"
    
    # Generate TXT report (human-readable)
    txt_path = os.path.join('reports', f"{base_filename}.txt")
    _generate_txt_report(txt_path, summary, score, readings)
    
    # Generate CSV report (for data analysis)
    csv_path = os.path.join('reports', f"{base_filename}.csv")
    _generate_csv_report(csv_path, readings)
    
    return txt_path


def _sanitize_filename(filename: str) -> str:
    """
    Remove characters that are invalid in filenames.
    
    Args:
        filename: Original process name
        
    Returns:
        Sanitized filename safe for file system
    """
    # Replace common problematic characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove extra whitespace and limit length
    filename = '_'.join(filename.split())
    return filename[:50]  # Limit to 50 characters


def _generate_txt_report(filepath: str, summary: Dict, score: Dict, readings: Dict):
    """
    Generate a formatted human-readable TXT report.
    
    Args:
        filepath: Path where the TXT report will be saved
        summary: Summary statistics dictionary
        score: Impact scores dictionary
        readings: Raw readings dictionary
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        # Header
        f.write("============================================\n")
        f.write("   BATTERY PERFORMANCE TEST REPORT\n")
        f.write("============================================\n")
        
        # Basic test information
        f.write(f"App Tested     : {summary['process_name']}\n")
        f.write(f"Test Duration  : {summary['duration_seconds']} seconds\n")
        f.write(f"Test Date/Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # System metrics summary
        f.write("--- SYSTEM METRICS SUMMARY ---\n")
        f.write(f"Average CPU Usage  : {summary['avg_cpu']}%\n")
        f.write(f"Peak CPU Usage     : {summary['peak_cpu']}%\n")
        f.write(f"Average Memory     : {summary['avg_memory_mb']} MB\n")
        f.write(f"Peak Memory        : {summary['peak_memory_mb']} MB\n")
        
        # Handle battery data (may be N/A if no battery available)
        if summary['battery_start'] is not None:
            f.write(f"Battery (Start)    : {summary['battery_start']}%\n")
            f.write(f"Battery (End)      : {summary['battery_end']}%\n")
            f.write(f"Battery Drain      : {summary['battery_drain']}%\n")
        else:
            f.write("Battery (Start)    : N/A (No battery detected)\n")
            f.write("Battery (End)      : N/A (No battery detected)\n")
            f.write("Battery Drain      : N/A (No battery detected)\n")
        
        f.write("\n")
        
        # Impact scores
        f.write("--- IMPACT SCORES ---\n")
        f.write(f"CPU Impact     : {score['cpu_score']}\n")
        f.write(f"Memory Impact  : {score['memory_score']}\n")
        f.write(f"Battery Impact : {score['battery_score']}\n")
        f.write(f"OVERALL SCORE  : {score['overall_score']}\n")
        f.write("\n")
        
        # Recommendation
        f.write("--- RECOMMENDATION ---\n")
        f.write(f"{score['recommendation']}\n")
        f.write("\n")
        
        # Raw readings table
        f.write("--- RAW READINGS ---\n")
        f.write("Timestamp   | CPU (%)  | Memory (MB) | Battery (%)\n")
        f.write("----------- | -------- | ----------- | -----------\n")
        
        # Write each reading as a row
        for i in range(len(readings['timestamps'])):
            timestamp = readings['timestamps'][i]
            cpu = readings['cpu'][i]
            memory = readings['memory'][i]
            battery = readings['battery'][i]
            
            # Format battery as "N/A" if None
            battery_str = f"{battery:.1f}" if battery is not None else "N/A"
            
            f.write(f"{timestamp:11} | {cpu:8.1f} | {memory:11.1f} | {battery_str:11}\n")
        
        f.write("============================================\n")


def _generate_csv_report(filepath: str, readings: Dict):
    """
    Generate a CSV file with raw data for further analysis.
    
    Args:
        filepath: Path where the CSV report will be saved
        readings: Raw readings dictionary
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Timestamp', 'CPU (%)', 'Memory (MB)', 'Battery (%)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for i in range(len(readings['timestamps'])):
            row = {
                'Timestamp': readings['timestamps'][i],
                'CPU (%)': readings['cpu'][i],
                'Memory (MB)': readings['memory'][i],
                'Battery (%)': readings['battery'][i] if readings['battery'][i] is not None else 'N/A'
            }
            writer.writerow(row)
