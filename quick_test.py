# Quick test to verify chart updates work
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app_window_redesigned import AppWindowRedesigned
from monitor import get_running_processes

def quick_test():
    """Quick test of the redesigned UI"""
    print("Starting quick test of redesigned UI...")
    
    # Create app
    app = AppWindowRedesigned()
    
    # Test process selection
    processes = get_running_processes()
    if processes:
        first_process = processes[0]
        process_name = first_process['name']
        pid = first_process['pid']
        
        print(f"Testing with process: {process_name} (PID: {pid})")
        
        # Set the dropdown
        app.process_var.set(f"{process_name} (PID: {pid})")
        
        # Start monitoring
        print("Starting monitoring...")
        app._start_monitoring()
        
        # Let it run for a few seconds
        import time
        time.sleep(8)
        
        # Stop monitoring
        print("Stopping monitoring...")
        app._stop_monitoring()
        
        # Check if results panel is visible
        print(f"Results panel packed: {app.results_frame.winfo_manager() != ''}")
        
        # Check if export button exists
        print(f"Export button exists: {hasattr(app, 'export_btn')}")
        
    else:
        print("No processes found to test with")
    
    # Don't show the GUI, just test functionality
    app.destroy()
    print("Test completed!")

if __name__ == "__main__":
    quick_test()
