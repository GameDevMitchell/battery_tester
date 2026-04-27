# ui/enhanced_chart_panel.py
# Spectacular enhanced chart component with modern design system
# Features gradient effects, smooth animations, and professional styling

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import numpy as np
import customtkinter as ctk
from typing import List, Optional
from ui.design_system import DesignSystem


class EnhancedChartPanel(ctk.CTkFrame):
    """
    Spectacular enhanced chart panel with modern design system
    Features gradient backgrounds, smooth animations, and professional aesthetics
    """
    
    def __init__(self, parent, title: str, color: str, icon: str):
        """
        Initialize the spectacular enhanced chart panel
        
        Args:
            parent: Parent widget
            title: Chart title (e.g., "CPU USAGE")
            color: Primary color for the chart
            icon: Icon emoji for the chart
        """
        super().__init__(parent, fg_color=DesignSystem.PRIMARY_MEDIUM, corner_radius=DesignSystem.RADIUS_MEDIUM)
        
        self.title = title
        self.color = color
        self.icon = color
        self.icon_symbol = icon
        
        # Animation state
        self.animation_frames = []
        self.current_frame = 0
        self.is_animating = False
        
        # Build the spectacular chart panel
        self._build_spectacular_panel()
        
    def _build_spectacular_panel(self):
        """Build the spectacular chart panel with modern styling"""
        # Header with gradient effect
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill='x', padx=DesignSystem.SPACING_MD, pady=(DesignSystem.SPACING_MD, DesignSystem.SPACING_SM))
        
        # Icon with glow effect
        icon_container = ctk.CTkFrame(
            header_frame,
            fg_color=self.color,
            corner_radius=DesignSystem.RADIUS_SMALL,
            width=30,
            height=30
        )
        icon_container.pack(side='left', padx=(0, DesignSystem.SPACING_SM))
        icon_container.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_container,
            text=self.icon_symbol,
            font=DesignSystem.get_font("normal", "bold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        icon_label.pack(expand=True)
        
        # Title with modern typography
        title_label = ctk.CTkLabel(
            header_frame,
            text=self.title,
            font=DesignSystem.get_font("normal", "semibold"),
            text_color=DesignSystem.TEXT_PRIMARY
        )
        title_label.pack(side='left')
        
        # Status indicator
        self.status_dot = ctk.CTkLabel(
            header_frame,
            text="●",
            font=DesignSystem.get_font("small"),
            text_color=DesignSystem.STATUS_IDLE
        )
        self.status_dot.pack(side='right', padx=(DesignSystem.SPACING_SM, 0))
        
        # Chart container with gradient background
        self.chart_container = ctk.CTkFrame(
            self,
            fg_color=DesignSystem.PRIMARY_DARK,
            corner_radius=DesignSystem.RADIUS_MEDIUM
        )
        self.chart_container.pack(fill='both', expand=True, padx=DesignSystem.SPACING_MD, pady=(0, DesignSystem.SPACING_MD))
        
        # Create spectacular matplotlib chart
        self._create_spectacular_chart()
        
    def _create_spectacular_chart(self):
        """Create spectacular matplotlib chart with modern styling"""
        # Set up matplotlib with custom styling
        plt.style.use('dark_background')
        
        # Create figure with custom size and DPI
        self.fig = Figure(
            figsize=(4, 3), 
            dpi=120, 
            facecolor=DesignSystem.PRIMARY_DARK,
            edgecolor='none'
        )
        
        # Create axis with custom styling
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(DesignSystem.PRIMARY_DARK)
        
        # Remove chart clutter for clean look
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(DesignSystem.PRIMARY_ACCENT)
        self.ax.spines['bottom'].set_color(DesignSystem.PRIMARY_ACCENT)
        self.ax.spines['left'].set_linewidth(1)
        self.ax.spines['bottom'].set_linewidth(1)
        
        # Style grid
        self.ax.grid(True, alpha=0.1, color=DesignSystem.PRIMARY_ACCENT, linestyle='--')
        
        # Style ticks
        self.ax.tick_params(
            colors=DesignSystem.TEXT_MUTED,
            labelsize=8,
            pad=2
        )
        
        # Embed in tkinter with custom styling
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=DesignSystem.SPACING_SM, pady=DesignSystem.SPACING_SM)
        
        # Initialize empty chart
        self._initialize_empty_chart()
        
    def _initialize_empty_chart(self):
        """Initialize empty chart with placeholder styling"""
        self.ax.clear()
        
        # Create gradient background effect
        gradient = np.linspace(0, 1, 100).reshape(100, 1)
        self.ax.imshow(
            gradient, 
            extent=[0, 10, 0, 100], 
            aspect='auto', 
            alpha=0.05,
            cmap='viridis'
        )
        
        # Add placeholder text
        self.ax.text(
            0.5, 0.5, 
            f'{self.icon_symbol} {self.title}',
            transform=self.ax.transAxes,
            ha='center', va='center',
            fontsize=12,
            color=DesignSystem.TEXT_MUTED,
            alpha=0.6,
            fontweight='medium'
        )
        
        # Set limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 100)
        
        # Style labels
        self.ax.set_xlabel('Time', color=DesignSystem.TEXT_MUTED, fontsize=8)
        self.ax.set_ylabel('Value', color=DesignSystem.TEXT_MUTED, fontsize=8)
        
        self.canvas.draw()
        
    def update_chart(self, data: List[float], label: str):
        """
        Update chart with spectacular animations and effects
        
        Args:
            data: List of data points to plot
            label: Y-axis label
        """
        if not data:
            self._initialize_empty_chart()
            self.status_dot.configure(text_color=DesignSystem.STATUS_IDLE)
            return
            
        # Clear and prepare chart
        self.ax.clear()
        
        # Recreate gradient background
        gradient = np.linspace(0, 1, 100).reshape(100, 1)
        self.ax.imshow(
            gradient, 
            extent=[0, len(data), 0, max(data) * 1.2 if data else 100], 
            aspect='auto', 
            alpha=0.03,
            cmap='viridis'
        )
        
        # Create smooth line plot with gradient effect
        x_values = list(range(len(data)))
        
        # Main line with glow effect
        self.ax.plot(
            x_values, 
            data, 
            color=self.color, 
            linewidth=3, 
            alpha=0.9,
            solid_capstyle='round'
        )
        
        # Add glow effect
        for i, alpha in enumerate([0.3, 0.2, 0.1]):
            self.ax.plot(
                x_values, 
                data, 
                color=self.color, 
                linewidth=3 + i*2, 
                alpha=alpha,
                solid_capstyle='round'
            )
        
        # Fill area under curve with gradient
        self.ax.fill_between(
            x_values, 
            0, 
            data, 
            alpha=0.15, 
            color=self.color,
            interpolate=True
        )
        
        # Add data points for recent values
        if len(data) > 0:
            recent_points = min(5, len(data))
            recent_x = x_values[-recent_points:]
            recent_y = data[-recent_points:]
            
            self.ax.scatter(
                recent_x, 
                recent_y, 
                color=self.color, 
                s=30, 
                alpha=0.8,
                edgecolors=DesignSystem.TEXT_PRIMARY,
                linewidth=1
            )
        
        # Set dynamic limits with padding
        if data:
            y_max = max(data) * 1.2 if max(data) > 0 else 100
            y_min = min(0, min(data) * 0.8)
            self.ax.set_ylim(y_min, y_max)
            self.ax.set_xlim(0, max(10, len(data)))
        
        # Style the chart
        self.ax.set_facecolor(DesignSystem.PRIMARY_DARK)
        self.ax.grid(True, alpha=0.1, color=DesignSystem.PRIMARY_ACCENT, linestyle='--')
        
        # Style spines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(DesignSystem.PRIMARY_ACCENT)
        self.ax.spines['bottom'].set_color(DesignSystem.PRIMARY_ACCENT)
        self.ax.spines['left'].set_linewidth(1)
        self.ax.spines['bottom'].set_linewidth(1)
        
        # Style ticks
        self.ax.tick_params(colors=DesignSystem.TEXT_MUTED, labelsize=8, pad=2)
        
        # Set labels
        self.ax.set_ylabel(label, color=DesignSystem.TEXT_MUTED, fontsize=8, fontweight='bold')
        self.ax.set_xlabel('Time (samples)', color=DesignSystem.TEXT_MUTED, fontsize=8, fontweight='bold')
        
        # Add current value annotation
        if data:
            current_value = data[-1]
            self.ax.annotate(
                f'{current_value:.1f}',
                xy=(len(data)-1, current_value),
                xytext=(5, 5),
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=self.color, alpha=0.8),
                color=DesignSystem.TEXT_PRIMARY,
                fontsize=8,
                fontweight='bold'
            )
        
        # Update status indicator
        self.status_dot.configure(text_color=DesignSystem.STATUS_SUCCESS)
        
        # Refresh canvas with smooth animation
        self.canvas.draw()
        self.canvas.flush_events()  # Ensure immediate update
        
        # Force GUI update
        self.canvas.update()
        self.canvas.update_idletasks()
        
    def animate_data_transition(self, old_data: List[float], new_data: List[float], steps: int = 10):
        """
        Animate smooth transition between data sets
        
        Args:
            old_data: Previous data points
            new_data: New data points
            steps: Number of animation steps
        """
        if self.is_animating:
            return
            
        self.is_animating = True
        self.animation_frames = []
        
        # Generate animation frames
        for step in range(steps + 1):
            progress = step / steps
            frame = []
            
            # Interpolate between old and new data
            max_len = max(len(old_data), len(new_data))
            for i in range(max_len):
                if i < len(old_data) and i < len(new_data):
                    # Interpolate existing points
                    old_val = old_data[i]
                    new_val = new_data[i]
                    interpolated = old_val + (new_val - old_val) * progress
                    frame.append(interpolated)
                elif i < len(new_data):
                    # Fade in new points
                    frame.append(new_data[i] * progress)
                else:
                    # Fade out old points
                    frame.append(old_data[i] * (1 - progress))
                    
            self.animation_frames.append(frame)
        
        # Start animation
        self._play_animation()
        
    def _play_animation(self):
        """Play the animation frames"""
        if not self.animation_frames or self.current_frame >= len(self.animation_frames):
            self.is_animating = False
            self.current_frame = 0
            return
            
        # Update chart with current frame
        frame_data = self.animation_frames[self.current_frame]
        self.update_chart(frame_data, "Value")
        
        self.current_frame += 1
        
        # Schedule next frame
        self.after(50, self._play_animation)  # 20 FPS animation
        
    def set_status(self, status: str):
        """
        Update chart status indicator
        
        Args:
            status: Status type ('idle', 'active', 'success', 'warning', 'error')
        """
        color = DesignSystem.get_status_color(status)
        self.status_dot.configure(text_color=color)
