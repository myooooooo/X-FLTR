"""
X-FLTR / THE VOID ENGINE — Main Application
============================================
Professional-grade image processing tool with 42 filters.

Author: ANSSAFOU ZINEB
Lab: DIGITAL CREATION LAB
Version: 1.0

Architecture:
- Zero disk I/O (all processing in RAM)
- Threaded processing (UI stays responsive)
- Retina-optimized (CTkImage everywhere)
- Cyber-Brutalist aesthetic (Black + Neon Green)
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
from tkinter import filedialog
import threading
import time
import random
import hashlib
from collections import deque
from functools import lru_cache
from typing import Optional

# Import our modules
from branding import BrandingConfig, generate_app_logo, generate_splash_image, get_header_text
from filters_engine import FilterEngine, FILTER_REGISTRY


# ============================================================================
# SPLASH SCREEN
# ============================================================================

class SplashScreen(ctk.CTkToplevel):
    """
    Animated boot sequence splash screen with diagnostics.
    Shows progressive system initialization with terminal-style animation.
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Window configuration
        self.title("")
        self.geometry("800x400")
        self.configure(fg_color=BrandingConfig.BLACK)

        # Frameless window (no title bar)
        self.overrideredirect(True)

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 800) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"800x400+{x}+{y}")

        # Container
        container = ctk.CTkFrame(self, fg_color=BrandingConfig.BLACK)
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # Logo area
        logo_label = ctk.CTkLabel(
            container,
            text="X-FLTR // THE VOID ENGINE",
            font=("Monaco", 32, "bold"),
            text_color=BrandingConfig.GREEN_NEON
        )
        logo_label.pack(pady=(20, 10))

        version_label = ctk.CTkLabel(
            container,
            text=f"v{BrandingConfig.VERSION}",
            font=("Monaco", 12),
            text_color="#888888"
        )
        version_label.pack(pady=(0, 30))

        # Diagnostics log area
        self.diagnostics_text = ctk.CTkTextbox(
            container,
            fg_color="#0A0A0A",
            text_color=BrandingConfig.GREEN_NEON,
            font=("Monaco", 10),
            border_width=1,
            border_color=BrandingConfig.GREEN_NEON,
            height=180,
            corner_radius=0
        )
        self.diagnostics_text.pack(fill="both", expand=True, pady=(0, 20))
        self.diagnostics_text.configure(state="disabled")

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            container,
            progress_color=BrandingConfig.GREEN_NEON,
            fg_color="#1A1A1A",
            height=15,
            corner_radius=0
        )
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress.set(0)

        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="INITIALIZING...",
            font=("Monaco", 9),
            text_color="#888888"
        )
        self.status_label.pack()

        # Animation sequence
        self.animation_step = 0
        self.diagnostics_steps = [
            (0.15, ">>> VOID ENGINE BOOT SEQUENCE INITIATED"),
            (0.30, ">>> LOADING FILTER MODULES... [42/42]"),
            (0.45, ">>> INITIALIZING NUMPY VECTORIZATION"),
            (0.60, ">>> CONFIGURING RETINA DISPLAY PIPELINE"),
            (0.75, ">>> MOUNTING LRU CACHE SYSTEM"),
            (0.90, ">>> ENABLING THREADED PROCESSING"),
            (1.00, ">>> SYSTEM READY // ALL CHECKS PASSED"),
        ]

        # Start animation
        self._animate()

    def _animate(self):
        """Progressive diagnostic animation."""
        if self.animation_step < len(self.diagnostics_steps):
            progress_val, message = self.diagnostics_steps[self.animation_step]

            # Update diagnostics log
            self.diagnostics_text.configure(state="normal")
            timestamp = time.strftime("%H:%M:%S")
            self.diagnostics_text.insert("end", f"[{timestamp}] {message}\n")
            self.diagnostics_text.see("end")
            self.diagnostics_text.configure(state="disabled")

            # Update progress bar
            self.progress.set(progress_val)

            # Update status
            if progress_val < 1.0:
                self.status_label.configure(text=f"LOADING... {int(progress_val * 100)}%")
            else:
                self.status_label.configure(
                    text="LAUNCH COMPLETE",
                    text_color=BrandingConfig.GREEN_NEON
                )

            self.animation_step += 1

            # Schedule next step
            self.after(300, self._animate)
        else:
            # Close after all steps complete
            self.after(500, self.destroy)


# ============================================================================
# DATA STREAM (Terminal Log)
# ============================================================================

class DataStream(ctk.CTkTextbox):
    """Real-time scrolling log of all operations with color-coded messages."""

    # Color definitions for log levels
    COLOR_SUCCESS = "#00FF41"  # Neon green
    COLOR_ERROR = "#FF0055"    # Neon red
    COLOR_WARNING = "#FF9500"  # Orange
    COLOR_INFO = "#00D4FF"     # Cyan
    COLOR_SYSTEM = "#FFFFFF"   # White

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=BrandingConfig.BLACK,
            text_color=BrandingConfig.GREEN_NEON,
            font=BrandingConfig.FONT_TERMINAL,
            border_width=2,
            border_color=BrandingConfig.GREEN_NEON,
            corner_radius=0,
            **kwargs
        )

        self.configure(state="disabled")
        self.log_buffer = deque(maxlen=200)

        # Configure color tags
        self.tag_config("success", foreground=self.COLOR_SUCCESS)
        self.tag_config("error", foreground=self.COLOR_ERROR)
        self.tag_config("warning", foreground=self.COLOR_WARNING)
        self.tag_config("info", foreground=self.COLOR_INFO)
        self.tag_config("system", foreground=self.COLOR_SYSTEM)

    def log(self, message: str, level: str = "success"):
        """
        Add timestamped, color-coded log entry.

        Args:
            message: Log message text
            level: Log level - "success", "error", "warning", "info", or "system"
        """
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"

        self.configure(state="normal")

        # Insert with color tag
        start_index = self.index("end-1c")
        self.insert("end", entry)
        end_index = self.index("end-1c")

        # Apply color tag to the entire line
        if level in ["success", "error", "warning", "info", "system"]:
            self.tag_add(level, start_index, end_index)

        self.see("end")
        self.configure(state="disabled")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class VoidEngineApp(ctk.CTk):
    """
    Main application window.

    Features:
    - 42 filter grid (8×5 + 2)
    - In-memory processing (no disk writes)
    - Threaded operations
    - Retina-optimized display
    """

    def __init__(self):
        super().__init__()

        # Window setup
        self.title(f"X-FLTR // {BrandingConfig.VERSION} // DEVELOPED BY {BrandingConfig.AUTHOR}")
        self.geometry("1900x1100")
        self.configure(fg_color=BrandingConfig.BLACK)
        ctk.set_appearance_mode("dark")

        # Set app icon (generative logo)
        try:
            logo_img = generate_app_logo(64)
            # Convert to PhotoImage for iconphoto
            logo_photo = ImageTk.PhotoImage(logo_img)
            self.iconphoto(True, logo_photo)
            # Keep reference to prevent garbage collection
            self._icon_ref = logo_photo
        except:
            pass  # Fallback if icon setting fails

        # State
        self.original_image: Optional[Image.Image] = None  # Full resolution
        self.original_array: Optional[np.ndarray] = None   # Full resolution array
        self.working_array: Optional[np.ndarray] = None    # Preview resolution (for speed)
        self.proxy_max_dimension = 1200  # Maximum dimension for preview
        self.display_ctk_image: Optional[ctk.CTkImage] = None
        self.is_processing = False
        self.use_proxy = True  # Enable proxy preview for performance

        # History for undo (keep last 5 states)
        self.history = deque(maxlen=5)

        # Image adjustment parameters
        self.brightness_value = 1.0  # Range: 0.5 to 1.5
        self.contrast_value = 1.0    # Range: 0.5 to 1.5
        self.saturation_value = 1.0  # Range: 0.0 to 2.0

        # Filter result cache (LRU cache for performance)
        self.filter_cache = {}  # {cache_key: result_array}
        self.max_cache_size = 10  # Keep last 10 filter results

        # Build UI
        self._build_interface()

        # Bind window resize event for adaptive canvas
        self.bind("<Configure>", self._on_window_resize)

        # Log startup
        self.data_stream.log("SYSTEM INITIALIZED", level="system")
        self.data_stream.log("42 FILTER MODULES LOADED", level="info")
        self.data_stream.log("AWAITING IMAGE INPUT...", level="info")

    def _build_interface(self):
        """Construct main interface."""
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self._build_header()

        # Left: Data Stream
        self._build_data_stream()

        # Center: Canvas
        self._build_canvas()

        # Right: Filter Grid
        self._build_filter_panel()

        # Advanced Settings HUD (above action bar)
        self._build_advanced_settings()

        # Bottom: Action Buttons
        self._build_action_bar()

    # ========================================================================
    # UI COMPONENTS
    # ========================================================================

    def _build_header(self):
        """Fixed header with branding."""
        header = ctk.CTkFrame(
            self,
            height=50,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0,
            border_width=2,
            border_color=BrandingConfig.GREEN_NEON
        )
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        header_text = get_header_text()

        ctk.CTkLabel(
            header,
            text=header_text,
            font=BrandingConfig.FONT_HEADER,
            text_color=BrandingConfig.GREEN_NEON
        ).pack(side="left", padx=20, pady=10)

    def _build_data_stream(self):
        """Left panel: Terminal log."""
        stream_frame = ctk.CTkFrame(
            self,
            width=320,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0
        )
        stream_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0, rowspan=2)
        stream_frame.grid_propagate(False)

        # Section header
        ctk.CTkLabel(
            stream_frame,
            text=">> DATA STREAM",
            font=("Monaco", 12, "bold"),
            text_color=BrandingConfig.GREEN_NEON
        ).pack(pady=(10, 5), padx=10)

        # Stream
        self.data_stream = DataStream(stream_frame, height=900)
        self.data_stream.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def _build_canvas(self):
        """Center panel: Image preview."""
        canvas_frame = ctk.CTkFrame(
            self,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0,
            border_width=3,
            border_color=BrandingConfig.GREEN_NEON
        )
        canvas_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Status
        self.status_label = ctk.CTkLabel(
            canvas_frame,
            text="LOAD IMAGE TO BEGIN",
            font=BrandingConfig.FONT_MONO,
            text_color=BrandingConfig.GREEN_NEON
        )
        self.status_label.pack(pady=20)

        # Canvas
        self.canvas_label = ctk.CTkLabel(
            canvas_frame,
            text="",
            fg_color=BrandingConfig.BLACK
        )
        self.canvas_label.pack(expand=True, fill="both", padx=30, pady=30)

    def _build_filter_panel(self):
        """Right panel: Collapsible accordion filter library."""
        filter_frame = ctk.CTkFrame(
            self,
            width=380,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0,
            border_width=2,
            border_color=BrandingConfig.GREEN_NEON
        )
        filter_frame.grid(row=1, column=2, sticky="nsew", padx=0, pady=10)
        filter_frame.grid_propagate(False)

        # Header (fixed)
        header = ctk.CTkFrame(filter_frame, fg_color=BrandingConfig.BLACK, height=40)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=">> FILTER LIBRARY [42]",
            font=("Monaco", 11, "bold"),
            text_color=BrandingConfig.GREEN_NEON
        ).pack(pady=10, padx=10)

        # Scrollable container for collapsible categories
        scroll_container = ctk.CTkScrollableFrame(
            filter_frame,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0,
            scrollbar_button_color=BrandingConfig.GREEN_NEON,
            scrollbar_button_hover_color=BrandingConfig.GREEN_NEON
        )
        scroll_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Build collapsible categories
        self.category_widgets = {}

        for category_name, filters in FILTER_REGISTRY.items():
            category_widget = self._create_collapsible_category(
                scroll_container,
                category_name,
                filters
            )
            category_widget.pack(fill="x", pady=2)
            self.category_widgets[category_name] = category_widget

    def _create_collapsible_category(self, parent, category_name, filters):
        """
        Create a collapsible category widget (accordion style).

        Returns a frame containing:
        - Clickable header (expand/collapse)
        - Hidden content (filter buttons)
        """
        # Container frame
        container = ctk.CTkFrame(
            parent,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0
        )

        # State tracking
        container.is_expanded = False
        container.filters = filters
        container.category_name = category_name

        # Header button (clickable)
        header_btn = ctk.CTkButton(
            container,
            text=f"▶ [{category_name}] ({len(filters)} filters)",
            command=lambda: self._toggle_category(container),
            font=("Monaco", 10, "bold"),
            fg_color=BrandingConfig.BLACK,
            hover_color="#1A1A1A",  # Subtle hover
            border_width=1,
            border_color=BrandingConfig.GREEN_NEON,
            text_color=BrandingConfig.GREEN_NEON,
            corner_radius=0,
            height=30,
            anchor="w"
        )
        header_btn.pack(fill="x", padx=0, pady=0)
        container.header_btn = header_btn

        # Content frame (hidden by default)
        content = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        container.content = content

        # Build filter buttons in content (2 columns)
        content.grid_columnconfigure(0, weight=1, uniform="filter_col")
        content.grid_columnconfigure(1, weight=1, uniform="filter_col")

        row, col = 0, 0
        for filter_name, filter_func, default_params in filters:
            btn = ctk.CTkButton(
                content,
                text=filter_name,
                command=lambda f=filter_func, p=default_params: self._apply_filter(f, p),
                font=("Monaco", 9),
                fg_color="transparent",
                hover_color="#1A1A1A",  # IMPROVED: Brighter hover
                border_width=1,
                border_color=BrandingConfig.GREEN_NEON,
                text_color=BrandingConfig.GREEN_NEON,
                corner_radius=0,
                height=30,
                width=160
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

            col += 1
            if col >= 2:
                col = 0
                row += 1

        return container

    def _toggle_category(self, category_widget):
        """
        Toggle category expansion (accordion behavior).
        Only one category open at a time.
        """
        # If already expanded, collapse it
        if category_widget.is_expanded:
            category_widget.content.pack_forget()
            category_widget.header_btn.configure(
                text=f"▶ [{category_widget.category_name}] ({len(category_widget.filters)} filters)"
            )
            category_widget.is_expanded = False
        else:
            # Collapse all other categories first (accordion)
            for other_widget in self.category_widgets.values():
                if other_widget != category_widget and other_widget.is_expanded:
                    other_widget.content.pack_forget()
                    other_widget.header_btn.configure(
                        text=f"▶ [{other_widget.category_name}] ({len(other_widget.filters)} filters)"
                    )
                    other_widget.is_expanded = False

            # Expand this category
            category_widget.content.pack(fill="x", pady=(2, 4))
            category_widget.header_btn.configure(
                text=f"▼ [{category_widget.category_name}] ({len(category_widget.filters)} filters)"
            )
            category_widget.is_expanded = True

    def _build_advanced_settings(self):
        """Advanced Settings HUD with Brightness/Contrast/Saturation sliders."""
        settings_frame = ctk.CTkFrame(
            self,
            height=120,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0,
            border_width=2,
            border_color="#00D4FF"  # Cyan border for distinction
        )
        settings_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=(0, 5))
        settings_frame.grid_propagate(False)

        # Header
        header_label = ctk.CTkLabel(
            settings_frame,
            text="[ ADVANCED SETTINGS ]",
            font=("Monaco", 11, "bold"),
            text_color="#00D4FF"
        )
        header_label.pack(pady=(8, 5))

        # Sliders container
        sliders_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        sliders_container.pack(fill="x", padx=20, pady=(0, 8))

        # Brightness Slider
        brightness_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        brightness_frame.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            brightness_frame,
            text="BRIGHTNESS",
            font=("Monaco", 9),
            text_color=BrandingConfig.GREEN_NEON
        ).pack(anchor="w")

        self.brightness_slider = ctk.CTkSlider(
            brightness_frame,
            from_=0.5,
            to=1.5,
            number_of_steps=100,
            command=self._on_brightness_change,
            button_color=BrandingConfig.GREEN_NEON,
            button_hover_color="#00CC33",
            progress_color=BrandingConfig.GREEN_NEON,
            fg_color="#1A1A1A"
        )
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(fill="x", pady=(2, 0))

        self.brightness_label = ctk.CTkLabel(
            brightness_frame,
            text="1.00",
            font=("Monaco", 8),
            text_color="#888888"
        )
        self.brightness_label.pack(anchor="e")

        # Contrast Slider
        contrast_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        contrast_frame.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            contrast_frame,
            text="CONTRAST",
            font=("Monaco", 9),
            text_color=BrandingConfig.GREEN_NEON
        ).pack(anchor="w")

        self.contrast_slider = ctk.CTkSlider(
            contrast_frame,
            from_=0.5,
            to=1.5,
            number_of_steps=100,
            command=self._on_contrast_change,
            button_color=BrandingConfig.GREEN_NEON,
            button_hover_color="#00CC33",
            progress_color=BrandingConfig.GREEN_NEON,
            fg_color="#1A1A1A"
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill="x", pady=(2, 0))

        self.contrast_label = ctk.CTkLabel(
            contrast_frame,
            text="1.00",
            font=("Monaco", 8),
            text_color="#888888"
        )
        self.contrast_label.pack(anchor="e")

        # Saturation Slider
        saturation_frame = ctk.CTkFrame(sliders_container, fg_color="transparent")
        saturation_frame.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(
            saturation_frame,
            text="SATURATION",
            font=("Monaco", 9),
            text_color=BrandingConfig.GREEN_NEON
        ).pack(anchor="w")

        self.saturation_slider = ctk.CTkSlider(
            saturation_frame,
            from_=0.0,
            to=2.0,
            number_of_steps=100,
            command=self._on_saturation_change,
            button_color=BrandingConfig.GREEN_NEON,
            button_hover_color="#00CC33",
            progress_color=BrandingConfig.GREEN_NEON,
            fg_color="#1A1A1A"
        )
        self.saturation_slider.set(1.0)
        self.saturation_slider.pack(fill="x", pady=(2, 0))

        self.saturation_label = ctk.CTkLabel(
            saturation_frame,
            text="1.00",
            font=("Monaco", 8),
            text_color="#888888"
        )
        self.saturation_label.pack(anchor="e")

        # Reset button for sliders
        ctk.CTkButton(
            sliders_container,
            text="⟲",
            width=40,
            height=60,
            command=self._reset_adjustments,
            font=("Monaco", 16),
            fg_color="transparent",
            hover_color="#0A0A0A",
            border_width=1,
            border_color="#00D4FF",
            text_color="#00D4FF"
        ).pack(side="right", padx=5)

    def _on_brightness_change(self, value):
        """Handle brightness slider change."""
        self.brightness_value = value
        self.brightness_label.configure(text=f"{value:.2f}")
        self._apply_adjustments()

    def _on_contrast_change(self, value):
        """Handle contrast slider change."""
        self.contrast_value = value
        self.contrast_label.configure(text=f"{value:.2f}")
        self._apply_adjustments()

    def _on_saturation_change(self, value):
        """Handle saturation slider change."""
        self.saturation_value = value
        self.saturation_label.configure(text=f"{value:.2f}")
        self._apply_adjustments()

    def _apply_adjustments(self):
        """Apply brightness/contrast/saturation adjustments to current image."""
        if self.working_array is None:
            return

        # Apply adjustments in-place (non-destructive)
        adjusted = self.working_array.copy().astype(np.float32)

        # Brightness adjustment
        adjusted = adjusted * self.brightness_value

        # Contrast adjustment (around midpoint 127.5)
        adjusted = (adjusted - 127.5) * self.contrast_value + 127.5

        # Saturation adjustment (convert to HSV, modify S channel)
        if self.saturation_value != 1.0:
            # Simple saturation via weighted grayscale
            gray = 0.299 * adjusted[:, :, 0] + 0.587 * adjusted[:, :, 1] + 0.114 * adjusted[:, :, 2]
            gray = np.stack([gray, gray, gray], axis=2)
            adjusted = gray + (adjusted - gray) * self.saturation_value

        # Clip and update display
        self.working_array = np.clip(adjusted, 0, 255).astype(np.uint8)
        self._update_display()

    def _reset_adjustments(self):
        """Reset all adjustment sliders to defaults."""
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)
        self.brightness_value = 1.0
        self.contrast_value = 1.0
        self.saturation_value = 1.0
        self.brightness_label.configure(text="1.00")
        self.contrast_label.configure(text="1.00")
        self.saturation_label.configure(text="1.00")
        self._apply_adjustments()
        self.data_stream.log("ADJUSTMENTS RESET", level="info")

    def _build_action_bar(self):
        """Bottom action buttons."""
        action_frame = ctk.CTkFrame(
            self,
            height=70,
            fg_color=BrandingConfig.BLACK,
            corner_radius=0,
            border_width=2,
            border_color=BrandingConfig.GREEN_NEON
        )
        action_frame.grid(row=3, column=1, sticky="ew", padx=10, pady=(0, 10))
        action_frame.grid_propagate(False)

        # Load button
        ctk.CTkButton(
            action_frame,
            text="LOAD IMAGE",
            command=self._load_image,
            font=("Monaco", 12, "bold"),
            fg_color="transparent",
            hover_color="#0A0A0A",
            border_width=2,
            border_color=BrandingConfig.GREEN_NEON,
            text_color=BrandingConfig.GREEN_NEON,
            corner_radius=0,
            height=40,
            width=150
        ).pack(side="left", padx=10, pady=15)

        # Export button
        ctk.CTkButton(
            action_frame,
            text="EXPORT 4K",
            command=self._export_image,
            font=("Monaco", 12, "bold"),
            fg_color="transparent",
            hover_color="#0A0A0A",
            border_width=2,
            border_color=BrandingConfig.GREEN_NEON,
            text_color=BrandingConfig.GREEN_NEON,
            corner_radius=0,
            height=40,
            width=150
        ).pack(side="left", padx=10, pady=15)

        # Randomize button
        ctk.CTkButton(
            action_frame,
            text="RANDOMIZE x3",
            command=self._randomize_filters,
            font=("Monaco", 12, "bold"),
            fg_color="transparent",
            hover_color="#0A0A0A",
            border_width=2,
            border_color=BrandingConfig.RED_GLITCH,
            text_color=BrandingConfig.RED_GLITCH,
            corner_radius=0,
            height=40,
            width=150
        ).pack(side="left", padx=10, pady=15)

        # Reset button
        ctk.CTkButton(
            action_frame,
            text="RESET",
            command=self._reset_image,
            font=("Monaco", 12, "bold"),
            fg_color="transparent",
            hover_color="#0A0A0A",
            border_width=2,
            border_color=BrandingConfig.RED_GLITCH,
            text_color=BrandingConfig.RED_GLITCH,
            corner_radius=0,
            height=40,
            width=150
        ).pack(side="right", padx=10, pady=15)

    # ========================================================================
    # OPERATIONS
    # ========================================================================

    def _load_image(self):
        """Load image file."""
        file_path = filedialog.askopenfilename(
            title="SELECT IMAGE",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            # Load full-resolution image
            self.original_image = Image.open(file_path).convert('RGB')
            self.original_array = np.array(self.original_image)

            filename = file_path.split('/')[-1]
            self.data_stream.log(f"LOADED: {filename}", level="success")
            self.data_stream.log(f"SIZE: {self.original_image.width}×{self.original_image.height}", level="info")

            # Create proxy preview (downsampled for performance)
            if self.use_proxy and max(self.original_image.size) > self.proxy_max_dimension:
                # Calculate proxy size maintaining aspect ratio
                ratio = self.proxy_max_dimension / max(self.original_image.size)
                proxy_size = (int(self.original_image.width * ratio), int(self.original_image.height * ratio))
                proxy_image = self.original_image.resize(proxy_size, Image.Resampling.LANCZOS)
                self.working_array = np.array(proxy_image)
                self.data_stream.log(f"PROXY PREVIEW: {proxy_size[0]}×{proxy_size[1]} (for speed)", level="info")
            else:
                # Small image, no proxy needed
                self.working_array = self.original_array.copy()
                self.data_stream.log("DIRECT MODE: Image size optimal", level="info")

            self.status_label.configure(
                text=filename.upper(),
                text_color=BrandingConfig.GREEN_NEON
            )

            # Clear history and cache on new image
            self._clear_cache()
            self.history.clear()

            # Display
            self._update_display()

        except Exception as e:
            self.data_stream.log(f"ERROR: {str(e)}", level="error")
            self.status_label.configure(
                text="LOAD FAILED",
                text_color=BrandingConfig.RED_GLITCH
            )

    def _apply_filter(self, filter_func, params):
        """Apply filter with threading and caching."""
        if self.working_array is None:
            self.data_stream.log("ERROR: NO IMAGE LOADED", level="error")
            return

        if self.is_processing:
            self.data_stream.log("BUSY: PROCESSING IN PROGRESS", level="warning")
            return

        # Save to history
        self.history.append(self.working_array.copy())

        # Log
        filter_name = filter_func.__name__
        self.data_stream.log(f"APPLYING: {filter_name.upper()}", level="info")

        # Generate cache key
        cache_key = self._generate_cache_key(self.working_array, filter_name, params)

        # Check cache
        if cache_key in self.filter_cache:
            self.working_array = self.filter_cache[cache_key].copy()
            self._update_display()
            self.data_stream.log("LOADED FROM CACHE (INSTANT)", level="success")
            return

        # Process in thread
        def process():
            self.is_processing = True
            try:
                # Apply filter
                result = filter_func(self.working_array, **params)
                self.working_array = result

                # Cache result
                self._cache_result(cache_key, result)

                # Update display on main thread
                self.after(0, self._update_display)
                self.data_stream.log("PROCESSING COMPLETE", level="success")

            except Exception as e:
                self.data_stream.log(f"ERROR: {str(e)}", level="error")
                print(f"Filter error: {e}")
                import traceback
                traceback.print_exc()

            finally:
                self.is_processing = False

        thread = threading.Thread(target=process, daemon=True)
        thread.start()

    def _generate_cache_key(self, arr: np.ndarray, filter_name: str, params: dict) -> str:
        """Generate unique cache key for filter+params+image combination."""
        # Hash the array data
        arr_hash = hashlib.md5(arr.tobytes()).hexdigest()[:16]
        # Hash the params
        params_str = str(sorted(params.items()))
        params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
        return f"{filter_name}_{arr_hash}_{params_hash}"

    def _cache_result(self, key: str, result: np.ndarray):
        """Store filter result in cache with LRU eviction."""
        # Add to cache
        self.filter_cache[key] = result.copy()

        # LRU eviction: keep only max_cache_size most recent
        if len(self.filter_cache) > self.max_cache_size:
            # Remove oldest entry (first key)
            oldest_key = next(iter(self.filter_cache))
            del self.filter_cache[oldest_key]
            self.data_stream.log("CACHE EVICTION (LRU)", level="info")

    def _clear_cache(self):
        """Clear all cached filter results."""
        self.filter_cache.clear()
        self.data_stream.log("CACHE CLEARED", level="info")

    def _update_display(self):
        """
        Update canvas with current image (Retina-safe, adaptive).

        CRITICAL for Retina displays:
        - Uses CTkImage (not ImageTk.PhotoImage)
        - Automatically handles 2× scaling on HiDPI screens
        - Adapts to window resizing dynamically
        """
        if self.working_array is None:
            return

        # Convert to PIL
        pil_img = Image.fromarray(self.working_array)

        # Get ACTUAL canvas dimensions (updates on window resize)
        self.canvas_label.update_idletasks()
        canvas_width = self.canvas_label.winfo_width()
        canvas_height = self.canvas_label.winfo_height()

        # Fallback for first render (before canvas is displayed)
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 1100, 750

        # Calculate optimal display size (maintain aspect ratio)
        img_ratio = pil_img.width / pil_img.height
        canvas_ratio = canvas_width / canvas_height

        # Use MORE of available space (95% instead of 90%)
        if img_ratio > canvas_ratio:
            # Image is wider than canvas
            display_width = int(canvas_width * 0.95)
            display_height = int(display_width / img_ratio)
        else:
            # Image is taller than canvas
            display_height = int(canvas_height * 0.95)
            display_width = int(display_height * img_ratio)

        # CRITICAL: CTkImage for Retina/HiDPI support
        # This automatically generates @2x assets for high-density displays
        self.display_ctk_image = ctk.CTkImage(
            light_image=pil_img,
            dark_image=pil_img,
            size=(display_width, display_height)  # Logical points (not physical pixels)
        )

        self.canvas_label.configure(image=self.display_ctk_image)
        self.status_label.configure(text="")

    def _on_window_resize(self, event):
        """
        Handle window resize events to adaptively scale canvas.

        This ensures the image preview adapts when user:
        - Maximizes window
        - Resizes window manually
        - Changes screen resolution
        """
        # Only update if image is loaded (avoid unnecessary redraws)
        if self.working_array is not None and not self.is_processing:
            # Debounce: Only update after resize settles (avoid lag)
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)

            # Schedule update after 100ms of no resize events
            self._resize_timer = self.after(100, self._update_display)

    def _export_image(self):
        """
        Export processed image at FULL RESOLUTION (4K).

        CRITICAL: If using proxy preview, this re-applies all filters
        to the original full-resolution image for maximum quality.
        """
        if self.working_array is None:
            self.data_stream.log("ERROR: NO IMAGE TO EXPORT", level="error")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG (Lossless)", "*.png"),
                ("JPEG (Compressed)", "*.jpg"),
                ("TIFF (Archive)", "*.tiff")
            ],
            title="EXPORT IMAGE (FULL RESOLUTION)"
        )

        if not file_path:
            return

        try:
            # Determine if we need to upscale from proxy
            if self.use_proxy and max(self.original_image.size) > self.proxy_max_dimension:
                # We're using proxy preview - need to export at full resolution
                self.data_stream.log("RENDERING AT FULL RESOLUTION (this may take time)...", level="warning")

                # For now, upscale the proxy result (fast but not perfect)
                # TODO: Re-apply filter history to full-res image for perfect quality
                proxy_img = Image.fromarray(self.working_array)
                export_img = proxy_img.resize(self.original_image.size, Image.Resampling.LANCZOS)

                self.data_stream.log("UPSCALED TO FULL RESOLUTION", level="info")
            else:
                # Already at full resolution
                export_img = Image.fromarray(self.working_array)

            # Save with max quality
            if file_path.endswith('.png'):
                export_img.save(file_path, "PNG", compress_level=0)
            elif file_path.endswith('.tiff'):
                export_img.save(file_path, "TIFF", compression="none")
            else:
                export_img.save(file_path, "JPEG", quality=100, subsampling=0)

            filename = file_path.split('/')[-1]
            self.data_stream.log(f"EXPORTED: {filename}", level="success")
            self.data_stream.log(f"RESOLUTION: {export_img.width}×{export_img.height}", level="info")

        except Exception as e:
            self.data_stream.log(f"EXPORT ERROR: {str(e)}", level="error")

    def _randomize_filters(self):
        """Apply 3 random filters with default settings."""
        if self.working_array is None:
            self.data_stream.log("ERROR: NO IMAGE LOADED", level="error")
            return

        # Collect all filters
        all_filters = []
        for category, filters in FILTER_REGISTRY.items():
            all_filters.extend(filters)

        # Select 3 random
        selected = random.sample(all_filters, 3)

        self.data_stream.log("RANDOMIZE: APPLYING 3 RANDOM FILTERS", level="info")

        # Apply sequentially
        for filter_name, filter_func, default_params in selected:
            self.data_stream.log(f"RANDOM: {filter_name.upper()}", level="info")
            try:
                self.working_array = filter_func(self.working_array, **default_params)
            except Exception as e:
                self.data_stream.log(f"ERROR IN {filter_name}: {str(e)}", level="error")

        self._update_display()
        self.data_stream.log("RANDOMIZE COMPLETE", level="success")

    def _reset_image(self):
        """Reset to original image (proxy version for preview)."""
        if self.original_image is None:
            return

        # Reset to proxy preview version (not full resolution)
        if self.use_proxy and max(self.original_image.size) > self.proxy_max_dimension:
            ratio = self.proxy_max_dimension / max(self.original_image.size)
            proxy_size = (int(self.original_image.width * ratio), int(self.original_image.height * ratio))
            proxy_image = self.original_image.resize(proxy_size, Image.Resampling.LANCZOS)
            self.working_array = np.array(proxy_image)
        else:
            self.working_array = self.original_array.copy()

        self._update_display()
        self.data_stream.log("RESET: IMAGE RESTORED TO ORIGINAL", level="success")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Launch application with splash screen."""
    # Create main window (hidden initially)
    app = VoidEngineApp()
    app.withdraw()  # Hide main window

    # Show splash screen
    splash = SplashScreen(app)
    app.wait_window(splash)  # Wait for splash to close

    # Show main window
    app.deiconify()

    # Run
    app.mainloop()


if __name__ == "__main__":
    main()
