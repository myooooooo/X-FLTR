# X-FLTR / THE VOID ENGINE — Multi-Platform Suite

![Version](https://img.shields.io/badge/version-2.0-00FF41) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow) ![License](https://img.shields.io/badge/license-MIT-green)

**Professional-grade image processing across Desktop & Adobe Photoshop**

Developed by **ANSSAFOU ZINEB** | Digital Creation Lab | MMI Portfolio Project 2025

---

## 🎯 Project Overview

**X-FLTR / THE VOID ENGINE** is a comprehensive image processing suite featuring **42 artistic filters** with a distinctive **Cyber-Brutalist aesthetic** (Neon Green #00FF41, Pure Black, Terminal UI).

This repository contains **two versions** of the engine:

### 1️⃣ **X-FLTR Desktop** (Standalone Python Application)
- **Location:** [`/X-FLTR-DESKTOP`](X-FLTR-DESKTOP/)
- **Technology:** Python 3.8+ (CustomTkinter + Numpy)
- **Features:** 42 real-time filters, proxy preview system, LRU cache
- **Performance:** 66× faster than v1.1 (Voronoi Cells in 120ms)
- **Platform:** macOS (Retina optimized)
- **Status:** ✅ **Production Ready** (v1.2)

### 2️⃣ **X-FLTR Adobe Plugin** (Native Photoshop Integration)
- **Location:** [`/X-FLTR-ADOBE-PLUGIN`](X-FLTR-ADOBE-PLUGIN/)
- **Technology:** JavaScript (Adobe UXP API)
- **Features:** Same 42 filters, native Photoshop layer integration
- **Platform:** Adobe Photoshop 2026+
- **Status:** 🚧 **In Development** (v2.0 - 2 filters ported as PoC)

---

## 🚀 Quick Start

### Desktop Version (Python)

```bash
cd X-FLTR-DESKTOP
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

**👉 [Read Full Desktop Documentation](X-FLTR-DESKTOP/README_XFLTR.md)**

### Adobe Plugin (UXP)

1. Install **[Adobe UXP Developer Tool](https://developer.adobe.com/photoshop/uxp/guides/get-started/)**
2. Open Photoshop 2026+
3. Load plugin via **Plugins → Development → Load Plugin**
4. Navigate to `/X-FLTR-ADOBE-PLUGIN/manifest.json`

**👉 [Read Plugin Documentation](X-FLTR-ADOBE-PLUGIN/README.md)** *(coming soon)*

---

## 📊 Technology Comparison

| Feature | Desktop (Python) | Adobe Plugin (UXP) |
|---------|------------------|--------------------|
| **Filters** | 42 fully functional | 2 ported (40 in progress) |
| **Performance** | Proxy preview (66× faster) | Native Photoshop API |
| **UI Framework** | CustomTkinter | HTML/CSS/JavaScript |
| **Aesthetic** | Cyber-Brutalist Terminal | Same (Neon Green + Black) |
| **Export** | 4K PNG/JPEG | Native PSD layers |
| **Platform** | Standalone macOS app | Photoshop 2026+ plugin |
| **Processing** | Numpy vectorized | UXP Imaging API + batchPlay |

---

## 🎨 Filter Categories (42 Total)

Both versions share the same filter library:

### **[GLITCH]** — 8 Filters
- Pixel Sort Horizontal/Vertical
- RGB Split Linear/Wave
- Datamosh Blocks
- Scanline Corrupt
- Bit Crush
- VHS Noise

### **[GENERATIVE]** — 8 Filters
- Reaction-Diffusion
- Voronoi Cells
- Mandelbrot Map
- Flow Field
- Perlin Warp
- Fractal Noise
- Cellular Automata
- Wave Distortion

### **[RETRO-TECH]** — 8 Filters
- GameBoy 4-bit
- C64 Palette
- Bayer Dithering
- ASCII Render
- CRT Curvature
- Phosphor Glow
- Terminal Text
- Dot Matrix

### **[GEOMETRIC]** — 8 Filters
- Hexagon Mosaic
- Stained Glass
- Kaleidoscope
- Isometric Voxels
- Triangle Mesh
- Polygon Reduce
- Crystal Facets
- Radial Blur

### **[EXPERIMENTAL]** — 10 Filters
- Chromatic Prism
- Infrared Sim
- Neon Edges
- Bloom Glow
- Posterize
- Solarize
- Edge Detect
- Emboss
- Oil Paint
- Watercolor

---

## 🏗️ Repository Structure

```
X-FLTR-VOID-ENGINE/
│
├── X-FLTR-DESKTOP/              ← Python Standalone Application
│   ├── main.py                  # UI + Application Logic (950+ lines)
│   ├── filters_engine.py        # 42 Filter Functions (900+ lines)
│   ├── branding.py              # Logo + Identity Generator
│   ├── requirements.txt         # Python dependencies
│   ├── README_XFLTR.md          # Full technical documentation
│   ├── QUICK_START_V1.2.md      # User guide
│   ├── PERFORMANCE_OPTIMIZATIONS.md
│   └── archive/                 # Previous versions
│
├── X-FLTR-ADOBE-PLUGIN/         ← Adobe UXP Plugin
│   ├── manifest.json            # Adobe plugin configuration
│   ├── index.html               # Cyber-Brutalist UI
│   ├── styles.css               # Neon Green + Black styling
│   ├── main.js                  # Filter logic (JavaScript ports)
│   └── README.md                # Plugin-specific docs (WIP)
│
├── README.md                    # This file (Multi-platform overview)
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
└── .gitignore                   # Git ignore rules
```

---

## 🔬 Technical Architecture

### Python Desktop Version

**Core Technologies:**
- **CustomTkinter** — Modern UI framework
- **Pillow (PIL)** — Image I/O and drawing
- **Numpy** — Vectorized array operations (no Python loops!)
- **SciPy** — Scientific computing (Delaunay, convolution)
- **Threading** — Non-blocking filter processing
- **Hashlib** — LRU cache key generation

**Performance Optimizations:**
1. **Proxy Preview System** — Downsample large images to 1200px for instant preview
2. **Vectorized Numpy** — All filters fully optimized (25× faster than v1.1)
3. **LRU Cache** — Instant retrieval on repeated filter application
4. **Threaded Processing** — UI stays responsive during heavy operations

### Adobe UXP Plugin

**Core Technologies:**
- **Adobe UXP** — Unified Extensibility Platform (HTML/CSS/JS)
- **Photoshop Imaging API** — Native pixel manipulation
- **batchPlay** — Advanced Photoshop actions scripting
- **executeAsModal** — Asynchronous operations wrapper

**Translation Challenges:**
- **Numpy → JavaScript:** No direct equivalent (manual array operations)
- **SciPy → UXP:** Use Photoshop native filters where possible
- **Threading → Async/Await:** Different paradigm for non-blocking execution

---

## 🎓 Educational Context

This project was developed for the **MMI (Métiers du Multimédia et de l'Internet)** program and demonstrates:

### Technical Competencies
✅ **Software Architecture** — Modular design, separation of concerns
✅ **Cross-Platform Development** — Desktop app + Plugin
✅ **Performance Optimization** — Numpy vectorization, proxy preview, LRU caching
✅ **Image Processing** — 42 unique algorithms, color space transformations
✅ **API Integration** — Adobe UXP, Photoshop Imaging API
✅ **Code Translation** — Python → JavaScript porting

### Creative Coding
✅ **Generative Art** — Runtime logo generation, procedural patterns
✅ **Glitch Aesthetics** — Databending, chromatic aberration, pixel sorting
✅ **UI/UX Design** — Cyber-Brutalist aesthetic, terminal-style interface
✅ **Color Theory** — Semantic color-coding (#00FF41 Neon Green)

---

## 📚 Documentation

### Desktop (Python)
- **[README_XFLTR.md](X-FLTR-DESKTOP/README_XFLTR.md)** — Complete technical documentation
- **[QUICK_START_V1.2.md](X-FLTR-DESKTOP/QUICK_START_V1.2_PERFORMANCE.md)** — User guide
- **[HOW_TO_ADD_FILTER.md](X-FLTR-DESKTOP/HOW_TO_ADD_FILTER.md)** — Add custom filters
- **[PERFORMANCE_OPTIMIZATIONS.md](X-FLTR-DESKTOP/PERFORMANCE_OPTIMIZATIONS.md)** — Deep-dive analysis

### Adobe Plugin (UXP)
- **[Plugin README](X-FLTR-ADOBE-PLUGIN/README.md)** — Installation & usage *(coming soon)*
- **[Translation Guide](X-FLTR-ADOBE-PLUGIN/TRANSLATION_GUIDE.md)** — Python → JS porting *(coming soon)*

---

## 🛠️ Development Roadmap

### ✅ Phase 1: Desktop Application (COMPLETED)
- [x] 42 filters implemented in Python
- [x] Real-time proxy preview system
- [x] LRU cache optimization
- [x] Cyber-Brutalist UI design
- [x] 4K export capability
- [x] Full documentation

### 🚧 Phase 2: Adobe Plugin (IN PROGRESS)
- [x] UXP project structure initialized
- [x] Cyber-Brutalist UI ported to HTML/CSS
- [x] 2 filters translated (RGB Split Linear/Wave) — **Proof of Concept**
- [ ] Remaining 40 filters translation (Python → JavaScript)
- [ ] batchPlay API integration for advanced filters
- [ ] Performance optimization for large images
- [ ] Full documentation & installation guide

### 🔮 Phase 3: Future Enhancements (PLANNED)
- [ ] Web version (WebAssembly + WASM)
- [ ] Mobile app (React Native)
- [ ] Real-time video processing (frame-by-frame)
- [ ] GPU acceleration (WebGL/CUDA)
- [ ] Custom filter creation UI

---

## 📄 License

**MIT License** — Free for personal and educational use.

```
Copyright © 2025 ANSSAFOU ZINEB

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🏆 Achievements

✅ **42 Fully Functional Filters** — No placeholders, all production-ready
✅ **Real-Time Performance** — 66× faster (Voronoi: 8s → 120ms)
✅ **Multi-Platform Architecture** — Desktop + Adobe Plugin
✅ **Cross-Language Translation** — Python → JavaScript porting
✅ **Professional UX** — Cyber-Brutalist aesthetic, color-coded logs
✅ **Well Documented** — 10+ comprehensive guides
✅ **Zero Disk I/O** — All processing in RAM
✅ **Retina Optimized** — Sharp on all macOS HiDPI displays

---

## 📞 Contact

**Author:** ANSSAFOU ZINEB
**Lab:** DIGITAL CREATION LAB
**Project Type:** MMI Portfolio — Multi-Platform Image Processing Suite
**Year:** 2025

---

## 🎓 Acknowledgments

- **MMI Program** — Métiers du Multimédia et de l'Internet
- **Numpy Community** — Incredible vectorization capabilities
- **CustomTkinter** — Modern Python UI framework
- **Adobe UXP Team** — Extensibility platform for Creative Cloud
- **Pillow Contributors** — Powerful image processing library

---

## 🌟 Project Philosophy

> **"Real-time rendering. 66× performance boost. 42 filters. Two platforms. Zero compromises."**

This project embodies the fusion of **performance engineering** (Numpy optimization, proxy preview) and **creative coding** (glitch aesthetics, generative art), demonstrating that artistic tools can be both **visually distinctive** and **technically sophisticated**.

The **Cyber-Brutalist aesthetic** (#00FF41 Neon Green, Pure Black, Terminal UI) is not just visual styling — it's a statement about **transparency, efficiency, and raw computational power**.

---

**⚡ One vision. Two platforms. Infinite possibilities. ⚡**

---

**Status:** 🚀 **Desktop: Production Ready** | 🚧 **Plugin: Active Development**

**All systems operational. Ready for portfolio presentation. 🎓**
