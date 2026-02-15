"""
NEURO-CORRUPT EXPERIMENTAL: The Anti-UI Edition
================================================
A Radical Critique of Standardized Interface Design

PHILOSOPHY:
This application rejects conventional GUI paradigms in favor of a
"command-center" aesthetic that foregrounds technical complexity and
manual control. Influenced by:
- Brutalist web design (raw HTML, no decoration)
- Music production DAWs (knobs, faders, technical interfaces)
- Hacker terminals (scrolling data streams, command logs)
- Anti-design movement (rejection of user-friendliness as infantilization)

NEW EXPERIMENTAL FILTERS:
- ASCII Glitch (text-based image representation)
- Reaction-Diffusion (Gray-Scott model simulation)
- Chromatic Prism Shift (chaos-based RGB displacement)
- Bayer Dithering (1980s 8-bit quantization)

UI PHILOSOPHY:
No buttons → Command nodes
No sliders → Circular knobs + vertical faders
No tooltips → You learn by experimentation
Data stream → Every operation is logged in real-time

Author: MMI Student — Experimental Media Project
"""

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from tkinter import filedialog
import threading
import time
import math
from typing import Optional, Tuple
from collections import deque


# ============================================================================
# EXPERIMENTAL PROCESSING ENGINE
# ============================================================================

class ExperimentalProcessor:
    """
    Rare and experimental image manipulation algorithms.
    These are NOT standard Photoshop filters.
    """

    @staticmethod
    def ascii_glitch(
        pil_image: Image.Image,
        char_width: int = 8,
        density: str = " .:-=+*#%@"
    ) -> Image.Image:
        """
        ASCII Art Glitch: Convert image to ASCII characters, then re-render.

        Process:
        1. Downsample image to character grid (e.g., 100×50 chars)
        2. Calculate luminance per character cell
        3. Map luminance to ASCII characters (density string)
        4. Render ASCII text as new image

        Artistic Effect:
        - Early computer graphics aesthetic (1970s terminal art)
        - Visible text structure
        - Lossy, destructive transformation
        """
        # Convert to grayscale
        gray = pil_image.convert('L')
        width, height = gray.size

        # Calculate character grid dimensions
        char_height = char_width * 2  # ASCII chars are ~2:1 aspect ratio
        cols = width // char_width
        rows = height // char_height

        # Create ASCII representation
        ascii_art = []
        pixels = gray.load()

        for row in range(rows):
            line = ""
            for col in range(cols):
                # Sample average luminance in cell
                x_start = col * char_width
                y_start = row * char_height
                total_lum = 0
                count = 0

                for y in range(y_start, min(y_start + char_height, height)):
                    for x in range(x_start, min(x_start + char_width, width)):
                        total_lum += pixels[x, y]
                        count += 1

                avg_lum = total_lum / count if count > 0 else 0

                # Map to ASCII character
                char_index = int((avg_lum / 255.0) * (len(density) - 1))
                line += density[char_index]

            ascii_art.append(line)

        # Render ASCII as image
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 12)
        except:
            font = ImageFont.load_default()

        # Calculate output size
        line_height = 14
        output_width = cols * 8
        output_height = rows * line_height

        canvas = Image.new('RGB', (output_width, output_height), 'black')
        draw = ImageDraw.Draw(canvas)

        for idx, line in enumerate(ascii_art):
            draw.text((0, idx * line_height), line, fill='#00FF41', font=font)

        return canvas.resize(pil_image.size, Image.Resampling.NEAREST)

    @staticmethod
    def reaction_diffusion(
        pil_image: Image.Image,
        iterations: int = 50,
        feed_rate: float = 0.055,
        kill_rate: float = 0.062
    ) -> Image.Image:
        """
        Reaction-Diffusion System (Gray-Scott Model)

        Mathematical Model:
        ∂u/∂t = Dᵤ∇²u - uv² + F(1 - u)
        ∂v/∂t = Dᵥ∇²v + uv² - (F + k)v

        Where:
        - u = concentration of chemical A
        - v = concentration of chemical B
        - Dᵤ, Dᵥ = diffusion rates
        - F = feed rate
        - k = kill rate

        Process:
        1. Initialize u and v grids from image luminance
        2. Iteratively simulate reaction-diffusion
        3. Convert v concentration back to RGB

        Artistic Effect:
        - Organic patterns (coral, leopard spots, maze-like)
        - Emerges from image contrast
        - Generative (same input → different outputs based on params)
        """
        # Downsample for performance (reaction-diffusion is O(n²) per iteration)
        small = pil_image.resize((256, 256), Image.Resampling.LANCZOS).convert('L')
        arr = np.array(small, dtype=np.float32) / 255.0

        # Initialize reaction-diffusion grids
        u = np.ones_like(arr)
        v = arr  # Initialize v from image luminance

        # Diffusion coefficients
        Du = 0.16
        Dv = 0.08

        # Laplacian kernel (for ∇² operator)
        laplacian_kernel = np.array([[0.05, 0.2, 0.05],
                                      [0.2, -1.0, 0.2],
                                      [0.05, 0.2, 0.05]])

        # Simulate reaction-diffusion
        for _ in range(iterations):
            # Compute Laplacians (convolution for ∇²)
            laplace_u = self._convolve2d(u, laplacian_kernel)
            laplace_v = self._convolve2d(v, laplacian_kernel)

            # Update equations
            uvv = u * v * v
            u += Du * laplace_u - uvv + feed_rate * (1 - u)
            v += Dv * laplace_v + uvv - (feed_rate + kill_rate) * v

            # Clamp values
            u = np.clip(u, 0, 1)
            v = np.clip(v, 0, 1)

        # Convert v concentration to RGB (artistic colorization)
        output = np.zeros((256, 256, 3), dtype=np.uint8)
        output[:, :, 0] = (v * 255).astype(np.uint8)  # Red channel
        output[:, :, 1] = (u * 128).astype(np.uint8)  # Green (dimmer)
        output[:, :, 2] = ((1 - v) * 200).astype(np.uint8)  # Blue (inverted)

        result = Image.fromarray(output)
        return result.resize(pil_image.size, Image.Resampling.LANCZOS)

    @staticmethod
    def _convolve2d(grid, kernel):
        """Simple 2D convolution for reaction-diffusion."""
        from scipy import ndimage
        return ndimage.convolve(grid, kernel, mode='wrap')

    @staticmethod
    def chromatic_prism_shift(
        pil_image: Image.Image,
        chaos: float = 0.5
    ) -> Image.Image:
        """
        Chromatic Aberration with Chaos-based displacement.

        Unlike simple RGB offset (linear shift), this uses:
        - Sinusoidal displacement (varies across image)
        - Chaos parameter (controls displacement magnitude)
        - Different wavelengths per channel

        Mathematical Model:
        R_offset(y) = chaos × A × sin(2π × y / λᵣ)
        G_offset(y) = chaos × A × sin(2π × y / λ_g + φ)
        B_offset(y) = chaos × A × sin(2π × y / λ_b + 2φ)

        Where:
        - A = amplitude (max displacement)
        - λ = wavelength (spatial frequency)
        - φ = phase shift (creates rainbow separation)
        """
        arr = np.array(pil_image)
        height, width, _ = arr.shape
        result = arr.copy()

        amplitude = int(chaos * 50)  # Max displacement in pixels

        # Different wavelengths and phases per channel
        wavelengths = {'r': height / 4, 'g': height / 3, 'b': height / 2}
        phases = {'r': 0, 'g': np.pi / 3, 'b': 2 * np.pi / 3}

        for y in range(height):
            # Calculate sinusoidal offsets
            r_offset = int(amplitude * np.sin(2 * np.pi * y / wavelengths['r'] + phases['r']))
            g_offset = int(amplitude * np.sin(2 * np.pi * y / wavelengths['g'] + phases['g']))
            b_offset = int(amplitude * np.sin(2 * np.pi * y / wavelengths['b'] + phases['b']))

            # Apply horizontal shifts
            result[y, :, 0] = np.roll(arr[y, :, 0], r_offset)
            result[y, :, 1] = np.roll(arr[y, :, 1], g_offset)
            result[y, :, 2] = np.roll(arr[y, :, 2], b_offset)

        return Image.fromarray(result)

    @staticmethod
    def bayer_dithering(
        pil_image: Image.Image,
        levels: int = 4
    ) -> Image.Image:
        """
        Bayer Ordered Dithering (1980s 8-bit aesthetic)

        Historical Context:
        - Used in early Macintosh (1-bit displays)
        - Simulates more colors through spatial patterns
        - Fixed threshold matrix (Bayer matrix)

        Mathematical Process:
        1. Use 8×8 Bayer threshold matrix
        2. For each pixel, compare luminance to matrix value
        3. Quantize to N levels (e.g., 4 levels = 2-bit color)

        Bayer Matrix (8×8):
        [[ 0 32  8 40  2 34 10 42]
         [48 16 56 24 50 18 58 26]
         [12 44  4 36 14 46  6 38]
         [60 28 52 20 62 30 54 22]
         [ 3 35 11 43  1 33  9 41]
         [51 19 59 27 49 17 57 25]
         [15 47  7 39 13 45  5 37]
         [63 31 55 23 61 29 53 21]]
        """
        # Bayer matrix (8×8 normalized to [0, 1])
        bayer_matrix = np.array([
            [ 0, 32,  8, 40,  2, 34, 10, 42],
            [48, 16, 56, 24, 50, 18, 58, 26],
            [12, 44,  4, 36, 14, 46,  6, 38],
            [60, 28, 52, 20, 62, 30, 54, 22],
            [ 3, 35, 11, 43,  1, 33,  9, 41],
            [51, 19, 59, 27, 49, 17, 57, 25],
            [15, 47,  7, 39, 13, 45,  5, 37],
            [63, 31, 55, 23, 61, 29, 53, 21]
        ], dtype=np.float32) / 64.0

        arr = np.array(pil_image).astype(np.float32) / 255.0
        height, width, channels = arr.shape

        # Tile Bayer matrix to match image size
        bayer_tiled = np.tile(bayer_matrix, (height // 8 + 1, width // 8 + 1, 1))
        bayer_tiled = bayer_tiled[:height, :width, :1]

        # Quantization levels
        step = 1.0 / (levels - 1)

        # Apply dithering
        for c in range(channels):
            channel = arr[:, :, c]
            threshold = bayer_tiled[:, :, 0]

            # Add Bayer threshold, then quantize
            dithered = channel + (threshold - 0.5) * step
            dithered = np.round(dithered / step) * step
            arr[:, :, c] = np.clip(dithered, 0, 1)

        result = (arr * 255).astype(np.uint8)
        return Image.fromarray(result)


# ============================================================================
# ANTI-UI THEME
# ============================================================================

class AntiUITheme:
    """Brutalist, anti-design aesthetic."""

    # Pure black background (no grays)
    BG_BLACK = "#000000"
    BG_PANEL = "#0A0A0A"  # Barely lighter

    # High-visibility accents
    ORANGE = "#FF5F1F"    # Construction cone orange
    GREEN = "#00FF41"     # Phosphor terminal green

    # Text
    TEXT = "#FFFFFF"
    TEXT_DIM = "#666666"

    # No rounded corners (pure brutalism)
    CORNER_RADIUS = 0

    # Typography
    FONT_MONO = ("Monaco", 11)
    FONT_TERMINAL = ("Monaco", 10)


# ============================================================================
# CUSTOM CIRCULAR KNOB WIDGET
# ============================================================================

class CircularKnob(ctk.CTkCanvas):
    """
    Custom circular knob control (like synthesizer/DAW knobs).

    Interaction:
    - Click and drag vertically to adjust value
    - Visual: Arc fills based on current value
    """

    def __init__(self, parent, from_=0, to=100, command=None, **kwargs):
        super().__init__(
            parent,
            width=60,
            height=60,
            bg=AntiUITheme.BG_BLACK,
            highlightthickness=0,
            **kwargs
        )

        self.from_ = from_
        self.to = to
        self.value = from_
        self.command = command

        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Button-1>", self._on_click)
        self._drag_start_y = 0
        self._draw()

    def _on_click(self, event):
        self._drag_start_y = event.y

    def _on_drag(self, event):
        # Vertical drag: up = increase, down = decrease
        delta_y = self._drag_start_y - event.y
        delta_value = delta_y * (self.to - self.from_) / 100

        self.value = max(self.from_, min(self.to, self.value + delta_value))
        self._drag_start_y = event.y

        self._draw()
        if self.command:
            self.command(self.value)

    def _draw(self):
        """Draw knob as circle with arc indicating value."""
        self.delete("all")

        # Background circle
        self.create_oval(5, 5, 55, 55, outline=AntiUITheme.TEXT_DIM, width=2)

        # Value arc (270° total range, starts at top)
        extent = ((self.value - self.from_) / (self.to - self.from_)) * 270
        self.create_arc(
            5, 5, 55, 55,
            start=135,  # Start at top-left
            extent=extent,
            outline=AntiUITheme.ORANGE,
            width=3,
            style="arc"
        )

        # Center indicator line
        angle_rad = math.radians(135 + extent)
        end_x = 30 + 18 * math.cos(angle_rad)
        end_y = 30 + 18 * math.sin(angle_rad)
        self.create_line(30, 30, end_x, end_y, fill=AntiUITheme.ORANGE, width=2)

    def get(self):
        return self.value

    def set(self, value):
        self.value = max(self.from_, min(self.to, value))
        self._draw()


# ============================================================================
# DATA STREAM WIDGET (Hacker Terminal)
# ============================================================================

class DataStream(ctk.CTkTextbox):
    """
    Real-time scrolling log of all operations.
    Every transformation is logged with timestamp.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=AntiUITheme.BG_BLACK,
            text_color=AntiUITheme.GREEN,
            font=AntiUITheme.FONT_TERMINAL,
            border_width=1,
            border_color=AntiUITheme.GREEN,
            corner_radius=0,
            **kwargs
        )

        self.configure(state="disabled")  # Read-only
        self.log_buffer = deque(maxlen=100)  # Keep last 100 entries

    def log(self, message: str):
        """Add timestamped log entry."""
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"

        self.configure(state="normal")
        self.insert("end", entry)
        self.see("end")  # Auto-scroll to bottom
        self.configure(state="disabled")


# ============================================================================
# MAIN ANTI-UI APPLICATION
# ============================================================================

class NeuroCorruptAntiUI(ctk.CTk):
    """
    Experimental interface rejecting conventional GUI design.

    No standard buttons → Command nodes
    No tooltips → Learn by doing
    Data stream → Every operation visible
    """

    def __init__(self):
        super().__init__()

        self.title("NEURO-CORRUPT :: EXPERIMENTAL ANTI-UI BUILD")
        self.geometry("1900x1100")
        self.configure(fg_color=AntiUITheme.BG_BLACK)
        ctk.set_appearance_mode("dark")

        # State
        self.original_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None
        self.is_processing = False

        # Parameters
        self.params = {
            'ascii_intensity': 0,
            'reaction_diff': 0,
            'prism_chaos': 0,
            'bayer_levels': 16  # 16 = no dithering
        }

        # Build interface
        self._build_ui()

    def _build_ui(self):
        """Construct brutalist interface."""
        # Grid layout: [Data Stream] [Canvas] [Controls]
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_data_stream()
        self._build_canvas()
        self._build_control_panel()

    # ========================================================================
    # DATA STREAM (Left Panel)
    # ========================================================================

    def _build_data_stream(self):
        """Terminal-style scrolling log."""
        stream_frame = ctk.CTkFrame(
            self,
            width=350,
            fg_color=AntiUITheme.BG_BLACK,
            corner_radius=0,
            border_width=2,
            border_color=AntiUITheme.GREEN
        )
        stream_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        stream_frame.grid_propagate(False)

        # Header
        header = ctk.CTkLabel(
            stream_frame,
            text=">> DATA STREAM",
            font=("Monaco", 14, "bold"),
            text_color=AntiUITheme.GREEN,
            anchor="w"
        )
        header.pack(pady=(10, 5), padx=10, fill="x")

        # Stream textbox
        self.data_stream = DataStream(stream_frame, height=800)
        self.data_stream.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Log startup
        self.data_stream.log("SYSTEM ONLINE")
        self.data_stream.log("EXPERIMENTAL BUILD v0.1")
        self.data_stream.log("AWAITING IMAGE INPUT...")

    # ========================================================================
    # CANVAS (Center Panel)
    # ========================================================================

    def _build_canvas(self):
        """Raw canvas with orange border."""
        canvas_frame = ctk.CTkFrame(
            self,
            fg_color=AntiUITheme.BG_BLACK,
            corner_radius=0,
            border_width=3,
            border_color=AntiUITheme.ORANGE
        )
        canvas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Status
        self.status_label = ctk.CTkLabel(
            canvas_frame,
            text="NO IMAGE LOADED",
            font=AntiUITheme.FONT_MONO,
            text_color=AntiUITheme.TEXT_DIM
        )
        self.status_label.pack(pady=20)

        # Canvas
        self.canvas_label = ctk.CTkLabel(
            canvas_frame,
            text="",
            fg_color=AntiUITheme.BG_BLACK
        )
        self.canvas_label.pack(expand=True, fill="both", padx=20, pady=20)

    # ========================================================================
    # CONTROL PANEL (Right Panel - Circular Knobs)
    # ========================================================================

    def _build_control_panel(self):
        """Knobs and faders instead of sliders."""
        control_frame = ctk.CTkFrame(
            self,
            width=300,
            fg_color=AntiUITheme.BG_PANEL,
            corner_radius=0,
            border_width=2,
            border_color=AntiUITheme.ORANGE
        )
        control_frame.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        control_frame.grid_propagate(False)

        # Header
        ctk.CTkLabel(
            control_frame,
            text=">> CONTROL NODES",
            font=("Monaco", 14, "bold"),
            text_color=AntiUITheme.ORANGE
        ).pack(pady=(15, 10), padx=15, anchor="w")

        # Command nodes (text buttons)
        self._create_command_node(
            control_frame,
            "LOAD.IMAGE",
            self._load_image
        ).pack(pady=5, padx=15, fill="x")

        self._create_command_node(
            control_frame,
            "EXPORT.4K",
            self._export_image
        ).pack(pady=5, padx=15, fill="x")

        # Separator
        ctk.CTkFrame(
            control_frame,
            height=2,
            fg_color=AntiUITheme.ORANGE
        ).pack(fill="x", padx=15, pady=15)

        # Knobs for experimental filters
        ctk.CTkLabel(
            control_frame,
            text=">> EXPERIMENTAL FILTERS",
            font=AntiUITheme.FONT_MONO,
            text_color=AntiUITheme.TEXT_DIM
        ).pack(pady=(10, 10), padx=15, anchor="w")

        # ASCII Intensity Knob
        self._create_knob_control(
            control_frame,
            "ASCII.GLITCH",
            'ascii_intensity',
            0, 100
        )

        # Reaction-Diffusion Knob
        self._create_knob_control(
            control_frame,
            "REACTION.DIFF",
            'reaction_diff',
            0, 100
        )

        # Prism Chaos Knob
        self._create_knob_control(
            control_frame,
            "PRISM.CHAOS",
            'prism_chaos',
            0, 100
        )

        # Bayer Levels Knob
        self._create_knob_control(
            control_frame,
            "BAYER.DITHER",
            'bayer_levels',
            2, 16
        )

        # Reset node
        ctk.CTkFrame(control_frame, fg_color="transparent").pack(expand=True)

        self._create_command_node(
            control_frame,
            "RESET.ALL",
            self._reset
        ).pack(pady=15, padx=15, fill="x", side="bottom")

    def _create_command_node(self, parent, text, command):
        """Text-based command button (no standard button look)."""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=("Monaco", 12, "bold"),
            fg_color="transparent",
            hover_color=AntiUITheme.BG_BLACK,
            border_width=2,
            border_color=AntiUITheme.ORANGE,
            text_color=AntiUITheme.ORANGE,
            corner_radius=0,
            height=40
        )

    def _create_knob_control(self, parent, label, param_key, from_, to):
        """Circular knob with label."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(pady=10, padx=15)

        # Label
        label_widget = ctk.CTkLabel(
            container,
            text=f"{label}: {self.params[param_key]}",
            font=AntiUITheme.FONT_MONO,
            text_color=AntiUITheme.TEXT
        )
        label_widget.pack()

        # Knob
        knob = CircularKnob(
            container,
            from_=from_,
            to=to,
            command=lambda v: self._on_knob_change(param_key, v, label_widget, label)
        )
        knob.set(self.params[param_key])
        knob.pack(pady=5)

    def _on_knob_change(self, param_key, value, label_widget, label_text):
        """Handle knob rotation."""
        value = int(value)
        self.params[param_key] = value
        label_widget.configure(text=f"{label_text}: {value}")

        self.data_stream.log(f"PARAM UPDATE: {param_key} = {value}")

        if self.original_image and not self.is_processing:
            self._process_threaded()

    # ========================================================================
    # OPERATIONS
    # ========================================================================

    def _load_image(self):
        """Load image with data stream logging."""
        file_path = filedialog.askopenfilename(
            title="SELECT IMAGE",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )

        if not file_path:
            return

        try:
            self.original_image = Image.open(file_path).convert('RGB')
            filename = file_path.split('/')[-1]

            self.data_stream.log(f"LOADED: {filename}")
            self.data_stream.log(f"SIZE: {self.original_image.width}x{self.original_image.height}")

            self.status_label.configure(
                text=filename.upper(),
                text_color=AntiUITheme.GREEN
            )

            self._process_threaded()

        except Exception as e:
            self.data_stream.log(f"ERROR: {str(e)}")

    def _process_threaded(self):
        """Process in background thread."""
        if self.is_processing:
            return

        self.is_processing = True
        self.data_stream.log("PROCESSING START...")

        thread = threading.Thread(target=self._process_pipeline)
        thread.daemon = True
        thread.start()

    def _process_pipeline(self):
        """Apply experimental filters."""
        try:
            result = self.original_image.copy()

            # ASCII Glitch
            if self.params['ascii_intensity'] > 0:
                self.data_stream.log("APPLYING: ASCII.GLITCH")
                char_width = max(2, 16 - int(self.params['ascii_intensity'] / 10))
                result = ExperimentalProcessor.ascii_glitch(result, char_width)

            # Reaction-Diffusion
            if self.params['reaction_diff'] > 0:
                self.data_stream.log("APPLYING: REACTION.DIFFUSION (HEAVY)")
                iterations = int(self.params['reaction_diff'] / 2)
                result = ExperimentalProcessor.reaction_diffusion(result, iterations)

            # Prism Chaos
            if self.params['prism_chaos'] > 0:
                self.data_stream.log("APPLYING: CHROMATIC.PRISM")
                chaos = self.params['prism_chaos'] / 100.0
                result = ExperimentalProcessor.chromatic_prism_shift(result, chaos)

            # Bayer Dithering
            if self.params['bayer_levels'] < 16:
                self.data_stream.log(f"APPLYING: BAYER.DITHER (LEVELS={self.params['bayer_levels']})")
                result = ExperimentalProcessor.bayer_dithering(result, self.params['bayer_levels'])

            self.processed_image = result
            self.after(0, self._update_display)
            self.data_stream.log("PROCESSING COMPLETE")

        except Exception as e:
            self.data_stream.log(f"CRITICAL ERROR: {str(e)}")
            print(f"Processing error: {e}")

        finally:
            self.is_processing = False

    def _update_display(self):
        """Update canvas with CTkImage (Retina support)."""
        if not self.processed_image:
            return

        canvas_width = self.canvas_label.winfo_width()
        canvas_height = self.canvas_label.winfo_height()

        if canvas_width <= 1:
            canvas_width, canvas_height = 1000, 800

        img_ratio = self.processed_image.width / self.processed_image.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            display_width = int(canvas_width * 0.9)
            display_height = int(display_width / img_ratio)
        else:
            display_height = int(canvas_height * 0.9)
            display_width = int(display_height * img_ratio)

        display_image = ctk.CTkImage(
            light_image=self.processed_image,
            dark_image=self.processed_image,
            size=(display_width, display_height)
        )

        self.canvas_label.configure(image=display_image)
        self.canvas_label.image = display_image
        self.status_label.configure(text="")

    def _export_image(self):
        """Export with logging."""
        if not self.processed_image:
            self.data_stream.log("ERROR: NO IMAGE TO EXPORT")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )

        if not file_path:
            return

        try:
            self.processed_image.save(file_path, quality=100)
            filename = file_path.split('/')[-1]
            self.data_stream.log(f"EXPORTED: {filename}")
            self.data_stream.log(f"RESOLUTION: {self.processed_image.width}x{self.processed_image.height}")

        except Exception as e:
            self.data_stream.log(f"EXPORT ERROR: {str(e)}")

    def _reset(self):
        """Reset all parameters."""
        self.data_stream.log("RESET: ALL PARAMETERS")

        self.params = {
            'ascii_intensity': 0,
            'reaction_diff': 0,
            'prism_chaos': 0,
            'bayer_levels': 16
        }

        if self.original_image:
            self._process_threaded()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        app = NeuroCorruptAntiUI()
        app.mainloop()
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()
