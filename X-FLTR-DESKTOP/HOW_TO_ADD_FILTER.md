# How to Add a 41st Filter — Technical Guide

## For MMI Jury / Technical Documentation

This guide explains how to extend X-FLTR with new filters using Numpy.

---

## Step 1: Write the Filter Function

Add to `filters_engine.py` in the `FilterEngine` class:

```python
@staticmethod
def your_filter_name(arr: np.ndarray, param1: int = 10, param2: float = 0.5) -> np.ndarray:
    """
    Brief description of what this filter does.

    Args:
        arr: Input image array (H, W, 3) dtype uint8
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        Processed image array (H, W, 3) dtype uint8
    """
    # CRITICAL: Always copy input to avoid mutation
    result = arr.copy()

    # Your Numpy processing here
    # Example: Invert colors
    result = 255 - result

    # CRITICAL: Ensure output is valid uint8 [0, 255]
    result = np.clip(result, 0, 255).astype(np.uint8)

    return result
```

---

## Step 2: Register the Filter

Add to `FILTER_REGISTRY` at bottom of `filters_engine.py`:

```python
FILTER_REGISTRY = {
    'GLITCH': [...],
    'GENERATIVE': [...],
    'RETRO_TECH': [...],
    'GEOMETRIC': [...],
    'EXPERIMENTAL': [
        # ... existing filters ...
        ('Your Filter Name', FilterEngine.your_filter_name, {'param1': 10, 'param2': 0.5}),
    ]
}
```

Format: `(Display Name, Function Reference, Default Parameters Dict)`

---

## Step 3: Test Locally

```python
# Test in Python shell
from filters_engine import FilterEngine
import numpy as np

# Create test image
arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

# Apply your filter
result = FilterEngine.your_filter_name(arr, param1=20, param2=0.8)

# Verify output
print(result.shape)  # Should be (100, 100, 3)
print(result.dtype)  # Should be uint8
print(result.min(), result.max())  # Should be in [0, 255]
```

---

## Step 4: Run Application

```bash
python main.py
```

Your filter now appears in the filter grid automatically!

---

## 🔧 Numpy Optimization Patterns

### Pattern 1: Vectorized Operations (FAST)

```python
# ❌ SLOW (Python loop)
for y in range(height):
    for x in range(width):
        arr[y, x] = arr[y, x] * 2  # 10,000× slower

# ✅ FAST (Numpy vectorized)
arr = arr * 2  # Entire image in one operation
```

### Pattern 2: Array Slicing

```python
# Modify only red channel
arr[:, :, 0] = arr[:, :, 0] * 1.5

# Flip image vertically
arr = arr[::-1, :, :]

# Flip horizontally
arr = arr[:, ::-1, :]
```

### Pattern 3: Channel Manipulation

```python
# Swap red and blue channels
arr[:, :, [0, 2]] = arr[:, :, [2, 0]]

# Convert to grayscale (weighted average)
gray = (0.299 * arr[:, :, 0] +
        0.587 * arr[:, :, 1] +
        0.114 * arr[:, :, 2])

# Expand back to RGB
arr = np.stack([gray, gray, gray], axis=2).astype(np.uint8)
```

### Pattern 4: Convolution (Blur, Sharpen, Edges)

```python
from scipy import ndimage

# Define kernel
blur_kernel = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]]) / 9.0

# Apply to each channel
result = np.zeros_like(arr)
for c in range(3):
    result[:, :, c] = ndimage.convolve(arr[:, :, c].astype(np.float32), blur_kernel)

result = np.clip(result, 0, 255).astype(np.uint8)
```

**Common Kernels:**
```python
# Sharpen
sharpen = np.array([[ 0, -1,  0],
                    [-1,  5, -1],
                    [ 0, -1,  0]])

# Edge detection (Sobel X)
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

# Emboss
emboss = np.array([[-2, -1, 0],
                   [-1,  1, 1],
                   [ 0,  1, 2]])
```

### Pattern 5: Thresholding

```python
# Binary threshold
mask = arr > 128
arr[mask] = 255
arr[~mask] = 0

# Multi-level quantization
levels = 4
step = 256 / levels
arr = (arr / step).astype(int) * step
arr = np.clip(arr, 0, 255).astype(np.uint8)
```

### Pattern 6: Noise Addition

```python
# Gaussian noise
noise = np.random.normal(0, 25, arr.shape)
arr = arr.astype(np.float32) + noise
arr = np.clip(arr, 0, 255).astype(np.uint8)

# Salt-and-pepper noise
mask = np.random.rand(*arr.shape[:2]) < 0.05
arr[mask] = 255  # Salt
mask = np.random.rand(*arr.shape[:2]) < 0.05
arr[mask] = 0    # Pepper
```

---

## 🎨 Example Filters

### Example 1: Sepia Tone

```python
@staticmethod
def sepia_tone(arr: np.ndarray, intensity: float = 1.0) -> np.ndarray:
    """Apply vintage sepia tone effect."""
    result = arr.astype(np.float32)

    # Sepia transformation matrix
    sepia = np.array([[0.393, 0.769, 0.189],
                      [0.349, 0.686, 0.168],
                      [0.272, 0.534, 0.131]])

    # Apply to each pixel
    h, w, _ = arr.shape
    result = result.reshape(-1, 3) @ sepia.T
    result = result.reshape(h, w, 3)

    # Blend with original
    result = arr.astype(np.float32) * (1 - intensity) + result * intensity

    return np.clip(result, 0, 255).astype(np.uint8)
```

### Example 2: Edge Highlight

```python
@staticmethod
def edge_highlight(arr: np.ndarray, threshold: int = 50) -> np.ndarray:
    """Detect and highlight edges."""
    from scipy import ndimage

    # Convert to grayscale
    gray = (0.299 * arr[:, :, 0] +
            0.587 * arr[:, :, 1] +
            0.114 * arr[:, :, 2])

    # Sobel edge detection
    edges_x = ndimage.sobel(gray, axis=1)
    edges_y = ndimage.sobel(gray, axis=0)
    edges = np.hypot(edges_x, edges_y)

    # Threshold
    edges = (edges > threshold).astype(np.uint8) * 255

    # Create edge overlay
    edge_color = np.stack([edges, edges, edges], axis=2)

    # Composite
    result = (arr.astype(np.float32) * 0.5 +
              edge_color.astype(np.float32) * 0.5)

    return result.astype(np.uint8)
```

### Example 3: Color Shift

```python
@staticmethod
def color_shift(arr: np.ndarray, hue_shift: int = 30) -> np.ndarray:
    """Shift hue in HSV color space."""
    from PIL import Image

    # Convert to PIL
    img = Image.fromarray(arr)

    # Convert to HSV
    hsv = img.convert('HSV')
    hsv_arr = np.array(hsv)

    # Shift hue channel
    hsv_arr[:, :, 0] = (hsv_arr[:, :, 0] + hue_shift) % 256

    # Convert back to RGB
    hsv_img = Image.fromarray(hsv_arr, 'HSV')
    rgb_img = hsv_img.convert('RGB')

    return np.array(rgb_img)
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Mutating Input

```python
# ❌ BAD: Modifies original array
def bad_filter(arr):
    arr[:, :, 0] = 0  # Destroys input!
    return arr

# ✅ GOOD: Copy first
def good_filter(arr):
    result = arr.copy()
    result[:, :, 0] = 0
    return result
```

### Pitfall 2: Wrong Data Type

```python
# ❌ BAD: Returns float64 (incompatible with PIL)
def bad_filter(arr):
    return arr * 1.5  # dtype becomes float64

# ✅ GOOD: Clip and convert back to uint8
def good_filter(arr):
    result = arr.astype(np.float32) * 1.5
    return np.clip(result, 0, 255).astype(np.uint8)
```

### Pitfall 3: Out-of-Bounds Values

```python
# ❌ BAD: Values can exceed 255 or go below 0
def bad_filter(arr):
    return arr + 100  # Can overflow!

# ✅ GOOD: Always clip to [0, 255]
def good_filter(arr):
    result = arr.astype(np.int16) + 100
    return np.clip(result, 0, 255).astype(np.uint8)
```

---

## 🚀 Performance Tips

1. **Use Numpy vectorization** (not Python loops)
   - 10-100× faster
   - Leverages CPU SIMD instructions

2. **Process in-place when possible**
   - Reduces memory allocations
   - Faster for large images

3. **Downsample for slow algorithms**
   ```python
   # Process at 1/4 resolution, upscale result
   small = arr[::2, ::2, :]
   processed = slow_algorithm(small)
   result = np.repeat(np.repeat(processed, 2, axis=0), 2, axis=1)
   ```

4. **Profile your code**
   ```python
   import time
   start = time.time()
   result = your_filter(arr)
   print(f"Took {time.time() - start:.2f}s")
   ```

---

## ✅ Checklist Before Submitting

- [ ] Filter function is a static method in `FilterEngine` class
- [ ] Has type hints: `arr: np.ndarray` → `np.ndarray`
- [ ] Has docstring explaining what it does
- [ ] Copies input array (`result = arr.copy()`)
- [ ] Returns `uint8` in range [0, 255]
- [ ] Added to `FILTER_REGISTRY` with default params
- [ ] Tested on 100×100 test image
- [ ] Processing time < 5 seconds for 2000×1500 image

---

**You now have the power to add infinite filters! 🎨**
