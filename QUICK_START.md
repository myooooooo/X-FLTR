# X-FLTR / VOID ENGINE — Quick Start Guide

**Author:** ANSSAFOU ZINEB | **Version:** 1.1

---

## ⚡ Launch Application (3 steps)

```bash
# 1. Navigate to project
cd "/Users/zineb/Documents/Code/dossier sans titre"

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Run application
python main.py
```

**Expected:** Splash screen appears for 2 seconds → Main window opens

---

## 🎮 Basic Operations

### Load Image
1. Click `LOAD IMAGE` (bottom left)
2. Select PNG/JPG/BMP/TIFF
3. Image appears in center canvas

### Apply Filter
1. Scroll through filter list (right panel)
2. Click any filter name
3. Processing happens in background
4. Canvas updates when complete

### Export Result
1. Click `EXPORT 4K` (bottom)
2. Choose format:
   - PNG → Lossless (best quality)
   - JPEG → Compressed (smaller file)
   - TIFF → Archive (professional)
3. Save location

### Randomize
1. Click `RANDOMIZE x3`
2. Applies 3 random filters
3. Uses stable default parameters

### Reset
1. Click `RESET`
2. Returns to original image

---

## 🎨 Filter Categories (42 Total)

**[GLITCH]** — 8 filters
- Pixel sorting, RGB splits, datamosh, scanlines

**[GENERATIVE]** — 8 filters
- Reaction-diffusion, Voronoi, fractals, cellular automata

**[RETRO_TECH]** — 8 filters
- Bayer dither, GameBoy palette, CRT, VHS, ASCII

**[GEOMETRIC]** — 8 filters
- Hexagons, stained glass, kaleidoscope, pixelation

**[EXPERIMENTAL]** — 10 filters
- Chromatic prism, infrared, neon edges, bloom, posterize

---

## 🔧 Keyboard Shortcuts (None Yet)

Currently: Mouse/trackpad only
Future: Add hotkeys for common operations

---

## 📊 Performance Tips

### Fast Filters (<200ms)
- RGB Split Linear
- Bit Crush
- Posterize
- Channel Mixer

### Medium Filters (200ms-1s)
- Pixel Sort
- Bayer Dithering
- CRT Curvature
- Sobel Neon

### Slow Filters (1s-5s)
- Reaction-Diffusion
- Voronoi Cells
- Delaunay Triangulation
- ASCII Render

**Note:** All filters run in background thread (UI never freezes)

---

## 🐛 Troubleshooting

### Problem: Blurry Images on Mac
**Cause:** Not using CTkImage
**Solution:** Already fixed in v1.1 (all images use CTkImage)

### Problem: Can't See All Filters
**Cause:** Window too small or scroll not working
**Solution:** Use trackpad/mouse to scroll filter list (right panel)

### Problem: Window Resize Doesn't Update Canvas
**Cause:** Old version
**Solution:** Already fixed in v1.1 (adaptive resize implemented)

### Problem: Processing Seems Stuck
**Check:** Data stream (left panel) shows current status
**Reality:** Heavy filters (reaction-diffusion) can take 3-5 seconds

### Problem: Export Fails
**Cause:** No image loaded or no write permissions
**Solution:** Load image first, ensure destination folder is writable

---

## 📁 Project Structure

```
x-fltr-void-engine/
├── main.py              # UI + Application (launch this)
├── filters_engine.py    # 42 Filter Functions
├── branding.py          # Logo + Identity
├── requirements.txt     # Dependencies
├── README_XFLTR.md      # Full documentation
└── archive/             # Previous versions
```

---

## 🎓 For Demo/Presentation

### Recommended Workflow

1. **Launch** → Show splash screen (branding)
2. **Load** → Select landscape photo (shows variety)
3. **Apply Sequence:**
   - **GameBoy 4-bit** → Instant retro palette
   - **Pixel Sort H** → Glitch aesthetic
   - **Sobel Neon** → Neon edge overlay
4. **Randomize x3** → Show unpredictability
5. **Resize Window** → Demonstrate adaptive canvas
6. **Export 4K** → Show professional output
7. **Data Stream** → Highlight real-time logging

**Total Demo Time:** 3-4 minutes

---

## 💡 Tips & Tricks

### Get Best Results
- Start with high-resolution images (2000×1500+)
- Apply filters sequentially (not all at once)
- Use "Reset" between experiments
- Export in PNG for maximum quality

### Creative Combos
- **Retro Gaming:** GameBoy 4-bit → Pixelate
- **Glitch Art:** RGB Split Wave → Scanline Corrupt
- **Abstract:** Reaction-Diffusion → Kaleidoscope
- **Neon Cyberpunk:** Sobel Neon → Bloom Glow

### Performance
- Close other apps during heavy filter processing
- Smaller images process faster (but export at full res)
- Monitor Data Stream for progress updates

---

## ⚙️ System Requirements

**Minimum:**
- macOS 11+ (Big Sur or newer)
- Python 3.8+
- 4GB RAM
- 500MB disk space

**Recommended:**
- macOS 14+ (Sonoma)
- Python 3.14+
- 8GB+ RAM
- M1/M2/M3 chip (faster processing)
- Retina display (for optimal visual quality)

---

## 🚨 Known Limitations

1. **Video:** Cannot process video files (images only)
2. **Batch:** Cannot process multiple images at once
3. **Undo:** No multi-level undo (only reset to original)
4. **Parameters:** Filters use default parameters (no sliders yet)
5. **Presets:** Cannot save/load filter combinations

**Future Enhancements:** See README_XFLTR.md

---

## 📞 Support

### If Something Goes Wrong

1. **Check Data Stream** (left panel) for error messages
2. **Restart Application** (close and relaunch)
3. **Check Dependencies:**
   ```bash
   pip list | grep -E "customtkinter|Pillow|numpy|scipy"
   ```
4. **Verify Python Version:**
   ```bash
   python3 --version  # Should be 3.8+
   ```

### Error Messages

**"No module named 'scipy'"**
→ `pip install scipy`

**"LOAD FAILED"**
→ Image file corrupted or unsupported format

**"EXPORT ERROR"**
→ Destination folder not writable or disk full

---

## ✅ Quick Checklist

Before presenting to MMI jury:

- [ ] Application launches without errors
- [ ] Splash screen displays (2 seconds)
- [ ] All 42 filters visible via scroll
- [ ] Images display sharp (not blurry) on Retina
- [ ] Window resize updates canvas
- [ ] Data stream logs operations
- [ ] Export saves high-resolution PNG
- [ ] Your name appears in header

---

## 🎯 Success Metrics

**Your application is working correctly if:**

1. ✅ Splash screen shows branding
2. ✅ Header shows: "ANSSAFOU ZINEB // DIGITAL CREATION LAB // VOID_ENGINE_V1.0"
3. ✅ Data stream logs: `[HH:MM:SS] SYSTEM INITIALIZED`
4. ✅ Right panel shows all 42 filters (scrollable)
5. ✅ Images remain sharp on Retina display
6. ✅ Window resize adapts canvas smoothly
7. ✅ Filters apply without freezing UI
8. ✅ Export creates valid PNG/JPG/TIFF

---

**All systems ready! 🚀 Launch and create amazing glitch art!**
