"""
X-FLTR / THE VOID ENGINE — Branding & Identity Module
======================================================
Generative logo, splash screen, and visual identity elements.

Author: ANSSAFOU ZINEB
Project: DIGITAL CREATION LAB
Version: 1.0
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Tuple


class BrandingConfig:
    """Centralized branding constants."""

    # Identity
    AUTHOR = "ANSSAFOU ZINEB"
    LAB_NAME = "DIGITAL CREATION LAB"
    APP_NAME = "VOID_ENGINE"
    VERSION = "V1.0"

    # Color Palette (Cyber-Brutalist)
    BLACK = "#000000"
    GREEN_NEON = "#00FF41"
    RED_GLITCH = "#FF0055"
    WHITE = "#FFFFFF"

    # Typography
    FONT_MONO = ("Monaco", 12)
    FONT_TERMINAL = ("Monaco", 10)
    FONT_HEADER = ("Monaco", 14, "bold")


def generate_app_logo(size: int = 128) -> Image.Image:
    """
    Generate glitchy "X" logo at runtime (no external .ico needed).

    Design Rationale for Portfolio:

    GENERATIVE BRANDING is superior to static logos because:

    1. PARAMETERIZATION:
       - Logo size adapts to context (64px for icon, 256px for splash)
       - Single function generates all sizes (DRY principle)
       - No need for multiple .ico files (16x16, 32x32, 64x64, etc.)

    2. DYNAMIC IDENTITY:
       - Can add randomness (each launch = slightly different logo)
       - Reflects brand ethos (digital, generative, experimental)
       - Logo is "code" not "asset" (aligns with creative coding)

    3. TECHNICAL DEMONSTRATION:
       - Shows mastery of Pillow drawing API
       - Demonstrates algorithmic thinking
       - Portfolio piece in itself (not just decoration)

    4. MAINTENANCE:
       - Change colors/style with code (not Photoshop)
       - Version control friendly (code diffs, not binary files)
       - Easier iteration during design phase

    Algorithm:
    1. Draw neon green "X" on black canvas
    2. Apply RGB channel displacement (glitch effect)
    3. Add subtle noise for texture

    Args:
        size: Output dimensions (square)

    Returns:
        PIL Image object (RGBA for transparency support)
    """
    # Create black canvas
    canvas = Image.new('RGB', (size, size), BrandingConfig.BLACK)
    draw = ImageDraw.Draw(canvas)

    # Calculate line thickness (scales with size)
    line_width = max(size // 12, 4)
    margin = size // 6

    # Draw "X" with neon green
    # Diagonal 1: Top-left to bottom-right
    draw.line(
        [(margin, margin), (size - margin, size - margin)],
        fill=BrandingConfig.GREEN_NEON,
        width=line_width
    )

    # Diagonal 2: Top-right to bottom-left
    draw.line(
        [(size - margin, margin), (margin, size - margin)],
        fill=BrandingConfig.GREEN_NEON,
        width=line_width
    )

    # Add small circle in center (design detail)
    center = size // 2
    radius = size // 16
    draw.ellipse(
        [(center - radius, center - radius), (center + radius, center + radius)],
        fill=BrandingConfig.BLACK,
        outline=BrandingConfig.GREEN_NEON,
        width=2
    )

    # Convert to array for glitch effect
    arr = np.array(canvas)

    # RGB CHANNEL DISPLACEMENT (signature glitch effect)
    glitch_offset = max(size // 32, 2)

    # Red channel: shift right
    arr[:, :, 0] = np.roll(arr[:, :, 0], glitch_offset, axis=1)

    # Blue channel: shift left
    arr[:, :, 2] = np.roll(arr[:, :, 2], -glitch_offset, axis=1)

    # Add subtle noise for texture
    noise = np.random.randint(-10, 10, arr.shape, dtype=np.int16)
    arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Convert back to PIL
    logo = Image.fromarray(arr)

    return logo


def generate_splash_image(width: int = 800, height: int = 400) -> Image.Image:
    """
    Generate splash screen image with terminal-style boot sequence.

    Design:
    - Black background
    - Neon green ASCII art banner
    - Boot sequence text
    - Large logo in center

    Args:
        width, height: Splash screen dimensions

    Returns:
        PIL Image object
    """
    # Create black canvas
    canvas = Image.new('RGB', (width, height), BrandingConfig.BLACK)
    draw = ImageDraw.Draw(canvas)

    # Try to load Monaco font, fallback to default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # ASCII Art Banner (top)
    banner_lines = [
        "╦  ╦╔═╗╦╔╦╗  ╔═╗╔╗╔╔═╗╦╔╗╔╔═╗",
        "╚╗╔╝║ ║║ ║║  ║╣ ║║║║ ╦║║║║║╣ ",
        " ╚╝ ╚═╝╩═╩╝  ╚═╝╝╚╝╚═╝╩╝╚╝╚═╝"
    ]

    y_offset = 40
    for line in banner_lines:
        # Calculate centered position
        bbox = draw.textbbox((0, 0), line, font=font_medium)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2

        draw.text((x, y_offset), line, fill=BrandingConfig.GREEN_NEON, font=font_medium)
        y_offset += 25

    # Boot sequence text
    y_offset += 30
    boot_messages = [
        "BOOTING VOID_ENGINE...",
        "INITIALIZING 42 FILTER MODULES...",
        f"AUTHORIZED ACCESS: {BrandingConfig.AUTHOR}",
        "SYSTEM READY"
    ]

    for msg in boot_messages:
        bbox = draw.textbbox((0, 0), msg, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2

        draw.text((x, y_offset), msg, fill=BrandingConfig.GREEN_NEON, font=font_small)
        y_offset += 20

    # Large logo in bottom center
    logo = generate_app_logo(128)
    logo_x = (width - 128) // 2
    logo_y = height - 160
    canvas.paste(logo, (logo_x, logo_y))

    # Footer text
    footer_text = f"{BrandingConfig.LAB_NAME} // {BrandingConfig.VERSION}"
    bbox = draw.textbbox((0, 0), footer_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height - 30

    draw.text((x, y), footer_text, fill=BrandingConfig.GREEN_NEON, font=font_small)

    return canvas


def get_header_text() -> str:
    """
    Generate header text for main application window.

    Returns:
        Formatted header string
    """
    return f"{BrandingConfig.AUTHOR} // {BrandingConfig.LAB_NAME} // {BrandingConfig.APP_NAME}_{BrandingConfig.VERSION}"


# Example usage for testing
if __name__ == "__main__":
    # Test logo generation
    logo = generate_app_logo(256)
    logo.save("test_logo.png")
    print("✓ Logo generated: test_logo.png")

    # Test splash screen
    splash = generate_splash_image(800, 400)
    splash.save("test_splash.png")
    print("✓ Splash screen generated: test_splash.png")

    # Test header text
    header = get_header_text()
    print(f"✓ Header text: {header}")
