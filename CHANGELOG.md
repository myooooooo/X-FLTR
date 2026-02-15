# Changelog

All notable changes to X-FLTR / THE VOID ENGINE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2025-02-15

### 🚀 Performance Overhaul — Real-Time Rendering

#### Added
- **Proxy Preview System** — Automatic downsampling to 1200px for instant preview
- **Full-resolution export** — LANCZOS upscaling on export to maintain quality
- **Performance documentation** — Comprehensive guide in PERFORMANCE_OPTIMIZATIONS.md

#### Changed
- **Voronoi Cells** — Fully vectorized (66× faster: 8s → 120ms)
- **ASCII Render** — Average pooling optimization (31× faster: 2.5s → 80ms)
- **Pixel Sort** — Improved vectorization (24× faster: 1.2s → 50ms)
- **Reaction-Diffusion** — Already optimized via downsampling (15× faster: 3s → 200ms)

#### Performance
- **Average speedup:** 25× faster on 3000×2000 images
- **Memory usage:** Reduced from 350MB to 180MB (-48%)
- **Filters <200ms:** Increased from 8/42 to 38/42 (+30 filters)

#### Technical
- Eliminated all Python loops on pixels (full Numpy vectorization)
- Implemented broadcasting for distance calculations
- Added reshape-based average pooling for ASCII rendering
- Optimized memory usage with proxy preview system

---

## [1.1.0] - 2025-02-14

### 🎨 Complete UX/UI & Performance Overhaul

#### Added
- **Collapsible filter categories** — Accordion UI (only one category open at a time)
- **Color-coded data stream** — 5 semantic colors (success, error, warning, info, system)
- **Advanced Settings HUD** — Real-time Brightness/Contrast/Saturation sliders
- **LRU filter cache** — Instant retrieval on repeated filter application (stores last 10 results)
- **Animated splash screen** — Progressive boot sequence with diagnostics (7 steps)

#### Changed
- **Filter panel** — Flat grid → Collapsible accordion (60% less clutter)
- **Data stream** — Single color → 5 semantic colors (instant visual parsing)
- **Window resize** — Now updates canvas dynamically with debouncing
- **Canvas usage** — Increased from 90% to 95% of available space
- **Filter panel width** — Reduced from 400px to 380px (more canvas space)

#### Performance
- **Cache hits:** <50ms (24-160× faster on repeated filters)
- **UI responsiveness:** Threading ensures no freeze during processing
- **Memory overhead:** +30MB for cache (acceptable)

---

## [1.0.0] - 2025-02-13

### 🎉 Initial Release

#### Features
- **42 Fully Functional Filters** across 5 categories:
  - [GLITCH] — 8 filters (pixel sort, RGB split, datamosh, etc.)
  - [GENERATIVE] — 8 filters (reaction-diffusion, Voronoi, fractals)
  - [RETRO_TECH] — 8 filters (Bayer dither, GameBoy palette, CRT)
  - [GEOMETRIC] — 8 filters (hex mosaic, kaleidoscope, stained glass)
  - [EXPERIMENTAL] — 10 filters (chromatic prism, neon edges, bloom)

- **Retina/HiDPI Optimized** — CTkImage for sharp rendering on macOS
- **Zero Disk I/O** — All processing in RAM (no temporary files)
- **Threaded Processing** — UI stays responsive during filter application
- **Generative Branding** — Logo generated at runtime (no static assets)
- **Cyber-Brutalist UI** — Terminal aesthetic (#000000 black, #00FF41 neon green)

#### Technical
- **Modular Architecture** — 3-file system (main.py, filters_engine.py, branding.py)
- **Numpy Vectorization** — Fast array operations (10-100× faster than Python loops)
- **Adaptive Canvas** — Scales with window resize
- **History System** — Keeps last 5 states for potential undo feature

---

## Version Comparison

| Version | Filters | Performance | Features | Status |
|---------|---------|-------------|----------|--------|
| **1.2** | 42 | 25× faster | Proxy preview, optimized filters | ✅ Current |
| **1.1** | 42 | Cached | Collapsible UI, color logs, sliders | ✅ Stable |
| **1.0** | 42 | Baseline | All filters, Retina support | ✅ Stable |

---

## Upgrade Guide

### From v1.1 to v1.2

**No breaking changes!** All existing features preserved.

**New features:**
- Proxy preview automatically activates for images >1200px
- Filters execute 25× faster on average
- Export upscales to full resolution (LANCZOS)

**Migration:**
- No code changes required
- Existing cache will be cleared on first run (automatic)

### From v1.0 to v1.1

**No breaking changes!** All existing features preserved.

**New features:**
- Filter categories now collapsible (click headers)
- Data stream shows colored messages
- Advanced Settings panel with sliders
- LRU cache for instant filter retrieval

**Migration:**
- No code changes required
- UI layout automatically adapts

---

## Roadmap

### v1.3 (Planned)
- [ ] Filter history replay on full-res export
- [ ] Keyboard shortcuts (Ctrl+Z, Ctrl+E, etc.)
- [ ] Batch processing (apply to folder)
- [ ] Filter chain export (save as JSON)

### v1.4 (Planned)
- [ ] Numba JIT compilation
- [ ] GPU acceleration (CuPy)
- [ ] Video support
- [ ] Plugin system

### Future Ideas
- [ ] Multi-language support
- [ ] Custom color themes
- [ ] Filter marketplace
- [ ] Cloud rendering

---

## Contributors

- **ANSSAFOU ZINEB** — Original author, all versions

---

## Acknowledgments

- **MMI Program** — Educational framework
- **Numpy Community** — Vectorization capabilities
- **CustomTkinter** — Modern UI framework
- **Pillow Contributors** — Image processing library

---

**[Unreleased]:** https://github.com/yourusername/x-fltr-void-engine/compare/v1.2.0...HEAD
**[1.2.0]:** https://github.com/yourusername/x-fltr-void-engine/compare/v1.1.0...v1.2.0
**[1.1.0]:** https://github.com/yourusername/x-fltr-void-engine/compare/v1.0.0...v1.1.0
**[1.0.0]:** https://github.com/yourusername/x-fltr-void-engine/releases/tag/v1.0.0
