"""
NEURO-CORRUPT: A Post-Digital Glitch Engine
============================================
A data-bending desktop application for generative texture creation.
Author: MMI Student Portfolio Project
Aesthetic: Cyber-Brutalist UI with Real-Time Glitch Manipulation
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
from tkinter import filedialog
import io


class GlitchEngine:
    """Core glitch algorithm processing engine."""

    @staticmethod
    def bit_shift_glitch(image_array, shift_amount):
        """
        Bit-shifting algorithm: Creates horizontal tearing artifacts.

        Args:
            image_array: Numpy array of image data
            shift_amount: Integer 0-255 for bit manipulation intensity
        """
        if shift_amount == 0:
            return image_array

        result = image_array.copy()
        # Apply bit-level shifting to create digital artifacts
        result = np.bitwise_xor(result, shift_amount)
        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def channel_offset(image_array, r_offset, g_offset, b_offset):
        """
        RGB Channel separation: Creates chromatic aberration effects.

        Args:
            image_array: Numpy array (H, W, 3)
            r_offset, g_offset, b_offset: Horizontal pixel shift values
        """
        height, width = image_array.shape[:2]
        result = image_array.copy()

        # Shift each color channel independently
        if r_offset != 0:
            result[:, :, 0] = np.roll(result[:, :, 0], r_offset, axis=1)
        if g_offset != 0:
            result[:, :, 1] = np.roll(result[:, :, 1], g_offset, axis=1)
        if b_offset != 0:
            result[:, :, 2] = np.roll(result[:, :, 2], b_offset, axis=1)

        return result

    @staticmethod
    def pixel_sort(image_array, threshold, direction='horizontal'):
        """
        Pixel-sorting algorithm: Reorders pixels by luminance values.
        Creates the iconic "data-mosh" aesthetic.

        Args:
            image_array: Numpy array of image
            threshold: Brightness threshold (0-255) for sorting trigger
            direction: 'horizontal' or 'vertical'
        """
        result = image_array.copy()

        # Calculate luminance using standard formula
        luminance = 0.299 * result[:,:,0] + 0.587 * result[:,:,1] + 0.114 * result[:,:,2]

        if direction == 'horizontal':
            for row_idx in range(result.shape[0]):
                row = result[row_idx]
                lum_row = luminance[row_idx]

                # Find segments above threshold
                mask = lum_row > threshold
                if np.any(mask):
                    # Sort pixels in bright regions by luminance
                    indices = np.argsort(lum_row)
                    bright_indices = indices[lum_row[indices] > threshold]

                    if len(bright_indices) > 0:
                        sorted_pixels = row[bright_indices]
                        sorted_lum = lum_row[bright_indices]
                        sort_order = np.argsort(sorted_lum)
                        result[row_idx][bright_indices] = sorted_pixels[sort_order]

        else:  # vertical
            for col_idx in range(result.shape[1]):
                col = result[:, col_idx]
                lum_col = luminance[:, col_idx]

                mask = lum_col > threshold
                if np.any(mask):
                    indices = np.argsort(lum_col)
                    bright_indices = indices[lum_col[indices] > threshold]

                    if len(bright_indices) > 0:
                        sorted_pixels = col[bright_indices]
                        sorted_lum = lum_col[bright_indices]
                        sort_order = np.argsort(sorted_lum)
                        result[:, col_idx][bright_indices] = sorted_pixels[sort_order]

        return result


class NeuroCorruptUI(ctk.CTk):
    """Main application window with cyber-brutalist aesthetic."""

    # COLOR PALETTE: Cyber-Brutalist System
    BG_PRIMARY = "#0D0D0D"
    BG_SECONDARY = "#1A1A1A"
    ACCENT_NEON = "#00FF41"
    ACCENT_CYBER = "#FF0055"
    TEXT_PRIMARY = "#E0E0E0"
    TEXT_SECONDARY = "#808080"

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("NEURO-CORRUPT v1.0 // DATA-BENDING ENGINE")
        self.geometry("1400x900")

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Data state
        self.original_image = None
        self.working_image = None
        self.display_image = None

        # Glitch parameters
        self.params = {
            'bit_shift': 0,
            'r_offset': 0,
            'g_offset': 0,
            'b_offset': 0,
            'sort_threshold': 128,
            'sort_direction': 'horizontal'
        }

        self._build_ui()

    def _build_ui(self):
        """Construct the modular command center layout."""

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # LEFT SIDEBAR: Control Panel
        self._build_sidebar()

        # CENTER: Glitch Canvas
        self._build_canvas()

    def _build_sidebar(self):
        """Industrial control panel with technical sliders."""

        sidebar = ctk.CTkFrame(
            self,
            width=350,
            corner_radius=0,
            fg_color=self.BG_SECONDARY,
            border_width=2,
            border_color=self.ACCENT_NEON
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_propagate(False)

        # HEADER
        header = ctk.CTkLabel(
            sidebar,
            text="[ CORRUPTION PARAMETERS ]",
            font=("JetBrains Mono", 16, "bold"),
            text_color=self.ACCENT_NEON
        )
        header.pack(pady=(20, 30), padx=20)

        # FILE OPERATIONS
        self._create_section_header(sidebar, "// FILE SYSTEM")

        btn_load = self._create_industrial_button(
            sidebar,
            "LOAD IMAGE",
            self._load_image,
            self.ACCENT_NEON
        )
        btn_load.pack(pady=5, padx=20, fill="x")

        btn_export = self._create_industrial_button(
            sidebar,
            "EXPORT PNG",
            self._export_image,
            self.ACCENT_CYBER
        )
        btn_export.pack(pady=5, padx=20, fill="x")

        # BIT-SHIFTING CONTROLS
        self._create_section_header(sidebar, "// BIT MANIPULATION")
        self._create_slider(
            sidebar,
            "Bit Shift",
            'bit_shift',
            0, 255, 1
        )

        # CHANNEL OFFSET CONTROLS
        self._create_section_header(sidebar, "// RGB SEPARATION")
        self._create_slider(sidebar, "Red Offset", 'r_offset', -100, 100, 1)
        self._create_slider(sidebar, "Green Offset", 'g_offset', -100, 100, 1)
        self._create_slider(sidebar, "Blue Offset", 'b_offset', -100, 100, 1)

        # PIXEL SORTING CONTROLS
        self._create_section_header(sidebar, "// PIXEL SORTING")
        self._create_slider(
            sidebar,
            "Sort Threshold",
            'sort_threshold',
            0, 255, 1
        )

        # Direction toggle
        direction_var = ctk.StringVar(value="horizontal")
        direction_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        direction_frame.pack(pady=5, padx=20, fill="x")

        ctk.CTkRadioButton(
            direction_frame,
            text="Horizontal",
            variable=direction_var,
            value="horizontal",
            font=("Courier", 11),
            text_color=self.TEXT_PRIMARY,
            fg_color=self.ACCENT_NEON,
            hover_color=self.ACCENT_CYBER,
            command=lambda: self._update_param('sort_direction', 'horizontal')
        ).pack(side="left", padx=5)

        ctk.CTkRadioButton(
            direction_frame,
            text="Vertical",
            variable=direction_var,
            value="vertical",
            font=("Courier", 11),
            text_color=self.TEXT_PRIMARY,
            fg_color=self.ACCENT_NEON,
            hover_color=self.ACCENT_CYBER,
            command=lambda: self._update_param('sort_direction', 'vertical')
        ).pack(side="left", padx=5)

        # RESET BUTTON
        btn_reset = self._create_industrial_button(
            sidebar,
            "RESET ALL",
            self._reset_parameters,
            self.TEXT_SECONDARY
        )
        btn_reset.pack(pady=20, padx=20, fill="x", side="bottom")

    def _build_canvas(self):
        """Central display area for glitch preview."""

        canvas_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.BG_PRIMARY,
            border_width=2,
            border_color=self.ACCENT_NEON
        )
        canvas_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        # Status label
        self.status_label = ctk.CTkLabel(
            canvas_frame,
            text="[ AWAITING INPUT :: LOAD IMAGE TO BEGIN ]",
            font=("JetBrains Mono", 14),
            text_color=self.TEXT_SECONDARY
        )
        self.status_label.pack(pady=20)

        # Canvas for image display
        self.canvas = ctk.CTkLabel(
            canvas_frame,
            text="",
            fg_color=self.BG_PRIMARY
        )
        self.canvas.pack(expand=True, fill="both", padx=40, pady=40)

    def _create_section_header(self, parent, text):
        """Create a section header with industrial styling."""
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=("Courier", 12, "bold"),
            text_color=self.ACCENT_CYBER,
            anchor="w"
        )
        label.pack(pady=(15, 5), padx=20, fill="x")

    def _create_industrial_button(self, parent, text, command, color):
        """Create a brutalist-styled button."""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=("JetBrains Mono", 13, "bold"),
            fg_color="transparent",
            hover_color=self.BG_PRIMARY,
            border_width=2,
            border_color=color,
            text_color=color,
            corner_radius=0,
            height=40
        )

    def _create_slider(self, parent, label, param_key, from_, to_, resolution):
        """Create a technical slider with real-time feedback."""

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=5, padx=20, fill="x")

        # Label with value display
        value_label = ctk.CTkLabel(
            frame,
            text=f"{label}: {self.params[param_key]:>4}",
            font=("Courier", 11),
            text_color=self.TEXT_PRIMARY,
            anchor="w"
        )
        value_label.pack(fill="x")

        # Slider
        slider = ctk.CTkSlider(
            frame,
            from_=from_,
            to=to_,
            number_of_steps=int((to_ - from_) / resolution),
            command=lambda v: self._on_slider_change(param_key, v, value_label, label),
            button_color=self.ACCENT_NEON,
            button_hover_color=self.ACCENT_CYBER,
            progress_color=self.ACCENT_NEON,
            fg_color=self.BG_PRIMARY,
            height=20
        )
        slider.set(self.params[param_key])
        slider.pack(fill="x", pady=(2, 0))

    def _on_slider_change(self, param_key, value, label_widget, label_text):
        """Handle slider value changes with real-time preview."""
        value = int(value)
        self.params[param_key] = value
        label_widget.configure(text=f"{label_text}: {value:>4}")

        # Trigger real-time glitch processing
        if self.original_image is not None:
            self._process_glitch()

    def _update_param(self, key, value):
        """Update parameter and refresh."""
        self.params[key] = value
        if self.original_image is not None:
            self._process_glitch()

    def _load_image(self):
        """Load image file for glitch processing."""
        file_path = filedialog.askopenfilename(
            title="SELECT IMAGE FOR CORRUPTION",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )

        if file_path:
            self.original_image = Image.open(file_path).convert('RGB')
            self.working_image = np.array(self.original_image)

            self.status_label.configure(
                text=f"[ LOADED :: {file_path.split('/')[-1]} ]",
                text_color=self.ACCENT_NEON
            )

            self._process_glitch()

    def _process_glitch(self):
        """Apply all glitch algorithms in sequence."""
        if self.working_image is None:
            return

        # Start with original
        result = self.working_image.copy()

        # Apply effects pipeline
        result = GlitchEngine.bit_shift_glitch(result, self.params['bit_shift'])
        result = GlitchEngine.channel_offset(
            result,
            self.params['r_offset'],
            self.params['g_offset'],
            self.params['b_offset']
        )
        result = GlitchEngine.pixel_sort(
            result,
            self.params['sort_threshold'],
            self.params['sort_direction']
        )

        # Convert to PIL and display
        self.display_image = Image.fromarray(result)
        self._update_canvas()

    def _update_canvas(self):
        """Render the processed image to canvas."""
        if self.display_image is None:
            return

        # Calculate scaling to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet rendered, use default
            canvas_width, canvas_height = 800, 700

        # Maintain aspect ratio
        img_ratio = self.display_image.width / self.display_image.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        # Resize and display
        display_img = self.display_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(display_img)

        self.canvas.configure(image=photo)
        self.canvas.image = photo  # Keep reference

    def _export_image(self):
        """Export high-resolution glitched image."""
        if self.display_image is None:
            self.status_label.configure(
                text="[ ERROR :: NO IMAGE TO EXPORT ]",
                text_color=self.ACCENT_CYBER
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")],
            title="EXPORT CORRUPTED IMAGE"
        )

        if file_path:
            self.display_image.save(file_path, "PNG", quality=100)
            self.status_label.configure(
                text=f"[ EXPORTED :: {file_path.split('/')[-1]} ]",
                text_color=self.ACCENT_NEON
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

        if self.original_image is not None:
            self.working_image = np.array(self.original_image)
            self._process_glitch()

        # Rebuild UI to reset sliders
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
        self._build_ui()


if __name__ == "__main__":
    app = NeuroCorruptUI()
    app.mainloop()
