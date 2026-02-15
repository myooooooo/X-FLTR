"""
NEURO-CORRUPT v2.0: Post-Digital Glitch Engine
==============================================
Master-Level Refactor: Glassmorphism UI + Retina-Optimized Display

Key Improvements:
- Fixed HiDPI/Retina display issues using CTkImage instead of ImageTk
- Separated Processing Logic from UI Logic for better performance
- Modern Dark-Mode Glassmorphism aesthetic
- Real-time preview with efficient image scaling
- System theme detection (Mac Light/Dark mode sync)
- Clean class-based architecture with proper separation of concerns

Author: MMI Student Portfolio Project
Framework: CustomTkinter 5.2+
"""

import customtkinter as ctk
from PIL import Image
import numpy as np
from tkinter import filedialog
import platform
import subprocess


# ============================================================================
# PROCESSING ENGINE (Separated from UI for Performance)
# ============================================================================

class GlitchProcessor:
    """
    Pure processing logic - no UI dependencies.
    This separation allows for:
    - Better testing (can test algorithms independently)
    - Potential CLI version or batch processing
    - Cleaner code organization
    """

    @staticmethod
    def bit_shift_glitch(image_array: np.ndarray, shift_amount: int) -> np.ndarray:
        """
        Bit-level manipulation using XOR operations.

        Technical explanation for oral presentation:
        - XOR (exclusive OR) flips bits at the binary level
        - When applied to pixel data, creates horizontal "tearing" artifacts
        - Higher shift_amount = more aggressive corruption

        Args:
            image_array: Numpy array of shape (H, W, 3) with dtype uint8
            shift_amount: Integer 0-255 for corruption intensity

        Returns:
            Corrupted image array with same shape and dtype
        """
        if shift_amount == 0:
            return image_array

        result = image_array.copy()
        result = np.bitwise_xor(result, shift_amount)
        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def channel_offset(
        image_array: np.ndarray,
        r_offset: int,
        g_offset: int,
        b_offset: int
    ) -> np.ndarray:
        """
        RGB channel separation - creates chromatic aberration.

        Technical explanation:
        - np.roll shifts array elements along an axis
        - Each color channel (R, G, B) is shifted independently
        - Mimics analog video artifacts and lens aberrations

        Args:
            image_array: Input image as numpy array
            r_offset, g_offset, b_offset: Horizontal shift in pixels (-100 to +100)

        Returns:
            Image with separated color channels
        """
        result = image_array.copy()

        if r_offset != 0:
            result[:, :, 0] = np.roll(result[:, :, 0], r_offset, axis=1)
        if g_offset != 0:
            result[:, :, 1] = np.roll(result[:, :, 1], g_offset, axis=1)
        if b_offset != 0:
            result[:, :, 2] = np.roll(result[:, :, 2], b_offset, axis=1)

        return result

    @staticmethod
    def pixel_sort(
        image_array: np.ndarray,
        threshold: int,
        direction: str = 'horizontal'
    ) -> np.ndarray:
        """
        Luminance-based pixel reorganization.

        Technical explanation:
        - Calculates brightness using standard ITU-R BT.601 formula
        - Sorts pixels above threshold by their luminance values
        - Creates "data-mosh" aesthetic without destroying image completely

        Args:
            image_array: Input image
            threshold: Brightness threshold 0-255 (only bright pixels get sorted)
            direction: 'horizontal' or 'vertical' sorting

        Returns:
            Image with sorted pixel regions
        """
        result = image_array.copy()

        # ITU-R BT.601 standard for luminance calculation
        luminance = (
            0.299 * result[:, :, 0] +
            0.587 * result[:, :, 1] +
            0.114 * result[:, :, 2]
        )

        if direction == 'horizontal':
            for row_idx in range(result.shape[0]):
                row = result[row_idx]
                lum_row = luminance[row_idx]

                # Find pixels above brightness threshold
                bright_mask = lum_row > threshold
                if np.any(bright_mask):
                    bright_indices = np.where(bright_mask)[0]

                    if len(bright_indices) > 0:
                        # Sort bright pixels by luminance
                        sorted_pixels = row[bright_indices]
                        sorted_lum = lum_row[bright_indices]
                        sort_order = np.argsort(sorted_lum)
                        result[row_idx][bright_indices] = sorted_pixels[sort_order]

        else:  # vertical
            for col_idx in range(result.shape[1]):
                col = result[:, col_idx]
                lum_col = luminance[:, col_idx]

                bright_mask = lum_col > threshold
                if np.any(bright_mask):
                    bright_indices = np.where(bright_mask)[0]

                    if len(bright_indices) > 0:
                        sorted_pixels = col[bright_indices]
                        sorted_lum = lum_col[bright_indices]
                        sort_order = np.argsort(sorted_lum)
                        result[:, col_idx][bright_indices] = sorted_pixels[sort_order]

        return result


# ============================================================================
# CONFIGURATION & THEME MANAGEMENT
# ============================================================================

class AppTheme:
    """
    Centralized theme configuration for consistent styling.

    GLASSMORPHISM PALETTE (Dark Mode):
    - Deep backgrounds with subtle transparency
    - Soft rounded corners (15px radius)
    - Neon accents for interactive elements
    - High contrast for accessibility
    """

    # Background Colors (Glassmorphism Base)
    BG_DARK = "#1A1B1E"          # Main background - Deep charcoal
    BG_GLASS = "#252730"         # Glass panels - Slightly lighter
    BG_GLASS_HOVER = "#2D2E38"   # Hover state for glass elements

    # Accent Colors (Cyber Neon)
    ACCENT_PRIMARY = "#6C63FF"   # Electric Purple - Primary actions
    ACCENT_SECONDARY = "#00D9FF" # Cyan - Secondary highlights
    ACCENT_SUCCESS = "#00FF88"   # Neon Green - Success states
    ACCENT_WARNING = "#FF6B6B"   # Coral Red - Warnings/Reset

    # Text Colors
    TEXT_PRIMARY = "#FFFFFF"     # Pure white - Headers
    TEXT_SECONDARY = "#B8B9BE"   # Light gray - Body text
    TEXT_MUTED = "#6B6C70"       # Dark gray - Hints/labels

    # UI Elements
    BORDER_SUBTLE = "#3A3B45"    # Subtle borders for glass effect
    BORDER_ACTIVE = "#6C63FF"    # Active element borders

    # Typography
    FONT_HEADING = ("SF Pro Display", 18, "bold")      # Mac native font
    FONT_BUTTON = ("SF Pro Text", 13, "bold")
    FONT_BODY = ("SF Pro Text", 12)
    FONT_MONO = ("SF Mono", 11)  # For technical values

    # Dimensions
    CORNER_RADIUS = 15
    BUTTON_HEIGHT = 44
    SLIDER_HEIGHT = 24


class SystemThemeDetector:
    """
    Detects macOS system theme (Light/Dark mode).
    Allows UI to sync with system preferences.
    """

    @staticmethod
    def get_macos_theme() -> str:
        """
        Query macOS for current appearance mode.

        Returns:
            'dark' or 'light' based on system preferences
        """
        if platform.system() != "Darwin":  # Not macOS
            return "dark"  # Default to dark

        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True
            )
            # If command succeeds and returns "Dark", system is in dark mode
            return "dark" if result.returncode == 0 else "light"
        except Exception:
            return "dark"  # Default to dark on error


# ============================================================================
# MAIN APPLICATION (Clean Class-Based Architecture)
# ============================================================================

class NeuroCorruptApp(ctk.CTk):
    """
    Main application window with glassmorphism UI.

    Architecture:
    - Sidebar navigation for tools/settings
    - Central canvas for real-time preview
    - Control panel with sliders for glitch parameters
    - Separation of concerns: UI logic vs. processing logic
    """

    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("NEURO-CORRUPT v2.0 — Glitch Engine")
        self.geometry("1600x1000")

        # Set theme based on system preference
        system_theme = SystemThemeDetector.get_macos_theme()
        ctk.set_appearance_mode(system_theme)

        # Application State
        self.original_image = None      # PIL Image - source
        self.original_array = None      # Numpy array - for processing
        self.processed_array = None     # Numpy array - after glitch effects
        self.display_image = None       # CTkImage - for HiDPI display

        # Glitch Parameters (separated from UI)
        self.params = {
            'bit_shift': 0,
            'r_offset': 0,
            'g_offset': 0,
            'b_offset': 0,
            'sort_threshold': 128,
            'sort_direction': 'horizontal'
        }

        # Build UI
        self._setup_layout()
        self._build_sidebar()
        self._build_main_panel()

    # ========================================================================
    # UI CONSTRUCTION
    # ========================================================================

    def _setup_layout(self):
        """Configure responsive grid layout."""
        self.grid_columnconfigure(1, weight=1)  # Main panel expands
        self.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        """
        Left sidebar with glassmorphism styling.
        Contains navigation, file operations, and control reset.
        """
        sidebar = ctk.CTkFrame(
            self,
            width=320,
            corner_radius=0,
            fg_color=AppTheme.BG_GLASS,
            border_width=1,
            border_color=AppTheme.BORDER_SUBTLE
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_propagate(False)

        # App Title
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(pady=(30, 20), padx=20, fill="x")

        ctk.CTkLabel(
            title_frame,
            text="NEURO-CORRUPT",
            font=("SF Pro Display", 24, "bold"),
            text_color=AppTheme.ACCENT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Post-Digital Glitch Engine",
            font=AppTheme.FONT_BODY,
            text_color=AppTheme.TEXT_MUTED
        ).pack(anchor="w")

        # Separator
        ctk.CTkFrame(
            sidebar,
            height=1,
            fg_color=AppTheme.BORDER_SUBTLE
        ).pack(fill="x", padx=20, pady=20)

        # File Operations Section
        self._create_section_label(sidebar, "File Operations")

        self._create_glass_button(
            sidebar,
            text="📁  Load Image",
            command=self._load_image,
            accent_color=AppTheme.ACCENT_PRIMARY
        ).pack(pady=5, padx=20, fill="x")

        self._create_glass_button(
            sidebar,
            text="💾  Export PNG",
            command=self._export_image,
            accent_color=AppTheme.ACCENT_SECONDARY
        ).pack(pady=5, padx=20, fill="x")

        # Spacer
        ctk.CTkFrame(sidebar, fg_color="transparent", height=20).pack()

        # Reset Section
        self._create_section_label(sidebar, "Controls")

        self._create_glass_button(
            sidebar,
            text="🔄  Reset All Parameters",
            command=self._reset_parameters,
            accent_color=AppTheme.ACCENT_WARNING
        ).pack(pady=5, padx=20, fill="x")

        # Info Footer
        info_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        info_frame.pack(side="bottom", pady=20, padx=20, fill="x")

        ctk.CTkLabel(
            info_frame,
            text="v2.0 • MMI Portfolio",
            font=("SF Mono", 10),
            text_color=AppTheme.TEXT_MUTED
        ).pack()

    def _build_main_panel(self):
        """
        Right panel with canvas and control sliders.
        Uses glassmorphism cards for each control group.
        """
        main_panel = ctk.CTkFrame(
            self,
            fg_color=AppTheme.BG_DARK,
            corner_radius=0
        )
        main_panel.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        main_panel.grid_columnconfigure(0, weight=1)
        main_panel.grid_rowconfigure(0, weight=1)

        # Top: Canvas Area
        self._build_canvas_area(main_panel)

        # Bottom: Controls
        self._build_controls_area(main_panel)

    def _build_canvas_area(self, parent):
        """
        Central preview canvas with glassmorphism card.
        Uses CTkImage for proper Retina/HiDPI scaling.
        """
        canvas_container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        canvas_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

        # Glass card for canvas
        canvas_card = ctk.CTkFrame(
            canvas_container,
            fg_color=AppTheme.BG_GLASS,
            corner_radius=AppTheme.CORNER_RADIUS,
            border_width=1,
            border_color=AppTheme.BORDER_SUBTLE
        )
        canvas_card.pack(fill="both", expand=True)

        # Status label
        self.status_label = ctk.CTkLabel(
            canvas_card,
            text="Load an image to begin",
            font=AppTheme.FONT_HEADING,
            text_color=AppTheme.TEXT_MUTED
        )
        self.status_label.pack(pady=30)

        # Canvas for image display
        # CRITICAL FOR RETINA/HiDPI:
        # We use CTkLabel to display CTkImage (not ImageTk.PhotoImage)
        # CTkImage automatically handles 2x scaling for Retina displays
        self.canvas_label = ctk.CTkLabel(
            canvas_card,
            text="",
            fg_color="transparent"
        )
        self.canvas_label.pack(expand=True, fill="both", padx=40, pady=40)

    def _build_controls_area(self, parent):
        """
        Control panel with glassmorphism cards for each effect category.
        """
        controls_container = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            height=280
        )
        controls_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 20))
        controls_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1: Bit Manipulation
        card1 = self._create_control_card(controls_container, "Bit Manipulation")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self._create_modern_slider(
            card1,
            label="Shift Amount",
            param_key='bit_shift',
            from_=0,
            to=255,
            color=AppTheme.ACCENT_PRIMARY
        )

        # Card 2: RGB Channel Separation
        card2 = self._create_control_card(controls_container, "RGB Separation")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self._create_modern_slider(
            card2,
            label="Red Offset",
            param_key='r_offset',
            from_=-100,
            to=100,
            color="#FF5555"
        )
        self._create_modern_slider(
            card2,
            label="Green Offset",
            param_key='g_offset',
            from_=-100,
            to=100,
            color="#55FF55"
        )
        self._create_modern_slider(
            card2,
            label="Blue Offset",
            param_key='b_offset',
            from_=-100,
            to=100,
            color="#5555FF"
        )

        # Card 3: Pixel Sorting
        card3 = self._create_control_card(controls_container, "Pixel Sorting")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self._create_modern_slider(
            card3,
            label="Threshold",
            param_key='sort_threshold',
            from_=0,
            to=255,
            color=AppTheme.ACCENT_SECONDARY
        )

        # Direction toggle
        direction_frame = ctk.CTkFrame(card3, fg_color="transparent")
        direction_frame.pack(pady=10, padx=15, fill="x")

        ctk.CTkLabel(
            direction_frame,
            text="Direction",
            font=AppTheme.FONT_BODY,
            text_color=AppTheme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 5))

        direction_var = ctk.StringVar(value="horizontal")

        btn_horizontal = ctk.CTkRadioButton(
            direction_frame,
            text="Horizontal",
            variable=direction_var,
            value="horizontal",
            font=AppTheme.FONT_BODY,
            text_color=AppTheme.TEXT_PRIMARY,
            fg_color=AppTheme.ACCENT_SECONDARY,
            hover_color=AppTheme.ACCENT_PRIMARY,
            command=lambda: self._update_param('sort_direction', 'horizontal')
        )
        btn_horizontal.pack(side="left", padx=5)

        btn_vertical = ctk.CTkRadioButton(
            direction_frame,
            text="Vertical",
            variable=direction_var,
            value="vertical",
            font=AppTheme.FONT_BODY,
            text_color=AppTheme.TEXT_PRIMARY,
            fg_color=AppTheme.ACCENT_SECONDARY,
            hover_color=AppTheme.ACCENT_PRIMARY,
            command=lambda: self._update_param('sort_direction', 'vertical')
        )
        btn_vertical.pack(side="left", padx=5)

    # ========================================================================
    # UI COMPONENT FACTORIES (Glassmorphism Styling)
    # ========================================================================

    def _create_section_label(self, parent, text):
        """Section header for sidebar."""
        label = ctk.CTkLabel(
            parent,
            text=text.upper(),
            font=("SF Mono", 11, "bold"),
            text_color=AppTheme.TEXT_MUTED,
            anchor="w"
        )
        label.pack(pady=(10, 8), padx=20, fill="x")
        return label

    def _create_glass_button(self, parent, text, command, accent_color):
        """
        Glassmorphism button with hover effects.

        Key features:
        - Transparent background with border
        - Smooth color transition on hover
        - Rounded corners for modern feel
        """
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=AppTheme.FONT_BUTTON,
            fg_color="transparent",
            hover_color=AppTheme.BG_GLASS_HOVER,
            border_width=2,
            border_color=accent_color,
            text_color=accent_color,
            corner_radius=AppTheme.CORNER_RADIUS,
            height=AppTheme.BUTTON_HEIGHT
        )

    def _create_control_card(self, parent, title):
        """
        Glassmorphism card for grouping related controls.
        """
        card = ctk.CTkFrame(
            parent,
            fg_color=AppTheme.BG_GLASS,
            corner_radius=AppTheme.CORNER_RADIUS,
            border_width=1,
            border_color=AppTheme.BORDER_SUBTLE
        )

        # Card title
        ctk.CTkLabel(
            card,
            text=title,
            font=("SF Pro Display", 16, "bold"),
            text_color=AppTheme.TEXT_PRIMARY
        ).pack(pady=(15, 10), padx=15, anchor="w")

        return card

    def _create_modern_slider(self, parent, label, param_key, from_, to, color):
        """
        Modern slider with real-time value display.

        CRITICAL: Uses CustomTkinter's native slider styling
        - Smooth animations
        - Hover effects
        - Custom accent colors per slider
        """
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(pady=8, padx=15, fill="x")

        # Label with live value
        value_label = ctk.CTkLabel(
            container,
            text=f"{label}: {self.params[param_key]}",
            font=AppTheme.FONT_BODY,
            text_color=AppTheme.TEXT_SECONDARY
        )
        value_label.pack(anchor="w")

        # Slider
        slider = ctk.CTkSlider(
            container,
            from_=from_,
            to=to,
            number_of_steps=int(to - from_),
            command=lambda v: self._on_slider_change(
                param_key, v, value_label, label
            ),
            button_color=color,
            button_hover_color=AppTheme.TEXT_PRIMARY,
            progress_color=color,
            fg_color=AppTheme.BG_DARK,
            height=AppTheme.SLIDER_HEIGHT,
            corner_radius=AppTheme.CORNER_RADIUS
        )
        slider.set(self.params[param_key])
        slider.pack(fill="x", pady=(5, 0))

    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    def _on_slider_change(self, param_key, value, label_widget, label_text):
        """
        Handle slider changes with real-time preview update.

        Performance optimization:
        - Only processes if image is loaded
        - Updates single parameter, not entire state
        """
        value = int(value)
        self.params[param_key] = value
        label_widget.configure(text=f"{label_text}: {value}")

        if self.original_array is not None:
            self._process_and_display()

    def _update_param(self, key, value):
        """Update parameter and trigger reprocessing."""
        self.params[key] = value
        if self.original_array is not None:
            self._process_and_display()

    def _load_image(self):
        """
        Load image with proper Retina/HiDPI handling.
        """
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            # Load as PIL Image (high quality)
            self.original_image = Image.open(file_path).convert('RGB')
            self.original_array = np.array(self.original_image)

            # Update status
            filename = file_path.split('/')[-1]
            self.status_label.configure(
                text=f"Loaded: {filename}",
                text_color=AppTheme.ACCENT_SUCCESS
            )

            # Initial display
            self._process_and_display()

        except Exception as e:
            self.status_label.configure(
                text=f"Error loading image: {str(e)}",
                text_color=AppTheme.ACCENT_WARNING
            )

    def _process_and_display(self):
        """
        Apply glitch effects pipeline and update canvas.

        CRITICAL FOR RETINA/HiDPI DISPLAYS:

        The Problem:
        - PIL's ImageTk.PhotoImage doesn't handle high-DPI scaling
        - Results in blurry images on Retina displays
        - Generates tkinter warnings about scaling

        The Solution:
        - Use CustomTkinter's CTkImage class
        - Automatically handles @2x scaling on Retina displays
        - Specify both light_image and dark_image (can be same)
        - Set explicit size=(width, height) for proper scaling
        - CTkImage creates appropriate @2x assets internally

        How it works for oral presentation:
        1. Process image as numpy array (full resolution)
        2. Convert to PIL Image
        3. Calculate display dimensions (fit to canvas)
        4. Create CTkImage with size parameter
        5. CTkImage handles HiDPI scaling automatically
        6. Display via CTkLabel (not tkinter Label)
        """
        if self.original_array is None:
            return

        # Apply effects pipeline (using separated processor)
        result = self.original_array.copy()
        result = GlitchProcessor.bit_shift_glitch(result, self.params['bit_shift'])
        result = GlitchProcessor.channel_offset(
            result,
            self.params['r_offset'],
            self.params['g_offset'],
            self.params['b_offset']
        )
        result = GlitchProcessor.pixel_sort(
            result,
            self.params['sort_threshold'],
            self.params['sort_direction']
        )

        self.processed_array = result
        pil_image = Image.fromarray(result)

        # Calculate display size (maintain aspect ratio)
        canvas_width = self.canvas_label.winfo_width()
        canvas_height = self.canvas_label.winfo_height()

        # Fallback if canvas not rendered yet
        if canvas_width <= 1:
            canvas_width, canvas_height = 1000, 600

        img_ratio = pil_image.width / pil_image.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            display_width = int(canvas_width * 0.9)
            display_height = int(display_width / img_ratio)
        else:
            display_height = int(canvas_height * 0.9)
            display_width = int(display_height * img_ratio)

        # CRITICAL: Use CTkImage for Retina/HiDPI support
        # This is what fixes the blurry display issue!
        self.display_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=(display_width, display_height)  # Explicit size for scaling
        )

        # Update canvas
        self.canvas_label.configure(image=self.display_image)
        self.status_label.configure(text="")  # Hide status when image shown

    def _export_image(self):
        """Export processed image at full resolution."""
        if self.processed_array is None:
            self.status_label.configure(
                text="No image to export",
                text_color=AppTheme.ACCENT_WARNING
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg"),
                ("All Files", "*.*")
            ],
            title="Export Glitched Image"
        )

        if not file_path:
            return

        try:
            # Export at full resolution (not scaled-down display version)
            export_image = Image.fromarray(self.processed_array)
            export_image.save(file_path, quality=100)

            filename = file_path.split('/')[-1]
            self.status_label.configure(
                text=f"Exported: {filename}",
                text_color=AppTheme.ACCENT_SUCCESS
            )

        except Exception as e:
            self.status_label.configure(
                text=f"Export failed: {str(e)}",
                text_color=AppTheme.ACCENT_WARNING
            )

    def _reset_parameters(self):
        """Reset all glitch parameters to defaults."""
        self.params = {
            'bit_shift': 0,
            'r_offset': 0,
            'g_offset': 0,
            'b_offset': 0,
            'sort_threshold': 128,
            'sort_direction': 'horizontal'
        }

        if self.original_array is not None:
            self._process_and_display()

        # Rebuild controls to reset slider positions
        # (In production, would use slider.set() instead of rebuilding)
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        self._setup_layout()
        self._build_sidebar()
        self._build_main_panel()

        # Reload image if one was loaded
        if self.original_array is not None:
            self._process_and_display()


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize and run
    app = NeuroCorruptApp()
    app.mainloop()
