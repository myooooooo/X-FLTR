# Quick Start Guide — X-FLTR Adobe Plugin

**Get your plugin running in Photoshop in 5 minutes**

Author: ANSSAFOU ZINEB | MMI Portfolio 2025

---

## 📋 Prerequisites

Before you begin:
- ✅ **Adobe Photoshop 2024 v27.3.1** or later
- ✅ **Adobe UXP Developer Tool** ([Download here](https://developer.adobe.com/photoshop/uxp/guides/get-started/))
- ✅ **macOS** (tested on macOS)

---

## 🚀 Installation (5 Steps)

### Step 1: Download UXP Developer Tool

1. Go to [Adobe UXP Developer Tool](https://developer.adobe.com/photoshop/uxp/guides/get-started/)
2. Click **"Download UXP Developer Tool"**
3. Install the application (drag to Applications folder)
4. Launch **UXP Developer Tool**

### Step 2: Add Plugin to UXP Developer Tool

1. Open **UXP Developer Tool**
2. Click **"Add Plugin..."** button
3. Navigate to this folder: `X-FLTR-ADOBE-PLUGIN/`
4. Select **`manifest.json`**
5. Click **"Open"**

You should see:
```
X-FLTR / THE VOID ENGINE
Version: 2.0.0
Status: Not Loaded
```

### Step 3: Load Plugin in Photoshop

1. **Launch Adobe Photoshop** (if not already running)
2. In **UXP Developer Tool**, find your plugin
3. Click the **"..."** menu (3 dots)
4. Select **"Load"**

**Expected Output:**
```
✅ Validate command successful in App with ID PS v27.3.1
✅ Load command successful in App with ID PS v27.3.1
```

**If you see an error**, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Step 4: Open Plugin Panel in Photoshop

In Photoshop:
1. Go to **Plugins → X-FLTR / THE VOID ENGINE**
2. The plugin panel should appear

**You should see:**
- Black background (#000000)
- Neon green text (#00FF41)
- Header with "X-FLTR / THE VOID ENGINE"
- Data stream console showing:
  ```
  > SYSTEM INITIALIZED
  > PLUGIN READY - 42 FILTERS LOADED
  > SELECT A CATEGORY TO BEGIN
  ```

### Step 5: Test a Filter

1. **Open an image** in Photoshop (or create a new document)
2. **Select a layer** in the Layers panel
3. In X-FLTR panel:
   - Click **"[GLITCH]"** to expand the category
   - Click **"RGB Split Linear"**
   - Click **"APPLY SELECTED FILTER"**

**Expected Result:**
- Data stream shows "APPLYING FILTER: RGB_SPLIT_LINEAR"
- Layer duplicates created with chromatic aberration effect
- Success message in console

---

## 🎨 Available Filters (v2.0.1)

### ✅ Implemented (2/42)

| Filter | Category | How It Works |
|--------|----------|--------------|
| **RGB Split Linear** | GLITCH | Duplicates layer, shifts red/blue channels horizontally |
| **RGB Split Wave** | GLITCH | Similar to linear but with varying offset (simplified) |

### 🚧 Coming Soon (40/42)

All other filters show buttons but display:
```
> FILTER 'filter_name' NOT YET IMPLEMENTED
> CURRENTLY AVAILABLE: RGB_SPLIT_LINEAR, RGB_SPLIT_WAVE
```

See [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) for implementation roadmap.

---

## 🧪 Testing Workflow

### Basic Test (2 minutes)

1. **Create test document:**
   - Photoshop → File → New
   - 1000×1000 px, RGB Color
   - Add some colorful content (gradient, shapes, text)

2. **Apply filter:**
   - Select layer
   - X-FLTR panel → [GLITCH] → RGB Split Linear
   - Click "APPLY SELECTED FILTER"

3. **Observe result:**
   - Check Layers panel for duplicated layers
   - See red/blue channel shift effect
   - Verify data stream logs

### Advanced Test (5 minutes)

1. **Test multiple filters:**
   - Apply RGB Split Linear
   - Then apply RGB Split Wave on a different layer
   - Compare effects

2. **Test error handling:**
   - Close all documents → Try to apply filter
   - Should see: "ERROR: NO DOCUMENT OPEN"
   - Deselect layers → Try to apply filter
   - Should see: "ERROR: NO LAYER SELECTED"

3. **Test UI interactions:**
   - Expand/collapse categories (accordion)
   - Select different filters (highlight changes)
   - Watch data stream updates

---

## 🎯 UI Overview

### Header Section
```
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│ X-FLTR / THE VOID ENGINE       │
│ — DEVELOPED BY ANSSAFOU ZINEB —│
│ v2.0.0 | ADOBE UXP | MMI 2025  │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
```

### Data Stream Console
```
[DATA_STREAM]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> SYSTEM INITIALIZED          (white)
> PLUGIN READY - 42 FILTERS   (green)
> SELECT A CATEGORY TO BEGIN  (cyan)
```

**Color Codes:**
- 🟢 **Green** = Success
- 🔴 **Red** = Error
- 🟠 **Orange** = Warning
- 🔵 **Cyan** = Info
- ⚪ **White** = System

### Filter Categories (Accordion)
```
[▸] GLITCH        8 filters
[▸] GENERATIVE    8 filters
[▸] RETRO-TECH    8 filters
[▸] GEOMETRIC     8 filters
[▸] EXPERIMENTAL  10 filters
```

Click category header to expand/collapse.

### Control Panel
```
┌──────────────────────────────┐
│ APPLY SELECTED FILTER        │ ← Button
└──────────────────────────────┘
┌──────────────────────────────┐
│ NO FILTER SELECTED           │ ← Status
└──────────────────────────────┘
```

---

## 🐛 Common Issues

### Issue: Plugin doesn't appear in Plugins menu
**Solution:**
1. Check UXP Developer Tool → Plugin status should be "Loaded"
2. Restart Photoshop
3. Reload plugin in UXP Developer Tool

### Issue: "ERROR: NO LAYER SELECTED"
**Solution:**
- Select a layer in Photoshop Layers panel before applying filter

### Issue: Filter button does nothing
**Solution:**
- Check data stream console for error messages
- Most filters not yet implemented (only RGB Split Linear/Wave work)

### Issue: Panel UI looks broken
**Solution:**
- Check browser console in UXP DevTools
- Reload plugin (UXP Developer Tool → "..." → Reload)

**For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

---

## 🔧 Development Mode

### Enable DevTools Console

1. In **UXP Developer Tool**, click **"..."** next to plugin
2. Select **"Open DevTools"**
3. Console will open with JavaScript logs
4. Use for debugging custom filters

### Reload Plugin After Changes

After editing code:
1. **UXP Developer Tool → "..." → Reload**
2. Changes take effect immediately
3. No need to restart Photoshop

### Live Coding Workflow

```bash
# 1. Edit code
code X-FLTR-ADOBE-PLUGIN/main.js

# 2. Reload plugin (UXP Developer Tool)
# Click "..." → "Reload"

# 3. Test in Photoshop
# Apply filter to verify changes
```

---

## 📊 Expected Performance

| Action | Time |
|--------|------|
| Plugin load | < 1s |
| Panel open | < 0.5s |
| Filter apply (RGB Split) | 1-2s |
| UI interaction | Instant |

---

## 🎓 Next Steps

### For Users
- ✅ Test the 2 working filters
- 📚 Read [README.md](README.md) for full documentation
- 🐛 Report issues (see [TROUBLESHOOTING.md](TROUBLESHOOTING.md))

### For Developers
- 📝 Read [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)
- 🔧 Implement more filters (40 remaining)
- ⚡ Optimize performance with batchPlay API

---

## 📚 Documentation Links

- **[README.md](README.md)** — Plugin overview & architecture
- **[TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)** — Python → JS porting guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Error solutions
- **[Adobe UXP Docs](https://developer.adobe.com/photoshop/uxp/)** — Official API reference

---

## ✅ Success Checklist

You've successfully installed the plugin when:
- ✅ UXP Developer Tool shows "Loaded"
- ✅ Photoshop Plugins menu has "X-FLTR / THE VOID ENGINE"
- ✅ Panel opens with neon green UI
- ✅ Data stream shows "SYSTEM INITIALIZED"
- ✅ RGB Split Linear filter works on a layer

---

**Status:** 🚀 **v2.0.1 Ready for Testing**

**Last Updated:** 2025-02-15

**⚡ From installation to creation in 5 minutes. Let's glitch! ⚡**
