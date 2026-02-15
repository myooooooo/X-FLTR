# X-FLTR v1.1 — Quick Start Guide

**Author:** ANSSAFOU ZINEB | **Version:** 1.1 (Complete Overhaul)

---

## 🚀 What's New in v1.1

### **1. Collapsible Filter Categories**
- Click category headers to expand/collapse
- Only one category open at a time (cleaner interface)
- Visual indicators: ▶ (collapsed) / ▼ (expanded)
- 5 categories: GLITCH, GENERATIVE, RETRO_TECH, GEOMETRIC, EXPERIMENTAL

### **2. Color-Coded Data Stream**
- **🟢 Green:** Success messages (LOADED, PROCESSING COMPLETE)
- **🔴 Red:** Error messages (ERROR: NO IMAGE)
- **🟠 Orange:** Warning messages (BUSY: PROCESSING)
- **🔵 Cyan:** Info messages (APPLYING: FILTER)
- **⚪ White:** System messages (SYSTEM INITIALIZED)

### **3. Advanced Settings HUD**
- **Brightness Slider:** 0.5× (dark) to 1.5× (bright)
- **Contrast Slider:** 0.5× (flat) to 1.5× (high contrast)
- **Saturation Slider:** 0.0× (grayscale) to 2.0× (hypersaturated)
- **Reset Button (⟲):** Restore all sliders to 1.0
- **Real-time Preview:** Changes apply instantly as you drag

### **4. LRU Filter Caching**
- Applying the same filter twice loads from cache (instant)
- Cache stores last 10 filter results
- Automatic cache eviction when full
- Cache cleared when new image is loaded
- Log message: "LOADED FROM CACHE (INSTANT)" when hit

### **5. Animated Splash Screen**
- Progressive boot sequence with diagnostics
- 7-step loading animation
- Real-time progress bar
- Terminal-style messages
- Total duration: ~2.5 seconds

---

## 🎮 Basic Workflow (Updated)

### Step 1: Launch
```bash
cd "/Users/zineb/Documents/Code/dossier sans titre"
source .venv/bin/activate
python main.py
```

**What you'll see:**
- Animated splash screen with diagnostics
- Progress bar animating from 0% → 100%
- Terminal-style boot messages
- Main window opens automatically

### Step 2: Load Image
1. Click `LOAD IMAGE` (bottom left)
2. Select PNG/JPG/BMP/TIFF
3. Image appears in center canvas
4. Data stream logs: 🟢 `LOADED: filename.jpg` (green)
5. Data stream logs: 🔵 `SIZE: 3000×2000` (cyan)

### Step 3: Navigate Filters
1. Click category header to expand (e.g., `▶ [GLITCH] (8 filters)`)
2. Category expands to show filters
3. Other categories automatically collapse
4. Header changes to `▼ [GLITCH] (8 filters)`

### Step 4: Apply Filter
1. Click any filter button
2. Data stream logs: 🔵 `APPLYING: PIXEL_SORT_H` (cyan)
3. Processing happens in background (UI stays responsive)
4. Data stream logs: 🟢 `PROCESSING COMPLETE` (green)
5. Canvas updates with filtered result

### Step 5: Adjust Image (NEW!)
1. Locate `[ ADVANCED SETTINGS ]` panel (above action bar)
2. Drag **BRIGHTNESS** slider to adjust brightness
3. Drag **CONTRAST** slider to adjust contrast
4. Drag **SATURATION** slider to adjust saturation
5. Changes apply in real-time (instant preview)
6. Click ⟲ button to reset all sliders to 1.0

### Step 6: Cache Performance (NEW!)
1. Apply any filter (e.g., Reaction-Diffusion)
2. Wait for processing (~3 seconds)
3. Apply the same filter again
4. Data stream logs: 🟢 `LOADED FROM CACHE (INSTANT)` (green)
5. Result appears instantly (<50ms)

### Step 7: Export
1. Click `EXPORT 4K` (bottom)
2. Choose format: PNG (lossless), JPEG (compressed), TIFF (archive)
3. Save location
4. Data stream logs: 🟢 `EXPORTED: filename.png` (green)
5. Data stream logs: 🔵 `RESOLUTION: 3000×2000` (cyan)

---

## 🎨 Advanced Settings Usage

### Brightness Adjustment
**Use case:** Image too dark or too bright
- **0.5×** = Very dark
- **1.0×** = Original brightness (default)
- **1.5×** = Very bright

**Example:** Portrait photo taken in low light
1. Load image
2. Drag Brightness slider to 1.3
3. Image brightens in real-time

### Contrast Adjustment
**Use case:** Flat, dull images need more "pop"
- **0.5×** = Flat, low contrast
- **1.0×** = Original contrast (default)
- **1.5×** = High contrast, dramatic

**Example:** Landscape photo needs more depth
1. Load image
2. Drag Contrast slider to 1.4
3. Shadows deepen, highlights brighten

### Saturation Adjustment
**Use case:** Make colors more or less vibrant
- **0.0×** = Full grayscale (black & white)
- **1.0×** = Original saturation (default)
- **2.0×** = Hypersaturated, intense colors

**Example:** Create black & white version
1. Load color photo
2. Drag Saturation slider to 0.0
3. Image becomes grayscale

### Reset Adjustments
**Use case:** Start fresh with default settings
1. Click ⟲ button (right side of Advanced Settings)
2. All sliders return to 1.0
3. Data stream logs: 🔵 `ADJUSTMENTS RESET` (cyan)

---

## 📊 Performance Tips

### Fast Operations (<200ms)
- RGB Split Linear
- Bit Crush
- Posterize
- Channel Mixer
- **All slider adjustments** (instant)

### Medium Operations (200ms-1s)
- Pixel Sort
- Bayer Dithering
- CRT Curvature
- Sobel Neon

### Slow Operations (1s-5s)
- Reaction-Diffusion
- Voronoi Cells
- Delaunay Triangulation
- ASCII Render

**Pro Tip:** Apply slow filters once, then use cache on repeat applications (instant)!

---

## 🎯 Color-Coded Log Guide

### What Each Color Means

**🟢 Green (Success):**
- `LOADED: image.jpg`
- `PROCESSING COMPLETE`
- `EXPORTED: output.png`
- `RANDOMIZE COMPLETE`
- `RESET: IMAGE RESTORED`
- `LOADED FROM CACHE (INSTANT)`

**🔴 Red (Error):**
- `ERROR: NO IMAGE LOADED`
- `ERROR: {exception message}`
- `EXPORT ERROR: {reason}`

**🟠 Orange (Warning):**
- `BUSY: PROCESSING IN PROGRESS`

**🔵 Cyan (Info):**
- `42 FILTER MODULES LOADED`
- `AWAITING IMAGE INPUT...`
- `SIZE: 3000×2000`
- `APPLYING: FILTER_NAME`
- `RESOLUTION: 3000×2000`
- `RANDOMIZE: APPLYING 3 RANDOM FILTERS`
- `RANDOM: FILTER_NAME`
- `ADJUSTMENTS RESET`
- `CACHE EVICTION (LRU)`
- `CACHE CLEARED`

**⚪ White (System):**
- `SYSTEM INITIALIZED`

---

## 🐛 Troubleshooting

### Problem: Filter categories not expanding
**Solution:** Ensure you're clicking the header button (not the filter buttons)

### Problem: Sliders not responding
**Solution:** Ensure an image is loaded first (sliders adjust working image)

### Problem: Cache not working
**Symptoms:** Same filter takes full time on second application
**Solution:** Verify exact same filter+parameters are used (different params = different cache key)

### Problem: Colors in data stream not showing
**Solution:** Already fixed in v1.1 (color tags implemented)

### Problem: Splash screen not animating
**Solution:** Check terminal for errors; animation requires 7 steps × 300ms each

---

## 🎓 For Demo/Presentation (Updated)

### Recommended Workflow (5 minutes)

1. **Launch** → Show animated splash screen with diagnostics
2. **Load** → Select landscape photo
3. **Navigate** → Expand [GLITCH] category (show accordion)
4. **Apply Filters:**
   - **Pixel Sort H** → Glitch effect
   - **Sobel Neon** → Neon edges
5. **Adjust Settings:**
   - Brightness → 1.2 (show real-time adjustment)
   - Saturation → 1.5 (show color boost)
6. **Cache Demo:**
   - Apply **Reaction-Diffusion** (wait ~3s)
   - Apply **Reaction-Diffusion** again (instant cache hit)
7. **Export** → Save as PNG
8. **Data Stream** → Highlight color-coded messages

**Talking Points:**
- "42 filters, organized into collapsible categories"
- "Color-coded logs for instant visual feedback"
- "Real-time brightness/contrast/saturation adjustments"
- "Intelligent caching makes repeated filters instant"
- "Animated splash screen with diagnostic boot sequence"
- "All processing in RAM, zero disk I/O"
- "Threaded processing, UI never freezes"

---

## 💡 Tips & Tricks (Updated)

### Get Best Results
- Start with high-resolution images (2000×1500+)
- Use Advanced Settings sliders for global adjustments
- Apply filters sequentially (not randomize unless experimenting)
- Use cache to your advantage (repeated filters are instant)
- Export in PNG for maximum quality

### Creative Combos
- **Retro Gaming:** GameBoy 4-bit → Saturation 0.5 → Pixelate
- **Glitch Art:** RGB Split Wave → Scanline Corrupt → Brightness 1.3
- **Abstract:** Reaction-Diffusion → Kaleidoscope → Contrast 1.5
- **Neon Cyberpunk:** Sobel Neon → Bloom Glow → Saturation 1.8

### Performance Tricks
- Apply slow filters once, then adjust with sliders
- Use cache for experimentation (try filter, adjust sliders, reapply if needed)
- Monitor data stream for cache hits (green "LOADED FROM CACHE")
- Close other apps during heavy filter processing

---

## ⚙️ Keyboard Shortcuts

**Currently:** None (mouse/trackpad only)

**Future v1.2:**
- `Ctrl+Z` → Undo
- `Ctrl+R` → Randomize
- `Ctrl+E` → Export
- `Ctrl+L` → Load Image
- `Space` → Reset Adjustments

---

## ✅ Quick Checklist (Before Presenting)

- [ ] Application launches with animated splash
- [ ] All 5 filter categories expand/collapse correctly
- [ ] Only one category open at a time
- [ ] Data stream shows 5 different colors
- [ ] Advanced Settings sliders adjust image in real-time
- [ ] ⟲ button resets all sliders to 1.0
- [ ] Applying same filter twice shows cache hit message
- [ ] Images remain sharp on Retina display
- [ ] Window resize updates canvas smoothly
- [ ] Export saves high-resolution PNG/JPEG/TIFF

---

## 🎯 Success Metrics (v1.1)

**Your application is working correctly if:**

1. ✅ Animated splash screen shows 7-step boot sequence
2. ✅ Header shows: "ANSSAFOU ZINEB // DIGITAL CREATION LAB // VOID_ENGINE_V1.0"
3. ✅ Data stream logs in 5 colors (green, red, orange, cyan, white)
4. ✅ Filter categories collapse/expand with ▶/▼ indicators
5. ✅ Advanced Settings panel shows 3 sliders + reset button
6. ✅ Sliders adjust image in real-time (instant preview)
7. ✅ Cache hit message appears when re-applying same filter
8. ✅ Filters apply without freezing UI
9. ✅ Export creates valid PNG/JPG/TIFF

---

**All systems upgraded! Ready for v1.1 presentation! 🎓**

---

## 📞 Support

### If Something Goes Wrong

1. **Check Data Stream** (left panel) for color-coded error messages
2. **Restart Application** (close and relaunch)
3. **Check Dependencies:**
   ```bash
   pip list | grep -E "customtkinter|Pillow|numpy|scipy"
   ```
4. **Verify Python Version:**
   ```bash
   python3 --version  # Should be 3.8+
   ```

### Common Issues

**"Advanced Settings sliders not working"**
→ Load an image first (sliders require working array)

**"Cache not triggering"**
→ Must apply exact same filter with same parameters twice

**"Data stream colors all green"**
→ Already fixed in v1.1; ensure you're running latest version

---

**Version:** X-FLTR / THE VOID ENGINE v1.1
**Author:** ANSSAFOU ZINEB
**Lab:** DIGITAL CREATION LAB
**Date:** 2025-02-15

**🚀 Launch and create with professional-grade tools!**
