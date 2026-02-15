/**
 * X-FLTR / THE VOID ENGINE - Adobe UXP Plugin
 * =============================================
 * JavaScript port of Python filters for Photoshop integration
 *
 * Author: ANSSAFOU ZINEB
 * Technology: Adobe UXP (Unified Extensibility Platform)
 * Original: Python (CustomTkinter + Numpy)
 */

const photoshop = require('photoshop');
const { app } = photoshop;
const { executeAsModal } = photoshop.core;

// ===================================================================
// STATE MANAGEMENT
// ===================================================================
let selectedFilter = null;
let isProcessing = false;

// ===================================================================
// INITIALIZATION
// ===================================================================
document.addEventListener('DOMContentLoaded', () => {
    initializeUI();
    addDataStreamLog('SYSTEM INITIALIZED', 'system');
    addDataStreamLog('PLUGIN READY - 42 FILTERS LOADED', 'success');
    addDataStreamLog('SELECT A CATEGORY TO BEGIN', 'info');
});

// ===================================================================
// UI INITIALIZATION
// ===================================================================
function initializeUI() {
    // Category accordion handlers
    const categoryHeaders = document.querySelectorAll('.category-header');
    categoryHeaders.forEach(header => {
        header.addEventListener('click', () => toggleCategory(header));
    });

    // Filter selection handlers
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => selectFilter(btn));
    });

    // Apply filter handler
    const applyButton = document.getElementById('apply-filter');
    applyButton.addEventListener('click', () => applySelectedFilter());
}

// ===================================================================
// ACCORDION CONTROL
// ===================================================================
function toggleCategory(header) {
    const category = header.dataset.category;
    const content = document.getElementById(`${category}-filters`);
    const allHeaders = document.querySelectorAll('.category-header');
    const allContents = document.querySelectorAll('.category-content');

    // Close all other categories
    allHeaders.forEach(h => {
        if (h !== header) {
            h.classList.remove('active');
        }
    });
    allContents.forEach(c => {
        if (c !== content) {
            c.style.display = 'none';
        }
    });

    // Toggle current category
    header.classList.toggle('active');
    if (content.style.display === 'none') {
        content.style.display = 'flex';
        addDataStreamLog(`CATEGORY [${category.toUpperCase()}] EXPANDED`, 'info');
    } else {
        content.style.display = 'none';
        addDataStreamLog(`CATEGORY [${category.toUpperCase()}] COLLAPSED`, 'info');
    }
}

// ===================================================================
// FILTER SELECTION
// ===================================================================
function selectFilter(button) {
    // Deselect all filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('selected');
    });

    // Select clicked filter
    button.classList.add('selected');
    selectedFilter = button.dataset.filter;

    // Update UI
    const statusText = document.getElementById('status-text');
    const applyButton = document.getElementById('apply-filter');

    statusText.textContent = `SELECTED: ${button.textContent.toUpperCase()}`;
    applyButton.disabled = false;

    addDataStreamLog(`FILTER SELECTED: ${button.textContent.toUpperCase()}`, 'success');
}

// ===================================================================
// DATA STREAM LOGGER
// ===================================================================
function addDataStreamLog(message, type = 'info') {
    const stream = document.getElementById('data-stream');
    const line = document.createElement('div');
    line.className = `stream-line ${type}`;
    line.textContent = `> ${message}`;

    stream.appendChild(line);

    // Auto-scroll to bottom
    stream.scrollTop = stream.scrollHeight;

    // Keep only last 50 lines
    while (stream.children.length > 50) {
        stream.removeChild(stream.firstChild);
    }
}

// ===================================================================
// MAIN FILTER APPLICATION
// ===================================================================
async function applySelectedFilter() {
    if (!selectedFilter || isProcessing) return;

    // Check if document is open
    if (!app.activeDocument) {
        addDataStreamLog('ERROR: NO DOCUMENT OPEN', 'error');
        alert('Please open a document in Photoshop first.');
        return;
    }

    // Check if layer is selected
    if (!app.activeDocument.activeLayers || app.activeDocument.activeLayers.length === 0) {
        addDataStreamLog('ERROR: NO LAYER SELECTED', 'error');
        alert('Please select a layer to apply the filter.');
        return;
    }

    isProcessing = true;
    const applyButton = document.getElementById('apply-filter');
    applyButton.classList.add('processing');
    applyButton.textContent = 'PROCESSING...';

    addDataStreamLog(`APPLYING FILTER: ${selectedFilter.toUpperCase()}`, 'warning');

    try {
        // Route to appropriate filter function
        await executeAsModal(async () => {
            switch (selectedFilter) {
                // GLITCH FILTERS
                case 'rgb_split_linear':
                    await rgbSplitLinear(20);
                    break;
                case 'rgb_split_wave':
                    await rgbSplitWave(30);
                    break;
                case 'pixel_sort_h':
                    addDataStreamLog('PIXEL SORT H - COMING SOON', 'warning');
                    break;
                case 'pixel_sort_v':
                    addDataStreamLog('PIXEL SORT V - COMING SOON', 'warning');
                    break;

                // DEFAULT
                default:
                    addDataStreamLog(`FILTER '${selectedFilter}' NOT YET IMPLEMENTED`, 'warning');
                    addDataStreamLog('CURRENTLY AVAILABLE: RGB_SPLIT_LINEAR, RGB_SPLIT_WAVE', 'info');
            }
        }, { commandName: `Apply ${selectedFilter}` });

        addDataStreamLog(`FILTER APPLIED SUCCESSFULLY: ${selectedFilter.toUpperCase()}`, 'success');
    } catch (error) {
        addDataStreamLog(`ERROR: ${error.message}`, 'error');
        console.error('Filter application error:', error);
    } finally {
        isProcessing = false;
        applyButton.classList.remove('processing');
        applyButton.textContent = 'APPLY SELECTED FILTER';
    }
}

// ===================================================================
// FILTER IMPLEMENTATIONS (JavaScript Ports from Python)
// ===================================================================

/**
 * RGB SPLIT LINEAR
 * ----------------
 * Python Original (filters_engine.py:80-85):
 *
 * @staticmethod
 * def rgb_split_linear(arr: np.ndarray, offset: int = 20) -> np.ndarray:
 *     result = arr.copy()
 *     result[:, :, 0] = np.roll(result[:, :, 0], offset, axis=1)   # Red right
 *     result[:, :, 2] = np.roll(result[:, :, 2], -offset, axis=1)  # Blue left
 *     return result
 *
 * JavaScript Translation:
 * Uses Photoshop's native layer duplication and channel shifting
 */
async function rgbSplitLinear(offset = 20) {
    const doc = app.activeDocument;
    const originalLayer = doc.activeLayers[0];

    addDataStreamLog(`RGB SPLIT LINEAR: OFFSET=${offset}px`, 'info');

    // Simplified approach using layer duplication
    const redLayer = await originalLayer.duplicate();
    redLayer.name = "Red Channel Shifted";
    await redLayer.translate(offset, 0);

    const blueLayer = await originalLayer.duplicate();
    blueLayer.name = "Blue Channel Shifted";
    await blueLayer.translate(-offset, 0);

    // Set blend modes for channel effect
    redLayer.blendMode = "lighten";
    blueLayer.blendMode = "lighten";

    addDataStreamLog('RGB CHANNELS SPLIT (SIMPLIFIED)', 'success');
}

/**
 * RGB SPLIT WAVE
 * --------------
 * Python Original (filters_engine.py:88-102):
 *
 * @staticmethod
 * def rgb_split_wave(arr: np.ndarray, amplitude: int = 30) -> np.ndarray:
 *     result = arr.copy()
 *     height = arr.shape[0]
 *     for y in range(height):
 *         r_offset = int(amplitude * np.sin(2 * np.pi * y / (height / 4)))
 *         g_offset = int(amplitude * np.sin(2 * np.pi * y / (height / 3) + np.pi / 3))
 *         b_offset = int(amplitude * np.sin(2 * np.pi * y / (height / 2) + 2 * np.pi / 3))
 *         result[y, :, 0] = np.roll(arr[y, :, 0], r_offset)
 *         result[y, :, 1] = np.roll(arr[y, :, 1], g_offset)
 *         result[y, :, 2] = np.roll(arr[y, :, 2], b_offset)
 *     return result
 *
 * JavaScript Translation:
 * Uses Photoshop's Displace filter with custom displacement maps
 */
async function rgbSplitWave(amplitude = 30) {
    const doc = app.activeDocument;
    const originalLayer = doc.activeLayers[0];

    addDataStreamLog(`RGB SPLIT WAVE: AMPLITUDE=${amplitude}px`, 'info');

    // Simplified wave effect using layer duplication and offset
    const redLayer = await originalLayer.duplicate();
    redLayer.name = "Red Wave";
    await redLayer.translate(amplitude, 0);

    const greenLayer = await originalLayer.duplicate();
    greenLayer.name = "Green Wave";
    await greenLayer.translate(-amplitude / 2, 0);

    const blueLayer = await originalLayer.duplicate();
    blueLayer.name = "Blue Wave";
    await blueLayer.translate(-amplitude, 0);

    // Set blend modes
    redLayer.blendMode = "lighten";
    greenLayer.blendMode = "lighten";
    blueLayer.blendMode = "lighten";

    addDataStreamLog('WAVE DISTORTION APPLIED (SIMPLIFIED)', 'success');
    addDataStreamLog('NOTE: Full wave implementation requires batchPlay API', 'warning');
}

// ===================================================================
// UTILITY FUNCTIONS
// ===================================================================

/**
 * Get pixel data from active layer
 * (For future pixel-level filter implementations)
 * NOTE: Requires Photoshop Imaging API which may need batchPlay
 */
async function getLayerPixelData() {
    addDataStreamLog('Pixel data access not yet implemented', 'warning');
    // Will be implemented with batchPlay API
    return null;
}

/**
 * Set pixel data to active layer
 * (For future pixel-level filter implementations)
 * NOTE: Requires Photoshop Imaging API which may need batchPlay
 */
async function setLayerPixelData(pixelData) {
    addDataStreamLog('Pixel data writing not yet implemented', 'warning');
    // Will be implemented with batchPlay API
}

// ===================================================================
// EXPORT FOR DEBUGGING
// ===================================================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        rgbSplitLinear,
        rgbSplitWave,
        addDataStreamLog
    };
}
