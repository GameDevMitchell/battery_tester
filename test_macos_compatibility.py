# Test macOS compatibility for the Battery Performance Tester
import psutil
import platform
import sys

def test_platform_compatibility():
    """Test if all required components work on the current platform"""
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python version: {sys.version}")
    print(f"psutil version: {psutil.__version__}\n")
    
    # Test 1: Process enumeration
    print("=== Process Enumeration Test ===")
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                if proc.info['status'] in ['running', 'sleeping']:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        print(f"✓ Found {len(processes)} running processes")
        
        # Show some common macOS apps
        mac_apps = [p for p in processes if any(app in p['name'].lower() for app in ['safari', 'chrome', 'finder', 'spotify', 'code'])]
        if mac_apps:
            print("✓ Found common macOS apps:")
            for app in mac_apps[:5]:
                print(f"  {app['name']} (PID: {app['pid']})")
        else:
            print("ℹ No common macOS apps found (but process enumeration works)")
            
    except Exception as e:
        print(f"✗ Process enumeration failed: {e}")
    
    # Test 2: CPU monitoring
    print("\n=== CPU Monitoring Test ===")
    try:
        # Test CPU percent on current process
        current_process = psutil.Process()
        cpu_percent = current_process.cpu_percent(interval=1)
        print(f"✓ CPU monitoring works: {cpu_percent}%")
    except Exception as e:
        print(f"✗ CPU monitoring failed: {e}")
    
    # Test 3: Memory monitoring
    print("\n=== Memory Monitoring Test ===")
    try:
        current_process = psutil.Process()
        memory_mb = current_process.memory_info().rss / (1024 * 1024)
        print(f"✓ Memory monitoring works: {memory_mb:.1f} MB")
    except Exception as e:
        print(f"✗ Memory monitoring failed: {e}")
    
    # Test 4: Battery monitoring
    print("\n=== Battery Monitoring Test ===")
    try:
        battery = psutil.sensors_battery()
        if battery:
            print(f"✓ Battery monitoring works: {battery.percent}%")
            print(f"  - Power plugged in: {battery.power_plugged}")
        else:
            print("ℹ No battery detected (desktop or virtual machine)")
    except Exception as e:
        print(f"✗ Battery monitoring failed: {e}")
    
    # Test 5: GUI frameworks
    print("\n=== GUI Framework Test ===")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✓ tkinter works")
    except Exception as e:
        print(f"✗ tkinter failed: {e}")
    
    try:
        import customtkinter
        print("✓ customtkinter imports successfully")
    except Exception as e:
        print(f"✗ customtkinter failed: {e}")
    
    # Test 6: Matplotlib
    print("\n=== Matplotlib Test ===")
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        print(f"✓ matplotlib works (backend: {matplotlib.get_backend()})")
    except Exception as e:
        print(f"✗ matplotlib failed: {e}")

if __name__ == "__main__":
    test_platform_compatibility()
