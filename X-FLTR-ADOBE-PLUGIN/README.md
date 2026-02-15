# X-FLTR / THE VOID ENGINE — Adobe Photoshop Plugin

![Version](https://img.shields.io/badge/version-2.0.0-00FF41) ![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow) ![Adobe](https://img.shields.io/badge/adobe-UXP-blue) ![Status](https://img.shields.io/badge/status-in_development-orange)

**Native Photoshop integration for X-FLTR's 42 artistic filters**

Developed by **ANSSAFOU ZINEB** | Digital Creation Lab | MMI Portfolio 2025

---

## 🎯 Overview

This is the **Adobe Photoshop plugin version** of X-FLTR / THE VOID ENGINE, translating all 42 Python filters to JavaScript using Adobe's **UXP (Unified Extensibility Platform)**.

**Current Status:** 🚧 **Proof of Concept** — 2 filters ported (RGB Split Linear/Wave)

---

## 🚀 Installation

### Prerequisites
- **Adobe Photoshop 2026** or later
- **Adobe UXP Developer Tool** ([Download here](https://developer.adobe.com/photoshop/uxp/guides/get-started/))

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/myooooooo/X-FLTR.git
   cd X-FLTR/X-FLTR-ADOBE-PLUGIN
   ```

2. **Open Adobe UXP Developer Tool:**
   - Launch the UXP Developer Tool application
   - Click **"Add Plugin"**
   - Navigate to `manifest.json` in this folder
   - Click **"Load"**

3. **Launch in Photoshop:**
   - Open Adobe Photoshop 2026+
   - Go to **Plugins → X-FLTR / THE VOID ENGINE**
   - The plugin panel will appear

---

## 📁 Project Structure

```
X-FLTR-ADOBE-PLUGIN/
├── manifest.json       # Adobe UXP configuration
├── index.html          # Cyber-Brutalist UI (Neon Green + Black)
├── styles.css          # Terminal-style CSS
├── main.js             # Filter implementations (JavaScript ports)
├── icons/              # Plugin icons (23×23, 48×48)
└── README.md           # This file
```

---

## 🎨 User Interface

The plugin preserves the **Cyber-Brutalist aesthetic** of the Desktop version:

- **Color Scheme:** Neon Green (#00FF41) on Pure Black (#000000)
- **Typography:** Courier New monospace
- **Layout:** Accordion-style filter categories
- **Console:** Live data stream with color-coded logs

### UI Components

1. **Header**
   - ASCII art logo
   - Project title
   - Author signature
   - Version number

2. **Data Stream Console**
   - Color-coded logs:
     - `White` — System messages
     - `Green` — Success
     - `Red` — Error
     - `Orange` — Warning
     - `Cyan` — Info

3. **Filter Categories (Accordion)**
   - `[GLITCH]` — 8 filters
   - `[GENERATIVE]` — 8 filters
   - `[RETRO-TECH]` — 8 filters
   - `[GEOMETRIC]` — 8 filters
   - `[EXPERIMENTAL]` — 10 filters

4. **Control Panel**
   - Apply Filter button (disabled until filter selected)
   - Status indicator

---

## 🔧 Technical Implementation

### Technology Stack

- **HTML5** — Structure
- **CSS3** — Cyber-Brutalist styling
- **JavaScript (ES6+)** — Filter logic
- **Adobe UXP API** — Photoshop integration
- **Photoshop Imaging API** — Pixel manipulation
- **batchPlay** — Advanced Photoshop actions

### Code Architecture

```javascript
// Filter Implementation Pattern
async function filterName(parameter) {
    const doc = app.activeDocument;
    const layer = doc.activeLayers[0];

    await executeAsModal(async () => {
        // Photoshop API operations here
        // (layer manipulation, pixel access, etc.)
    }, { commandName: 'Filter Name' });
}
```

### Translation Approach

**Python (Numpy) → JavaScript (UXP)**

| Python | JavaScript UXP |
|--------|----------------|
| `np.roll()` | Manual pixel shifting + layer translate |
| `np.copy()` | `layer.duplicate()` |
| `scipy.ndimage` | Photoshop native filters via `batchPlay` |
| `PIL.Image` | `imaging.getPixels()` / `putPixels()` |
| Threading | `async`/`await` + `executeAsModal` |

---

## 📊 Filter Implementation Status

### ✅ Implemented (2/42)

| Filter | Category | Status | Notes |
|--------|----------|--------|-------|
| RGB Split Linear | GLITCH | ✅ Working | Layer duplication + channel mixer |
| RGB Split Wave | GLITCH | ✅ Working | Simplified (full wave needs batchPlay) |

### 🚧 In Progress (40/42)

**Next Priorities:**
1. **Pixel Sort Horizontal** — Requires pixel-level access via `getPixels()`
2. **Pixel Sort Vertical** — Same approach as horizontal
3. **Datamosh Blocks** — Block shuffling via `getPixels()` manipulation
4. **GameBoy 4-bit** — Color palette mapping (straightforward)
5. **Bayer Dithering** — Pattern-based dithering (medium complexity)

**Complex Filters (Require batchPlay):**
- Voronoi Cells (no native Photoshop equivalent)
- Reaction-Diffusion (custom convolution kernel)
- ASCII Render (text generation)

---

## 🛠️ Development

### Adding a New Filter

1. **Analyze Python implementation** in `X-FLTR-DESKTOP/filters_engine.py`
2. **Identify Photoshop equivalent** (native filter vs. pixel manipulation)
3. **Implement in `main.js`:**

```javascript
async function myCustomFilter(param1, param2) {
    addDataStreamLog(`MY FILTER: PARAM1=${param1}`, 'info');

    await executeAsModal(async () => {
        const doc = app.activeDocument;
        const layer = doc.activeLayers[0];

        // Your implementation here
        // Option 1: Use Photoshop native filters
        // Option 2: Pixel-level manipulation via getPixels()
        // Option 3: Layer operations (duplicate, blend modes, etc.)

    }, { commandName: 'My Custom Filter' });

    addDataStreamLog('FILTER APPLIED SUCCESSFULLY', 'success');
}
```

4. **Add to switch statement** in `applySelectedFilter()`
5. **Test in Photoshop**

### Debugging

- Use **UXP Developer Tool Console** for logs
- `console.log()` outputs appear in DevTools
- Check `addDataStreamLog()` for user-facing messages

---

## 📚 Resources

### Adobe UXP Documentation
- **[UXP for Photoshop](https://developer.adobe.com/photoshop/uxp/)** — Main guide
- **[Imaging API](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/imaging/)** — Pixel manipulation
- **[batchPlay](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/batchplay/)** — Advanced actions
- **[executeAsModal](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/modules/core/)** — Async operations

### Python Original
- **[filters_engine.py](../X-FLTR-DESKTOP/filters_engine.py)** — Reference implementation
- **[Desktop README](../X-FLTR-DESKTOP/README_XFLTR.md)** — Full technical docs

---

## 🔬 Translation Challenges

### 1. **Numpy Arrays → JavaScript Arrays**
**Problem:** Numpy's vectorized operations don't have direct JS equivalents.

**Solution:**
- Simple operations: Manual loops (acceptable for UXP performance)
- Complex operations: Use Photoshop native filters via `batchPlay`

### 2. **SciPy Functions → Photoshop Filters**
**Problem:** No `scipy.ndimage`, `scipy.spatial`, etc.

**Solution:**
- Voronoi/Delaunay: Pre-render patterns or use external library
- Convolution: Photoshop's native filters (Gaussian Blur, etc.)

### 3. **Performance**
**Problem:** JavaScript loops are slower than vectorized Numpy.

**Solution:**
- Use `getPixels()` sparingly (large data transfer)
- Prefer Photoshop native operations
- Consider WebAssembly for compute-heavy filters

---

## 🎓 Educational Value

This plugin demonstrates:

✅ **Cross-Language Translation** — Python → JavaScript
✅ **API Integration** — Adobe UXP, Photoshop Imaging API
✅ **Platform Constraints** — Working within UXP limitations
✅ **Performance Optimization** — Choosing appropriate approaches
✅ **UI Consistency** — Preserving Cyber-Brutalist aesthetic across platforms

---

## 🚀 Roadmap

### Phase 1: Core Filters (Current)
- [x] Project structure
- [x] UI implementation
- [x] 2 proof-of-concept filters
- [ ] 10 GLITCH filters (8 remaining)
- [ ] Documentation

### Phase 2: Advanced Filters
- [ ] 8 GENERATIVE filters (require custom algorithms)
- [ ] 8 RETRO-TECH filters (palette mappings)
- [ ] 8 GEOMETRIC filters (spatial transformations)
- [ ] 10 EXPERIMENTAL filters (mixed approaches)

### Phase 3: Optimization
- [ ] Performance profiling
- [ ] batchPlay integration for complex filters
- [ ] WebAssembly for compute-heavy operations
- [ ] Batch processing support

---

## 📄 License

**MIT License** — Free for personal and educational use.

Copyright © 2025 ANSSAFOU ZINEB

---

## 🏆 Goals

The goal is to achieve **feature parity** with the Desktop version:
- ✅ Same 42 filters
- ✅ Same Cyber-Brutalist aesthetic
- ✅ Native Photoshop integration (layers, history, undo)
- ⚡ Performance optimized for large images

---

**Status:** 🚧 **Active Development** (2/42 filters ported)

**Next Steps:** Implement remaining GLITCH category filters (6 more)

**⚡ From Standalone to Integrated. From Python to JavaScript. The Void Engine evolves. ⚡**
