# 🔋 Battery Performance Tester — Full Build Prompt
### A detailed architect prompt for Cursor / Windsurf / Windsurf / v0 / any AI code builder

---

## ⚠️ IMPORTANT INSTRUCTIONS FOR THE CODE BUILDER

Before writing a single line of code, read this entire prompt. Every section matters.

- **Every file** must have a comment block at the top explaining what the file does and why it exists.
- **Every function** must have a comment above it explaining: what it does, what its parameters mean, and what it returns.
- **Every major block of logic** (loops, conditionals, calculations) must have an inline comment explaining the thinking — not just *what* it does, but *why*.
- **No magic numbers** — if you write a number like `0.3` or `30`, there must be a comment or a named constant explaining what it represents.
- The goal is that a software engineering student reading this code for the first time can understand EVERYTHING without asking anyone.

---

## 📌 PROJECT OVERVIEW

**Project Name:** Battery Performance Tester
**Type:** Desktop GUI Application
**Language:** Python 3.10+
**Purpose:** A tool that lets a user select any currently-running application on their computer, monitor its real-time impact on battery and system resources, and generate a detailed performance report with a final battery impact score.

This is a **Software QA and Testing** project. Think of it as an automated test harness — the "app under test" is any process the user picks, and the "test metrics" are CPU usage, memory usage, and battery drain.

---

## 🛠️ TECH STACK

| Tool | Purpose |
|---|---|
| `Python 3.10+` | Core language |
| `psutil` | Reading system metrics: CPU, memory, battery |
| `customtkinter` | Modern-looking GUI (better than default Tkinter) |
| `matplotlib` | Drawing real-time charts inside the app |
| `matplotlib.backends.backend_tkagg` | Embedding matplotlib charts into Tkinter/customtkinter |
| `csv` | Built-in — for exporting reports |
| `datetime` | Built-in — for timestamps |
| `threading` | Built-in — to run monitoring in the background without freezing the UI |
| `time` | Built-in — for the polling loop interval |

Install command to include in README:
```
pip install psutil customtkinter matplotlib
```

---

## 📁 FOLDER AND FILE STRUCTURE

```
battery_tester/
│
├── main.py                  # Entry point — launches the app
├── monitor.py               # Core logic — reads system metrics using psutil
├── scorer.py                # Scoring logic — calculates battery impact rating
├── report.py                # Report generation — exports results to CSV and TXT
├── ui/
│   ├── __init__.py          # Makes ui/ a Python package (can be empty)
│   ├── app_window.py        # Main window: process selector, start/stop, live stats
│   └── chart_panel.py       # The real-time chart component (matplotlib embedded)
├── assets/
│   └── (empty for now — reserved for icons or logos if added later)
├── reports/                 # Auto-created folder where exported reports are saved
└── README.md                # Setup and usage instructions
```

Create this entire structure. Every file listed above must exist and be populated.

---

## 🧠 DETAILED MODULE BREAKDOWN

---

### 1. `monitor.py` — The Brain of the Tester

This module is responsible for all system data collection. It uses `psutil` to read live data.

#### What it must contain:

**Class: `BatteryMonitor`**

This class manages the monitoring session for a single target process.

```
Constructor: __init__(self, pid: int, process_name: str)
```
- Accepts a process ID (pid) and the process name as a string
- Initializes empty lists to store readings over time: `cpu_readings`, `memory_readings`, `battery_readings`, `timestamps`
- Sets a flag `self.is_running = False` to track whether monitoring is active

```
Method: start(self)
```
- Sets `self.is_running = True`
- Clears all previous readings (so it's safe to reuse)
- Starts a background thread that calls `self._poll_loop()`
- COMMENT: Explain why threading is needed here (so the UI doesn't freeze while data is being collected)

```
Method: stop(self)
```
- Sets `self.is_running = False`
- This causes the poll loop to exit on its next cycle

```
Method: _poll_loop(self)` (private)
```
- Runs in a background thread
- Uses a `while self.is_running:` loop
- On each iteration (every 2 seconds):
  1. Read CPU percent of the target process using `psutil.Process(self.pid).cpu_percent(interval=1)`
  2. Read memory usage in MB: `psutil.Process(self.pid).memory_info().rss / (1024 * 1024)`
  3. Read battery percentage: `psutil.sensors_battery().percent` — handle the case where `sensors_battery()` returns None (some desktops have no battery)
  4. Record the current timestamp: `datetime.now().strftime("%H:%M:%S")`
  5. Append each value to its corresponding list
  6. Sleep for 2 seconds using `time.sleep(2)`
- COMMENT: Explain what `rss` means (Resident Set Size — actual physical RAM used)
- COMMENT: Explain what `cpu_percent(interval=1)` means (it measures over a 1-second window)
- Wrap the entire loop body in a `try/except psutil.NoSuchProcess` block — if the monitored process closes mid-test, catch the error gracefully and stop the loop

```
Method: get_summary(self) -> dict
```
- Returns a dictionary with:
  - `process_name`: str
  - `avg_cpu`: float — average of `cpu_readings`, rounded to 2 decimal places
  - `peak_cpu`: float — max of `cpu_readings`
  - `avg_memory_mb`: float — average of `memory_readings`
  - `peak_memory_mb`: float — max of `memory_readings`
  - `battery_start`: float — first value in `battery_readings` (or None if unavailable)
  - `battery_end`: float — last value in `battery_readings` (or None if unavailable)
  - `battery_drain`: float — difference between start and end (positive = drained)
  - `duration_seconds`: int — number of readings × 2 (since we poll every 2 seconds)
  - `timestamps`: list — all timestamps recorded

**Standalone function: `get_running_processes() -> list[dict]`**
- Uses `psutil.process_iter(['pid', 'name', 'status'])` to get all running processes
- Filters to only include processes where `status == 'running'` or `status == 'sleeping'`
- Returns a list of dicts, each with `'pid'` and `'name'`
- Sort alphabetically by name
- COMMENT: Explain why we filter by status (zombie and dead processes aren't real targets)
- Wrap in try/except to skip processes that throw `AccessDenied` or `NoSuchProcess`

---

### 2. `scorer.py` — The Scoring Engine

This module takes the summary data from `BatteryMonitor.get_summary()` and produces a human-readable impact score.

#### What it must contain:

**Constants at the top of the file** (with comments explaining each threshold):
```python
# CPU thresholds — average CPU usage that defines impact levels
CPU_LOW_THRESHOLD = 15       # Below 15% average CPU = low impact
CPU_MEDIUM_THRESHOLD = 40    # 15–40% = medium impact
# Above 40% = high impact

# Memory thresholds (in MB)
MEMORY_LOW_THRESHOLD = 200   # Below 200MB = low
MEMORY_MEDIUM_THRESHOLD = 500  # 200–500MB = medium

# Battery drain thresholds (percentage points lost during test)
BATTERY_LOW_THRESHOLD = 0.5   # Less than 0.5% drained = low
BATTERY_MEDIUM_THRESHOLD = 2.0  # 0.5–2% = medium
```

**Function: `calculate_score(summary: dict) -> dict`**
- Takes the summary dict from `get_summary()`
- Scores CPU, memory, and battery drain independently, each as "Low", "Medium", or "High"
- Combines the three into an overall score using this logic:
  - If all three are Low → overall = "🟢 Low Impact"
  - If any one is High OR two are Medium → overall = "🔴 High Impact"
  - Otherwise → overall = "🟡 Medium Impact"
- Returns a dict with:
  - `cpu_score`: "Low" / "Medium" / "High"
  - `memory_score`: "Low" / "Medium" / "High"
  - `battery_score`: "Low" / "Medium" / "High" / "N/A" (if no battery data)
  - `overall_score`: one of the three strings above
  - `recommendation`: a short human-readable recommendation string (see below)

**Recommendation strings** (pick based on overall score):
- Low: "This app is battery-friendly. Safe to run in the background."
- Medium: "This app has moderate battery impact. Avoid running alongside other heavy apps."
- High: "This app is a battery drain. Close it when not actively using it."

---

### 3. `report.py` — The Report Exporter

This module saves the test results to disk after a session ends.

#### What it must contain:

**Function: `generate_report(summary: dict, score: dict, readings: dict) -> str`**
- `summary`: from `BatteryMonitor.get_summary()`
- `score`: from `scorer.calculate_score()`
- `readings`: a dict with keys `'cpu'`, `'memory'`, `'battery'`, `'timestamps'` — the raw lists

- Creates a `reports/` folder if it doesn't already exist using `os.makedirs('reports', exist_ok=True)`
- Generates a filename using the process name and current datetime:
  `reports/{process_name}_{YYYYMMDD_HHMMSS}.txt`
- Writes a formatted `.txt` report with:
  - Header: "BATTERY PERFORMANCE TEST REPORT"
  - App name, test duration, date/time
  - Section: "SYSTEM METRICS SUMMARY" — avg/peak CPU, avg/peak memory, battery start/end/drain
  - Section: "IMPACT SCORES" — CPU score, memory score, battery score, overall score
  - Section: "RECOMMENDATION" — the recommendation string
  - Section: "RAW READINGS" — a table of all timestamps with CPU %, Memory MB, Battery %
- Also saves a `.csv` file with the same name but `.csv` extension:
  - Columns: Timestamp, CPU (%), Memory (MB), Battery (%)
  - One row per reading
- Returns the path of the `.txt` file as a string (so the UI can display it)
- COMMENT: Explain why we save both TXT and CSV — TXT is human-readable, CSV is for further analysis

---

### 4. `ui/chart_panel.py` — The Live Chart Component

This is a reusable UI component that shows a real-time line chart. It embeds a `matplotlib` figure into the `customtkinter` window.

#### What it must contain:

**Class: `ChartPanel`**

- Inherits from `customtkinter.CTkFrame`
- Takes `parent` as the first argument (standard Tkinter/CTk pattern)

```
Constructor: __init__(self, parent, title: str, color: str)
```
- `title`: label shown above the chart (e.g. "CPU Usage (%)")
- `color`: the line color for this chart (e.g. "#00BFFF" for blue, "#FF6B6B" for red, "#50FA7B" for green)
- Creates a `matplotlib.figure.Figure` with a clean, dark-themed style
- Embeds it using `FigureCanvasTkAgg(fig, master=self)`
- Use `plt.style.use('dark_background')` for the chart background
- COMMENT: Explain what `FigureCanvasTkAgg` does (it's a bridge between matplotlib and Tkinter)

```
Method: update_chart(self, data: list, label: str)
```
- Clears the current chart with `ax.clear()`
- Plots `data` as a line using `ax.plot(data, color=self.color, linewidth=2)`
- Sets the y-axis label to `label`
- Adds a subtle grid: `ax.grid(True, alpha=0.3)`
- Calls `self.canvas.draw()` to refresh the visual
- COMMENT: Explain why we call `ax.clear()` before each update (to avoid layering old lines on top)

---

### 5. `ui/app_window.py` — The Main Window

This is the heart of the UI. It brings everything together.

#### Layout (describe this clearly in comments):

The window is divided into three vertical sections:
1. **Top Panel** — Process selector and controls
2. **Middle Panel** — Live metrics display (three charts side by side)
3. **Bottom Panel** — Stats summary and export button

#### What it must contain:

**Class: `AppWindow`**

- Inherits from `customtkinter.CTk` (the main app window class)

```
Constructor: __init__(self)
```
- Sets window title: "Battery Performance Tester"
- Sets window size: `1100 x 700` minimum
- Sets color theme: `customtkinter.set_appearance_mode("dark")`
- Sets CTk color theme: `customtkinter.set_default_color_theme("blue")`
- Calls `self._build_ui()` to create all widgets
- Initializes `self.monitor = None` (will be set when monitoring starts)
- Initializes `self.update_job = None` (for the scheduled UI refresh)

```
Method: _build_ui(self)
```
Builds the full interface. Every widget must have a comment explaining its purpose.

**Top Panel — "Control Center":**
- A label: "🔋 Battery Performance Tester" — large, bold, centered at the top
- A subtitle label: "Select an app and start monitoring its battery impact"
- A dropdown (`CTkComboBox`) listing all running processes from `monitor.get_running_processes()`
  - Format each entry as: "ProcessName (PID: 1234)"
  - COMMENT: Explain why we include the PID (multiple processes can have the same name)
- A "Refresh List" button that re-populates the dropdown
- A "▶ Start Test" button (green) that calls `self._start_monitoring()`
- A "⏹ Stop Test" button (red) that calls `self._stop_monitoring()` — disabled initially

**Middle Panel — "Live Monitor":**
- Three `ChartPanel` instances side by side using a grid layout:
  - CPU Chart: title="CPU Usage (%)", color="#00BFFF"
  - Memory Chart: title="Memory Usage (MB)", color="#FF6B6B"
  - Battery Chart: title="Battery Level (%)", color="#50FA7B"
- A status label beneath the charts: "Status: Idle" — updates to "Monitoring: [app name]..." when running

**Bottom Panel — "Results":**
- Four metric cards in a row (shown after test ends, hidden initially):
  - Avg CPU | Peak CPU | Avg Memory | Battery Drain
- A large score label showing the overall impact score (e.g. "🔴 High Impact")
- A recommendation text label
- A "💾 Export Report" button — calls `self._export_report()`
- A "Test another app" button — resets the UI

```
Method: _start_monitoring(self)
```
- Reads the selected process from the dropdown
- Parses the PID out of the string (e.g. extract `1234` from `"Chrome (PID: 1234)"`)
- Creates a new `BatteryMonitor(pid, name)` instance
- Calls `self.monitor.start()`
- Updates the status label
- Disables the Start button, enables the Stop button
- Starts the live UI update loop by calling `self._schedule_ui_update()`
- COMMENT: Explain the try/except block for handling the case where the process no longer exists

```
Method: _stop_monitoring(self)
```
- Calls `self.monitor.stop()`
- Cancels the UI update loop
- Calls `self._display_results()`

```
Method: _schedule_ui_update(self)
```
- Uses `self.after(2000, self._update_charts)` — schedules `_update_charts` to run every 2 seconds
- COMMENT: Explain why we use `self.after()` instead of a loop — `after()` is Tkinter's safe way to update the UI from a timed event without blocking

```
Method: _update_charts(self)
```
- Reads the latest data from `self.monitor.cpu_readings`, `memory_readings`, `battery_readings`
- Calls `update_chart()` on each of the three ChartPanel instances
- Reschedules itself: `self.update_job = self.after(2000, self._update_charts)`
- Only runs if `self.monitor.is_running` is True

```
Method: _display_results(self)
```
- Gets the summary from `self.monitor.get_summary()`
- Gets the score from `scorer.calculate_score(summary)`
- Populates the four metric cards with values from the summary
- Shows the overall score label with correct color:
  - Green for "Low Impact"
  - Orange/Yellow for "Medium Impact"
  - Red for "High Impact"
- Shows the recommendation text
- Reveals the bottom panel (make it visible)

```
Method: _export_report(self)
```
- Calls `report.generate_report(summary, score, readings)`
- Shows a popup dialog confirming: "Report saved to: reports/appname_datetime.txt"

---

### 6. `main.py` — Entry Point

Simple and clean:

```python
# main.py
# Entry point for the Battery Performance Tester application.
# Run this file to launch the GUI.

from ui.app_window import AppWindow

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
```

- COMMENT: Explain what `if __name__ == "__main__":` means and why it matters
- COMMENT: Explain what `.mainloop()` does (it starts the Tkinter event loop — the app stays open and responsive until the window is closed)

---

## 🎨 UI DESIGN REQUIREMENTS

The app must look professional and modern — not like a default grey Tkinter window from 2005.

- **Theme:** Dark mode using `customtkinter.set_appearance_mode("dark")`
- **Color Palette:**
  - Background: `#1a1a2e` (deep navy)
  - Card surfaces: `#16213e`
  - Accent / Primary: `#0f3460`
  - Highlight: `#e94560` (red-pink for danger/high impact)
  - Success: `#50FA7B`
  - Warning: `#FFB86C`
  - Text: `#eaeaea`
- **Typography:** Use CTk's built-in font scaling. Titles at 24px bold, labels at 14px, stats at 20px bold.
- **Charts:** Use `dark_background` matplotlib style. Line charts only — no bar charts.
- **Spacing:** Add padding of at least 10px around all panels. Cards should have rounded corners (`corner_radius=10` in CTk).
- **Buttons:** Start button is green, Stop button is red. Both should be `CTkButton` with rounded corners.
- **Status indicator:** A colored dot or label that changes color based on state (grey = idle, blue = monitoring, green = complete).

---

## 📊 SCORING LOGIC (Summary)

| Metric | Low | Medium | High |
|---|---|---|---|
| Avg CPU | < 15% | 15–40% | > 40% |
| Avg Memory | < 200 MB | 200–500 MB | > 500 MB |
| Battery Drain | < 0.5% | 0.5–2% | > 2% |

**Overall score:**
- All Low → 🟢 Low Impact
- Any High OR two Mediums → 🔴 High Impact
- Anything else → 🟡 Medium Impact

---

## 📝 REPORT FORMAT (TXT)

```
============================================
   BATTERY PERFORMANCE TEST REPORT
============================================
App Tested     : Google Chrome
Test Duration  : 60 seconds
Test Date/Time : 2025-04-20 14:32:11

--- SYSTEM METRICS SUMMARY ---
Average CPU Usage  : 23.4%
Peak CPU Usage     : 58.1%
Average Memory     : 312.5 MB
Peak Memory        : 410.2 MB
Battery (Start)    : 87.0%
Battery (End)      : 85.2%
Battery Drain      : 1.8%

--- IMPACT SCORES ---
CPU Impact     : Medium
Memory Impact  : Medium
Battery Impact : Medium
OVERALL SCORE  : 🟡 Medium Impact

--- RECOMMENDATION ---
This app has moderate battery impact. Avoid running it alongside other heavy apps.

--- RAW READINGS ---
Timestamp   | CPU (%)  | Memory (MB) | Battery (%)
----------- | -------- | ----------- | -----------
14:32:11    | 22.1     | 308.4       | 87.0
14:32:13    | 25.7     | 315.2       | 87.0
14:32:15    | 19.3     | 312.8       | 86.8
...
============================================
```

---

## 🧪 ERROR HANDLING REQUIREMENTS

Handle all of the following gracefully — with a user-visible error message in the UI (not a crash):

1. User selects a process that has already closed → Show: "Process no longer running. Please select another."
2. No battery detected (desktop PC) → Battery fields show "N/A", battery score shows "N/A", and this is noted in the report.
3. Access denied to a process (system process, elevated privileges required) → Show: "Access denied to this process. Try a user-level application."
4. User clicks "Stop" before any readings are collected → Show: "Not enough data. Run the test for at least 6 seconds."
5. Reports folder cannot be created (permissions issue) → Show a dialog: "Could not save report. Check folder permissions."

---

## 📄 README.md REQUIREMENTS

The README must include:
1. **What this project is** — one short paragraph
2. **Requirements** — Python version, pip install command
3. **How to run** — `python main.py`
4. **How to use** — step-by-step numbered instructions
5. **What the scores mean** — the scoring table
6. **Known limitations** — battery reading is unavailable on desktops, some system processes are inaccessible
7. **Project structure** — a copy of the folder tree shown above

---

## ✅ FINAL CHECKLIST FOR THE CODE BUILDER

Before considering this complete, verify:

- [ ] Every file has a top-level docstring/comment block
- [ ] Every function/method has a comment explaining its purpose, parameters, and return value
- [ ] Every constant has a comment explaining what it represents
- [ ] All 5 error scenarios listed above are handled
- [ ] The app runs from `python main.py` with no errors on Windows and Linux
- [ ] Battery N/A case is handled (no crash on a desktop)
- [ ] Reports are saved to `reports/` folder automatically
- [ ] Live charts update every 2 seconds during a test
- [ ] UI does not freeze during monitoring
- [ ] Start/Stop buttons are correctly enabled/disabled during states
- [ ] README.md is complete and accurate
