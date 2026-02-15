# NEURO-CORRUPT v1.0
## A Post-Digital Glitch Engine for Creative Technologists

![License: MIT](https://img.shields.io/badge/License-MIT-00FF41.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-FF0055.svg)
![Status: Portfolio Ready](https://img.shields.io/badge/Status-Portfolio_Ready-00FF41.svg)

---

## 🎯 Project Overview

**NEURO-CORRUPT** is a desktop data-bending application that transforms images into glitch art textures through algorithmic corruption. Built with a Cyber-Brutalist interface, it empowers motion designers, digital artists, and creative coders to explore post-digital aesthetics through real-time visual manipulation.

### Key Features
- **Bit-Shifting Engine**: Binary-level manipulation for horizontal tearing artifacts
- **RGB Channel Separation**: Chromatic aberration effects via independent channel offsetting
- **Pixel Sorting Algorithm**: Luminance-based reorganization for "data-mosh" aesthetics
- **Real-Time Preview**: Near-instant visual feedback as parameters change
- **High-Res Export**: One-click PNG export for use in Adobe Creative Cloud
- **Cyber-Brutalist UI**: Industrial command-center interface with neon accents

---

## 🖥️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**
```bash
cd /path/to/project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

---

## 🎨 Usage Guide

### Basic Workflow

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Load Image**
   - Click `LOAD IMAGE` in the sidebar
   - Select a PNG, JPG, or BMP file
   - Image appears in the center canvas

3. **Apply Glitch Effects**
   - **Bit Shift** (0-255): Digital artifacts and horizontal tearing
   - **RGB Offsets** (-100 to +100): Chromatic aberration per channel
   - **Sort Threshold** (0-255): Luminance-based pixel reorganization
   - **Sort Direction**: Horizontal or Vertical sorting

4. **Export Result**
   - Click `EXPORT PNG`
   - Choose save location
   - High-resolution PNG is saved

5. **Reset Parameters**
   - Click `RESET ALL` to return to original image

---

## 🔧 Technical Architecture

### Code Structure

```
main.py
├── GlitchEngine (Static Methods)
│   ├── bit_shift_glitch()      # Binary XOR operations
│   ├── channel_offset()        # RGB layer displacement
│   └── pixel_sort()            # Luminance-based sorting
│
└── NeuroCorruptUI (CustomTkinter App)
    ├── _build_sidebar()        # Control panel construction
    ├── _build_canvas()         # Preview area
    ├── _process_glitch()       # Effect pipeline
    └── _export_image()         # High-res PNG export
```

### Algorithm Deep-Dive

#### 1. Bit-Shifting (Binary Manipulation)
```python
result = np.bitwise_xor(image_array, shift_amount)
```
- Applies XOR operation at bit level
- Creates horizontal "tearing" artifacts
- Exposes digital materiality of image data

#### 2. Channel Offset (Chromatic Aberration)
```python
result[:, :, 0] = np.roll(result[:, :, 0], r_offset, axis=1)  # Red
result[:, :, 1] = np.roll(result[:, :, 1], g_offset, axis=1)  # Green
result[:, :, 2] = np.roll(result[:, :, 2], b_offset, axis=1)  # Blue
```
- Shifts each RGB channel independently
- Mimics VHS tracking errors and lens aberrations
- Creates prismatic, lo-fi distortions

#### 3. Pixel Sorting (Data-Mosh)
```python
luminance = 0.299*R + 0.587*G + 0.114*B  # Standard luminance formula
# Sort pixels above threshold by brightness
```
- Calculates per-pixel luminance
- Reorders bright regions based on brightness values
- Produces structured, organic glitch patterns

---

## 🎭 UI Design Philosophy

### Cyber-Brutalist Aesthetic

**Core Principles:**
- **Anti-Skeuomorphic**: No rounded corners, gradients, or shadows
- **Honest Structure**: Visible borders, grid-based layout
- **Terminal-Inspired**: Monospace fonts, technical language
- **High Contrast**: Deep blacks with neon green/pink accents

**Color Palette:**
| Color | Hex | Usage |
|-------|-----|-------|
| Deep Black | `#0D0D0D` | Main background |
| Charcoal | `#1A1A1A` | Sidebar panels |
| Matrix Green | `#00FF41` | Primary actions, borders |
| Cyber Pink | `#FF0055` | Section headers, warnings |

**Typography:**
- Headers: **JetBrains Mono** (Bold, 16px)
- Buttons: **JetBrains Mono** (Bold, 13px)
- Labels: **Courier** (Regular, 11px)

*(See [STYLE_GUIDE.md](STYLE_GUIDE.md) for complete design system)*

---

## 📐 Customization

### Adding New Glitch Effects

1. **Add algorithm to `GlitchEngine` class:**
```python
@staticmethod
def custom_effect(image_array, param):
    # Your glitch logic here
    return modified_array
```

2. **Create UI slider in `_build_sidebar()`:**
```python
self._create_slider(sidebar, "Effect Name", 'param_key', 0, 100, 1)
```

3. **Add to processing pipeline in `_process_glitch()`:**
```python
result = GlitchEngine.custom_effect(result, self.params['param_key'])
```

### Modifying Colors

Edit the class constants in `NeuroCorruptUI`:
```python
BG_PRIMARY = "#0D0D0D"      # Your custom background
ACCENT_NEON = "#00FF41"     # Your primary accent color
```

---

## 🎓 Educational Context

This project demonstrates proficiency in:

**Technical Skills:**
- Object-Oriented Programming (classes, static methods)
- Numpy array manipulation for image processing
- GUI development with CustomTkinter
- Real-time data visualization

**Creative Competencies:**
- Algorithmic art and generative design
- Post-digital aesthetic theory
- UI/UX design with custom theming
- Creative coding for motion design workflows

**MMI Portfolio Value:**
- Bridges computer science, visual arts, and design theory
- Production-ready tool with professional interface
- Demonstrates understanding of glitch art history and contemporary digital aesthetics

---

## 📚 References & Influences

**Glitch Art Theory:**
- Rosa Menkman – *The Glitch Moment(um)* (2011)
- Iman Moradi – *Glitch Aesthetics* (2004)
- Nick Briz – Glitch Codec Tutorials

**Technical Inspiration:**
- Kim Asendorf – Pixel Sorting Algorithms
- Phillip Stearns – *Year of the Glitch*
- Processing Foundation – Creative Coding Community

**UI/UX Precedents:**
- Wireshark (network protocol analyzer)
- Metasploit Console (penetration testing framework)
- Ableton Live (music production DAW)

---

## 🚀 Future Enhancements

**Planned Features:**
- [ ] Audio-reactive mode (map sound to glitch parameters)
- [ ] Batch processing with preset "glitch signatures"
- [ ] Video databending (frame-by-frame corruption)
- [ ] Webcam input for live glitch performance
- [ ] Machine learning-generated glitch presets

**Advanced Techniques:**
- [ ] JPEG/PNG compression artifacts simulation
- [ ] Dithering algorithms (Floyd-Steinberg, Bayer)
- [ ] Voronoi-based pixel displacement
- [ ] FFT-based frequency domain manipulation

---

## 📄 License

MIT License – Free for personal and commercial use.

```
Copyright (c) 2025 MMI Student Portfolio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, modify, and distribute for creative projects.
```

---

## 🤝 Contributing

This is a student portfolio project, but suggestions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-glitch-algorithm`)
3. Commit changes (`git commit -m 'Add RGB displacement effect'`)
4. Open a pull request

---

## 📧 Contact

**Project Type**: MMI 2nd Year Portfolio
**Technologies**: Python, CustomTkinter, Numpy, Pillow
**Aesthetic**: Cyber-Brutalist, Post-Digital
**Status**: Production Ready

---

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application launches without errors (`python main.py`)
- [ ] Test image loaded successfully
- [ ] Sliders modify preview in real-time
- [ ] PNG export works correctly
- [ ] Interface displays neon green borders and monospace fonts

---

**[ SYSTEM READY :: BEGIN CORRUPTION ]**
