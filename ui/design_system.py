# ui/design_system.py
# Professional Design System for Battery Performance Tester
# Modern color palette, typography, and visual styling

import customtkinter as ctk

class DesignSystem:
    """
    Professional design system with modern color palette and styling
    """
    
    # ===== COLOR PALETTE =====
    # Primary - Deep Space Purple theme
    PRIMARY_DARK = "#0A0E27"          # Deep space background
    PRIMARY_MEDIUM = "#1A1F3A"        # Card backgrounds
    PRIMARY_LIGHT = "#2D3561"         # Hover states
    PRIMARY_ACCENT = "#4A5F8A"        # Active elements
    
    # Accent Colors - Vibrant gradient theme
    ACCENT_PRIMARY = "#6366F1"        # Electric blue
    ACCENT_SECONDARY = "#8B5CF6"      # Vibrant purple  
    ACCENT_TERTIARY = "#EC4899"       # Hot pink
    ACCENT_SUCCESS = "#10B981"        # Emerald green
    ACCENT_WARNING = "#F59E0B"        # Amber
    ACCENT_DANGER = "#EF4444"         # Red
    
    # Gradient Colors
    GRADIENT_START = "#6366F1"        # Electric blue
    GRADIENT_END = "#8B5CF6"          # Vibrant purple
    GRADIENT_SUCCESS = "#10B981"      # Emerald
    GRADIENT_DANGER = "#EF4444"       # Red
    
    # Text Colors
    TEXT_PRIMARY = "#F8FAFC"          # White text
    TEXT_SECONDARY = "#CBD5E1"        # Light gray
    TEXT_MUTED = "#94A3B8"            # Muted gray
    TEXT_ACCENT = "#A78BFA"           # Purple accent text
    
    # Status Colors
    STATUS_IDLE = "#64748B"           # Gray for idle
    STATUS_ACTIVE = "#3B82F6"        # Blue for active
    STATUS_SUCCESS = "#10B981"       # Green for success
    STATUS_WARNING = "#F59E0B"       # Amber for warning
    STATUS_ERROR = "#EF4444"          # Red for error
    
    # ===== TYPOGRAPHY =====
    FONT_FAMILY = "SF Pro Display" if ctk.get_appearance_mode() == "dark" else "Inter"
    
    # Font Sizes
    FONT_SIZE_LARGE = 24              # Headers
    FONT_SIZE_MEDIUM = 18             # Subheaders
    FONT_SIZE_NORMAL = 14             # Body text
    FONT_SIZE_SMALL = 12              # Captions
    FONT_SIZE_TINY = 10               # Fine print
    
    # Font Weights (tkinter only supports normal and bold)
    FONT_WEIGHT_BOLD = "bold"
    FONT_WEIGHT_NORMAL = "normal"
    
    # ===== SPACING =====
    SPACING_XS = 4                    # Extra small
    SPACING_SM = 8                    # Small
    SPACING_MD = 16                   # Medium
    SPACING_LG = 24                   # Large
    SPACING_XL = 32                   # Extra large
    SPACING_XXL = 48                  # Extra extra large
    
    # ===== BORDER RADIUS =====
    RADIUS_SMALL = 8                  # Small elements
    RADIUS_MEDIUM = 12                # Cards, buttons
    RADIUS_LARGE = 16                 # Large containers
    RADIUS_XL = 20                    # Main panels
    
    # ===== SHADOWS =====
    SHADOW_LIGHT = "2px 2px 8px rgba(0,0,0,0.1)"
    SHADOW_MEDIUM = "4px 4px 16px rgba(0,0,0,0.15)"
    SHADOW_HEAVY = "8px 8px 24px rgba(0,0,0,0.2)"
    
    # ===== ANIMATION =====
    ANIMATION_FAST = 150              # Fast transitions (ms)
    ANIMATION_NORMAL = 250           # Normal transitions (ms)
    ANIMATION_SLOW = 400              # Slow transitions (ms)
    
    @classmethod
    def get_font(cls, size="normal", weight="normal"):
        """Get configured font"""
        size_map = {
            "large": cls.FONT_SIZE_LARGE,
            "medium": cls.FONT_SIZE_MEDIUM,
            "normal": cls.FONT_SIZE_NORMAL,
            "small": cls.FONT_SIZE_SMALL,
            "tiny": cls.FONT_SIZE_TINY
        }
        
        # Map weight descriptions to tkinter-supported weights
        weight_map = {
            "bold": cls.FONT_WEIGHT_BOLD,
            "semibold": cls.FONT_WEIGHT_BOLD,  # Map semibold to bold
            "medium": cls.FONT_WEIGHT_NORMAL,  # Map medium to normal
            "normal": cls.FONT_WEIGHT_NORMAL
        }
        
        return ctk.CTkFont(
            family=cls.FONT_FAMILY,
            size=size_map.get(size, cls.FONT_SIZE_NORMAL),
            weight=weight_map.get(weight, cls.FONT_WEIGHT_NORMAL)
        )
    
    @classmethod
    def get_gradient_colors(cls, gradient_type="primary"):
        """Get gradient color pair"""
        gradients = {
            "primary": (cls.GRADIENT_START, cls.GRADIENT_END),
            "success": (cls.ACCENT_SUCCESS, cls.GRADIENT_SUCCESS),
            "danger": (cls.ACCENT_DANGER, cls.GRADIENT_DANGER),
            "warning": (cls.ACCENT_WARNING, cls.ACCENT_TERTIARY)
        }
        return gradients.get(gradient_type, gradients["primary"])
    
    @classmethod
    def get_status_color(cls, status):
        """Get color based on status"""
        status_colors = {
            "idle": cls.STATUS_IDLE,
            "active": cls.STATUS_ACTIVE,
            "success": cls.STATUS_SUCCESS,
            "warning": cls.STATUS_WARNING,
            "error": cls.STATUS_ERROR
        }
        return status_colors.get(status, cls.STATUS_IDLE)
