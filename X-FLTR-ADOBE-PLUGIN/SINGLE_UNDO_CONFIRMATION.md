# ✅ SINGLE UNDO CONFIRMATION

## Structure actuelle vérifiée

Tous les filtres utilisent la structure correcte pour un **SINGLE UNDO** :

```javascript
await executeAsModal(async () => {
    // Toutes les opérations du filtre
}, { commandName: 'Filter Name' });
```

## Filtres vérifiés (27 total)

1. RGB Split Linear - ✅ commandName présent
2. RGB Split Wave - ✅ commandName présent  
3. Scanline Corrupt - ✅ commandName présent
4. Bit Crush - ✅ commandName présent
5. Pixelate - ✅ commandName présent
6. GameBoy Palette - ✅ commandName présent
7. Commodore 64 - ✅ commandName présent
8. CGA Palette - ✅ commandName présent
9. Duotone - ✅ commandName présent
10. Y2K Halftone Crush - ✅ commandName présent
11. Dot Matrix Live Preview - ✅ commandName présent
12. Bake Dot Matrix - ✅ commandName présent
13. Cancel Preview - ✅ commandName présent
14. Chroma Bleed - ✅ commandName présent
15. Pixel Sort - ✅ commandName présent
16. VCR Tracking - ✅ commandName présent
17. FLIR Thermal - ✅ commandName présent
18. Sonar Radar - ✅ commandName présent
19. Ferrofluid - ✅ commandName présent
20. Anamorphic Flare - ✅ commandName présent
21. Prism Shift - ✅ commandName présent
22. Retinal Burn - ✅ commandName présent
23. Xerox Gen 10 - ✅ commandName présent
24. Microfiche - ✅ commandName présent
25. GameBoy Dither - ✅ commandName présent
26. CCTV Night - ✅ commandName présent
27. Ghost Noise - ✅ commandName présent
28. Typographic - ✅ commandName présent

## Comportement attendu

**Un seul Ctrl+Z** annule :
- Toutes les duplications de calques
- Tous les batchPlay
- Tous les groupings
- Tous les renommages
- Toutes les modifications de blend modes

→ Retour exact à l'état initial avant le clic

## Import vérifié

```javascript
const { executeAsModal } = require('photoshop').core;
```

✅ Import correct depuis photoshop.core
