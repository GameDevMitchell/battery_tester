# monitor.py
# Core system monitoring module for the Battery Performance Tester.
# This module contains the BatteryMonitor class that collects real-time CPU, memory, and battery data
# for a specified process using the psutil library.

import psutil
import time
import threading
from datetime import datetime
from typing import List, Dict, Optional


class BatteryMonitor:
    """
    Manages monitoring session for a single target process.
    Collects CPU usage, memory usage, and battery level data over time.
    """
    
    def __init__(self, pid: int, process_name: str):
        """
        Initialize the monitor for a specific process.
        
        Args:
            pid: Process ID of the target application
            process_name: Human-readable name of the process
        """
        self.pid = pid
        self.process_name = process_name
        
        # Lists to store readings over time
        self.cpu_readings: List[float] = []
        self.memory_readings: List[float] = []
        self.battery_readings: List[float] = []
        self.timestamps: List[str] = []
        
        # Control flag for the monitoring loop
        self.is_running = False
        self._monitor_thread: Optional[threading.Thread] = None
        
    def start(self):
        """
        Start monitoring the target process.
        Clears previous readings and begins background data collection.
        Threading is used here to prevent the UI from freezing while data is being collected.
        """
        if self.is_running:
            return
            
        # Clear any previous data
        self.cpu_readings.clear()
        self.memory_readings.clear()
        self.battery_readings.clear()
        self.timestamps.clear()
        
        # Set running flag and start background thread
        self.is_running = True
        self._monitor_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._monitor_thread.start()
        
    def stop(self):
        """
        Stop monitoring the target process.
        Sets the running flag to False, causing the poll loop to exit naturally.
        """
        self.is_running = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
            
    def _poll_loop(self):
        """
        Background thread method that continuously collects system metrics.
        Runs every 2 seconds while self.is_running is True.
        """
        try:
            process = psutil.Process(self.pid)
        except psutil.NoSuchProcess:
            self.is_running = False
            return
            
        while self.is_running:
            try:
                # 1. Read CPU percentage over a 1-second window
                cpu_percent = process.cpu_percent(interval=1)
                
                # 2. Read memory usage in MB (RSS = Resident Set Size - actual physical RAM used)
                memory_mb = process.memory_info().rss / (1024 * 1024)
                
                # 3. Read battery percentage (handle case where no battery is available)
                battery_percent = None
                try:
                    battery = psutil.sensors_battery()
                    if battery:
                        battery_percent = battery.percent
                except (AttributeError, TypeError):
                    # No battery sensor available (common on desktop PCs)
                    pass
                
                # 4. Record current timestamp
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # 5. Store all readings
                self.cpu_readings.append(cpu_percent)
                self.memory_readings.append(memory_mb)
                self.battery_readings.append(battery_percent)
                self.timestamps.append(timestamp)
                
                # 6. Sleep for 2 seconds before next reading
                time.sleep(2)
                
            except psutil.NoSuchProcess:
                # Target process has closed during monitoring
                self.is_running = False
                break
            except (psutil.AccessDenied, psutil.ZombieProcess):
                # Process became inaccessible
                self.is_running = False
                break
                
    def get_summary(self) -> Dict:
        """
        Calculate summary statistics from collected readings.
        
        Returns:
            Dictionary containing averaged metrics, peak values, and test duration
        """
        if not self.cpu_readings:
            # No data collected
            return {
                'process_name': self.process_name,
                'avg_cpu': 0.0,
                'peak_cpu': 0.0,
                'avg_memory_mb': 0.0,
                'peak_memory_mb': 0.0,
                'battery_start': None,
                'battery_end': None,
                'battery_drain': 0.0,
                'duration_seconds': 0,
                'timestamps': []
            }
            
        # Calculate averages and peaks
        avg_cpu = round(sum(self.cpu_readings) / len(self.cpu_readings), 2)
        peak_cpu = max(self.cpu_readings)
        avg_memory_mb = round(sum(self.memory_readings) / len(self.memory_readings), 2)
        peak_memory_mb = max(self.memory_readings)
        
        # Handle battery data (may be None if no battery available)
        battery_start = self.battery_readings[0] if self.battery_readings[0] is not None else None
        battery_end = self.battery_readings[-1] if self.battery_readings[-1] is not None else None
        battery_drain = 0.0
        
        if battery_start is not None and battery_end is not None:
            battery_drain = round(battery_start - battery_end, 2)
            
        # Calculate duration (readings × 2 seconds each)
        duration_seconds = len(self.timestamps) * 2
        
        return {
            'process_name': self.process_name,
            'avg_cpu': avg_cpu,
            'peak_cpu': peak_cpu,
            'avg_memory_mb': avg_memory_mb,
            'peak_memory_mb': peak_memory_mb,
            'battery_start': battery_start,
            'battery_end': battery_end,
            'battery_drain': battery_drain,
            'duration_seconds': duration_seconds,
            'timestamps': self.timestamps.copy()
        }


def get_running_processes() -> List[Dict]:
    """
    Get a list of all currently running processes on the system.
    
    Returns:
        List of dictionaries containing 'pid' and 'name' for each running process.
        Processes are filtered to exclude zombies and dead processes that aren't real targets.
    """
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                # Filter out zombie and dead processes
                if proc.info['status'] in ['running', 'sleeping']:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Skip processes that can't be accessed
                continue
    except Exception:
        # If we can't enumerate processes, return empty list
        pass
        
    # Sort alphabetically by process name for better user experience
    processes.sort(key=lambda x: x['name'].lower())
    return processes
