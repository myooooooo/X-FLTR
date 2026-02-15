"""
X-FLTR / THE VOID ENGINE — Filter Processing Engine
====================================================
42 fully functional image filters using optimized Numpy operations.

Architecture:
- All filters are static methods (pure functions)
- Input/Output: numpy arrays (H, W, 3) uint8
- Convolution kernels for efficiency (one function, many effects)
- Zero disk I/O (all processing in RAM)

Author: ANSSAFOU ZINEB
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from scipy.spatial import Delaunay, Voronoi
from typing import Tuple, List
import random


class FilterEngine:
    """
    High-performance image processing engine.

    42 filters across 5 categories:
    - [GLITCH] (8 filters)
    - [GENERATIVE] (8 filters)
    - [RETRO-TECH] (8 filters)
    - [GEOMETRIC] (8 filters)
    - [EXPERIMENTAL] (10 filters)
    """

    # =======================================================================
    # CATEGORY 1: [GLITCH] — 8 Filters
    # =======================================================================

    @staticmethod
    def pixel_sort_horizontal(arr: np.ndarray, threshold: int = 128) -> np.ndarray:
        """Sort pixels horizontally by luminance."""
        result = arr.copy()
        luminance = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]

        for row_idx in range(result.shape[0]):
            row = result[row_idx]
            lum_row = luminance[row_idx]
            bright_mask = lum_row > threshold

            if np.any(bright_mask):
                bright_indices = np.where(bright_mask)[0]
                sorted_pixels = row[bright_indices]
                sorted_lum = lum_row[bright_indices]
                sort_order = np.argsort(sorted_lum)
                result[row_idx][bright_indices] = sorted_pixels[sort_order]

        return result

    @staticmethod
    def pixel_sort_vertical(arr: np.ndarray, threshold: int = 128) -> np.ndarray:
        """Sort pixels vertically by luminance."""
        result = arr.copy()
        luminance = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]

        for col_idx in range(result.shape[1]):
            col = result[:, col_idx]
            lum_col = luminance[:, col_idx]
            bright_mask = lum_col > threshold

            if np.any(bright_mask):
                bright_indices = np.where(bright_mask)[0]
                sorted_pixels = col[bright_indices]
                sorted_lum = lum_col[bright_indices]
                sort_order = np.argsort(sorted_lum)
                result[:, col_idx][bright_indices] = sorted_pixels[sort_order]

        return result

    @staticmethod
    def rgb_split_linear(arr: np.ndarray, offset: int = 20) -> np.ndarray:
        """Linear RGB channel displacement."""
        result = arr.copy()
        result[:, :, 0] = np.roll(result[:, :, 0], offset, axis=1)     # Red right
        result[:, :, 2] = np.roll(result[:, :, 2], -offset, axis=1)    # Blue left
        return result

    @staticmethod
    def rgb_split_wave(arr: np.ndarray, amplitude: int = 30) -> np.ndarray:
        """Sinusoidal RGB channel displacement."""
        result = arr.copy()
        height = arr.shape[0]

        for y in range(height):
            r_offset = int(amplitude * np.sin(2 * np.pi * y / (height / 4)))
            g_offset = int(amplitude * np.sin(2 * np.pi * y / (height / 3) + np.pi / 3))
            b_offset = int(amplitude * np.sin(2 * np.pi * y / (height / 2) + 2 * np.pi / 3))

            result[y, :, 0] = np.roll(arr[y, :, 0], r_offset)
            result[y, :, 1] = np.roll(arr[y, :, 1], g_offset)
            result[y, :, 2] = np.roll(arr[y, :, 2], b_offset)

        return result

    @staticmethod
    def datamosh_blocks(arr: np.ndarray, block_size: int = 32) -> np.ndarray:
        """Shuffle rectangular blocks randomly."""
        result = arr.copy()
        h, w, _ = arr.shape

        # Create grid of blocks
        blocks = []
        for y in range(0, h - block_size, block_size):
            for x in range(0, w - block_size, block_size):
                blocks.append((y, x))

        # Shuffle blocks
        random.shuffle(blocks)

        # Reassemble
        output = np.zeros_like(arr)
        for idx, (src_y, src_x) in enumerate(blocks):
            dst_y = (idx // (w // block_size)) * block_size
            dst_x = (idx % (w // block_size)) * block_size

            if dst_y + block_size <= h and dst_x + block_size <= w:
                output[dst_y:dst_y+block_size, dst_x:dst_x+block_size] = \
                    result[src_y:src_y+block_size, src_x:src_x+block_size]

        return output

    @staticmethod
    def scanline_corruption(arr: np.ndarray, intensity: int = 10) -> np.ndarray:
        """Horizontal scanline artifacts."""
        result = arr.copy()
        h, w, _ = arr.shape

        # Random scanlines
        num_lines = h // intensity
        scanline_indices = np.random.choice(h, num_lines, replace=False)

        for y in scanline_indices:
            # Shift scanline randomly
            offset = np.random.randint(-50, 50)
            result[y] = np.roll(result[y], offset, axis=0)

        return result

    @staticmethod
    def bit_crush(arr: np.ndarray, bits: int = 4) -> np.ndarray:
        """Reduce bit depth per channel."""
        result = arr.copy().astype(np.float32)
        levels = 2 ** bits
        result = np.round(result / 255.0 * (levels - 1)) / (levels - 1) * 255.0
        return result.astype(np.uint8)

    @staticmethod
    def jpeg_artifact_sim(arr: np.ndarray, block_size: int = 8) -> np.ndarray:
        """Simulate JPEG compression blocks."""
        result = arr.copy().astype(np.float32)
        h, w, _ = arr.shape

        # Average each block
        for y in range(0, h, block_size):
            for x in range(0, w, block_size):
                block = result[y:y+block_size, x:x+block_size]
                if block.size > 0:
                    avg_color = block.mean(axis=(0, 1))
                    result[y:y+block_size, x:x+block_size] = avg_color

        return result.astype(np.uint8)

    # =======================================================================
    # CATEGORY 2: [GENERATIVE] — 8 Filters
    # =======================================================================

    @staticmethod
    def reaction_diffusion(arr: np.ndarray, iterations: int = 30) -> np.ndarray:
        """Gray-Scott reaction-diffusion pattern."""
        # Downsample for performance
        small = Image.fromarray(arr).resize((128, 128), Image.Resampling.LANCZOS)
        gray = np.array(small.convert('L'), dtype=np.float32) / 255.0

        # Initialize u and v
        u = np.ones_like(gray)
        v = gray

        # Parameters
        Du, Dv = 0.16, 0.08
        F, k = 0.055, 0.062

        # Laplacian kernel
        kernel = np.array([[0.05, 0.2, 0.05],
                           [0.2, -1.0, 0.2],
                           [0.05, 0.2, 0.05]])

        # Simulate
        for _ in range(iterations):
            laplace_u = ndimage.convolve(u, kernel, mode='wrap')
            laplace_v = ndimage.convolve(v, kernel, mode='wrap')

            uvv = u * v * v
            u += Du * laplace_u - uvv + F * (1 - u)
            v += Dv * laplace_v + uvv - (F + k) * v

            u = np.clip(u, 0, 1)
            v = np.clip(v, 0, 1)

        # Colorize
        output = np.zeros((128, 128, 3), dtype=np.uint8)
        output[:, :, 0] = (v * 255).astype(np.uint8)
        output[:, :, 1] = (u * 128).astype(np.uint8)
        output[:, :, 2] = ((1 - v) * 200).astype(np.uint8)

        # Upscale back
        result_img = Image.fromarray(output).resize(arr.shape[:2][::-1], Image.Resampling.LANCZOS)
        return np.array(result_img)

    @staticmethod
    def voronoi_cells(arr: np.ndarray, num_cells: int = 100) -> np.ndarray:
        """
        Voronoi cellular pattern overlay.

        OPTIMIZED: Fully vectorized, no Python loops.
        Uses broadcasting to compute all distances at once.
        """
        h, w, _ = arr.shape

        # Generate random seed points
        points = np.random.rand(num_cells, 2)
        points[:, 0] *= h
        points[:, 1] *= w

        # Create coordinate grids (vectorized)
        y_coords, x_coords = np.mgrid[0:h, 0:w]  # Shape: (h, w)

        # Reshape for broadcasting: (h, w, 1)
        y_grid = y_coords[:, :, np.newaxis]
        x_grid = x_coords[:, :, np.newaxis]

        # Points shape: (num_cells, 2) → reshape to (1, 1, num_cells)
        points_y = points[:, 0].reshape(1, 1, -1)
        points_x = points[:, 1].reshape(1, 1, -1)

        # Compute all distances at once via broadcasting
        # Result shape: (h, w, num_cells)
        distances = np.sqrt((y_grid - points_y)**2 + (x_grid - points_x)**2)

        # Find nearest cell for each pixel (vectorized)
        nearest_indices = np.argmin(distances, axis=2)  # Shape: (h, w)

        # Sample colors from seed points (vectorized indexing)
        seed_y = np.clip(points[nearest_indices, 0].astype(int), 0, h-1)
        seed_x = np.clip(points[nearest_indices, 1].astype(int), 0, w-1)

        # Create output by indexing into original array
        output = arr[seed_y, seed_x]

        return output

    @staticmethod
    def perlin_noise_blend(arr: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """Blend with Perlin-like noise."""
        h, w, _ = arr.shape

        # Generate noise (simplified Perlin-like)
        noise = np.random.rand(h // 4, w // 4, 3) * 255
        noise_img = Image.fromarray(noise.astype(np.uint8))
        noise_upscaled = noise_img.resize((w, h), Image.Resampling.BILINEAR)
        noise_arr = np.array(noise_upscaled)

        # Blend
        result = arr.astype(np.float32) * (1 - intensity) + noise_arr.astype(np.float32) * intensity
        return result.astype(np.uint8)

    @staticmethod
    def delaunay_triangles(arr: np.ndarray, num_points: int = 200) -> np.ndarray:
        """Low-poly Delaunay triangulation."""
        h, w, _ = arr.shape

        # Generate random points
        points = np.random.rand(num_points, 2)
        points[:, 0] *= h
        points[:, 1] *= w

        # Add corners
        corners = np.array([[0, 0], [0, w-1], [h-1, 0], [h-1, w-1]])
        points = np.vstack([points, corners])

        # Delaunay triangulation
        try:
            tri = Delaunay(points)
        except:
            return arr  # Fallback if triangulation fails

        # Create output
        canvas = Image.new('RGB', (w, h), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Draw each triangle with average color
        for simplex in tri.simplices:
            triangle_points = points[simplex]

            # Sample color from triangle center
            center_y = int(triangle_points[:, 0].mean())
            center_x = int(triangle_points[:, 1].mean())
            center_y = np.clip(center_y, 0, h-1)
            center_x = np.clip(center_x, 0, w-1)

            color = tuple(arr[center_y, center_x].tolist())

            # Draw filled triangle
            coords = [(int(p[1]), int(p[0])) for p in triangle_points]
            draw.polygon(coords, fill=color, outline=None)

        return np.array(canvas)

    @staticmethod
    def fractal_noise(arr: np.ndarray, octaves: int = 4) -> np.ndarray:
        """Multi-octave fractal noise overlay."""
        h, w, _ = arr.shape
        noise = np.zeros((h, w, 3), dtype=np.float32)

        # Generate multiple octaves
        for octave in range(octaves):
            scale = 2 ** octave
            freq_h, freq_w = h // scale, w // scale

            octave_noise = np.random.rand(max(freq_h, 1), max(freq_w, 1), 3) * 255
            octave_img = Image.fromarray(octave_noise.astype(np.uint8))
            octave_upscaled = octave_img.resize((w, h), Image.Resampling.BILINEAR)

            noise += np.array(octave_upscaled) / (2 ** octave)

        noise = np.clip(noise, 0, 255).astype(np.uint8)

        # Blend with original
        result = (arr.astype(np.float32) * 0.6 + noise.astype(np.float32) * 0.4)
        return result.astype(np.uint8)

    @staticmethod
    def cellular_automata(arr: np.ndarray, generations: int = 10) -> np.ndarray:
        """Conway's Game of Life overlay."""
        # Convert to binary (threshold)
        gray = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
        grid = (gray > 128).astype(np.uint8)

        # Evolve
        for _ in range(generations):
            # Count neighbors
            neighbors = (
                np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
                np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1) +
                np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
                np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
                np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
                np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
            )

            # Apply rules
            grid = ((grid == 1) & ((neighbors == 2) | (neighbors == 3))) | \
                   ((grid == 0) & (neighbors == 3))
            grid = grid.astype(np.uint8)

        # Colorize and blend
        ca_color = np.stack([grid * 255, grid * 100, grid * 50], axis=2)
        result = (arr.astype(np.float32) * 0.7 + ca_color.astype(np.float32) * 0.3)
        return result.astype(np.uint8)

    @staticmethod
    def mandelbrot_colorize(arr: np.ndarray, max_iter: int = 50) -> np.ndarray:
        """Mandelbrot fractal-based color mapping."""
        h, w, _ = arr.shape

        # Generate Mandelbrot set
        x = np.linspace(-2.5, 1.0, w)
        y = np.linspace(-1.0, 1.0, h)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y

        Z = np.zeros_like(C)
        M = np.zeros(C.shape, dtype=int)

        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i

        # Normalize
        M = (M / max_iter * 255).astype(np.uint8)

        # Use Mandelbrot as color map
        mandel_color = np.stack([M, M // 2, 255 - M], axis=2)

        # Blend with original
        result = (arr.astype(np.float32) * 0.5 + mandel_color.astype(np.float32) * 0.5)
        return result.astype(np.uint8)

    @staticmethod
    def flow_field(arr: np.ndarray, strength: int = 20) -> np.ndarray:
        """Vector field distortion."""
        h, w, _ = arr.shape
        output = np.zeros_like(arr)

        # Generate flow field
        for y in range(h):
            for x in range(w):
                # Calculate flow vector
                angle = (x / w + y / h) * np.pi * 4
                dx = int(np.cos(angle) * strength)
                dy = int(np.sin(angle) * strength)

                # Sample from displaced position
                src_y = np.clip(y + dy, 0, h - 1)
                src_x = np.clip(x + dx, 0, w - 1)

                output[y, x] = arr[src_y, src_x]

        return output

    # =======================================================================
    # CATEGORY 3: [RETRO-TECH] — 8 Filters
    # =======================================================================

    @staticmethod
    def bayer_dithering(arr: np.ndarray, levels: int = 4) -> np.ndarray:
        """Bayer ordered dithering."""
        bayer_matrix = np.array([
            [0, 32, 8, 40, 2, 34, 10, 42],
            [48, 16, 56, 24, 50, 18, 58, 26],
            [12, 44, 4, 36, 14, 46, 6, 38],
            [60, 28, 52, 20, 62, 30, 54, 22],
            [3, 35, 11, 43, 1, 33, 9, 41],
            [51, 19, 59, 27, 49, 17, 57, 25],
            [15, 47, 7, 39, 13, 45, 5, 37],
            [63, 31, 55, 23, 61, 29, 53, 21]
        ], dtype=np.float32) / 64.0

        result = arr.astype(np.float32) / 255.0
        h, w, _ = arr.shape

        # Tile Bayer matrix
        bayer_tiled = np.tile(bayer_matrix, (h // 8 + 1, w // 8 + 1))[:h, :w]
        bayer_tiled = np.expand_dims(bayer_tiled, axis=2)

        # Quantize
        step = 1.0 / (levels - 1)
        for c in range(3):
            channel = result[:, :, c]
            threshold = bayer_tiled[:, :, 0]

            dithered = channel + (threshold - 0.5) * step
            dithered = np.round(dithered / step) * step
            result[:, :, c] = np.clip(dithered, 0, 1)

        return (result * 255).astype(np.uint8)

    @staticmethod
    def floyd_steinberg(arr: np.ndarray, levels: int = 4) -> np.ndarray:
        """Floyd-Steinberg error diffusion dithering."""
        result = arr.astype(np.float32) / 255.0
        h, w, _ = arr.shape

        step = 1.0 / (levels - 1)

        for c in range(3):
            for y in range(h):
                for x in range(w):
                    old_pixel = result[y, x, c]
                    new_pixel = np.round(old_pixel / step) * step
                    result[y, x, c] = new_pixel

                    error = old_pixel - new_pixel

                    # Distribute error
                    if x + 1 < w:
                        result[y, x + 1, c] += error * 7 / 16
                    if y + 1 < h:
                        if x > 0:
                            result[y + 1, x - 1, c] += error * 3 / 16
                        result[y + 1, x, c] += error * 5 / 16
                        if x + 1 < w:
                            result[y + 1, x + 1, c] += error * 1 / 16

        result = np.clip(result, 0, 1)
        return (result * 255).astype(np.uint8)

    @staticmethod
    def gameboy_4bit(arr: np.ndarray, intensity: float = 1.0) -> np.ndarray:
        """GameBoy 4-color green palette."""
        # GameBoy palette (darkest to lightest green)
        palette = np.array([
            [15, 56, 15],     # Darkest
            [48, 98, 48],     # Dark
            [139, 172, 15],   # Light
            [155, 188, 15]    # Lightest
        ], dtype=np.uint8)

        # Convert to grayscale
        gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)

        # Map to 4 levels
        indices = (gray / 64).astype(int)
        indices = np.clip(indices, 0, 3)

        # Apply palette
        result = palette[indices]

        # Blend with original based on intensity
        result = (arr.astype(np.float32) * (1 - intensity) + result.astype(np.float32) * intensity)
        return result.astype(np.uint8)

    @staticmethod
    def commodore64_palette(arr: np.ndarray, intensity: float = 1.0) -> np.ndarray:
        """Commodore 64 16-color palette."""
        # C64 color palette
        c64_palette = np.array([
            [0, 0, 0], [255, 255, 255], [136, 0, 0], [170, 255, 238],
            [204, 68, 204], [0, 204, 85], [0, 0, 170], [238, 238, 119],
            [221, 136, 85], [102, 68, 0], [255, 119, 119], [51, 51, 51],
            [119, 119, 119], [170, 255, 102], [0, 136, 255], [187, 187, 187]
        ], dtype=np.uint8)

        # Quantize to nearest C64 color
        result = np.zeros_like(arr)
        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                pixel = arr[y, x]
                distances = np.sum((c64_palette - pixel)**2, axis=1)
                nearest_idx = np.argmin(distances)
                result[y, x] = c64_palette[nearest_idx]

        # Blend
        result = (arr.astype(np.float32) * (1 - intensity) + result.astype(np.float32) * intensity)
        return result.astype(np.uint8)

    @staticmethod
    def crt_curvature(arr: np.ndarray, strength: float = 0.2) -> np.ndarray:
        """CRT barrel distortion + scanlines."""
        h, w, _ = arr.shape
        output = np.zeros_like(arr)

        # Center coordinates
        cy, cx = h / 2, w / 2

        for y in range(h):
            for x in range(w):
                # Normalized coordinates
                ny = (y - cy) / cy
                nx = (x - cx) / cx

                # Barrel distortion
                r2 = nx**2 + ny**2
                distortion = 1 + strength * r2

                src_x = int(cx + nx * cx * distortion)
                src_y = int(cy + ny * cy * distortion)

                if 0 <= src_y < h and 0 <= src_x < w:
                    output[y, x] = arr[src_y, src_x]

        # Add scanlines
        for y in range(0, h, 2):
            output[y] = (output[y].astype(np.float32) * 0.7).astype(np.uint8)

        return output

    @staticmethod
    def vhs_noise(arr: np.ndarray, intensity: float = 0.2) -> np.ndarray:
        """VHS tape noise artifacts."""
        result = arr.copy().astype(np.float32)

        # Add random noise
        noise = np.random.randn(*arr.shape) * intensity * 255
        result += noise

        # Add horizontal tracking errors
        for _ in range(5):
            y = np.random.randint(0, arr.shape[0])
            offset = np.random.randint(-20, 20)
            result[y] = np.roll(result[y], offset, axis=0)

        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def ascii_render(arr: np.ndarray, char_width: int = 8) -> np.ndarray:
        """
        ASCII art representation.

        OPTIMIZED: Uses Numpy average pooling instead of nested loops.
        """
        density = " .:-=+*#%@"
        gray = Image.fromarray(arr).convert('L')
        w, h = gray.size
        gray_arr = np.array(gray)

        char_height = char_width * 2
        cols = w // char_width
        rows = h // char_height

        # Crop to exact grid
        cropped_h = rows * char_height
        cropped_w = cols * char_width
        gray_arr = gray_arr[:cropped_h, :cropped_w]

        # Reshape for vectorized averaging (average pooling)
        # Reshape to (rows, char_height, cols, char_width)
        reshaped = gray_arr.reshape(rows, char_height, cols, char_width)

        # Average over char_height and char_width axes → shape: (rows, cols)
        avg_luminance = reshaped.mean(axis=(1, 3))

        # Convert to character indices (vectorized)
        char_indices = ((avg_luminance / 255.0) * (len(density) - 1)).astype(int)

        # Build ASCII art string
        ascii_art = []
        for row_idx in range(rows):
            line = "".join(density[char_indices[row_idx, col_idx]] for col_idx in range(cols))
            ascii_art.append(line)

        # Render ASCII as image
        from PIL import ImageFont
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 12)
        except:
            font = ImageFont.load_default()

        line_height = 14
        output_width = cols * 8
        output_height = rows * line_height

        canvas = Image.new('RGB', (output_width, output_height), 'black')
        draw = ImageDraw.Draw(canvas)

        for idx, line in enumerate(ascii_art):
            draw.text((0, idx * line_height), line, fill='#00FF41', font=font)

        return np.array(canvas.resize((w, h), Image.Resampling.NEAREST))

    @staticmethod
    def teletext_mode(arr: np.ndarray, block_size: int = 16) -> np.ndarray:
        """Blocky teletext graphics."""
        h, w, _ = arr.shape
        output = np.zeros_like(arr)

        # Quantize to blocks
        for y in range(0, h, block_size):
            for x in range(0, w, block_size):
                block = arr[y:y+block_size, x:x+block_size]
                if block.size > 0:
                    avg_color = block.mean(axis=(0, 1)).astype(np.uint8)
                    output[y:y+block_size, x:x+block_size] = avg_color

        return output

    # =======================================================================
    # CATEGORY 4: [GEOMETRIC] — 8 Filters
    # =======================================================================

    @staticmethod
    def hexagonal_mosaic(arr: np.ndarray, hex_size: int = 20) -> np.ndarray:
        """Hexagonal tiling."""
        h, w, _ = arr.shape
        canvas = Image.new('RGB', (w, h), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Hexagon geometry
        hex_height = int(hex_size * np.sqrt(3))
        hex_width = hex_size * 2

        for row in range(-1, h // hex_height + 2):
            for col in range(-1, w // hex_width + 2):
                # Hexagon center
                x = col * hex_width * 0.75
                y = row * hex_height + (col % 2) * hex_height / 2

                # Sample color
                sample_y = int(np.clip(y, 0, h - 1))
                sample_x = int(np.clip(x, 0, w - 1))
                color = tuple(arr[sample_y, sample_x].tolist())

                # Draw hexagon
                points = []
                for angle in range(0, 360, 60):
                    rad = np.radians(angle)
                    px = x + hex_size * np.cos(rad)
                    py = y + hex_size * np.sin(rad)
                    points.append((int(px), int(py)))

                draw.polygon(points, fill=color, outline=None)

        return np.array(canvas)

    @staticmethod
    def stained_glass(arr: np.ndarray, num_cells: int = 100) -> np.ndarray:
        """Voronoi with black outlines (stained glass effect)."""
        result = FilterEngine.voronoi_cells(arr, num_cells)

        # Add black outlines (edge detection)
        pil_img = Image.fromarray(result)
        edges = pil_img.filter(ImageFilter.FIND_EDGES)
        edges_arr = np.array(edges)

        # Composite edges
        mask = edges_arr.max(axis=2) > 30
        result[mask] = [0, 0, 0]

        return result

    @staticmethod
    def isometric_voxels(arr: np.ndarray, voxel_size: int = 10) -> np.ndarray:
        """Isometric 3D cube projection."""
        h, w, _ = arr.shape
        canvas = Image.new('RGB', (w * 2, h * 2), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Sample grid
        for y in range(0, h, voxel_size):
            for x in range(0, w, voxel_size):
                color = tuple(arr[y, x].tolist())

                # Isometric projection
                iso_x = (x - y) + w
                iso_y = (x + y) // 2

                # Draw cube (simplified)
                points = [
                    (iso_x, iso_y),
                    (iso_x + voxel_size, iso_y + voxel_size // 2),
                    (iso_x, iso_y + voxel_size),
                    (iso_x - voxel_size, iso_y + voxel_size // 2)
                ]
                draw.polygon(points, fill=color)

        # Crop back to original size
        canvas = canvas.crop((w // 2, h // 2, w + w // 2, h + h // 2))
        return np.array(canvas.resize((w, h), Image.Resampling.LANCZOS))

    @staticmethod
    def polygon_shatter(arr: np.ndarray, num_polygons: int = 50) -> np.ndarray:
        """Random polygon regions."""
        h, w, _ = arr.shape
        canvas = Image.new('RGB', (w, h), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        for _ in range(num_polygons):
            # Random polygon
            num_vertices = np.random.randint(3, 8)
            points = []
            for _ in range(num_vertices):
                px = np.random.randint(0, w)
                py = np.random.randint(0, h)
                points.append((px, py))

            # Sample color from center
            center_x = int(np.mean([p[0] for p in points]))
            center_y = int(np.mean([p[1] for p in points]))
            center_x = np.clip(center_x, 0, w - 1)
            center_y = np.clip(center_y, 0, h - 1)
            color = tuple(arr[center_y, center_x].tolist())

            draw.polygon(points, fill=color)

        return np.array(canvas)

    @staticmethod
    def kaleidoscope(arr: np.ndarray, segments: int = 6) -> np.ndarray:
        """Radial kaleidoscope effect."""
        h, w, _ = arr.shape
        cy, cx = h // 2, w // 2
        output = np.zeros_like(arr)

        angle_step = 2 * np.pi / segments

        for y in range(h):
            for x in range(w):
                # Polar coordinates
                dx, dy = x - cx, y - cy
                r = np.sqrt(dx**2 + dy**2)
                theta = np.arctan2(dy, dx)

                # Mirror angle
                segment = int(theta / angle_step)
                if segment % 2 == 1:
                    theta = segment * angle_step + (angle_step - (theta - segment * angle_step))

                # Back to Cartesian
                src_x = int(cx + r * np.cos(theta))
                src_y = int(cy + r * np.sin(theta))

                if 0 <= src_y < h and 0 <= src_x < w:
                    output[y, x] = arr[src_y, src_x]

        return output

    @staticmethod
    def pixelate_adaptive(arr: np.ndarray, detail_threshold: int = 30) -> np.ndarray:
        """Variable pixelation based on image complexity."""
        h, w, _ = arr.shape
        output = arr.copy()

        # Detect edges
        gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)
        edges = ndimage.sobel(gray)

        # Pixelate more in low-detail areas
        for y in range(0, h, 4):
            for x in range(0, w, 4):
                edge_strength = edges[y:y+4, x:x+4].mean()

                if edge_strength < detail_threshold:
                    block_size = 16
                else:
                    block_size = 4

                block = arr[y:y+block_size, x:x+block_size]
                if block.size > 0:
                    avg_color = block.mean(axis=(0, 1)).astype(np.uint8)
                    output[y:y+block_size, x:x+block_size] = avg_color

        return output

    @staticmethod
    def triangle_mesh(arr: np.ndarray, num_triangles: int = 200) -> np.ndarray:
        """Delaunay mesh with colored triangles."""
        return FilterEngine.delaunay_triangles(arr, num_triangles)

    @staticmethod
    def concentric_circles(arr: np.ndarray, num_rings: int = 20) -> np.ndarray:
        """Polar coordinate mapping (concentric circles)."""
        h, w, _ = arr.shape
        cy, cx = h // 2, w // 2
        output = np.zeros_like(arr)

        max_radius = np.sqrt(cy**2 + cx**2)

        for y in range(h):
            for x in range(w):
                dx, dy = x - cx, y - cy
                r = np.sqrt(dx**2 + dy**2)
                theta = np.arctan2(dy, dx)

                # Quantize radius
                ring = int(r / max_radius * num_rings)
                new_r = ring * max_radius / num_rings

                # Map back
                src_x = int(cx + new_r * np.cos(theta))
                src_y = int(cy + new_r * np.sin(theta))

                if 0 <= src_y < h and 0 <= src_x < w:
                    output[y, x] = arr[src_y, src_x]

        return output

    # =======================================================================
    # CATEGORY 5: [EXPERIMENTAL] — 10 Filters (USING CONVOLUTION KERNELS)
    # =======================================================================

    @staticmethod
    def apply_convolution_kernel(arr: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """
        Apply convolution kernel to image.

        This single function powers multiple filters:
        - Blur, Sharpen, Emboss, Edge Detection, etc.
        """
        result = np.zeros_like(arr)
        for c in range(3):
            result[:, :, c] = ndimage.convolve(arr[:, :, c].astype(np.float32), kernel, mode='reflect')

        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def chromatic_prism(arr: np.ndarray, chaos: float = 0.5) -> np.ndarray:
        """Chaos-based RGB displacement (sinusoidal)."""
        result = arr.copy()
        h = arr.shape[0]
        amplitude = int(chaos * 50)

        wavelengths = {'r': h / 4, 'g': h / 3, 'b': h / 2}
        phases = {'r': 0, 'g': np.pi / 3, 'b': 2 * np.pi / 3}

        for y in range(h):
            r_offset = int(amplitude * np.sin(2 * np.pi * y / wavelengths['r'] + phases['r']))
            g_offset = int(amplitude * np.sin(2 * np.pi * y / wavelengths['g'] + phases['g']))
            b_offset = int(amplitude * np.sin(2 * np.pi * y / wavelengths['b'] + phases['b']))

            result[y, :, 0] = np.roll(arr[y, :, 0], r_offset)
            result[y, :, 1] = np.roll(arr[y, :, 1], g_offset)
            result[y, :, 2] = np.roll(arr[y, :, 2], b_offset)

        return result

    @staticmethod
    def infrared_sim(arr: np.ndarray, intensity: float = 1.0) -> np.ndarray:
        """False-color infrared simulation."""
        # Infrared mapping: G → R, R → G, B → B (channel swap)
        result = arr.copy()
        result[:, :, 0], result[:, :, 1] = arr[:, :, 1].copy(), arr[:, :, 0].copy()

        # Enhance contrast
        result = np.clip(result.astype(np.float32) * 1.3, 0, 255).astype(np.uint8)

        # Blend
        result = (arr.astype(np.float32) * (1 - intensity) + result.astype(np.float32) * intensity)
        return result.astype(np.uint8)

    @staticmethod
    def sobel_neon_edges(arr: np.ndarray, intensity: float = 1.0) -> np.ndarray:
        """Sobel edge detection with neon overlay."""
        # Convert to grayscale
        gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)

        # Sobel edge detection
        edges_x = ndimage.sobel(gray, axis=1)
        edges_y = ndimage.sobel(gray, axis=0)
        edges = np.hypot(edges_x, edges_y)
        edges = np.clip(edges, 0, 255).astype(np.uint8)

        # Neon colorization
        neon_color = np.stack([edges * 0, edges, edges], axis=2).astype(np.uint8)

        # Darken original
        darkened = (arr.astype(np.float32) * 0.3).astype(np.uint8)

        # Composite
        result = (darkened.astype(np.float32) * (1 - intensity) + neon_color.astype(np.float32) * intensity)
        return result.astype(np.uint8)

    @staticmethod
    def duotone_gradient(arr: np.ndarray, color1: tuple = (255, 0, 100), color2: tuple = (0, 255, 200)) -> np.ndarray:
        """Two-color gradient mapping."""
        # Convert to grayscale
        gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255.0

        # Map to gradient
        result = np.zeros_like(arr)
        for c in range(3):
            result[:, :, c] = (gray * color2[c] + (1 - gray) * color1[c]).astype(np.uint8)

        return result

    @staticmethod
    def heatmap_solarize(arr: np.ndarray, intensity: float = 1.0) -> np.ndarray:
        """Temperature-based false-color mapping."""
        # Convert to grayscale
        gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2])

        # Heatmap colorization (blue → green → yellow → red)
        heatmap = np.zeros_like(arr)
        heatmap[:, :, 0] = np.clip(gray * 2, 0, 255)           # Red
        heatmap[:, :, 1] = np.clip((gray - 128) * 2, 0, 255)   # Green
        heatmap[:, :, 2] = np.clip((255 - gray) * 2, 0, 255)   # Blue

        # Blend
        result = (arr.astype(np.float32) * (1 - intensity) + heatmap.astype(np.float32) * intensity)
        return result.astype(np.uint8)

    @staticmethod
    def oil_painting(arr: np.ndarray, radius: int = 5) -> np.ndarray:
        """Kuwahara filter approximation (oil painting effect)."""
        # Simplified oil painting using median filter
        result = np.zeros_like(arr)
        for c in range(3):
            result[:, :, c] = ndimage.median_filter(arr[:, :, c], size=radius)
        return result

    @staticmethod
    def glitch_displacement(arr: np.ndarray, strength: int = 20) -> np.ndarray:
        """Random pixel displacement."""
        h, w, _ = arr.shape
        output = arr.copy()

        # Random displacement vectors
        for _ in range(h // 10):
            y = np.random.randint(0, h)
            width = np.random.randint(1, w // 4)
            offset = np.random.randint(-strength, strength)

            x_start = np.random.randint(0, w - width)
            output[y, x_start:x_start+width] = np.roll(arr[y, x_start:x_start+width], offset, axis=0)

        return output

    @staticmethod
    def channel_mixer(arr: np.ndarray, r_mix: tuple = (1, 0, 0), g_mix: tuple = (0, 1, 0), b_mix: tuple = (0, 0, 1)) -> np.ndarray:
        """Custom RGB channel blending."""
        result = np.zeros_like(arr, dtype=np.float32)

        # Red output
        result[:, :, 0] = (arr[:, :, 0] * r_mix[0] + arr[:, :, 1] * r_mix[1] + arr[:, :, 2] * r_mix[2])

        # Green output
        result[:, :, 1] = (arr[:, :, 0] * g_mix[0] + arr[:, :, 1] * g_mix[1] + arr[:, :, 2] * g_mix[2])

        # Blue output
        result[:, :, 2] = (arr[:, :, 0] * b_mix[0] + arr[:, :, 1] * b_mix[1] + arr[:, :, 2] * b_mix[2])

        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def bloom_glow(arr: np.ndarray, threshold: int = 200, intensity: float = 0.5) -> np.ndarray:
        """HDR-style bloom (bright areas glow)."""
        # Extract bright regions
        mask = arr > threshold
        bright = arr.copy()
        bright[~mask] = 0

        # Blur bright regions
        blurred = np.zeros_like(bright, dtype=np.float32)
        for c in range(3):
            blurred[:, :, c] = ndimage.gaussian_filter(bright[:, :, c].astype(np.float32), sigma=10)

        # Composite
        result = arr.astype(np.float32) + blurred * intensity
        return np.clip(result, 0, 255).astype(np.uint8)

    @staticmethod
    def posterize_levels(arr: np.ndarray, levels: int = 4) -> np.ndarray:
        """Reduce color levels (posterization)."""
        result = arr.astype(np.float32)
        step = 256 / levels
        result = np.floor(result / step) * step
        return np.clip(result, 0, 255).astype(np.uint8)


# Filter registry for UI generation
FILTER_REGISTRY = {
    'GLITCH': [
        ('Pixel Sort H', FilterEngine.pixel_sort_horizontal, {'threshold': 128}),
        ('Pixel Sort V', FilterEngine.pixel_sort_vertical, {'threshold': 128}),
        ('RGB Split Linear', FilterEngine.rgb_split_linear, {'offset': 20}),
        ('RGB Split Wave', FilterEngine.rgb_split_wave, {'amplitude': 30}),
        ('Datamosh Blocks', FilterEngine.datamosh_blocks, {'block_size': 32}),
        ('Scanline Corrupt', FilterEngine.scanline_corruption, {'intensity': 10}),
        ('Bit Crush', FilterEngine.bit_crush, {'bits': 4}),
        ('JPEG Artifact', FilterEngine.jpeg_artifact_sim, {'block_size': 8}),
    ],
    'GENERATIVE': [
        ('Reaction Diffusion', FilterEngine.reaction_diffusion, {'iterations': 30}),
        ('Voronoi Cells', FilterEngine.voronoi_cells, {'num_cells': 100}),
        ('Perlin Noise', FilterEngine.perlin_noise_blend, {'intensity': 0.3}),
        ('Delaunay Tri', FilterEngine.delaunay_triangles, {'num_points': 200}),
        ('Fractal Noise', FilterEngine.fractal_noise, {'octaves': 4}),
        ('Cellular Auto', FilterEngine.cellular_automata, {'generations': 10}),
        ('Mandelbrot Map', FilterEngine.mandelbrot_colorize, {'max_iter': 50}),
        ('Flow Field', FilterEngine.flow_field, {'strength': 20}),
    ],
    'RETRO_TECH': [
        ('Bayer Dither', FilterEngine.bayer_dithering, {'levels': 4}),
        ('Floyd-Steinberg', FilterEngine.floyd_steinberg, {'levels': 4}),
        ('GameBoy 4-bit', FilterEngine.gameboy_4bit, {'intensity': 1.0}),
        ('C64 Palette', FilterEngine.commodore64_palette, {'intensity': 1.0}),
        ('CRT Curvature', FilterEngine.crt_curvature, {'strength': 0.2}),
        ('VHS Noise', FilterEngine.vhs_noise, {'intensity': 0.2}),
        ('ASCII Render', FilterEngine.ascii_render, {'char_width': 8}),
        ('Teletext Mode', FilterEngine.teletext_mode, {'block_size': 16}),
    ],
    'GEOMETRIC': [
        ('Hex Mosaic', FilterEngine.hexagonal_mosaic, {'hex_size': 20}),
        ('Stained Glass', FilterEngine.stained_glass, {'num_cells': 100}),
        ('Isometric Voxels', FilterEngine.isometric_voxels, {'voxel_size': 10}),
        ('Polygon Shatter', FilterEngine.polygon_shatter, {'num_polygons': 50}),
        ('Kaleidoscope', FilterEngine.kaleidoscope, {'segments': 6}),
        ('Adaptive Pixelate', FilterEngine.pixelate_adaptive, {'detail_threshold': 30}),
        ('Triangle Mesh', FilterEngine.triangle_mesh, {'num_triangles': 200}),
        ('Concentric Circles', FilterEngine.concentric_circles, {'num_rings': 20}),
    ],
    'EXPERIMENTAL': [
        ('Chromatic Prism', FilterEngine.chromatic_prism, {'chaos': 0.5}),
        ('Infrared Sim', FilterEngine.infrared_sim, {'intensity': 1.0}),
        ('Sobel Neon', FilterEngine.sobel_neon_edges, {'intensity': 1.0}),
        ('Duotone Gradient', FilterEngine.duotone_gradient, {}),
        ('Heatmap Solarize', FilterEngine.heatmap_solarize, {'intensity': 1.0}),
        ('Oil Painting', FilterEngine.oil_painting, {'radius': 5}),
        ('Glitch Displace', FilterEngine.glitch_displacement, {'strength': 20}),
        ('Channel Mixer', FilterEngine.channel_mixer, {}),
        ('Bloom Glow', FilterEngine.bloom_glow, {'threshold': 200, 'intensity': 0.5}),
        ('Posterize', FilterEngine.posterize_levels, {'levels': 4}),
    ]
}
