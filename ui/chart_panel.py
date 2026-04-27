# ui/chart_panel.py
# Real-time chart component for the Battery Performance Tester GUI.
# This module provides a reusable ChartPanel class that displays live line charts
# embedded in the customtkinter interface using matplotlib.

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
from typing import List


class ChartPanel(ctk.CTkFrame):
    """
    A reusable UI component that displays a real-time line chart.
    Embeds a matplotlib figure into a customtkinter frame for live data visualization.
    """
    
    def __init__(self, parent, title: str, color: str):
        """
        Initialize the chart panel with title and line color.
        
        Args:
            parent: Parent widget (typically the main window or another frame)
            title: Label displayed above the chart (e.g., "CPU Usage (%)")
            color: Line color for the chart (e.g., "#00BFFF" for blue)
        """
        super().__init__(parent)
        
        self.title = title
        self.color = color
        
        # Set up matplotlib with dark theme
        mplstyle.use('dark_background')
        
        # Create the matplotlib figure and axis with responsive sizing
        self.fig = Figure(figsize=(3.5, 2.5), dpi=100, facecolor='#1a1a2e')
        self.ax = self.fig.add_subplot(111)
        
        # Embed the matplotlib figure in the tkinter frame
        # FigureCanvasTkAgg is the bridge between matplotlib and Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add title label above the chart
        self.title_label = ctk.CTkLabel(
            self, 
            text=title, 
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color='#eaeaea'
        )
        self.title_label.pack(pady=(10, 5))
        
        # Initialize empty chart
        self._initialize_chart()
        
    def _initialize_chart(self):
        """
        Set up the initial empty chart with proper styling.
        """
        self.ax.clear()
        self.ax.set_facecolor('#16213e')
        self.fig.patch.set_facecolor('#1a1a2e')
        
        # Set initial empty data
        self.ax.plot([], [], color=self.color, linewidth=2)
        
        # Style the chart
        self.ax.grid(True, alpha=0.3, color='#444444')
        self.ax.spines['bottom'].set_color('#666666')
        self.ax.spines['top'].set_color('#666666')
        self.ax.spines['left'].set_color('#666666')
        self.ax.spines['right'].set_color('#666666')
        self.ax.tick_params(colors='#eaeaea')
        
        # Initial canvas draw
        self.canvas.draw()
        
    def update_chart(self, data: List[float], label: str):
        """
        Update the chart with new data points.
        
        Args:
            data: List of numeric data points to plot
            label: Y-axis label (e.g., "CPU (%)", "Memory (MB)")
        """
        # Clear the current chart to avoid layering old lines on top
        self.ax.clear()
        
        if not data:
            # If no data, show empty chart
            self._initialize_chart()
            return
            
        # Plot the new data
        x_values = list(range(len(data)))
        self.ax.plot(x_values, data, color=self.color, linewidth=2, alpha=0.8)
        
        # Set labels and styling
        self.ax.set_ylabel(label, color='#eaeaea', fontsize=10)
        self.ax.set_xlabel('Time (samples)', color='#eaeaea', fontsize=10)
        
        # Set reasonable y-axis limits with some padding
        if data:
            min_val = min(data)
            max_val = max(data)
            padding = (max_val - min_val) * 0.1 if max_val != min_val else 1
            self.ax.set_ylim(max(0, min_val - padding), max_val + padding)
        
        # Apply dark theme styling
        self.ax.set_facecolor('#16213e')
        self.ax.grid(True, alpha=0.3, color='#444444')
        self.ax.spines['bottom'].set_color('#666666')
        self.ax.spines['top'].set_color('#666666')
        self.ax.spines['left'].set_color('#666666')
        self.ax.spines['right'].set_color('#666666')
        self.ax.tick_params(colors='#eaeaea')
        
        # Refresh the canvas to show the updated chart
        self.canvas.draw()
