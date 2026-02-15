# NEURO-CORRUPT v2.0: Technical Documentation
## Master-Level Refactor with Glassmorphism UI

---

## 🎯 What Changed from v1.0

### Critical Bug Fixes

#### **1. Retina/HiDPI Display Issue (FIXED)**

**The Problem:**
```python
# v1.0 - WRONG approach
photo = ImageTk.PhotoImage(display_img)
self.canvas.configure(image=photo)
# Results in:
# - Blurry images on Retina displays
# - tkinter warnings about image scaling
# - Poor quality on high-DPI screens
```

**The Solution:**
```python
# v2.0 - CORRECT approach
self.display_image = ctk.CTkImage(
    light_image=pil_image,
    dark_image=pil_image,
    size=(display_width, display_height)  # Explicit scaling
)
self.canvas_label.configure(image=self.display_image)
```

**Why This Works:**
- `CTkImage` is CustomTkinter's HiDPI-aware image class
- Automatically generates @2x assets for Retina displays
- Handles scaling based on system DPI settings
- No tkinter warnings or quality degradation

**For Your Oral Presentation:**
> "The original version used PIL's ImageTk, which doesn't support modern high-DPI displays. On Retina screens, images appeared blurry because tkinter doesn't handle @2x scaling. I refactored the image rendering pipeline to use CustomTkinter's CTkImage class, which automatically generates appropriately scaled assets for high-density displays. This is critical for professional applications on modern hardware."

---

#### **2. Code Architecture (Separated Concerns)**

**v1.0 Structure:**
```
├── GlitchEngine (algorithms)
└── NeuroCorruptUI (UI + processing mixed)
```

**v2.0 Structure:**
```
├── GlitchProcessor (pure processing logic)
├── AppTheme (centralized styling)
├── SystemThemeDetector (macOS integration)
└── NeuroCorruptApp (UI only, delegates processing)
```

**Benefits:**
- **Testability**: Can unit test algorithms independently
- **Maintainability**: Changes to UI don't affect processing
- **Scalability**: Easy to add CLI version or batch processing
- **Performance**: Clearer separation improves profiling

---

### UI/UX Improvements

#### **Glassmorphism Aesthetic**

**Before (Cyber-Brutalist):**
- Sharp corners (radius=0)
- High-contrast borders (#00FF41 neon green)
- Terminal-inspired (monospace fonts)
- "Hacker tool" aesthetic

**After (Glassmorphism):**
- Rounded corners (radius=15px)
- Subtle borders with transparency
- Modern sans-serif (SF Pro on Mac)
- Professional creative tool aesthetic

**Why Glassmorphism?**
- More approachable for creative professionals
- Aligns with modern design trends (iOS, macOS Big Sur+)
- Better visual hierarchy with layered glass cards
- Softer, less aggressive than brutalism

---

## 📊 Complete Color Palette

### Glassmorphism Palette (Copy these HEX codes for your portfolio)

| Color Name | HEX Code | RGB | Usage |
|------------|----------|-----|-------|
| **Backgrounds** |
| BG_DARK | `#1A1B1E` | rgb(26, 27, 30) | Main window background |
| BG_GLASS | `#252730` | rgb(37, 39, 48) | Glass panels/cards |
| BG_GLASS_HOVER | `#2D2E38` | rgb(45, 46, 56) | Hover state for interactive elements |
| **Accents** |
| ACCENT_PRIMARY | `#6C63FF` | rgb(108, 99, 255) | Electric Purple - Primary actions |
| ACCENT_SECONDARY | `#00D9FF` | rgb(0, 217, 255) | Cyan - Secondary highlights |
| ACCENT_SUCCESS | `#00FF88` | rgb(0, 255, 136) | Neon Green - Success states |
| ACCENT_WARNING | `#FF6B6B` | rgb(255, 107, 107) | Coral Red - Warnings/destructive |
| **Text** |
| TEXT_PRIMARY | `#FFFFFF` | rgb(255, 255, 255) | Headers, active text |
| TEXT_SECONDARY | `#B8B9BE` | rgb(184, 185, 190) | Body text, labels |
| TEXT_MUTED | `#6B6C70` | rgb(107, 108, 112) | Hints, disabled state |
| **UI Elements** |
| BORDER_SUBTLE | `#3A3B45` | rgb(58, 59, 69) | Card borders, separators |
| BORDER_ACTIVE | `#6C63FF` | rgb(108, 99, 255) | Active element borders |

---

### Color Usage Matrix

| Component | Background | Border | Text | Accent |
|-----------|-----------|--------|------|--------|
| Sidebar | BG_GLASS | BORDER_SUBTLE | TEXT_PRIMARY | - |
| Glass Card | BG_GLASS | BORDER_SUBTLE | TEXT_PRIMARY | - |
| Primary Button | transparent | ACCENT_PRIMARY | ACCENT_PRIMARY | ACCENT_PRIMARY |
| Secondary Button | transparent | ACCENT_SECONDARY | ACCENT_SECONDARY | ACCENT_SECONDARY |
| Warning Button | transparent | ACCENT_WARNING | ACCENT_WARNING | ACCENT_WARNING |
| Slider Track | BG_DARK | - | - | - |
| Slider Progress | - | - | - | ACCENT_PRIMARY |
| Slider Handle | - | - | - | ACCENT_PRIMARY |
| Status Success | - | - | ACCENT_SUCCESS | - |
| Status Error | - | - | ACCENT_WARNING | - |

---

## 🎨 Design System Breakdown

### Typography Hierarchy

```python
# Mac Native Font Stack (SF Pro)
FONT_HEADING = ("SF Pro Display", 18, "bold")    # Card titles
FONT_BUTTON = ("SF Pro Text", 13, "bold")        # Button labels
FONT_BODY = ("SF Pro Text", 12)                  # Body text
FONT_MONO = ("SF Mono", 11)                      # Technical values
```

**Fallbacks for Non-Mac Systems:**
If SF Pro isn't available, CustomTkinter falls back to:
- Windows: Segoe UI
- Linux: Ubuntu / DejaVu Sans

### Component Dimensions

| Element | Height | Corner Radius | Border Width |
|---------|--------|---------------|--------------|
| Button | 44px | 15px | 2px |
| Slider | 24px | 15px | - |
| Card | auto | 15px | 1px |
| Sidebar | 100% | 0px | 1px |

**Why 44px buttons?**
- iOS Human Interface Guidelines recommend 44pt minimum touch target
- Even for desktop, larger buttons improve usability
- Professional apps (Adobe, Figma) use similar sizing

---

## 🔧 How CTkImage Solves Retina Issues

### The Technical Deep-Dive

#### Step 1: Understanding the Problem

**Retina Display Characteristics:**
- 2x pixel density (or higher)
- Physical pixel ≠ logical pixel
- 1 "point" = 2x2 physical pixels on Retina

**What tkinter/ImageTk Does Wrong:**
```python
# Old approach (v1.0)
img = Image.open("photo.jpg")          # 1000x1000 pixels
img_resized = img.resize((500, 500))   # Resize to fit canvas
photo = ImageTk.PhotoImage(img_resized)
label.configure(image=photo)

# On Retina display:
# - tkinter displays 500 logical points
# - Should use 1000 physical pixels
# - But only has 500 pixels of data
# - Result: Blurry, upscaled image
```

#### Step 2: CTkImage's Solution

```python
# New approach (v2.0)
img = Image.open("photo.jpg")          # 1000x1000 pixels

ctk_img = ctk.CTkImage(
    light_image=img,
    dark_image=img,
    size=(500, 500)  # Logical size (points)
)
label.configure(image=ctk_img)

# What CTkImage does internally:
# 1. Detects system DPI scaling factor (e.g., 2x on Retina)
# 2. Creates 1000x1000 internal texture for 500pt logical size
# 3. Maintains full resolution for 2x displays
# 4. Automatically downsamples for 1x displays
# 5. Result: Sharp, crisp image on all displays
```

#### Step 3: Implementation in Our Code

```python
def _process_and_display(self):
    # Process at full resolution
    result = self.original_array.copy()
    # ... apply glitch effects ...

    pil_image = Image.fromarray(result)  # Full resolution

    # Calculate LOGICAL display size
    display_width = 1000   # Logical points
    display_height = 600   # Logical points

    # CRITICAL: CTkImage handles physical pixels internally
    self.display_image = ctk.CTkImage(
        light_image=pil_image,      # Full-res source
        dark_image=pil_image,        # Same for dark mode
        size=(display_width, display_height)  # Logical size
    )
    # CTkImage automatically:
    # - Uses full resolution on Retina (2000x1200 physical pixels)
    # - Uses logical resolution on standard (1000x600 physical pixels)
```

### For Your Oral Presentation

**Q: Why did you switch from ImageTk to CTkImage?**

**A:** "Modern displays like Apple's Retina screens use pixel density scaling, where one 'logical pixel' corresponds to 2x2 or 3x3 physical pixels. The standard tkinter ImageTk.PhotoImage doesn't account for this, resulting in blurry images because it's displaying low-resolution data on high-density screens.

CustomTkinter's CTkImage class automatically detects the system's DPI scaling factor and maintains the appropriate physical resolution. When I specify `size=(500, 500)`, CTkImage interprets this as 500 *logical points* and automatically generates a 1000x1000 pixel texture for 2x Retina displays, ensuring the image remains sharp.

This is essential for professional creative tools, where image quality directly impacts the user's ability to evaluate their work."

---

## 🏗️ Architecture: Separation of Concerns

### Why Separate Processing from UI?

#### Old Approach (Monolithic)
```python
class NeuroCorruptUI(ctk.CTk):
    def _process_glitch(self):
        # UI code mixed with processing
        result = self.working_image.copy()
        result = np.bitwise_xor(result, shift)  # Processing logic
        self.canvas.configure(...)              # UI logic
```

**Problems:**
- Can't test algorithms without launching UI
- Hard to add CLI version
- Performance profiling includes UI overhead
- Violates Single Responsibility Principle

#### New Approach (Separated)
```python
# Pure processing (no UI dependencies)
class GlitchProcessor:
    @staticmethod
    def bit_shift_glitch(image_array, shift):
        result = image_array.copy()
        return np.bitwise_xor(result, shift)

# Pure UI (delegates processing)
class NeuroCorruptApp(ctk.CTk):
    def _process_and_display(self):
        result = GlitchProcessor.bit_shift_glitch(
            self.original_array,
            self.params['bit_shift']
        )
        self._display(result)  # UI only
```

**Benefits:**
- ✅ Unit testable: `assert GlitchProcessor.bit_shift_glitch(...) == expected`
- ✅ CLI version: Import `GlitchProcessor`, skip UI
- ✅ Batch processing: Loop over images without UI overhead
- ✅ Clear contracts: Processor takes arrays, returns arrays

---

### Class Responsibilities

| Class | Responsibility | Dependencies |
|-------|---------------|--------------|
| `GlitchProcessor` | Image manipulation algorithms | Numpy only |
| `AppTheme` | Design system constants | None |
| `SystemThemeDetector` | macOS theme detection | subprocess (macOS) |
| `NeuroCorruptApp` | UI rendering, event handling | CustomTkinter, GlitchProcessor |

**Dependency Flow:**
```
NeuroCorruptApp
    ↓ uses
GlitchProcessor (pure logic)
    ↓ uses
Numpy (computation)
```

No circular dependencies = clean architecture.

---

## 🔍 Code Walkthrough for Oral Defense

### Key Sections to Explain

#### 1. Glitch Algorithm Example

**Pixel Sorting Logic:**
```python
# Calculate luminance (brightness) using ITU-R BT.601 standard
luminance = 0.299*R + 0.587*G + 0.114*B

# For each row in the image:
for row_idx in range(image.shape[0]):
    # Find pixels brighter than threshold
    bright_mask = luminance[row_idx] > threshold

    # Sort only the bright pixels by luminance
    bright_pixels = row[bright_mask]
    sorted_pixels = bright_pixels[np.argsort(luminance[row_idx][bright_mask])]

    # Replace bright region with sorted version
    row[bright_mask] = sorted_pixels
```

**Why This Creates Glitch Aesthetic:**
- Preserves dark regions (no sorting) → maintains structure
- Sorts bright regions → creates "data-mosh" streaks
- Threshold control → user decides what counts as "bright"
- Result: Partially corrupted image, not pure noise

---

#### 2. Real-Time Preview Optimization

**Challenge:** Processing large images on every slider move is slow.

**Solution:**
```python
def _on_slider_change(self, param_key, value, label, text):
    # Update parameter
    self.params[param_key] = int(value)

    # Only process if image exists (early return pattern)
    if self.original_array is None:
        return

    # Trigger single reprocess (not rebuild entire UI)
    self._process_and_display()
```

**Performance Tips:**
- Process on original array (not re-read from disk)
- Use numpy vectorized operations (not Python loops)
- CTkImage caching reduces redraw overhead

---

#### 3. Glassmorphism Button Factory

```python
def _create_glass_button(self, parent, text, command, accent_color):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color="transparent",          # No fill = glass effect
        hover_color=AppTheme.BG_GLASS_HOVER,  # Subtle hover
        border_width=2,
        border_color=accent_color,       # Colored border
        text_color=accent_color,         # Match text to border
        corner_radius=15,                # Rounded = modern
        height=44                        # iOS touch target size
    )
```

**Design Rationale:**
- `fg_color="transparent"` → see-through button (glassmorphism)
- Border provides visual boundary without solid background
- Hover state gives tactile feedback
- Accent color parameter → reusable for different button types

---

## 🎓 MMI Jury Talking Points

### Technical Competencies Demonstrated

1. **Advanced Python**
   - Object-oriented design (classes, static methods)
   - Type hints for clarity (`image_array: np.ndarray`)
   - List comprehensions, generators (efficient)

2. **Image Processing**
   - Numpy array manipulation (vectorized operations)
   - Color space transformations (RGB to luminance)
   - Bit-level operations (XOR for corruption)

3. **UI/UX Engineering**
   - Responsive grid layout (expands with window)
   - Design system (centralized theme)
   - Accessibility (high contrast, large touch targets)

4. **Platform Integration**
   - macOS theme detection (subprocess)
   - HiDPI/Retina support (CTkImage)
   - Native fonts (SF Pro on Mac)

5. **Software Architecture**
   - Separation of concerns (processing vs. UI)
   - Factory pattern (button/slider creation)
   - Single Responsibility Principle

---

### Creative/Artistic Competencies

1. **Post-Digital Theory**
   - Glitch as aesthetic intervention, not error
   - References: Rosa Menkman, databending culture

2. **Design Trends**
   - Glassmorphism (iOS 14+, Windows 11 Acrylic)
   - Color theory (complementary neon accents)

3. **UX Psychology**
   - Real-time feedback reduces cognitive load
   - Grouped controls (cards) improve discoverability
   - Visual hierarchy guides user attention

---

## 📋 Comparison Chart (v1 vs v2)

| Feature | v1.0 (Cyber-Brutalist) | v2.0 (Glassmorphism) |
|---------|------------------------|----------------------|
| **Display Technology** | ImageTk (blurry on Retina) | CTkImage (HiDPI-aware) |
| **Architecture** | Monolithic (UI + processing mixed) | Separated concerns |
| **Corner Radius** | 0px (sharp) | 15px (rounded) |
| **Color Palette** | Neon green/pink on black | Purple/cyan on charcoal |
| **Typography** | Monospace only | SF Pro (modern sans-serif) |
| **Layout** | Fixed sidebar + canvas | Responsive grid with cards |
| **Theme Sync** | Manual dark mode | Detects macOS system theme |
| **Button Style** | Brutalist borders | Glassmorphism transparency |
| **Code Structure** | 2 classes | 4 classes (separated) |
| **Lines of Code** | 421 | 680 (more comments/docs) |
| **Target Aesthetic** | "Hacker tool" | "Creative professional tool" |

---

## 🚀 Running the Application

### Installation
```bash
pip install -r requirements.txt
python main_v2.py
```

### First Run Checklist
- [ ] Window opens at 1600x1000
- [ ] Glassmorphism cards visible (rounded corners)
- [ ] Purple accent color on "Load Image" button
- [ ] Click "Load Image" → select PNG/JPG
- [ ] Image appears sharp (not blurry) on Retina display
- [ ] Move sliders → image updates in real-time
- [ ] "Export PNG" saves full-resolution file

---

## 🎤 Sample Jury Q&A

**Q: Why did you choose glassmorphism over your original brutalist design?**

**A:** "While the brutalist aesthetic effectively communicated the 'data corruption' concept, glassmorphism better aligns with modern creative software standards. Tools like Figma, Adobe XD, and Final Cut Pro use softer, layered interfaces that feel more approachable to designers and motion artists—my target audience. Glassmorphism also provides better visual hierarchy through depth and transparency, making complex controls easier to parse at a glance."

---

**Q: How does your application handle different screen sizes and DPI settings?**

**A:** "The UI uses a responsive grid layout where the sidebar has a fixed 320px width, and the main canvas expands to fill available space. For high-DPI displays like Apple's Retina screens, I use CustomTkinter's CTkImage class, which automatically scales images based on the system's pixel density. This ensures images remain sharp on 2x or 3x density displays without manual DPI detection or multiple asset versions."

---

**Q: Could this tool be extended to video processing?**

**A:** "Absolutely. Since I separated the processing logic into the `GlitchProcessor` class, it's agnostic to whether the input is a single image or video frames. For video databending, I'd add an FFmpeg wrapper to extract frames as numpy arrays, apply the same glitch algorithms in a loop, and re-encode the sequence. The UI could add a progress bar and batch export controls, but the core algorithms wouldn't change."

---

## 📚 References for Deep Dive

**CustomTkinter Documentation:**
- [CTkImage Class](https://customtkinter.tomschimansky.com/documentation/widgets/image)
- [HiDPI Scaling](https://customtkinter.tomschimansky.com/documentation/scaling)

**Design Inspiration:**
- Apple Human Interface Guidelines (Glassmorphism)
- Figma Plugin UI Patterns
- Adobe Spectrum Design System

**Glitch Art Theory:**
- Rosa Menkman – "The Glitch Moment(um)"
- Kim Asendorf – Pixel Sorting Experiments

---

**This documentation is designed to be printed/presented during your oral defense. Each section has talking points optimized for technical jury questions.**
