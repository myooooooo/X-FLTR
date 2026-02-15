# Troubleshooting Guide — X-FLTR Adobe Plugin

**Common issues and solutions for the UXP plugin**

Author: ANSSAFOU ZINEB | MMI Portfolio 2025

---

## 🚨 Common Loading Errors

### Error: "Plugin Load Failed"

**Symptoms:**
- Plugin validates but fails to load in Photoshop
- Error message: "Load command failed in App with ID PS"

**Causes & Solutions:**

#### 1. Missing Icon Files
**Problem:** `manifest.json` references icon files that don't exist

**Solution:**
- Icons have been removed from manifest for minimal setup
- To add icons later, create `icons/` folder with:
  - `icon-dark.png` (23×23 and 48×48)
  - `icon-light.png` (23×23 and 48×48)

#### 2. API Compatibility Issues
**Problem:** Using deprecated or incorrect UXP APIs

**Solution:**
```javascript
// ❌ OLD (doesn't work in UXP 5+)
const { imaging } = require('photoshop');
await imaging.applyChannelMixer(...);

// ✅ NEW (works in PS 2024+)
const photoshop = require('photoshop');
const { app } = photoshop;
// Use batchPlay for advanced operations
```

#### 3. JavaScript Syntax Errors
**Problem:** ES6+ features not supported in older UXP versions

**Solution:**
- Check UXP Developer Tool console for errors
- Avoid optional chaining (`?.`) if not supported
- Use `function` instead of arrow functions for top-level

---

## 🔧 Fixed Issues (v2.0.1)

### v2.0.0 → v2.0.1 Changes

#### Issue #1: Missing Icons Blocking Load
**Fixed:** Removed icon references from `manifest.json`
- Removed `entrypoints[0].icons` array
- Removed root-level `icons` array
- Removed `requiredPermissions` (not needed for basic layer operations)

#### Issue #2: Obsolete API Calls
**Fixed:** Replaced `imaging` API with direct layer operations
```javascript
// Before (causing errors):
await imaging.applyChannelMixer(layer, {...});

// After (working):
await layer.translate(offset, 0);
layer.blendMode = "lighten";
```

#### Issue #3: Incorrect Module Import
**Fixed:** Updated require statement
```javascript
// Before:
const { app, core, imaging } = require('photoshop');

// After:
const photoshop = require('photoshop');
const { app } = photoshop;
const { executeAsModal } = photoshop.core;
```

---

## 📋 Loading Checklist

Before loading the plugin in Photoshop:

- [ ] `manifest.json` is valid JSON (no trailing commas)
- [ ] `index.html` exists and is well-formed
- [ ] `main.js` has no syntax errors
- [ ] No ES modules syntax (`import`/`export`) — use `require`
- [ ] All file paths in manifest are correct
- [ ] Photoshop version >= 27.3.1 (check `minVersion`)

---

## 🛠️ Debugging Steps

### Step 1: Check UXP Developer Tool Console
1. Open **UXP Developer Tool**
2. Click **"..."** next to your plugin
3. Select **"Open DevTools"**
4. Check **Console** tab for errors

### Step 2: Validate Manifest
```bash
# Check JSON syntax
cat X-FLTR-ADOBE-PLUGIN/manifest.json | python -m json.tool
```

### Step 3: Test JavaScript Syntax
```bash
# Check for syntax errors
node --check X-FLTR-ADOBE-PLUGIN/main.js
```

### Step 4: Reload Plugin
1. In **UXP Developer Tool**, click **"..."**
2. Select **"Unload"**
3. Click **"Load"** again
4. Check Photoshop **Plugins** menu

---

## ⚠️ Known Limitations

### Current Implementation (v2.0.1)

#### Limited Filter Functionality
- Only 2 filters implemented (RGB Split Linear/Wave)
- Filters use **simplified layer-based approach**
- Full pixel-level manipulation not yet implemented

#### No Advanced Effects
- Channel Mixer API not available → Using blend modes instead
- Wave distortion simplified → Full implementation needs batchPlay
- No Voronoi/complex algorithms → Requires external libraries

### Planned Improvements (v2.1+)
- [ ] Implement batchPlay for native Photoshop filters
- [ ] Add pixel-level manipulation via Actions API
- [ ] Integrate external libraries (d3-delaunay for Voronoi)
- [ ] Add proper error handling and user feedback

---

## 📚 API References

### Working APIs (Tested in PS 27.3.1)
- ✅ `app.activeDocument`
- ✅ `layer.duplicate()`
- ✅ `layer.translate(x, y)`
- ✅ `layer.blendMode = "lighten"|"screen"|"multiply"`
- ✅ `executeAsModal(async () => {...})`

### Not Yet Implemented
- ⏳ `imaging.getPixels()` / `putPixels()`
- ⏳ `imaging.applyChannelMixer()`
- ⏳ batchPlay for native filters

### Documentation Links
- [UXP for Photoshop](https://developer.adobe.com/photoshop/uxp/)
- [batchPlay Reference](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/batchplay/)
- [Layer API](https://developer.adobe.com/photoshop/uxp/2022/ps_reference/classes/layer/)

---

## 🎯 Quick Fixes

### "Cannot read property 'duplicate' of undefined"
**Cause:** No layer selected in Photoshop

**Fix:** Select a layer before applying filter

### "executeAsModal is not a function"
**Cause:** Incorrect import statement

**Fix:**
```javascript
const { executeAsModal } = require('photoshop').core;
```

### "Plugin not appearing in Plugins menu"
**Cause:** Plugin failed to load silently

**Fix:**
1. Check UXP Developer Tool for errors
2. Verify `manifest.json` entrypoints
3. Reload plugin completely

---

## 🐛 Reporting Issues

If you encounter new issues:

1. **Check UXP Developer Tool Console** for error messages
2. **Note your Photoshop version** (`Help → About Photoshop`)
3. **Document the steps** to reproduce
4. **Check this guide** for existing solutions

---

## ✅ Success Indicators

Plugin loaded successfully when:
- ✅ "Validate command successful" in UXP Developer Tool
- ✅ "Load command successful" (not just validate)
- ✅ "X-FLTR" appears in **Plugins → X-FLTR / THE VOID ENGINE**
- ✅ Panel opens with green neon UI
- ✅ Data stream shows "SYSTEM INITIALIZED"

---

**Status:** 🔧 Updated for v2.0.1

**Last Updated:** 2025-02-15

**⚡ Troubleshooting is debugging. Debugging is learning. ⚡**
