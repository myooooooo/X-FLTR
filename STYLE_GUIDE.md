# NEURO-CORRUPT: UI Style Guide
## Achieving the Cyber-Brutalist Aesthetic

---

## Color System

### Primary Palette
```python
BG_PRIMARY = "#0D0D0D"      # Deep Black (main background)
BG_SECONDARY = "#1A1A1A"    # Charcoal (sidebar, panels)
ACCENT_NEON = "#00FF41"     # Matrix Green (primary actions, borders)
ACCENT_CYBER = "#FF0055"    # Cyber Pink (secondary actions, warnings)
TEXT_PRIMARY = "#E0E0E0"    # Light Gray (main text)
TEXT_SECONDARY = "#808080"  # Medium Gray (labels, hints)
```

### Color Usage Rules

**Matrix Green (#00FF41)** – Use for:
- Success states
- Primary action buttons (LOAD, EXPORT)
- Active borders
- Confirmation messages
- Focused input elements

**Cyber Pink (#FF0055)** – Use for:
- Section headers
- Secondary actions (RESET)
- Warning states
- Destructive operations
- Hover states on critical buttons

---

## Typography

### Font Stack
```
Primary: "JetBrains Mono" (headers, buttons)
Secondary: "Courier" (body text, labels)
Fallback: monospace
```

### Size Hierarchy
- **Headers**: 16px bold (section titles)
- **Buttons**: 13px bold (call-to-action)
- **Body**: 11-12px regular (labels, values)
- **Status**: 14px regular (system messages)

### Styling Principles
1. **Always use monospaced fonts** – reinforces "code/terminal" aesthetic
2. **Uppercase for critical actions** – "LOAD IMAGE" not "Load Image"
3. **Technical language** – "RGB SEPARATION" not "Color Adjustments"
4. **Bracket notation** – `[ AWAITING INPUT ]` for system states

---

## Component Styling

### Buttons (Industrial Style)

```python
# Template for all action buttons
ctk.CTkButton(
    text="ACTION NAME",
    font=("JetBrains Mono", 13, "bold"),
    fg_color="transparent",           # No fill – ghost button
    hover_color="#0D0D0D",            # Subtle dark hover
    border_width=2,                   # Visible border
    border_color="#00FF41",           # Neon accent
    text_color="#00FF41",             # Match border
    corner_radius=0,                  # SHARP corners (brutalist)
    height=40
)
```

**Why this works:**
- Transparent background = minimal, industrial
- 2px border = technical, blueprint-like
- 0 corner radius = anti-Apple, anti-rounded, brutalist
- Monospace font = command-line interface

---

### Sliders (Technical Control)

```python
ctk.CTkSlider(
    button_color="#00FF41",           # Neon green handle
    button_hover_color="#FF0055",     # Pink on hover
    progress_color="#00FF41",         # Green progress bar
    fg_color="#0D0D0D",              # Black track
    height=20                         # Chunkier = more tactile
)
```

**Design rationale:**
- High contrast handle (green on black) = precision control
- Pink hover state = immediate visual feedback
- 20px height = professional tool (not mobile-friendly slider)

---

### Frames (Modular Panels)

```python
ctk.CTkFrame(
    corner_radius=0,                  # NO rounding
    fg_color="#1A1A1A",              # Charcoal background
    border_width=2,
    border_color="#00FF41"           # Neon border
)
```

**Brutalist principle:**
- Every panel has a visible border (no subtle shadows)
- Hard edges throughout (corner_radius=0)
- Visible structure = honest design (no hidden hierarchy)

---

## Layout Principles

### Grid Structure
```
┌─────────────────────────────────────────┐
│  [350px Sidebar]  │  [Flex Canvas]     │
│  ┌──────────┐     │  ┌──────────────┐  │
│  │ CONTROLS │     │  │   PREVIEW    │  │
│  │   GRID   │     │  │    CANVAS    │  │
│  └──────────┘     │  └──────────────┘  │
└─────────────────────────────────────────┘
```

**Fixed sidebar** (350px) vs. **fluid canvas**:
- Sidebar = control center (always visible)
- Canvas = expands to fill space (responsive to window size)

---

### Section Headers

```python
# Use for each control group
"// FILE SYSTEM"
"// BIT MANIPULATION"
"// RGB SEPARATION"
```

**Why the `//` prefix?**
- References C/C++ comment syntax
- Reinforces "code environment" metaphor
- Visual separator without horizontal rules

---

## Interaction States

### Status Messages

```python
# Default state
"[ AWAITING INPUT :: LOAD IMAGE TO BEGIN ]"

# Success state (green)
"[ LOADED :: image_name.png ]"

# Export confirmation (green)
"[ EXPORTED :: output_file.png ]"

# Error state (pink)
"[ ERROR :: NO IMAGE TO EXPORT ]"
```

**Format rules:**
1. Always use square brackets `[ ]`
2. Double colon `::` as separator
3. Uppercase for system states
4. Filename in lowercase (technical precision)

---

## Anti-Patterns (What NOT to Do)

❌ **Rounded corners** – breaks brutalist aesthetic
❌ **Soft shadows** – too "consumer app"
❌ **Gradients** – avoid unless for canvas preview
❌ **Sans-serif fonts** – use monospace only
❌ **Emoji or icons** – text-based interface only
❌ **Pastels or muted colors** – need high contrast
❌ **Friendly language** – "Oops!" → "[ ERROR ]"

---

## Professional Hacking Tool Look

To make this feel like **Wireshark, Burp Suite, or Metasploit** (not Photoshop):

1. **Terminal-inspired language**
   - "LOAD" not "Open"
   - "EXPORT PNG" not "Save As..."
   - "CORRUPTION PARAMETERS" not "Settings"

2. **Monospace everything**
   - Code editor fonts only
   - Fixed-width layouts
   - ASCII-style borders

3. **Visible structure**
   - Every panel has a border
   - No floating elements
   - Grid-based layout (not organic)

4. **Technical precision**
   - Show exact values (not "low/medium/high")
   - Use numeric readouts (`Bit Shift: 127`)
   - Hexadecimal color codes in UI

5. **Dark mode only**
   - No light theme option
   - Deep blacks (not gray)
   - Neon accents for visibility

---

## CustomTkinter Overrides

To achieve maximum brutalism, override these defaults:

```python
# Global theme settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Remove ALL corner radius
ctk.CTkButton(..., corner_radius=0)
ctk.CTkFrame(..., corner_radius=0)

# Force border visibility
border_width=2  # Minimum
border_color="#00FF41"  # Always neon

# No hover animations
# (keep instant color changes, not fade transitions)
```

---

## Example: Before & After

### ❌ Standard Desktop App
```
┌───────────────────────┐
│  Open File...         │  ← Rounded button
│  ┌─────────────────┐ │
│  │                 │ │  ← Soft shadow
│  │   Image Here    │ │
│  │                 │ │
│  └─────────────────┘ │
│  Brightness: ▓▓▓░░░ │  ← Generic slider
└───────────────────────┘
```

### ✅ NEURO-CORRUPT Aesthetic
```
┌───────────────────────────┐
│ [ CORRUPTION PARAMETERS ] │  ← Bracketed header
│ // FILE SYSTEM            │  ← Code comment style
│ ┌─────────────────┐       │
│ │  LOAD IMAGE     │       │  ← All caps, border
│ └─────────────────┘       │
│ // BIT MANIPULATION       │
│ Bit Shift:  127           │  ← Exact numeric value
│ ████████████░░░░░         │  ← Neon green bar
└───────────────────────────┘
```

---

## Final Checklist for "High-End" Aesthetic

- [ ] All corners are sharp (radius=0)
- [ ] All buttons have visible 2px borders
- [ ] Only monospace fonts used
- [ ] All text in UPPERCASE or technical_case
- [ ] Color palette limited to black/gray/neon green/cyber pink
- [ ] No icons – text-only interface
- [ ] Status messages use `[ BRACKET :: NOTATION ]`
- [ ] Section headers use `// COMMENT SYNTAX`
- [ ] No friendly language ("Oops!", "Please")
- [ ] Sidebar has fixed width (350px)
- [ ] Canvas has visible border frame

---

**Remember**: You're designing a **creative weapon**, not a consumer app. Every pixel should communicate **technical precision** and **post-digital defiance**.
