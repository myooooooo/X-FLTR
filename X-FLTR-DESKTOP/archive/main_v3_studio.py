"""
NEURO-CORRUPT v3.0 STUDIO: Advanced Aesthetic Engine
=====================================================
The Professional Creative Tool with Pointillism, Film Grain, and Neon Edges

NEW FEATURES:
- Pointillism filter (circle-based rendering by luminance)
- Film grain overlay for tactile texture
- Neon edge detection mode
- Threaded processing (no UI freeze)
- 4K export capability
- Dynamic border glow (matches dominant image color)
- Icon-based minimalist sliders (pro interface)

Author: MMI Student Portfolio Project
Framework: CustomTkinter 5.2+ with PIL/Pillow and Threading
"""

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageStat
import numpy as np
from tkinter import filedialog
import threading
import random
from typing import Optional, Tuple
import colorsys


# ============================================================================
# ADVANCED PROCESSING ENGINE (Pure Logic - Separated from UI)
# ============================================================================

class AestheticProcessor:
    """
    Advanced image processing algorithms for creative effects.
    All methods are static for easy testing and potential CLI usage.
    """

    @staticmethod
    def bit_shift_glitch(image_array: np.ndarray, shift_amount: int) -> np.ndarray:
        """Binary-level corruption using XOR operations."""
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
        """RGB chromatic aberration effect."""
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
        """Luminance-based pixel reorganization."""
        result = image_array.copy()
        luminance = (
            0.299 * result[:, :, 0] +
            0.587 * result[:, :, 1] +
            0.114 * result[:, :, 2]
        )

        if direction == 'horizontal':
            for row_idx in range(result.shape[0]):
                row = result[row_idx]
                lum_row = luminance[row_idx]
                bright_mask = lum_row > threshold
                if np.any(bright_mask):
                    bright_indices = np.where(bright_mask)[0]
                    if len(bright_indices) > 0:
                        sorted_pixels = row[bright_indices]
                        sorted_lum = lum_row[bright_indices]
                        sort_order = np.argsort(sorted_lum)
                        result[row_idx][bright_indices] = sorted_pixels[sort_order]
        else:
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

    @staticmethod
    def pointillism_filter(
        pil_image: Image.Image,
        dot_size_range: Tuple[int, int] = (2, 12),
        density: float = 0.5
    ) -> Image.Image:
        """
        POINTILLISM ALGORITHM - Technical Explanation for MMI Jury:

        Mathematical Process:
        1. SAMPLING GRID: Divide image into grid based on density parameter
           - Grid spacing = 1/density (e.g., density=0.5 → sample every 2 pixels)
           - This creates a sparse sampling pattern (not every pixel)

        2. LUMINANCE CALCULATION: For each sample point (x, y):
           - Extract RGB values: pixel = image[x, y] → (R, G, B)
           - Calculate perceived brightness using ITU-R BT.601 standard:
             Luminance = 0.299*R + 0.587*G + 0.114*B
           - Range: 0 (black) to 255 (white)

        3. DOT SIZE MAPPING: Map luminance to circle radius
           - Bright pixels → smaller dots (preserve detail)
           - Dark pixels → larger dots (fill space, create contrast)
           - Formula: radius = max_radius - (luminance/255) * (max_radius - min_radius)
           - This creates an inverse relationship (darker = bigger)

        4. RENDERING: Draw circles using Pillow's ImageDraw
           - Create blank canvas (white background)
           - For each sampled point:
               * Calculate dot radius based on luminance
               * Draw filled circle at (x, y) with original color
           - Overlapping circles create organic texture

        Artistic Effect:
        - Mimics Pointillism painting technique (Seurat, Signac)
        - Reduces image to colored dots while maintaining recognizability
        - Creates tactile, printed aesthetic (newspaper halftone)

        Performance Considerations:
        - Sampling density controls computation time
        - Lower density = faster (fewer dots to draw)
        - Threaded processing prevents UI freeze
        """
        # Create white canvas
        canvas = Image.new('RGB', pil_image.size, 'white')
        draw = ImageDraw.Draw(canvas)

        width, height = pil_image.size
        pixels = pil_image.load()

        # Calculate sampling step based on density
        step = int(1 / density) if density > 0 else 2

        min_dot, max_dot = dot_size_range

        # Sample grid and draw dots
        for y in range(0, height, step):
            for x in range(0, width, step):
                try:
                    # Get pixel color at sample point
                    color = pixels[x, y]

                    # Calculate luminance (perceived brightness)
                    luminance = (
                        0.299 * color[0] +
                        0.587 * color[1] +
                        0.114 * color[2]
                    )

                    # Map luminance to dot size (inverse relationship)
                    # Darker pixels → larger dots
                    normalized_lum = luminance / 255.0
                    radius = max_dot - (normalized_lum * (max_dot - min_dot))
                    radius = int(radius)

                    # Draw filled circle at sample point
                    if radius > 0:
                        draw.ellipse(
                            [(x - radius, y - radius), (x + radius, y + radius)],
                            fill=color,
                            outline=None
                        )
                except IndexError:
                    continue

        return canvas

    @staticmethod
    def film_grain_overlay(
        pil_image: Image.Image,
        intensity: float = 0.3
    ) -> Image.Image:
        """
        Add analog film grain texture.

        Process:
        1. Generate random noise pattern (uniform distribution)
        2. Scale noise by intensity parameter
        3. Blend with original image using additive mode
        4. Clip values to valid range [0, 255]

        Artistic Effect:
        - Simulates analog photography grain
        - Adds tactile, organic feel to digital images
        - Reduces "too clean" digital look
        """
        img_array = np.array(pil_image).astype(np.float32)

        # Generate grain noise
        noise = np.random.uniform(
            -intensity * 255,
            intensity * 255,
            img_array.shape
        )

        # Add grain to image
        grainy = img_array + noise
        grainy = np.clip(grainy, 0, 255).astype(np.uint8)

        return Image.fromarray(grainy)

    @staticmethod
    def neon_edge_detection(
        pil_image: Image.Image,
        neon_color: Tuple[int, int, int] = (0, 255, 255)  # Cyan
    ) -> Image.Image:
        """
        Extract edges and tint with neon glow.

        Process:
        1. Convert to grayscale (edges are luminance-based)
        2. Apply Pillow's FIND_EDGES filter (Sobel-like operator)
        3. Enhance edge contrast
        4. Tint edges with specified neon color
        5. Composite over darkened original (for glow effect)

        Artistic Effect:
        - Cyberpunk/neon aesthetic
        - Emphasizes structure and form
        - Creates "glowing outline" look
        """
        # Detect edges
        edges = pil_image.convert('L').filter(ImageFilter.FIND_EDGES)

        # Enhance edge contrast
        edges = ImageEnhance.Contrast(edges).enhance(2.0)

        # Create neon-tinted version
        neon_img = Image.new('RGB', pil_image.size, (0, 0, 0))
        neon_draw = ImageDraw.Draw(neon_img)

        edge_pixels = edges.load()
        width, height = edges.size

        for y in range(height):
            for x in range(width):
                edge_intensity = edge_pixels[x, y]
                if edge_intensity > 50:  # Threshold for visible edges
                    # Scale neon color by edge intensity
                    alpha = edge_intensity / 255.0
                    tinted_color = tuple(int(c * alpha) for c in neon_color)
                    neon_draw.point((x, y), fill=tinted_color)

        # Darken original and composite edges
        darkened = ImageEnhance.Brightness(pil_image).enhance(0.3)
        return Image.blend(darkened, neon_img, 0.7)


# ============================================================================
# THEME & CONFIGURATION
# ============================================================================

class StudioTheme:
    """Professional studio interface color palette."""

    # Glassmorphism backgrounds
    BG_DARK = "#0F0F12"
    BG_GLASS = "#1C1C22"
    BG_GLASS_LIGHT = "#25252C"

    # Professional accents
    ACCENT_PRIMARY = "#8B5CF6"      # Violet
    ACCENT_SECONDARY = "#10B981"    # Emerald
    ACCENT_NEON = "#06B6D4"         # Cyan
    ACCENT_WARM = "#F59E0B"         # Amber

    # Text colors
    TEXT_PRIMARY = "#FAFAFA"
    TEXT_SECONDARY = "#A1A1AA"
    TEXT_MUTED = "#52525B"

    # UI elements
    BORDER_SUBTLE = "#27272A"
    BORDER_GLOW = "#8B5CF6"

    # Typography
    FONT_HEADING = ("SF Pro Display", 20, "bold")
    FONT_LABEL = ("SF Pro Text", 11)
    FONT_MONO = ("SF Mono", 10)

    CORNER_RADIUS = 16
    BUTTON_HEIGHT = 48


# ============================================================================
# MAIN STUDIO APPLICATION
# ============================================================================

class NeuroCorruptStudio(ctk.CTk):
    """
    Professional creative tool with advanced aesthetic filters.

    NEW FEATURES v3.0:
    - Pointillism rendering
    - Film grain overlay
    - Neon edge detection
    - Threaded processing (no UI freeze)
    - 4K export
    - Dynamic canvas border glow
    """

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("NEURO-CORRUPT STUDIO — v3.0")
        self.geometry("1800x1100")
        ctk.set_appearance_mode("dark")

        # State
        self.original_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None
        self.display_ctk_image: Optional[ctk.CTkImage] = None
        self.is_processing = False

        # Parameters
        self.params = {
            # Glitch effects
            'bit_shift': 0,
            'r_offset': 0,
            'g_offset': 0,
            'b_offset': 0,
            'sort_threshold': 128,
            'sort_direction': 'horizontal',

            # Aesthetic effects (NEW)
            'pointillism': 0,           # 0 = off, 1-100 = intensity
            'film_grain': 0,            # 0 = off, 1-100 = intensity
            'neon_edges': False         # Boolean toggle
        }

        # Build UI
        self._setup_layout()
        self._build_interface()

    def _setup_layout(self):
        """Configure responsive grid."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _build_interface(self):
        """Construct studio interface."""
        self._build_sidebar()
        self._build_main_canvas()
        self._build_control_panel()

    # ========================================================================
    # SIDEBAR (Glassmorphism Navigation)
    # ========================================================================

    def _build_sidebar(self):
        """Semi-transparent glassmorphism sidebar."""
        sidebar = ctk.CTkFrame(
            self,
            width=280,
            fg_color=StudioTheme.BG_GLASS,
            corner_radius=0,
            border_width=1,
            border_color=StudioTheme.BORDER_SUBTLE
        )
        sidebar.grid(row=0, column=0, sticky="nsew", rowspan=2)
        sidebar.grid_propagate(False)

        # Studio branding
        brand_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand_frame.pack(pady=(40, 30), padx=24)

        ctk.CTkLabel(
            brand_frame,
            text="STUDIO",
            font=("SF Pro Display", 28, "bold"),
            text_color=StudioTheme.ACCENT_PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_frame,
            text="Advanced Aesthetic Engine",
            font=StudioTheme.FONT_LABEL,
            text_color=StudioTheme.TEXT_MUTED
        ).pack(anchor="w", pady=(4, 0))

        # Separator
        ctk.CTkFrame(
            sidebar,
            height=1,
            fg_color=StudioTheme.BORDER_SUBTLE
        ).pack(fill="x", padx=24, pady=24)

        # File operations
        self._add_section_header(sidebar, "PROJECT")

        self._create_studio_button(
            sidebar,
            text="⬆  Load Image",
            command=self._load_image,
            color=StudioTheme.ACCENT_PRIMARY
        ).pack(pady=6, padx=24, fill="x")

        self._create_studio_button(
            sidebar,
            text="⬇  Save Artwork (4K)",
            command=self._export_4k,
            color=StudioTheme.ACCENT_NEON
        ).pack(pady=6, padx=24, fill="x")

        # Spacer
        ctk.CTkFrame(sidebar, fg_color="transparent", height=32).pack()

        # Aesthetic toggles
        self._add_section_header(sidebar, "EFFECTS")

        # Neon edges toggle
        self.neon_var = ctk.BooleanVar(value=False)
        neon_toggle = ctk.CTkSwitch(
            sidebar,
            text="Neon Edge Detection",
            variable=self.neon_var,
            command=self._toggle_neon_edges,
            font=StudioTheme.FONT_LABEL,
            text_color=StudioTheme.TEXT_SECONDARY,
            fg_color=StudioTheme.ACCENT_NEON,
            progress_color=StudioTheme.ACCENT_PRIMARY,
            button_color=StudioTheme.TEXT_PRIMARY,
            button_hover_color=StudioTheme.ACCENT_WARM
        )
        neon_toggle.pack(pady=8, padx=24, anchor="w")

        # Reset
        ctk.CTkFrame(sidebar, fg_color="transparent").pack(expand=True)

        self._create_studio_button(
            sidebar,
            text="↻  Reset All",
            command=self._reset_all,
            color=StudioTheme.TEXT_MUTED
        ).pack(pady=24, padx=24, fill="x", side="bottom")

    def _add_section_header(self, parent, text):
        """Minimalist section label."""
        ctk.CTkLabel(
            parent,
            text=text,
            font=("SF Mono", 10, "bold"),
            text_color=StudioTheme.TEXT_MUTED,
            anchor="w"
        ).pack(pady=(16, 8), padx=24, fill="x")

    def _create_studio_button(self, parent, text, command, color):
        """Professional glass button."""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=("SF Pro Text", 14, "bold"),
            fg_color="transparent",
            hover_color=StudioTheme.BG_GLASS_LIGHT,
            border_width=2,
            border_color=color,
            text_color=color,
            corner_radius=StudioTheme.CORNER_RADIUS,
            height=StudioTheme.BUTTON_HEIGHT
        )

    # ========================================================================
    # MAIN CANVAS (Dynamic Border Glow)
    # ========================================================================

    def _build_main_canvas(self):
        """Canvas with dynamic border glow matching image dominant color."""
        canvas_container = ctk.CTkFrame(
            self,
            fg_color=StudioTheme.BG_DARK
        )
        canvas_container.grid(row=0, column=1, sticky="nsew", padx=24, pady=(24, 12))

        # Canvas card with dynamic border
        self.canvas_card = ctk.CTkFrame(
            canvas_container,
            fg_color=StudioTheme.BG_GLASS,
            corner_radius=StudioTheme.CORNER_RADIUS,
            border_width=3,
            border_color=StudioTheme.BORDER_SUBTLE  # Will update dynamically
        )
        self.canvas_card.pack(fill="both", expand=True)

        # Status label
        self.status_label = ctk.CTkLabel(
            self.canvas_card,
            text="Load an image to begin creating",
            font=StudioTheme.FONT_HEADING,
            text_color=StudioTheme.TEXT_MUTED
        )
        self.status_label.pack(pady=40)

        # Canvas for CTkImage display
        self.canvas_label = ctk.CTkLabel(
            self.canvas_card,
            text="",
            fg_color="transparent"
        )
        self.canvas_label.pack(expand=True, fill="both", padx=48, pady=48)

    # ========================================================================
    # CONTROL PANEL (Icon-Based Minimalist Sliders)
    # ========================================================================

    def _build_control_panel(self):
        """Bottom control panel with icon-based sliders."""
        controls_bg = ctk.CTkFrame(
            self,
            fg_color=StudioTheme.BG_DARK
        )
        controls_bg.grid(row=1, column=1, sticky="ew", padx=24, pady=(12, 24))

        # Scrollable container
        controls = ctk.CTkScrollableFrame(
            controls_bg,
            fg_color="transparent",
            height=260
        )
        controls.pack(fill="both", expand=True)
        controls.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Card 1: Glitch - Bit Manipulation
        card1 = self._create_control_card(controls, "⚡ Glitch")
        card1.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        self._create_icon_slider(card1, "💥", 'bit_shift', 0, 255)

        # Card 2: RGB Separation
        card2 = self._create_control_card(controls, "🌈 RGB Split")
        card2.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        self._create_icon_slider(card2, "🔴", 'r_offset', -100, 100)
        self._create_icon_slider(card2, "🟢", 'g_offset', -100, 100)
        self._create_icon_slider(card2, "🔵", 'b_offset', -100, 100)

        # Card 3: Pixel Sorting
        card3 = self._create_control_card(controls, "📊 Pixel Sort")
        card3.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")
        self._create_icon_slider(card3, "🔆", 'sort_threshold', 0, 255)

        # Card 4: NEW - Aesthetic Filters
        card4 = self._create_control_card(controls, "🎨 Aesthetic")
        card4.grid(row=0, column=3, padx=8, pady=8, sticky="nsew")
        self._create_icon_slider(card4, "⚪", 'pointillism', 0, 100, label="Pointillism")
        self._create_icon_slider(card4, "📽", 'film_grain', 0, 100, label="Film Grain")

    def _create_control_card(self, parent, title):
        """Glass card for controls."""
        card = ctk.CTkFrame(
            parent,
            fg_color=StudioTheme.BG_GLASS,
            corner_radius=StudioTheme.CORNER_RADIUS,
            border_width=1,
            border_color=StudioTheme.BORDER_SUBTLE
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("SF Pro Text", 15, "bold"),
            text_color=StudioTheme.TEXT_PRIMARY
        ).pack(pady=(16, 12), padx=16, anchor="w")

        return card

    def _create_icon_slider(
        self,
        parent,
        icon: str,
        param_key: str,
        from_: int,
        to: int,
        label: str = ""
    ):
        """
        Minimalist slider with icon (no verbose labels).
        Pro interface style like Lightroom/Capture One.
        """
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(pady=6, padx=16, fill="x")

        # Icon + value label
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text=icon,
            font=("SF Pro Text", 16)
        ).pack(side="left")

        value_label = ctk.CTkLabel(
            header,
            text=f"{self.params[param_key]}",
            font=StudioTheme.FONT_MONO,
            text_color=StudioTheme.TEXT_SECONDARY
        )
        value_label.pack(side="right")

        if label:
            ctk.CTkLabel(
                header,
                text=label,
                font=StudioTheme.FONT_LABEL,
                text_color=StudioTheme.TEXT_SECONDARY
            ).pack(side="left", padx=(8, 0))

        # Slider
        slider = ctk.CTkSlider(
            container,
            from_=from_,
            to=to,
            number_of_steps=to - from_,
            command=lambda v: self._on_slider_change(param_key, v, value_label),
            button_color=StudioTheme.ACCENT_PRIMARY,
            button_hover_color=StudioTheme.ACCENT_WARM,
            progress_color=StudioTheme.ACCENT_PRIMARY,
            fg_color=StudioTheme.BG_DARK,
            height=20,
            corner_radius=10
        )
        slider.set(self.params[param_key])
        slider.pack(fill="x", pady=(4, 0))

    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    def _on_slider_change(self, param_key, value, label_widget):
        """Update parameter and trigger threaded processing."""
        value = int(value)
        self.params[param_key] = value
        label_widget.configure(text=f"{value}")

        if self.original_image and not self.is_processing:
            self._process_threaded()

    def _toggle_neon_edges(self):
        """Toggle neon edge detection."""
        self.params['neon_edges'] = self.neon_var.get()
        if self.original_image and not self.is_processing:
            self._process_threaded()

    def _load_image(self):
        """Load image file."""
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
            self.original_image = Image.open(file_path).convert('RGB')
            filename = file_path.split('/')[-1]
            self.status_label.configure(
                text=f"Loaded: {filename}",
                text_color=StudioTheme.ACCENT_SECONDARY
            )
            self._process_threaded()

        except Exception as e:
            self.status_label.configure(
                text=f"Error: {str(e)}",
                text_color=StudioTheme.ACCENT_WARM
            )

    def _process_threaded(self):
        """
        Process image in background thread to prevent UI freeze.

        CRITICAL for heavy operations like Pointillism:
        - Drawing thousands of circles takes time
        - Without threading, UI would freeze
        - User can't interact during processing
        - Threading keeps app responsive
        """
        if self.is_processing:
            return

        self.is_processing = True
        self.status_label.configure(
            text="Processing...",
            text_color=StudioTheme.TEXT_MUTED
        )

        # Run processing in separate thread
        thread = threading.Thread(target=self._process_pipeline)
        thread.daemon = True
        thread.start()

    def _process_pipeline(self):
        """
        Full processing pipeline (runs in background thread).

        Order matters:
        1. Glitch effects (bit shift, channels, sorting)
        2. Aesthetic effects (pointillism, grain, edges)
        3. Update display on main thread
        """
        try:
            result = self.original_image.copy()

            # Convert to array for glitch effects
            result_array = np.array(result)

            # Apply glitch effects
            result_array = AestheticProcessor.bit_shift_glitch(
                result_array,
                self.params['bit_shift']
            )
            result_array = AestheticProcessor.channel_offset(
                result_array,
                self.params['r_offset'],
                self.params['g_offset'],
                self.params['b_offset']
            )
            result_array = AestheticProcessor.pixel_sort(
                result_array,
                self.params['sort_threshold'],
                self.params['sort_direction']
            )

            # Convert back to PIL for aesthetic effects
            result = Image.fromarray(result_array)

            # Apply NEW aesthetic effects
            if self.params['pointillism'] > 0:
                density = self.params['pointillism'] / 100.0
                result = AestheticProcessor.pointillism_filter(
                    result,
                    dot_size_range=(1, 8),
                    density=density * 0.3  # Scale for performance
                )

            if self.params['film_grain'] > 0:
                intensity = self.params['film_grain'] / 100.0
                result = AestheticProcessor.film_grain_overlay(result, intensity * 0.5)

            if self.params['neon_edges']:
                result = AestheticProcessor.neon_edge_detection(result)

            self.processed_image = result

            # Update UI on main thread
            self.after(0, self._update_display)

        except Exception as e:
            print(f"Processing error: {e}")
            self.after(0, lambda: self.status_label.configure(
                text=f"Processing failed: {str(e)}",
                text_color=StudioTheme.ACCENT_WARM
            ))

        finally:
            self.is_processing = False

    def _update_display(self):
        """
        Update canvas with processed image.
        Uses CTkImage for Retina/HiDPI support.
        """
        if not self.processed_image:
            return

        # Calculate display size
        canvas_width = self.canvas_label.winfo_width()
        canvas_height = self.canvas_label.winfo_height()

        if canvas_width <= 1:
            canvas_width, canvas_height = 1200, 700

        img_ratio = self.processed_image.width / self.processed_image.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            display_width = int(canvas_width * 0.85)
            display_height = int(display_width / img_ratio)
        else:
            display_height = int(canvas_height * 0.85)
            display_width = int(display_height * img_ratio)

        # Use CTkImage for sharp Retina display
        self.display_ctk_image = ctk.CTkImage(
            light_image=self.processed_image,
            dark_image=self.processed_image,
            size=(display_width, display_height)
        )

        self.canvas_label.configure(image=self.display_ctk_image)
        self.status_label.configure(text="")

        # Update border glow with dominant color
        self._update_border_glow()

    def _update_border_glow(self):
        """
        Dynamic border glow matching image dominant color.

        Process:
        1. Calculate average RGB from entire image
        2. Convert to hex color
        3. Update canvas border color
        4. Creates visual connection between content and UI
        """
        if not self.processed_image:
            return

        try:
            # Get dominant color (mean RGB values)
            stat = ImageStat.Stat(self.processed_image)
            avg_color = stat.mean

            # Convert to hex
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(avg_color[0]),
                int(avg_color[1]),
                int(avg_color[2])
            )

            # Update border
            self.canvas_card.configure(border_color=hex_color)

        except Exception as e:
            print(f"Border glow update failed: {e}")

    def _export_4k(self):
        """
        Export at 4K resolution (3840×2160) or original resolution if larger.

        CRITICAL: Exports processed_image at full resolution,
        not the scaled-down display version.
        """
        if not self.processed_image:
            self.status_label.configure(
                text="No artwork to export",
                text_color=StudioTheme.ACCENT_WARM
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG (High Quality)", "*.png"),
                ("JPEG", "*.jpg"),
                ("TIFF (Lossless)", "*.tiff")
            ],
            title="Save Artwork"
        )

        if not file_path:
            return

        try:
            # Determine export size
            original_w, original_h = self.processed_image.size

            # If image is smaller than 4K, upscale; otherwise keep original
            target_4k = (3840, 2160)
            if original_w < target_4k[0] or original_h < target_4k[1]:
                # Upscale to 4K maintaining aspect ratio
                aspect = original_w / original_h
                if aspect > target_4k[0] / target_4k[1]:
                    export_size = (target_4k[0], int(target_4k[0] / aspect))
                else:
                    export_size = (int(target_4k[1] * aspect), target_4k[1])

                export_image = self.processed_image.resize(
                    export_size,
                    Image.Resampling.LANCZOS
                )
            else:
                # Keep original resolution
                export_image = self.processed_image

            # Export with maximum quality
            if file_path.endswith('.png'):
                export_image.save(file_path, "PNG", compress_level=0)
            elif file_path.endswith('.tiff'):
                export_image.save(file_path, "TIFF", compression="none")
            else:
                export_image.save(file_path, "JPEG", quality=100, subsampling=0)

            filename = file_path.split('/')[-1]
            self.status_label.configure(
                text=f"Saved: {filename} ({export_image.width}×{export_image.height})",
                text_color=StudioTheme.ACCENT_SECONDARY
            )

        except Exception as e:
            self.status_label.configure(
                text=f"Export failed: {str(e)}",
                text_color=StudioTheme.ACCENT_WARM
            )

    def _reset_all(self):
        """Reset all parameters to defaults."""
        self.params = {
            'bit_shift': 0,
            'r_offset': 0,
            'g_offset': 0,
            'b_offset': 0,
            'sort_threshold': 128,
            'sort_direction': 'horizontal',
            'pointillism': 0,
            'film_grain': 0,
            'neon_edges': False
        }
        self.neon_var.set(False)

        if self.original_image:
            self._process_threaded()

        # Rebuild controls to reset sliders
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        self._setup_layout()
        self._build_interface()

        if self.original_image:
            self._process_threaded()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app = NeuroCorruptStudio()
    app.mainloop()
