# 🔋 Battery Performance Tester

A desktop GUI application that monitors real-time battery and system resource usage of any running application. Perfect for software QA testing to identify battery-intensive applications.

## What This Project Is

The Battery Performance Tester is a Python-based desktop tool that allows you to select any currently running application and monitor its impact on CPU usage, memory consumption, and battery life. The application provides real-time charts and generates detailed performance reports with impact scoring.

## Requirements

- **Python 3.10+**
- Required packages (install with pip):
  ```bash
  pip install psutil customtkinter matplotlib
  ```

## How to Run

1. Clone or download this project to your local machine
2. Navigate to the project directory
3. Install the required dependencies:
   ```bash
   pip install psutil customtkinter matplotlib
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## How to Use

1. **Launch the application** by running `python main.py`
2. **Select a process** from the dropdown list showing all running applications
3. **Click "▶ Start Test"** to begin monitoring the selected application
4. **Watch real-time charts** showing CPU usage, memory usage, and battery level
5. **Click "⏹ Stop Test"** when you want to end the monitoring session
6. **View results** including average/peak metrics and overall impact score
7. **Export reports** to both TXT (human-readable) and CSV (for analysis) formats
8. **Test another app** or close the application

## What the Scores Mean

The application evaluates three metrics and provides an overall impact score:

| Metric | Low Impact | Medium Impact | High Impact |
|--------|------------|---------------|-------------|
| **Average CPU** | < 15% | 15–40% | > 40% |
| **Average Memory** | < 200 MB | 200–500 MB | > 500 MB |
| **Battery Drain** | < 0.5% | 0.5–2% | > 2% |

**Overall Score Logic:**
- 🟢 **Low Impact**: All three metrics are in the "Low" range
- 🔴 **High Impact**: Any metric is "High" OR two metrics are "Medium"
- 🟡 **Medium Impact**: Everything else

## Project Structure

```
battery_tester/
│
├── main.py                  # Entry point — launches the app
├── monitor.py               # Core logic — reads system metrics using psutil
├── scorer.py                # Scoring logic — calculates battery impact rating
├── report.py                # Report generation — exports results to CSV and TXT
├── ui/
│   ├── __init__.py          # Makes ui/ a Python package
│   ├── app_window.py        # Main window: process selector, start/stop, live stats
│   └── chart_panel.py       # The real-time chart component (matplotlib embedded)
├── assets/                  # Reserved for icons or logos (currently empty)
├── reports/                 # Auto-created folder where exported reports are saved
└── README.md                # This file
```

## Known Limitations

- **Battery Reading**: Battery metrics are unavailable on desktop PCs without batteries. In this case, battery-related fields will show "N/A".
- **System Processes**: Some system processes may be inaccessible due to permission restrictions. The application will show an error message if you try to monitor such processes.
- **Process Availability**: If a monitored process closes during testing, the monitoring will stop automatically.
- **Platform**: Tested on Windows and Linux. macOS support should work but hasn't been extensively tested.

## Features

- **Real-time Monitoring**: Live charts update every 2 seconds during testing
- **Process Selection**: Dropdown lists all currently running applications with PIDs
- **Impact Scoring**: Automatic calculation of battery impact based on CPU, memory, and battery usage
- **Report Export**: Generates both human-readable TXT reports and CSV files for data analysis
- **Dark Theme**: Modern, professional dark mode interface
- **Error Handling**: Graceful handling of process termination, access denied, and missing battery sensors

## Troubleshooting

**Application won't start:**
- Ensure Python 3.10+ is installed
- Verify all required packages are installed: `pip install psutil customtkinter matplotlib`

**No processes showing in dropdown:**
- Try clicking "🔄 Refresh List" to reload the process list
- Some systems may require administrator privileges to access all processes

**Battery shows "N/A":**
- This is normal on desktop computers without batteries
- On laptops, ensure battery drivers are properly installed

**Process monitoring fails:**
- The process may have closed after being listed
- Try selecting a different process or refreshing the list
- Some system processes require elevated privileges

## Technical Details

- **Threading**: Uses background threads for monitoring to keep the UI responsive
- **Data Collection**: Polls system metrics every 2 seconds using psutil
- **Chart Rendering**: Embeds matplotlib charts in customtkinter using FigureCanvasTkAgg
- **Report Generation**: Creates timestamped reports in the `reports/` directory
- **Error Recovery**: Handles process termination, access denied, and missing sensors gracefully

## License

This project is provided as-is for educational and testing purposes.
