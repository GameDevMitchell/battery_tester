# ui/app_window_redesigned.py
# Spectacular redesigned main application window for Battery Performance Tester
# Features modern design system, gradients, animations, and professional aesthetics

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import re
from typing import Optional

from monitor import BatteryMonitor, get_running_processes
from scorer import calculate_score
from report import generate_report
from ui.enhanced_chart_panel import EnhancedChartPanel
from ui.design_system import DesignSystem


class AppWindowRedesigned(ctk.CTk):
    """
    Spectacular redesigned application window with modern aesthetics
    Professional design system with gradients, animations, and unique styling
    """
    
    def __init__(self):
        """
        Initialize the spectacular redesigned application window
        """
        super().__init__()
        
        # Apply custom design system
        self._apply_theme()
        
        # Window configuration with modern styling
        self.title("🔋 Battery Performance Tester Pro")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Set window icon and transparency effects
        self.attributes('-alpha', 0.98)  # Slight transparency for modern look
        
        # Initialize monitoring state
        self.monitor: Optional[BatteryMonitor] = None
        self.update_job = None
        self.is_monitoring = False
        
        # Build the spectacular UI
        self._build_spectacular_ui()
        
    def _apply_theme(self):
        """Apply custom theme settings"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure custom colors
        self.configure(fg_color=DesignSystem.PRIMARY_DARK)
        
    def _build_spectacular_ui(self):
        """
        Build the spectacular user interface with modern design
        """
        # Main container with gradient background effect
        main_container = ctk.CTkFrame(self, fg_color=DesignSystem.PRIMARY_DARK)
        main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # === HEADER SECTION ===
        self._build_header_section(main_container)
        
        # === CONTROL PANEL ===
        self._build_control_panel(main_container)
        
        # === MONITORING DASHBOARD ===
        self._build_monitoring_dashboard(main_container)
        
        # === RESULTS PANEL ===
        self._build_results_panel(main_container)
        
    def _build_header_section(self, parent):
        """Build spectacular header with gradient effects"""
        header_frame = ctk.CTkFrame(
            parent, 
            fg_color=DesignSystem.PRIMARY_MEDIUM,
            corner_radius=DesignSystem.RADIUS_XL
        )
        header_frame.pack(fill='x', padx=DesignSystem.SPACING_LG, pady=(DesignSystem.SPACING_LG, DesignSystem.SPACING_MD))
        
        # Main title with gradient effect
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(pady=DesignSystem.SPACING_LG)
        
        # Icon and title
        title_row = ctk.CTkFrame(title_container, fg_color="transparent")
        title_row.pack()
        
        # Battery icon with custom styling
        icon_label = ctk.CTkLabel(
            title_row,
            text="⚡",
            font=DesignSystem.get_font("large", "bold"),
            text_color=DesignSystem.ACCENT_PRIMARY
        )
        icon_label.pack(side='left', padx=(0, DesignSystem.SPACING_SM))
        
        # Main title
        title_label = ctk.CTkLabel(
            title_row,
            text="Battery Performance Tester",
            font=DesignSystem.get_font("large", "bold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        title_label.pack(side='left')
        
        # Subtitle with gradient effect
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Professional System Resource Monitoring & Impact Analysis",
            font=DesignSystem.get_font("medium", "medium"),
            text_color=DesignSystem.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, DesignSystem.SPACING_LG))
        
        # Status indicator with modern design
        self.status_container = ctk.CTkFrame(
            header_frame,
            fg_color=DesignSystem.PRIMARY_LIGHT,
            corner_radius=DesignSystem.RADIUS_MEDIUM
        )
        self.status_container.pack(pady=DesignSystem.SPACING_MD)
        
        self.status_dot = ctk.CTkLabel(
            self.status_container,
            text="●",
            font=DesignSystem.get_font("medium"),
            text_color=DesignSystem.STATUS_IDLE
        )
        self.status_dot.pack(side='left', padx=(DesignSystem.SPACING_MD, DesignSystem.SPACING_SM))
        
        self.status_label = ctk.CTkLabel(
            self.status_container,
            text="System Ready",
            font=DesignSystem.get_font("normal", "medium"),
            text_color=DesignSystem.TEXT_SECONDARY
        )
        self.status_label.pack(side='left', padx=(0, DesignSystem.SPACING_MD))
        
    def _build_control_panel(self, parent):
        """Build modern control panel with enhanced styling"""
        control_frame = ctk.CTkFrame(
            parent,
            fg_color=DesignSystem.PRIMARY_MEDIUM,
            corner_radius=DesignSystem.RADIUS_XL
        )
        control_frame.pack(fill='x', padx=DesignSystem.SPACING_LG, pady=DesignSystem.SPACING_MD)
        
        # Process selection section
        selection_container = ctk.CTkFrame(control_frame, fg_color="transparent")
        selection_container.pack(fill='x', padx=DesignSystem.SPACING_LG, pady=DesignSystem.SPACING_LG)
        
        # Section header
        section_header = ctk.CTkLabel(
            selection_container,
            text="🎯 Target Application",
            font=DesignSystem.get_font("medium", "semibold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        section_header.pack(anchor='w', pady=(0, DesignSystem.SPACING_MD))
        
        # Process selection row
        process_row = ctk.CTkFrame(selection_container, fg_color="transparent")
        process_row.pack(fill='x', pady=DesignSystem.SPACING_SM)
        
        # Dropdown with modern styling
        dropdown_container = ctk.CTkFrame(
            process_row,
            fg_color=DesignSystem.PRIMARY_DARK,
            corner_radius=DesignSystem.RADIUS_MEDIUM
        )
        dropdown_container.pack(side='left', fill='x', expand=True, padx=(0, DesignSystem.SPACING_MD))
        
        self.process_var = tk.StringVar()
        self.process_dropdown = ctk.CTkComboBox(
            dropdown_container,
            variable=self.process_var,
            width=400,
            height=40,
            font=DesignSystem.get_font("normal"),
            fg_color=DesignSystem.PRIMARY_DARK,
            border_color=DesignSystem.PRIMARY_ACCENT,
            button_color=DesignSystem.ACCENT_PRIMARY,
            button_hover_color=DesignSystem.ACCENT_SECONDARY,
            text_color=DesignSystem.TEXT_PRIMARY,
            dropdown_text_color=DesignSystem.TEXT_PRIMARY,
            dropdown_fg_color=DesignSystem.PRIMARY_DARK
        )
        self.process_dropdown.pack(fill='x', padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM)
        
        # Refresh button with gradient effect
        refresh_btn = ctk.CTkButton(
            process_row,
            text="🔄",
            font=DesignSystem.get_font("medium"),
            width=50,
            height=40,
            fg_color=DesignSystem.ACCENT_SECONDARY,
            hover_color=DesignSystem.ACCENT_TERTIARY,
            text_color=DesignSystem.TEXT_PRIMARY,
            corner_radius=DesignSystem.RADIUS_MEDIUM,
            command=self._refresh_process_list
        )
        refresh_btn.pack(side='left', padx=DesignSystem.SPACING_SM)
        
        # Control buttons with spectacular styling
        button_container = ctk.CTkFrame(selection_container, fg_color="transparent")
        button_container.pack(fill='x', pady=DesignSystem.SPACING_MD)
        
        # Start button with gradient effect
        self.start_btn = ctk.CTkButton(
            button_container,
            text="▶ START MONITORING",
            font=DesignSystem.get_font("normal", "semibold"),
            width=200,
            height=45,
            fg_color=(DesignSystem.GRADIENT_START, DesignSystem.GRADIENT_END),
            hover_color=(DesignSystem.ACCENT_PRIMARY, DesignSystem.ACCENT_SECONDARY),
            text_color=DesignSystem.TEXT_PRIMARY,
            corner_radius=DesignSystem.RADIUS_MEDIUM,
            command=self._start_monitoring
        )
        self.start_btn.pack(side='left', padx=(0, DesignSystem.SPACING_MD))
        
        # Stop button (disabled initially)
        self.stop_btn = ctk.CTkButton(
            button_container,
            text="⏹ STOP MONITORING",
            font=DesignSystem.get_font("normal", "semibold"),
            width=200,
            height=45,
            fg_color=DesignSystem.GRADIENT_DANGER,
            hover_color=DesignSystem.ACCENT_DANGER,
            text_color=DesignSystem.TEXT_PRIMARY,
            corner_radius=DesignSystem.RADIUS_MEDIUM,
            state='disabled',
            command=self._stop_monitoring
        )
        self.stop_btn.pack(side='left')
        
        # Initialize process list
        self._refresh_process_list()
        
    def _build_monitoring_dashboard(self, parent):
        """Build spectacular monitoring dashboard with enhanced charts"""
        dashboard_frame = ctk.CTkFrame(
            parent,
            fg_color=DesignSystem.PRIMARY_MEDIUM,
            corner_radius=DesignSystem.RADIUS_XL
        )
        dashboard_frame.pack(fill='both', expand=True, padx=DesignSystem.SPACING_LG, pady=DesignSystem.SPACING_MD)
        
        # Dashboard header
        dashboard_header = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
        dashboard_header.pack(fill='x', padx=DesignSystem.SPACING_LG, pady=DesignSystem.SPACING_LG)
        
        header_title = ctk.CTkLabel(
            dashboard_header,
            text="📊 Real-Time Performance Dashboard",
            font=DesignSystem.get_font("medium", "semibold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        header_title.pack(anchor='w')
        
        # Charts container with modern grid layout
        charts_container = ctk.CTkFrame(
            dashboard_frame,
            fg_color=DesignSystem.PRIMARY_DARK,
            corner_radius=DesignSystem.RADIUS_LARGE
        )
        charts_container.pack(fill='both', expand=True, padx=DesignSystem.SPACING_LG, pady=DesignSystem.SPACING_MD)
        
        # Create enhanced chart panels
        self._create_enhanced_charts(charts_container)
        
    def _create_enhanced_charts(self, parent):
        """Create enhanced chart panels with modern styling"""
        # Chart grid configuration
        for i in range(3):
            parent.grid_columnconfigure(i, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # CPU Chart with enhanced styling
        self.cpu_chart = EnhancedChartPanel(
            parent, 
            "CPU USAGE", 
            DesignSystem.ACCENT_PRIMARY,
            "🔥"
        )
        self.cpu_chart.grid(row=0, column=0, padx=DesignSystem.SPACING_MD, pady=DesignSystem.SPACING_MD, sticky='nsew')
        
        # Memory Chart with enhanced styling
        self.memory_chart = EnhancedChartPanel(
            parent,
            "MEMORY USAGE", 
            DesignSystem.ACCENT_TERTIARY,
            "💾"
        )
        self.memory_chart.grid(row=0, column=1, padx=DesignSystem.SPACING_MD, pady=DesignSystem.SPACING_MD, sticky='nsew')
        
        # Battery Chart with enhanced styling
        self.battery_chart = EnhancedChartPanel(
            parent,
            "BATTERY LEVEL",
            DesignSystem.ACCENT_SUCCESS,
            "🔋"
        )
        self.battery_chart.grid(row=0, column=2, padx=DesignSystem.SPACING_MD, pady=DesignSystem.SPACING_MD, sticky='nsew')
        
    def _build_results_panel(self, parent):
        """Build spectacular results panel with modern styling"""
        self.results_frame = ctk.CTkFrame(
            parent,
            fg_color=DesignSystem.PRIMARY_MEDIUM,
            corner_radius=DesignSystem.RADIUS_XL
        )
        # Don't pack initially - will be shown after test completes
        
        # Results container
        results_container = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        results_container.pack(fill='x', padx=DesignSystem.SPACING_LG, pady=DesignSystem.SPACING_LG)
        
        # Results header
        results_header = ctk.CTkLabel(
            results_container,
            text="📈 Performance Analysis Results",
            font=DesignSystem.get_font("medium", "semibold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        results_header.pack(anchor='w', pady=(0, DesignSystem.SPACING_MD))
        
        # Metrics cards with modern styling
        metrics_container = ctk.CTkFrame(
            results_container,
            fg_color=DesignSystem.PRIMARY_DARK,
            corner_radius=DesignSystem.RADIUS_LARGE
        )
        metrics_container.pack(fill='x', pady=DesignSystem.SPACING_MD)
        
        self._create_metric_cards(metrics_container)
        
        # Score display with spectacular styling
        self._create_score_display(results_container)
        
        # Action buttons
        self._create_action_buttons(results_container)
        
    def _create_metric_cards(self, parent):
        """Create modern metric cards"""
        metrics_grid = ctk.CTkFrame(parent, fg_color="transparent")
        metrics_grid.pack(fill='x', padx=DesignSystem.SPACING_MD, pady=DesignSystem.SPACING_MD)
        
        # Configure grid
        for i in range(4):
            metrics_grid.grid_columnconfigure(i, weight=1)
        
        # Create metric cards
        self.avg_cpu_card = MetricCard(metrics_grid, "AVG CPU", "--%", DesignSystem.ACCENT_PRIMARY, "📊")
        self.avg_cpu_card.grid(row=0, column=0, padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM, sticky='ew')
        
        self.peak_cpu_card = MetricCard(metrics_grid, "PEAK CPU", "--%", DesignSystem.ACCENT_WARNING, "⚡")
        self.peak_cpu_card.grid(row=0, column=1, padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM, sticky='ew')
        
        self.avg_memory_card = MetricCard(metrics_grid, "AVG MEMORY", "--MB", DesignSystem.ACCENT_TERTIARY, "💾")
        self.avg_memory_card.grid(row=0, column=2, padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM, sticky='ew')
        
        self.battery_drain_card = MetricCard(metrics_grid, "BATTERY DRAIN", "--%", DesignSystem.ACCENT_SUCCESS, "🔋")
        self.battery_drain_card.grid(row=0, column=3, padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM, sticky='ew')
        
    def _create_score_display(self, parent):
        """Create spectacular score display"""
        score_container = ctk.CTkFrame(
            parent,
            fg_color=DesignSystem.PRIMARY_DARK,
            corner_radius=DesignSystem.RADIUS_LARGE
        )
        score_container.pack(fill='x', pady=DesignSystem.SPACING_MD)
        
        # Overall score label
        self.overall_score_label = ctk.CTkLabel(
            score_container,
            text="",
            font=DesignSystem.get_font("large", "bold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        self.overall_score_label.pack(pady=DesignSystem.SPACING_MD)
        
        # Recommendation label
        self.recommendation_label = ctk.CTkLabel(
            score_container,
            text="",
            font=DesignSystem.get_font("normal"),
            text_color=DesignSystem.TEXT_SECONDARY,
            wraplength=800,
            justify='center'
        )
        self.recommendation_label.pack(pady=(0, DesignSystem.SPACING_MD))
        
    def _create_action_buttons(self, parent):
        """Create modern action buttons"""
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack(pady=DesignSystem.SPACING_MD)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            button_container,
            text="💾 EXPORT REPORT",
            font=DesignSystem.get_font("normal", "semibold"),
            width=180,
            height=40,
            fg_color=DesignSystem.ACCENT_SUCCESS,
            hover_color=DesignSystem.GRADIENT_SUCCESS,
            text_color=DesignSystem.TEXT_PRIMARY,
            corner_radius=DesignSystem.RADIUS_MEDIUM,
            command=self._export_report
        )
        self.export_btn.pack(side='left', padx=DesignSystem.SPACING_SM)
        
        # Reset button
        self.reset_btn = ctk.CTkButton(
            button_container,
            text="🔄 TEST ANOTHER APP",
            font=DesignSystem.get_font("normal", "semibold"),
            width=180,
            height=40,
            fg_color=DesignSystem.ACCENT_SECONDARY,
            hover_color=DesignSystem.ACCENT_TERTIARY,
            text_color=DesignSystem.TEXT_PRIMARY,
            corner_radius=DesignSystem.RADIUS_MEDIUM,
            command=self._reset_ui
        )
        self.reset_btn.pack(side='left', padx=DesignSystem.SPACING_SM)
        
    # === FUNCTIONALITY METHODS ===
    
    def _refresh_process_list(self):
        """Refresh the dropdown list with currently running processes"""
        try:
            processes = get_running_processes()
            process_list = [f"{proc['name']} (PID: {proc['pid']})" for proc in processes]
            self.process_dropdown.configure(values=process_list)
            
            if process_list and not self.process_var.get():
                self.process_dropdown.set(process_list[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh process list: {str(e)}")
            
    def _start_monitoring(self):
        """Start monitoring the selected process with spectacular UI updates"""
        try:
            selected = self.process_var.get()
            if not selected:
                messagebox.showerror("Error", "Please select a process to monitor.")
                return
                
            match = re.search(r'PID: (\d+)', selected)
            if not match:
                messagebox.showerror("Error", "Invalid process selection.")
                return
                
            pid = int(match.group(1))
            process_name = selected.split(' (PID:')[0]
            
            # Create and start monitor
            self.monitor = BatteryMonitor(pid, process_name)
            self.monitor.start()
            self.is_monitoring = True
            
            # Update UI state with spectacular effects
            self._update_ui_for_monitoring(process_name)
            
            # Start UI update loop
            self._schedule_ui_update()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            
    def _update_ui_for_monitoring(self, process_name):
        """Update UI for monitoring state with spectacular effects"""
        # Update status
        self.status_dot.configure(text_color=DesignSystem.STATUS_ACTIVE)
        self.status_label.configure(text=f"Monitoring: {process_name}")
        
        # Update buttons
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.process_dropdown.configure(state='disabled')
        
        # Hide results if visible
        self.results_frame.pack_forget()
        
    def _stop_monitoring(self):
        """Stop monitoring and display spectacular results"""
        try:
            if self.monitor:
                self.monitor.stop()
                
            self.is_monitoring = False
            
            # Cancel UI update loop
            if self.update_job:
                self.after_cancel(self.update_job)
                self.update_job = None
                
            # Update status
            self.status_dot.configure(text_color=DesignSystem.STATUS_SUCCESS)
            self.status_label.configure(text="Analysis Complete")
            
            # Display spectacular results
            self._display_spectacular_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
            
    def _schedule_ui_update(self):
        """Schedule the next chart update"""
        if self.is_monitoring:
            self.update_job = self.after(2000, self._update_charts)
            
    def _update_charts(self):
        """Update charts with latest data"""
        if self.monitor and self.monitor.is_running:
            try:
                # Get latest data
                cpu_data = self.monitor.cpu_readings.copy()
                memory_data = self.monitor.memory_readings.copy()
                battery_data = [b if b is not None else 0 for b in self.monitor.battery_readings]
                
                # Update enhanced charts
                self.cpu_chart.update_chart(cpu_data, "CPU (%)")
                self.memory_chart.update_chart(memory_data, "Memory (MB)")
                self.battery_chart.update_chart(battery_data, "Battery (%)")
                
                # Schedule next update
                self._schedule_ui_update()
                
            except Exception as e:
                print(f"Error updating charts: {e}")
                self._schedule_ui_update()
                
    def _display_spectacular_results(self):
        """Display spectacular results with animations"""
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
            
            # Update metric cards with spectacular animations
            self.avg_cpu_card.update_value(f"{summary['avg_cpu']}%")
            self.peak_cpu_card.update_value(f"{summary['peak_cpu']}%")
            self.avg_memory_card.update_value(f"{summary['avg_memory_mb']} MB")
            
            battery_text = f"{summary['battery_drain']}%" if summary['battery_start'] is not None else "N/A"
            self.battery_drain_card.update_value(battery_text)
            
            # Update overall score with spectacular styling
            self.overall_score_label.configure(text=score['overall_score'])
            if "Low Impact" in score['overall_score']:
                self.overall_score_label.configure(text_color=DesignSystem.ACCENT_SUCCESS)
            elif "High Impact" in score['overall_score']:
                self.overall_score_label.configure(text_color=DesignSystem.ACCENT_DANGER)
            else:  # Medium Impact
                self.overall_score_label.configure(text_color=DesignSystem.ACCENT_WARNING)
                
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
            
            # Show spectacular results panel
            self.results_frame.pack(fill='x', pady=(DesignSystem.SPACING_MD, 0))
            
            # Update button states
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            self.process_dropdown.configure(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display results: {str(e)}")
            
    def _export_report(self):
        """Export the test results"""
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
        """Reset the UI to initial state"""
        # Hide results panel
        self.results_frame.pack_forget()
        
        # Reset status
        self.status_dot.configure(text_color=DesignSystem.STATUS_IDLE)
        self.status_label.configure(text="System Ready")
        
        # Reset button states
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.process_dropdown.configure(state='normal')
        
        # Clear charts
        self.cpu_chart.update_chart([], "CPU (%)")
        self.memory_chart.update_chart([], "Memory (MB)")
        self.battery_chart.update_chart([], "Battery (%)")
        
        # Reset metric cards
        self.avg_cpu_card.update_value("--%")
        self.peak_cpu_card.update_value("--%")
        self.avg_memory_card.update_value("--MB")
        self.battery_drain_card.update_value("--%")
        
        # Clear score
        self.overall_score_label.configure(text="")
        self.recommendation_label.configure(text="")
        
        # Clear monitor
        self.monitor = None
        self.is_monitoring = False


class EnhancedChartPanel(ctk.CTkFrame):
    """Enhanced chart panel with spectacular styling"""
    
    def __init__(self, parent, title: str, color: str, icon: str):
        super().__init__(parent, fg_color=DesignSystem.PRIMARY_MEDIUM, corner_radius=DesignSystem.RADIUS_MEDIUM)
        
        self.title = title
        self.color = color
        self.icon = icon
        
        # Build enhanced chart panel
        self._build_enhanced_panel()
        
    def _build_enhanced_panel(self):
        """Build enhanced chart panel with modern styling"""
        # Header with icon and title
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill='x', padx=DesignSystem.SPACING_MD, pady=(DesignSystem.SPACING_MD, DesignSystem.SPACING_SM))
        
        # Icon
        icon_label = ctk.CTkLabel(
            header,
            text=self.icon,
            font=DesignSystem.get_font("medium"),
            text_color=self.color
        )
        icon_label.pack(side='left', padx=(0, DesignSystem.SPACING_SM))
        
        # Title
        title_label = ctk.CTkLabel(
            header,
            text=self.title,
            font=DesignSystem.get_font("normal", "semibold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        title_label.pack(side='left')
        
        # Chart placeholder (would integrate with actual chart component)
        chart_placeholder = ctk.CTkFrame(
            self,
            fg_color=DesignSystem.PRIMARY_DARK,
            corner_radius=DesignSystem.RADIUS_SMALL,
            height=150
        )
        chart_placeholder.pack(fill='both', expand=True, padx=DesignSystem.SPACING_MD, pady=(0, DesignSystem.SPACING_MD))
        
        # Placeholder text
        placeholder_label = ctk.CTkLabel(
            chart_placeholder,
            text="📊 Chart Display",
            font=DesignSystem.get_font("small"),
            text_color=DesignSystem.TEXT_MUTED
        )
        placeholder_label.pack(expand=True)
        
        # Store placeholder for actual chart updates
        self.chart_widget = chart_placeholder
        
    def update_chart(self, data, label):
        """Update chart with new data"""
        # This would integrate with the actual chart component
        # For now, update placeholder with data info
        if data:
            self.chart_widget.configure(fg_color=self.color)
            for widget in self.chart_widget.winfo_children():
                widget.configure(text=f"📊 {label}: {len(data)} points")


class MetricCard(ctk.CTkFrame):
    """Spectacular metric card with modern styling"""
    
    def __init__(self, parent, title: str, value: str, color: str, icon: str):
        super().__init__(parent, fg_color=DesignSystem.PRIMARY_LIGHT, corner_radius=DesignSystem.RADIUS_MEDIUM)
        
        self.title = title
        self.value = value
        self.color = color
        self.icon = icon
        
        # Build metric card
        self._build_metric_card()
        
    def _build_metric_card(self):
        """Build metric card with modern styling"""
        # Card content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill='both', expand=True, padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM)
        
        # Icon and title row
        header_row = ctk.CTkFrame(content, fg_color="transparent")
        header_row.pack(fill='x')
        
        # Icon
        icon_label = ctk.CTkLabel(
            header_row,
            text=self.icon,
            font=DesignSystem.get_font("small"),
            text_color=self.color
        )
        icon_label.pack(side='left')
        
        # Title
        title_label = ctk.CTkLabel(
            header_row,
            text=self.title,
            font=DesignSystem.get_font("tiny", "medium"),
            text_color=DesignSystem.TEXT_MUTED
        )
        title_label.pack(side='left', padx=(DesignSystem.SPACING_XS, 0))
        
        # Value
        self.value_label = ctk.CTkLabel(
            content,
            text=self.value,
            font=DesignSystem.get_font("medium", "bold"),
            text_color=self.color
        )
        self.value_label.pack(pady=(DesignSystem.SPACING_XS, 0))
        
    def update_value(self, new_value):
        """Update metric value with animation effect"""
        self.value_label.configure(text=new_value)
