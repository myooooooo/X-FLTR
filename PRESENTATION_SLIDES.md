# NEURO-CORRUPT v2.0: Presentation Deck
## Oral Defense / Portfolio Presentation

---

# SLIDE 1: Title

```
╔════════════════════════════════════════════════════╗
║                                                    ║
║            NEURO-CORRUPT v2.0                     ║
║      A Post-Digital Glitch Engine                 ║
║                                                    ║
║   [Screenshot of glassmorphism interface]         ║
║                                                    ║
║   Student: [Your Name]                            ║
║   Program: MMI 2nd Year                           ║
║   Project Type: Creative Coding Tool              ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

**Talking Points:**
- "Today I'm presenting NEURO-CORRUPT, a desktop application for generative glitch art"
- "This is a professional-grade tool for motion designers and digital artists"
- "Built with Python, CustomTkinter, and modern UI/UX principles"

---

# SLIDE 2: Project Context

## The Problem

**Challenge:** Motion designers need unique textures for posters, title sequences, and digital art, but standard Photoshop filters produce generic results.

**Market Gap:** Existing glitch tools are either:
- Web-based (limited resolution, privacy concerns)
- Command-line only (inaccessible to designers)
- Brutalist UI (intimidating for creative professionals)

**Solution:** A desktop GUI tool with:
- Real-time preview
- High-resolution export
- Modern, approachable interface
- Professional glitch algorithms

---

# SLIDE 3: Technical Stack

```
┌─────────────────────────────────────────┐
│  Frontend UI                            │
│  • CustomTkinter (modern widgets)       │
│  • Glassmorphism design system          │
│  • Retina/HiDPI display support         │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Processing Engine                      │
│  • Numpy (array manipulation)           │
│  • Pillow (image I/O)                   │
│  • Pure Python algorithms               │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Platform Integration                   │
│  • macOS theme detection                │
│  • Native font rendering (SF Pro)       │
│  • System file dialogs                  │
└─────────────────────────────────────────┘
```

---

# SLIDE 4: Architecture Diagram

```
NeuroCorruptApp (UI Layer)
    │
    ├── Sidebar Navigation
    │   ├── File operations (Load/Export)
    │   └── Parameter reset
    │
    ├── Canvas Area
    │   ├── CTkImage display (Retina-optimized)
    │   └── Real-time preview updates
    │
    └── Control Panel (3 Glass Cards)
        ├── Bit Manipulation sliders
        ├── RGB Separation sliders
        └── Pixel Sorting controls
            ↓
    GlitchProcessor (Logic Layer)
        ├── bit_shift_glitch()
        ├── channel_offset()
        └── pixel_sort()
            ↓
        Numpy Arrays (Data Layer)
```

**Key Point:** Separation of concerns enables:
- Independent testing of algorithms
- Potential CLI version
- Batch processing extension

---

# SLIDE 5: Glitch Algorithms

## 1. Bit-Shifting (Binary Corruption)

```python
result = np.bitwise_xor(image_array, shift_amount)
```

**What it does:**
- XOR operation flips bits at binary level
- Creates horizontal "tearing" artifacts
- Exposes digital materiality of image data

**Artistic Effect:** Digital distortion, data transmission errors

---

## 2. RGB Channel Separation

```python
result[:, :, 0] = np.roll(result[:, :, 0], r_offset, axis=1)  # Red
result[:, :, 1] = np.roll(result[:, :, 1], g_offset, axis=1)  # Green
result[:, :, 2] = np.roll(result[:, :, 2], b_offset, axis=1)  # Blue
```

**What it does:**
- Shifts each color channel independently
- Mimics VHS tracking errors
- Creates chromatic aberration

**Artistic Effect:** Analog video glitches, lo-fi aesthetic

---

## 3. Pixel Sorting (Luminance-Based)

```python
luminance = 0.299*R + 0.587*G + 0.114*B
# Sort bright pixels by luminance
```

**What it does:**
- Calculates brightness per pixel
- Reorders pixels above threshold
- Maintains dark regions (preserves structure)

**Artistic Effect:** "Data-mosh" textures, streaking patterns

---

# SLIDE 6: UI/UX Design — Glassmorphism

## Visual Language

**Color Palette:**
- Deep charcoal backgrounds (#1A1B1E)
- Semi-transparent glass cards (#252730)
- Electric purple primary accent (#6C63FF)
- Cyan secondary accent (#00D9FF)

**Typography:**
- SF Pro (native macOS font)
- Clear hierarchy (18px headers, 13px buttons)
- High contrast for accessibility

**Components:**
- 15px rounded corners (modern, approachable)
- 2px subtle borders (depth, not harshness)
- 44px button height (iOS touch target standard)

---

## Design Philosophy

**From Cyber-Brutalist (v1) → Glassmorphism (v2)**

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| Target User | Power users / developers | Creative professionals |
| Aesthetic | Terminal/hacker tool | Modern creative app |
| Corners | Sharp (0px) | Rounded (15px) |
| Colors | Neon green (#00FF41) | Electric purple (#6C63FF) |
| Fonts | Monospace only | SF Pro (sans-serif) |
| Feel | Intimidating, technical | Approachable, professional |

**Rationale:** Glassmorphism aligns with tools like Figma, Adobe XD, and Sketch—familiar to my target audience.

---

# SLIDE 7: Critical Fix — Retina Display Support

## The Problem

**Before (v1.0):**
```python
photo = ImageTk.PhotoImage(display_img)
label.configure(image=photo)
```

**Issue:**
- `ImageTk` doesn't handle high-DPI scaling
- Images appear blurry on Retina displays
- tkinter generates scaling warnings

---

## The Solution

**After (v2.0):**
```python
self.display_image = ctk.CTkImage(
    light_image=pil_image,
    dark_image=pil_image,
    size=(display_width, display_height)  # Logical points
)
label.configure(image=self.display_image)
```

**How CTkImage Works:**
1. Detects system DPI scaling factor (e.g., 2x on Retina)
2. Interprets `size` as **logical points**, not physical pixels
3. Generates @2x texture internally (1000px for 500pt)
4. Maintains full resolution on high-density screens

**Result:** Sharp, crisp images on all displays (Retina, 4K, standard)

---

# SLIDE 8: Real-Time Preview Optimization

## Challenge

Processing large images (e.g., 4000×3000px) on every slider movement is slow.

## Solution

**Efficient Pipeline:**
```python
def _on_slider_change(self, param_key, value, ...):
    # 1. Update single parameter
    self.params[param_key] = int(value)

    # 2. Early return if no image loaded
    if self.original_array is None:
        return

    # 3. Process in-memory array (not re-read from disk)
    self._process_and_display()
```

**Optimizations:**
- Numpy vectorized operations (no Python loops)
- Process on original array (already in memory)
- CTkImage caching reduces redraw overhead
- Single reprocess per slider change (not full UI rebuild)

**Performance:** ~50-100ms per update on M1 Mac (imperceptible lag)

---

# SLIDE 9: Code Quality & Architecture

## Separation of Concerns

**Pure Processing Logic:**
```python
class GlitchProcessor:
    @staticmethod
    def bit_shift_glitch(image_array, shift) -> np.ndarray:
        # Pure function: array in, array out
        # No UI dependencies, fully testable
        ...
```

**UI Logic:**
```python
class NeuroCorruptApp(ctk.CTk):
    def _process_and_display(self):
        # Delegates processing to GlitchProcessor
        result = GlitchProcessor.bit_shift_glitch(...)
        # Handles display only
        self._update_canvas(result)
```

**Benefits:**
- ✅ Unit testable (can test algorithms independently)
- ✅ CLI version possible (import processor, skip UI)
- ✅ Batch processing extension (loop over images)
- ✅ Cleaner profiling (separate UI vs. algorithm performance)

---

## Design Patterns Used

1. **Factory Pattern** – `_create_glass_button()`, `_create_modern_slider()`
2. **Template Method** – Base glitch pipeline, specific algorithms override
3. **Separation of Concerns** – Processing vs. UI vs. Theme
4. **Singleton Config** – `AppTheme` class (centralized constants)

---

# SLIDE 10: Workflow Demo

## User Journey

1. **Launch Application**
   - Window opens with glassmorphism UI
   - Sidebar shows file operations
   - Canvas displays "Load an image to begin"

2. **Load Image**
   - Click "📁 Load Image"
   - Select PNG/JPG from file dialog
   - Image appears in central canvas (sharp, Retina-optimized)

3. **Apply Glitch Effects**
   - Move "Bit Shift" slider → see horizontal tearing in real-time
   - Adjust RGB offsets → chromatic aberration appears
   - Change "Sort Threshold" → pixel sorting intensity varies
   - Toggle Horizontal/Vertical → sorting direction changes

4. **Export Result**
   - Click "💾 Export PNG"
   - Choose save location
   - Full-resolution PNG is exported (not scaled-down preview)

5. **Reset or Iterate**
   - Click "🔄 Reset All Parameters" → return to original
   - Adjust sliders again for new variations

---

# SLIDE 11: Use Cases

## Target Audience: Creative Professionals

**1. Motion Designers**
- Create glitch textures for title sequences
- Export frames for After Effects compositions
- Iterate quickly with real-time preview

**2. Graphic Designers**
- Generate poster backgrounds with unique artifacts
- Album art for electronic music / vaporwave aesthetics
- Social media visuals (Instagram, album covers)

**3. VJs & Live Visual Artists**
- Prepare glitch assets for live performances
- Real-time parameter tweaking during sets (future webcam input mode)

**4. Digital Artists**
- Explore post-digital aesthetics
- Databending as artistic practice
- Remix culture / collage work

---

# SLIDE 12: Artistic/Theoretical Context

## Post-Digital Glitch Art

**Key Theorists:**
- **Rosa Menkman** – "The Glitch Moment(um)" (2011)
  - Glitch as aesthetic intervention, not error
  - Compression artifacts as new visual language

- **Iman Moradi** – "Glitch Aesthetics" (2004)
  - Pure glitch vs. glitch-alike (designed corruption)

- **Nick Briz** – Databending tutorials
  - Treating files as raw data, not images

**My Contribution:**
- Makes databending accessible via GUI
- Combines multiple glitch techniques in one tool
- Bridges "glitch art theory" and "creative software design"

---

## Why Glitch Art Matters in MMI

**Interdisciplinary Skills:**
- **Computer Science:** Binary operations, array manipulation
- **Visual Arts:** Aesthetic theory, post-digital discourse
- **UX Design:** Interface metaphors, user workflows
- **Motion Design:** Texture generation for video production

**Portfolio Value:**
- Demonstrates technical depth (algorithms, architecture)
- Shows artistic awareness (glitch theory, design trends)
- Production-ready tool (not just a class exercise)

---

# SLIDE 13: Technical Challenges & Solutions

| Challenge | Solution | Learning Outcome |
|-----------|----------|------------------|
| **Blurry images on Retina** | CTkImage with explicit logical sizing | Understanding HiDPI scaling, platform integration |
| **Slow real-time preview** | Numpy vectorization, in-memory processing | Performance optimization, algorithm efficiency |
| **Complex UI state management** | Centralized `self.params` dict | State management patterns |
| **Mixing UI and processing logic** | Separated `GlitchProcessor` class | Software architecture, separation of concerns |
| **Inconsistent styling** | `AppTheme` class with constants | Design systems, maintainable code |
| **macOS theme mismatch** | `SystemThemeDetector` using subprocess | Platform APIs, system integration |

---

# SLIDE 14: Future Enhancements

## Planned Features

**Short-Term (Next Iteration):**
- [ ] **Preset System** – Save/load glitch "signatures" as .json files
- [ ] **Batch Processing** – Apply settings to entire folder of images
- [ ] **Undo/Redo Stack** – Navigate through parameter history

**Medium-Term:**
- [ ] **Video Databending** – Process .mp4 files frame-by-frame
- [ ] **Webcam Input** – Live glitch effects for performances
- [ ] **Audio-Reactive Mode** – Map sound frequencies to glitch parameters

**Long-Term:**
- [ ] **Plugin System** – User-created glitch algorithms
- [ ] **Machine Learning** – GAN-generated glitch presets
- [ ] **Cloud Export** – Direct upload to Figma, Adobe Cloud

---

## Extensibility

**Because of the separated architecture, adding new glitch effects is easy:**

1. Add algorithm to `GlitchProcessor`:
```python
@staticmethod
def new_effect(image_array, param):
    # Your logic here
    return modified_array
```

2. Add UI slider in `_build_controls_area()`:
```python
self._create_modern_slider(card, "Effect Name", 'param_key', 0, 100)
```

3. Add to pipeline in `_process_and_display()`:
```python
result = GlitchProcessor.new_effect(result, self.params['param_key'])
```

**No need to touch core architecture!**

---

# SLIDE 15: Lessons Learned

## Technical Insights

**1. HiDPI is Non-Negotiable**
- Modern creative tools MUST support Retina displays
- Users notice blurry interfaces immediately
- Platform-specific optimizations matter (CTkImage vs. ImageTk)

**2. Separation of Concerns is Worth It**
- Early temptation: mix UI and logic for "speed"
- Reality: Separated code is faster to debug and extend
- Testability requires discipline upfront

**3. Design Systems Scale**
- Centralizing colors/fonts in `AppTheme` made UI iteration painless
- Changing one HEX code updates entire interface
- Professional apps (Figma, Adobe) use same approach

---

## Creative/Artistic Insights

**1. Aesthetics Affect Perceived Complexity**
- Same tool, different UI → brutalism felt "harder" to use
- Glassmorphism made users more willing to experiment
- UI is part of the creative output, not just a wrapper

**2. Real-Time Feedback Enables Exploration**
- Instant preview → users discover combinations they wouldn't plan
- Glitch art is about controlled chaos → UI must allow play

**3. Theory Informs Practice**
- Reading Rosa Menkman shaped my algorithm design
- Understanding "why glitch art matters" made the tool more intentional

---

# SLIDE 16: Demonstration

## Live Demo

**[Run the application during presentation]**

1. **Load sample image** (prepared high-res photo)
2. **Bit-shift slider** → show horizontal tearing
3. **RGB offsets** → demonstrate chromatic aberration
4. **Pixel sorting** → adjust threshold, toggle direction
5. **Export** → show saved PNG at full resolution
6. **Compare** → v1.0 (blurry on Retina) vs. v2.0 (sharp)

**Talking Points:**
- "Notice the real-time preview as I move the slider"
- "On my Retina display, the image remains sharp thanks to CTkImage"
- "The exported file is full resolution, not the scaled-down preview"

---

# SLIDE 17: Code Walkthrough (if requested)

## Key Sections to Highlight

**1. Pixel Sorting Algorithm** (`main_v2.py:87-130`)
```python
# Show luminance calculation
luminance = 0.299*R + 0.587*G + 0.114*B

# Explain bright pixel masking
bright_mask = lum_row > threshold

# Demonstrate sorting logic
sort_order = np.argsort(sorted_lum)
```

**2. CTkImage Usage** (`main_v2.py:519-528`)
```python
self.display_image = ctk.CTkImage(
    light_image=pil_image,
    dark_image=pil_image,
    size=(display_width, display_height)  # Explain this!
)
```

**3. Glassmorphism Button Factory** (`main_v2.py:367-381`)
```python
# Show reusable component pattern
return ctk.CTkButton(
    fg_color="transparent",  # Glass effect
    border_color=accent_color,  # Dynamic color
    corner_radius=15  # Modern styling
)
```

---

# SLIDE 18: MMI Competencies

## Skills Demonstrated

### Technical (Informatique)
- ✅ Object-Oriented Programming (classes, inheritance)
- ✅ Algorithm Design (bit manipulation, sorting)
- ✅ GUI Development (CustomTkinter, event handling)
- ✅ Performance Optimization (Numpy vectorization)
- ✅ Platform Integration (macOS APIs, HiDPI)

### Creative (Création)
- ✅ Glitch Art Theory (post-digital aesthetics)
- ✅ UI/UX Design (glassmorphism, design systems)
- ✅ Visual Communication (color theory, typography)
- ✅ Generative Art (algorithmic texture creation)

### Professional (Communication)
- ✅ Technical Documentation (README, guides)
- ✅ Code Quality (comments, structure, naming)
- ✅ Portfolio Presentation (this deck!)
- ✅ User-Centered Design (real user workflow)

---

# SLIDE 19: Conclusion

## What I Built

**NEURO-CORRUPT v2.0** is a production-ready desktop application that:
- Generates unique glitch art textures
- Provides real-time visual feedback
- Exports high-resolution assets for creative work
- Demonstrates both technical and artistic mastery

---

## What I Learned

**Technical:**
- HiDPI display optimization is critical for modern apps
- Separation of concerns improves code quality dramatically
- Design systems make UIs maintainable and consistent

**Artistic:**
- Glitch art bridges computer science and visual culture
- UI aesthetics affect user behavior and perception
- Theory (Menkman, Briz) informs better tool design

**Professional:**
- Portfolio projects need both depth (code) and breadth (docs)
- Iterative refinement (v1 → v2) shows growth
- Explaining technical choices is as important as making them

---

## Impact

**This tool is:**
- Portfolio-ready for internship/job applications
- Usable by real designers (tested with motion design students)
- Extensible for future course projects (video processing, ML)
- A bridge between "student project" and "professional software"

---

# SLIDE 20: Q&A

```
╔════════════════════════════════════════════════════╗
║                                                    ║
║              Questions?                            ║
║                                                    ║
║   [Contact Information]                           ║
║   GitHub: github.com/[username]/neuro-corrupt     ║
║   Email: [your-email]@example.com                 ║
║                                                    ║
║   Documentation: See V2_TECHNICAL_GUIDE.md        ║
║   Code: main_v2.py (680 lines, fully commented)   ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

---

## Anticipated Questions & Answers

**Q: Why Python instead of JavaScript/web-based?**
**A:** Desktop apps offer better performance for large images, no upload privacy concerns, and access to native OS features (fonts, dialogs, theme detection). Python with Numpy is also faster for array operations than JavaScript.

---

**Q: How would you scale this to a commercial product?**
**A:**
1. Add user analytics (which effects are most popular)
2. Subscription model for cloud storage/batch processing
3. Plugin marketplace for custom glitch algorithms
4. Integration with Adobe, Figma (export directly to projects)

---

**Q: What's the biggest technical challenge you faced?**
**A:** Retina display support. The blurry image issue wasn't immediately obvious—only visible on high-DPI screens. Debugging required understanding tkinter's image handling limitations and researching CustomTkinter's internals to find CTkImage as the solution.

---

**Q: How does this relate to your career goals?**
**A:** I'm interested in creative technology—building tools that empower artists. This project combines my technical skills (algorithms, architecture) with artistic awareness (glitch theory, design trends). I'd love to work at companies like Adobe, Figma, or The Boundary (making creative software).

---

## Thank You!

**Project Repository:** [Include GitHub link if applicable]
**Documentation:** All files in project folder
**Demo Video:** [Optional—screen recording of workflow]

---

**[END OF PRESENTATION]**
