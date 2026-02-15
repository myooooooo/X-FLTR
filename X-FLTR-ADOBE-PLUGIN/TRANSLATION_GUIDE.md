# Python → JavaScript Translation Guide

**X-FLTR / THE VOID ENGINE — Filter Porting Reference**

Author: ANSSAFOU ZINEB | MMI Portfolio 2025

---

## 🎯 Purpose

This guide documents the translation strategy for porting all **42 filters** from Python (Numpy/SciPy) to JavaScript (Adobe UXP).

---

## 📊 Translation Progress

**Current Status:** 2/42 filters ported (4.8%)

| Category | Total | Ported | Pending | Complexity |
|----------|-------|--------|---------|------------|
| GLITCH | 8 | 2 | 6 | Low-Medium |
| GENERATIVE | 8 | 0 | 8 | High |
| RETRO-TECH | 8 | 0 | 8 | Medium |
| GEOMETRIC | 8 | 0 | 8 | Medium-High |
| EXPERIMENTAL | 10 | 0 | 10 | Medium |

---

## 🔬 Translation Patterns

### Pattern 1: Layer-Based Operations (Easiest)

**Use When:** Filter can be achieved with layer duplication + blend modes

**Python Example:**
```python
def rgb_split_linear(arr, offset=20):
    result = arr.copy()
    result[:, :, 0] = np.roll(result[:, :, 0], offset, axis=1)
    result[:, :, 2] = np.roll(result[:, :, 2], -offset, axis=1)
    return result
```

**JavaScript Translation:**
```javascript
async function rgbSplitLinear(offset = 20) {
    const redLayer = await originalLayer.duplicate();
    redLayer.translate(offset, 0);

    const blueLayer = await originalLayer.duplicate();
    blueLayer.translate(-offset, 0);

    // Isolate channels via Channel Mixer
    await imaging.applyChannelMixer(redLayer, {
        redChannel: { red: 100, green: 0, blue: 0 }
    });

    redLayer.blendMode = "screen";
}
```

**Filters Using This Pattern:**
- ✅ RGB Split Linear
- ✅ RGB Split Wave
- [ ] Chromatic Prism
- [ ] Bloom Glow

---

### Pattern 2: Pixel-Level Manipulation (Medium)

**Use When:** Filter requires reading/writing individual pixels

**Python Example:**
```python
def pixel_sort_horizontal(arr, threshold=128):
    result = arr.copy()
    luminance = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]

    for row_idx in range(arr.shape[0]):
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
```

**JavaScript Translation:**
```javascript
async function pixelSortHorizontal(threshold = 128) {
    const pixelData = await imaging.getPixels({
        documentID: doc.id,
        layerID: layer.id
    });

    const { imageData, width, height } = pixelData;
    const result = new Uint8Array(imageData);

    // Process row by row
    for (let y = 0; y < height; y++) {
        const rowStart = y * width * 4;
        const rowPixels = [];

        // Extract row with luminance
        for (let x = 0; x < width; x++) {
            const idx = rowStart + x * 4;
            const r = imageData[idx];
            const g = imageData[idx + 1];
            const b = imageData[idx + 2];
            const lum = 0.299 * r + 0.587 * g + 0.114 * b;

            if (lum > threshold) {
                rowPixels.push({ x, r, g, b, lum });
            }
        }

        // Sort by luminance
        rowPixels.sort((a, b) => a.lum - b.lum);

        // Write back sorted pixels
        rowPixels.forEach((pixel, sortedIdx) => {
            const originalIdx = rowStart + pixel.x * 4;
            result[originalIdx] = pixel.r;
            result[originalIdx + 1] = pixel.g;
            result[originalIdx + 2] = pixel.b;
        });
    }

    await imaging.putPixels({
        documentID: doc.id,
        layerID: layer.id,
        imageData: result
    });
}
```

**Filters Using This Pattern:**
- [ ] Pixel Sort Horizontal
- [ ] Pixel Sort Vertical
- [ ] Datamosh Blocks
- [ ] Bayer Dithering
- [ ] GameBoy 4-bit
- [ ] C64 Palette

---

### Pattern 3: Native Photoshop Filters (Easiest via batchPlay)

**Use When:** Photoshop has a native filter that approximates the effect

**Python Example:**
```python
def gaussian_blur(arr, sigma=5):
    from scipy.ndimage import gaussian_filter
    result = arr.copy().astype(np.float32)
    for c in range(3):
        result[:,:,c] = gaussian_filter(result[:,:,c], sigma=sigma)
    return result.astype(np.uint8)
```

**JavaScript Translation:**
```javascript
async function gaussianBlur(radius = 5) {
    await require('photoshop').action.batchPlay([{
        "_obj": "gaussianBlur",
        "radius": {
            "_unit": "pixelsUnit",
            "_value": radius
        }
    }], {});
}
```

**Filters Using This Pattern:**
- [ ] Bloom Glow (Gaussian Blur + Screen blend)
- [ ] Emboss (Native Emboss filter)
- [ ] Edge Detect (Find Edges filter)
- [ ] Oil Paint (Oil Paint filter)

---

### Pattern 4: Custom Algorithm Implementation (Hardest)

**Use When:** No Photoshop equivalent, requires full custom logic

**Python Example:**
```python
def voronoi_cells(arr, num_points=50):
    from scipy.spatial import Voronoi
    h, w, _ = arr.shape
    points = np.random.rand(num_points, 2) * [w, h]
    vor = Voronoi(points)

    # Complex tessellation logic...
    # (100+ lines of Voronoi cell rendering)

    return result
```

**JavaScript Translation:**
**Option A:** Pre-render pattern and overlay
```javascript
async function voronoiCells(numPoints = 50) {
    // Create new document for pattern
    const patternDoc = await app.documents.add();

    // Generate Voronoi points
    const points = [];
    for (let i = 0; i < numPoints; i++) {
        points.push({
            x: Math.random() * doc.width,
            y: Math.random() * doc.height
        });
    }

    // Use getPixels() to manually compute Voronoi
    // (or use external library like d3-delaunay)
}
```

**Option B:** Use external library (d3-delaunay, etc.)

**Filters Using This Pattern:**
- [ ] Voronoi Cells (SciPy Voronoi)
- [ ] Reaction-Diffusion (Gray-Scott model)
- [ ] Mandelbrot Map (Fractal generation)
- [ ] Cellular Automata (Conway's Game of Life variant)
- [ ] Flow Field (Vector field computation)

---

## 🛠️ Translation Toolbox

### Numpy Equivalents

| Numpy | JavaScript UXP |
|-------|----------------|
| `arr.copy()` | `new Uint8Array(imageData)` |
| `arr.shape` | `[height, width, 4]` (RGBA) |
| `np.roll(arr, offset, axis=1)` | Manual loop with modulo |
| `np.argsort(arr)` | `arr.sort()` with index tracking |
| `np.where(condition)` | `arr.filter((v, i) => condition)` |
| `np.clip(arr, 0, 255)` | `Math.max(0, Math.min(255, v))` |
| `np.random.rand()` | `Math.random()` |
| `np.sin(x)` | `Math.sin(x)` |

### SciPy Equivalents

| SciPy | Photoshop/UXP |
|-------|---------------|
| `scipy.ndimage.gaussian_filter` | `batchPlay("gaussianBlur")` |
| `scipy.ndimage.sobel` | `batchPlay("findEdges")` |
| `scipy.spatial.Voronoi` | External lib (d3-delaunay) |
| `scipy.spatial.Delaunay` | External lib (d3-delaunay) |
| `scipy.ndimage.convolve` | Custom convolution or native filters |

### PIL Equivalents

| PIL | Photoshop/UXP |
|-----|---------------|
| `Image.new()` | `app.documents.add()` |
| `Image.open()` | `app.activeDocument` |
| `ImageDraw.Draw()` | Layer operations |
| `ImageFilter.BLUR` | `batchPlay("gaussianBlur")` |

---

## 📝 Implementation Checklist

For each filter translation:

### 1. Analysis Phase
- [ ] Read Python implementation in `filters_engine.py`
- [ ] Identify Numpy/SciPy dependencies
- [ ] Determine translation pattern (Layer/Pixel/Native/Custom)
- [ ] Check if Photoshop has native equivalent

### 2. Implementation Phase
- [ ] Write JavaScript function in `main.js`
- [ ] Add data stream logging
- [ ] Wrap in `executeAsModal`
- [ ] Add to switch statement in `applySelectedFilter()`

### 3. Testing Phase
- [ ] Test on small image (500×500)
- [ ] Test on medium image (2000×2000)
- [ ] Test on large image (4000×4000)
- [ ] Compare output with Desktop version
- [ ] Check performance (< 5s for medium images)

### 4. Documentation Phase
- [ ] Update this guide with translation notes
- [ ] Add JSDoc comments
- [ ] Update README.md filter count
- [ ] Mark as completed in progress table

---

## ⚡ Performance Tips

### 1. Minimize `getPixels()` / `putPixels()` Calls
- These transfer large amounts of data (slow)
- Batch operations when possible
- Use layer operations instead if feasible

### 2. Use Photoshop Native Filters
- Always faster than custom JavaScript
- Check `batchPlay` documentation for available filters
- Combine multiple native filters instead of pixel loops

### 3. Optimize Loops
- Avoid nested loops when possible
- Use typed arrays (`Uint8Array`, `Float32Array`)
- Pre-allocate arrays instead of push/concat

### 4. Consider WebAssembly for Complex Filters
- Compile compute-heavy logic to WASM
- 10-100× faster than JavaScript for numerical operations
- Worth it for filters like Reaction-Diffusion, Voronoi

---

## 🎯 Next Filters to Port (Priority Order)

### Easy Wins (Layer-based)
1. **Scanline Corrupt** — Horizontal line displacement
2. **Neon Edges** — Sobel + colorize (native filter)
3. **Posterize** — Native Photoshop filter
4. **Solarize** — Native Photoshop filter

### Medium Complexity (Pixel-level)
5. **Pixel Sort Horizontal** — Documented above
6. **Pixel Sort Vertical** — Same as horizontal
7. **GameBoy 4-bit** — 4-color palette mapping
8. **Bayer Dithering** — 8×8 pattern dithering

### High Complexity (Custom algorithms)
9. **Voronoi Cells** — Requires d3-delaunay
10. **Reaction-Diffusion** — Gray-Scott PDE simulation
11. **ASCII Render** — Text rendering + sampling
12. **Mandelbrot Map** — Fractal generation

---

## 📚 Resources

### Adobe UXP API
- [Imaging API](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/imaging/)
- [batchPlay Reference](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/batchplay/)
- [Layer API](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/classes/layer/)

### External Libraries
- [d3-delaunay](https://github.com/d3/d3-delaunay) — Voronoi/Delaunay
- [ml-matrix](https://github.com/mljs/matrix) — Matrix operations
- [ndarray](https://github.com/scijs/ndarray) — N-dimensional arrays

### Reference Implementations
- [Desktop filters_engine.py](../X-FLTR-DESKTOP/filters_engine.py)
- [Processing.js filters](https://github.com/processing/p5.js) — Similar patterns

---

## 🏆 Translation Examples

See `main.js` for complete implementations:
- ✅ `rgbSplitLinear()` — Layer-based pattern
- ✅ `rgbSplitWave()` — Layer-based + distortion
- 🚧 `pixelSortHorizontal()` — Pixel-level pattern (to implement)

---

**Status:** 📚 Living document — Updated as filters are ported

**Last Updated:** 2025-02-15

**⚡ From Numpy to UXP. From arrays to layers. The translation continues. ⚡**
