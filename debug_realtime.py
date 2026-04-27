# Debug script to test real-time chart updates
import time
import threading
from ui.app_window_redesigned import AppWindowRedesigned
from monitor import BatteryMonitor

def test_realtime_charts():
    """Test real-time chart updates with actual monitoring"""
    print("Testing real-time chart updates...")
    
    # Create the app
    app = AppWindowRedesigned()
    
    # Simulate monitoring with fake data
    print("Starting simulated monitoring...")
    
    # Create a fake monitor for testing
    class FakeMonitor:
        def __init__(self):
            self.cpu_readings = []
            self.memory_readings = []
            self.battery_readings = []
            self.timestamps = []
            self.is_running = False
            
        def start(self):
            self.is_running = True
            self.cpu_readings = []
            self.memory_readings = []
            self.battery_readings = []
            self.timestamps = []
            
            # Start data generation in background thread
            threading.Thread(target=self._generate_data, daemon=True).start()
            
        def stop(self):
            self.is_running = False
            
        def _generate_data(self):
            """Generate fake data every 2 seconds"""
            import random
            from datetime import datetime
            
            for i in range(10):  # Generate 10 data points
                if not self.is_running:
                    break
                    
                # Generate fake data
                cpu = random.uniform(5, 25)
                memory = random.uniform(100, 200)
                battery = random.uniform(80, 90)
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                self.cpu_readings.append(cpu)
                self.memory_readings.append(memory)
                self.battery_readings.append(battery)
                self.timestamps.append(timestamp)
                
                print(f"Generated data point {i+1}: CPU={cpu:.1f}%, Memory={memory:.1f}MB, Battery={battery:.1f}%")
                time.sleep(2)
    
    # Create and start fake monitor
    fake_monitor = FakeMonitor()
    app.monitor = fake_monitor
    app.is_monitoring = True
    
    # Update UI state
    app._update_ui_for_monitoring("Test Process")
    
    # Start UI updates
    def update_loop():
        """Update charts with fake data"""
        for i in range(10):  # Update for 20 seconds
            if not app.is_monitoring:
                break
                
            print(f"Updating charts with {len(fake_monitor.cpu_readings)} data points...")
            
            # Update charts
            app.cpu_chart.update_chart(fake_monitor.cpu_readings.copy(), "CPU (%)")
            app.memory_chart.update_chart(fake_monitor.memory_readings.copy(), "Memory (MB)")
            app.battery_chart.update_chart(fake_monitor.battery_readings.copy(), "Battery (%)")
            
            # Update status
            app.status_label.configure(text=f"Monitoring: {len(fake_monitor.cpu_readings)} data points")
            
            time.sleep(2)
    
    # Start update loop in background
    update_thread = threading.Thread(target=update_loop, daemon=True)
    update_thread.start()
    
    # Start fake monitoring
    fake_monitor.start()
    
    # Show the app for testing
    print("App is running with simulated data. Close the window to stop.")
    app.mainloop()

if __name__ == "__main__":
    test_realtime_charts()
