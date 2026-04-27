# ui/app_window.py
# Main application window for the Battery Performance Tester.
# This module contains the AppWindow class that provides the complete GUI interface
# for selecting processes, monitoring system metrics, and displaying results.

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import re
from typing import Optional

from monitor import BatteryMonitor, get_running_processes
from scorer import calculate_score
from report import generate_report
from ui.chart_panel import ChartPanel


class AppWindow(ctk.CTk):
    """
    Main application window that brings together all components of the Battery Performance Tester.
    Provides process selection, real-time monitoring charts, and results display.
    """
    
    def __init__(self):
        """
        Initialize the main application window with dark theme and all UI components.
        """
        super().__init__()
        
        # Window configuration
        self.title("Battery Performance Tester")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize monitoring state
        self.monitor: Optional[BatteryMonitor] = None
        self.update_job = None
        
        # Build the complete UI
        self._build_ui()
        
    def _build_ui(self):
        """
        Build the complete user interface with three main sections:
        1. Top Panel - Process selector and controls
        2. Middle Panel - Live metrics display with charts  
        3. Bottom Panel - Stats summary and export functionality
        """
        # Main container with scrolling
        main_container = ctk.CTkScrollableFrame(self)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # === TOP PANEL - Control Center ===
        self._build_top_panel(main_container)
        
        # === MIDDLE PANEL - Live Monitor ===
        self._build_middle_panel(main_container)
        
        # === BOTTOM PANEL - Results ===
        self._build_bottom_panel(main_container)
        
    def _build_top_panel(self, parent):
        """
        Build the top control panel with process selection and test controls.
        """
        top_frame = ctk.CTkFrame(parent, corner_radius=10)
        top_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            top_frame,
            text="🔋 Battery Performance Tester",
            font=ctk.CTkFont(size=24, weight='bold')
        )
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            top_frame,
            text="Select an app and start monitoring its battery impact",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Process selection frame
        selection_frame = ctk.CTkFrame(top_frame)
        selection_frame.pack(pady=10, padx=10, fill='x')
        
        # Process dropdown
        process_label = ctk.CTkLabel(selection_frame, text="Select Process:")
        process_label.pack(side='left', padx=(10, 5))
        
        self.process_var = tk.StringVar()
        self.process_dropdown = ctk.CTkComboBox(
            selection_frame,
            variable=self.process_var,
            width=250,
            command=self._on_process_select
        )
        self.process_dropdown.pack(side='left', padx=(0, 5))
        
        # Include PID in dropdown entries since multiple processes can have the same name
        self._refresh_process_list()
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            selection_frame,
            text="🔄 Refresh List",
            command=self._refresh_process_list,
            width=100
        )
        refresh_btn.pack(side='left', padx=(0, 10))
        
        # Control buttons frame
        button_frame = ctk.CTkFrame(top_frame)
        button_frame.pack(pady=10)
        
        # Start button (green)
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="▶ Start Test",
            command=self._start_monitoring,
            fg_color='#2ECC71',
            hover_color='#27AE60',
            width=150,
            height=40
        )
        self.start_btn.pack(side='left', padx=10)
        
        # Stop button (red) - disabled initially
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="⏹ Stop Test",
            command=self._stop_monitoring,
            fg_color='#E74C3C',
            hover_color='#C0392B',
            width=150,
            height=40,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=10)
        
    def _build_middle_panel(self, parent):
        """
        Build the middle panel with three real-time charts side by side.
        """
        middle_frame = ctk.CTkFrame(parent, corner_radius=10)
        middle_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Charts container
        charts_container = ctk.CTkFrame(middle_frame)
        charts_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create three ChartPanel instances in a grid layout
        # CPU Chart: blue color
        self.cpu_chart = ChartPanel(charts_container, "CPU Usage (%)", "#00BFFF")
        self.cpu_chart.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Memory Chart: red color
        self.memory_chart = ChartPanel(charts_container, "Memory Usage (MB)", "#FF6B6B")
        self.memory_chart.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        # Battery Chart: green color
        self.battery_chart = ChartPanel(charts_container, "Battery Level (%)", "#50FA7B")
        self.battery_chart.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        
        # Configure grid weights for equal spacing
        charts_container.grid_columnconfigure(0, weight=1)
        charts_container.grid_columnconfigure(1, weight=1)
        charts_container.grid_columnconfigure(2, weight=1)
        charts_container.grid_rowconfigure(0, weight=1)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            middle_frame,
            text="Status: Idle",
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color='#FFB86C'
        )
        self.status_label.pack(pady=(5, 10))
        
    def _build_bottom_panel(self, parent):
        """
        Build the bottom panel for displaying results and export functionality.
        Initially hidden until test completes.
        """
        self.bottom_frame = ctk.CTkFrame(parent, corner_radius=10)
        # Don't pack initially - will be shown after test completes
        
        # Results container
        results_container = ctk.CTkFrame(self.bottom_frame)
        results_container.pack(fill='x', padx=10, pady=10)
        
        # Metric cards frame
        metrics_frame = ctk.CTkFrame(results_container)
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        # Create metric labels (initially empty) - wrap in scrollable frame for small screens
        metrics_scroll = ctk.CTkScrollableFrame(results_container, height=60)
        metrics_scroll.pack(fill='x', pady=(0, 15))
        
        metrics_frame = ctk.CTkFrame(metrics_scroll)
        metrics_frame.pack(fill='x')
        
        self.avg_cpu_label = ctk.CTkLabel(
            metrics_frame,
            text="Avg CPU: --",
            font=ctk.CTkFont(size=14, weight='bold')
        )
        self.avg_cpu_label.pack(side='left', padx=10)
        
        self.peak_cpu_label = ctk.CTkLabel(
            metrics_frame,
            text="Peak CPU: --",
            font=ctk.CTkFont(size=14, weight='bold')
        )
        self.peak_cpu_label.pack(side='left', padx=10)
        
        self.avg_memory_label = ctk.CTkLabel(
            metrics_frame,
            text="Avg Memory: --",
            font=ctk.CTkFont(size=14, weight='bold')
        )
        self.avg_memory_label.pack(side='left', padx=10)
        
        self.battery_drain_label = ctk.CTkLabel(
            metrics_frame,
            text="Battery Drain: --",
            font=ctk.CTkFont(size=14, weight='bold')
        )
        self.battery_drain_label.pack(side='left', padx=10)
        
        # Overall score label
        self.overall_score_label = ctk.CTkLabel(
            results_container,
            text="",
            font=ctk.CTkFont(size=18, weight='bold')
        )
        self.overall_score_label.pack(pady=(0, 8))
        
        # Recommendation label
        self.recommendation_label = ctk.CTkLabel(
            results_container,
            text="",
            font=ctk.CTkFont(size=13),
            wraplength=600,
            justify='center'
        )
        self.recommendation_label.pack(pady=(0, 15))
        
        # Action buttons frame
        action_frame = ctk.CTkFrame(results_container)
        action_frame.pack()
        
        # Export button
        self.export_btn = ctk.CTkButton(
            action_frame,
            text="💾 Export Report",
            command=self._export_report,
            width=150,
            height=40
        )
        self.export_btn.pack(side='left', padx=10)
        
        # Test another app button
        self.reset_btn = ctk.CTkButton(
            action_frame,
            text="🔄 Test Another App",
            command=self._reset_ui,
            width=150,
        )
        self.reset_btn.pack(side='left', padx=10)
        
    def _refresh_process_list(self):
        """
        Refresh dropdown list with currently running processes.
        """
        try:
            processes = get_running_processes()
            process_list = [f"{proc['name']} (PID: {proc['pid']})" for proc in processes]
            self.process_dropdown.configure(values=process_list)
            
            if process_list and not self.process_var.get():
                self.process_dropdown.set(process_list[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh process list: {str(e)}")
            
    def _on_process_select(self, selection):
        """
        Handle process selection from dropdown.
        """
        pass  # Currently no special handling needed
        
    def _start_monitoring(self):
        """
        Start monitoring the selected process.
        """
        try:
            # Get selected process from dropdown
            selected = self.process_var.get()
            if not selected:
                messagebox.showerror("Error", "Please select a process to monitor.")
                return
                
            # Extract PID from selection string using regex
            match = re.search(r'PID: (\d+)', selected)
            if not match:
                messagebox.showerror("Error", "Invalid process selection.")
                return
                
            pid = int(match.group(1))
            process_name = selected.split(' (PID:')[0]
            
            # Create and start monitor
            self.monitor = BatteryMonitor(pid, process_name)
            self.monitor.start()
            
            # Update UI state
            self.status_label.configure(text=f"Status: Monitoring {process_name}...", text_color='#00BFFF')
            self.start_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
            self.process_dropdown.configure(state='disabled')
            
            # Start UI update loop
            self._schedule_ui_update()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            
    def _stop_monitoring(self):
        """
        Stop monitoring and display results.
        """
        try:
            if self.monitor:
                self.monitor.stop()
                
            # Cancel UI update loop
            if self.update_job:
                self.after_cancel(self.update_job)
                self.update_job = None
                
            # Update status
            self.status_label.configure(text="Status: Processing results...", text_color='#FFB86C')
            
            # Display results
            self._display_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
            
    def _schedule_ui_update(self):
        """
        Schedule the next chart update using Tkinter's after() method.
        This is the safe way to update the UI from a timed event without blocking.
        """
        self.update_job = self.after(2000, self._update_charts)
        
    def _update_charts(self):
        """
        Update all three charts with the latest data from the monitor.
        Reschedules itself to run every 2 seconds while monitoring is active.
        """
        if self.monitor and self.monitor.is_running:
            try:
                # Get latest data
                cpu_data = self.monitor.cpu_readings.copy()
                memory_data = self.monitor.memory_readings.copy()
                battery_data = [b if b is not None else 0 for b in self.monitor.battery_readings]
                
                # Update charts
                self.cpu_chart.update_chart(cpu_data, "CPU (%)")
                self.memory_chart.update_chart(memory_data, "Memory (MB)")
                self.battery_chart.update_chart(battery_data, "Battery (%)")
                
                # Schedule next update
                self._schedule_ui_update()
                
            except Exception as e:
                print(f"Error updating charts: {e}")
                self._schedule_ui_update()  # Continue trying
                
    def _display_results(self):
        """
        Calculate and display the test results in the bottom panel.
        """
        try:
            if not self.monitor:
                return
                
            # Get summary and calculate scores
            summary = self.monitor.get_summary()
            
            if summary['duration_seconds'] < 6:
                messagebox.showwarning("Warning", "Not enough data collected. Run the test for at least 6 seconds.")
                self._reset_ui()
                return
                
            score = calculate_score(summary)
            
            # Update metric labels
            self.avg_cpu_label.configure(text=f"Avg CPU: {summary['avg_cpu']}%")
            self.peak_cpu_label.configure(text=f"Peak CPU: {summary['peak_cpu']}%")
            self.avg_memory_label.configure(text=f"Avg Memory: {summary['avg_memory_mb']} MB")
            
            battery_text = f"Battery Drain: {summary['battery_drain']}%" if summary['battery_start'] is not None else "Battery Drain: N/A"
            self.battery_drain_label.configure(text=battery_text)
            
            # Update overall score with appropriate color
            self.overall_score_label.configure(text=score['overall_score'])
            if "Low Impact" in score['overall_score']:
                self.overall_score_label.configure(text_color='#50FA7B')
            elif "High Impact" in score['overall_score']:
                self.overall_score_label.configure(text_color='#E74C3C')
            else:  # Medium Impact
                self.overall_score_label.configure(text_color='#FFB86C')
                
            # Update recommendation
            self.recommendation_label.configure(text=score['recommendation'])
            
            # Store results for export
            self.last_summary = summary
            self.last_score = score
            self.last_readings = {
                'cpu': self.monitor.cpu_readings,
                'memory': self.monitor.memory_readings,
                'battery': self.monitor.battery_readings,
                'timestamps': self.monitor.timestamps
            }
            
            # Show bottom panel
            self.bottom_frame.pack(fill='x', pady=(10, 0))
            
            # Update status
            self.status_label.configure(text="Status: Test completed", text_color='#50FA7B')
            
            # Update button states
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display results: {str(e)}")
            
    def _export_report(self):
        """
        Export the test results to TXT and CSV files.
        """
        try:
            if not hasattr(self, 'last_summary'):
                messagebox.showerror("Error", "No test results to export.")
                return
                
            # Generate report
            txt_path = generate_report(
                self.last_summary,
                self.last_score,
                self.last_readings
            )
            
            messagebox.showinfo("Success", f"Report saved to: {txt_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
            
    def _reset_ui(self):
        """
        Reset the UI to its initial state for testing another app.
        """
        # Hide bottom panel
        self.bottom_frame.pack_forget()
        
        # Reset status
        self.status_label.configure(text="Status: Idle", text_color='#FFB86C')
        
        # Reset button states
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.process_dropdown.configure(state='normal')
        
        # Clear charts
        self.cpu_chart.update_chart([], "CPU (%)")
        self.memory_chart.update_chart([], "Memory (MB)")
        self.battery_chart.update_chart([], "Battery (%)")
        
        # Clear monitor
        self.monitor = None
