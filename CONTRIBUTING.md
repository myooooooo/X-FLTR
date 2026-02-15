# Contributing to X-FLTR / THE VOID ENGINE

Thank you for your interest in contributing to X-FLTR! This document provides guidelines for contributing to the project.

---

## 🎯 Project Philosophy

X-FLTR is a **creative coding tool** focused on:
- **Real-time performance** — All filters must execute in <500ms on 1200×800 images
- **Artistic quality** — Filters should produce visually interesting results
- **Zero disk I/O** — All processing in RAM (no temporary files)
- **Numpy vectorization** — No Python loops on pixels

---

## 🚀 How to Contribute

### 1. Add a New Filter

The easiest way to contribute! See **[HOW_TO_ADD_FILTER.md](HOW_TO_ADD_FILTER.md)** for detailed guide.

**Quick steps:**

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-awesome-filter`)
3. Add your filter to `filters_engine.py`:

```python
@staticmethod
def my_awesome_filter(arr: np.ndarray, param: int = 10) -> np.ndarray:
    """
    Brief description of what this filter does.

    Args:
        arr: Input image array (H, W, 3) dtype uint8
        param: Description of parameter

    Returns:
        Processed image array (H, W, 3) dtype uint8
    """
    result = arr.copy().astype(np.float32)

    # Your Numpy operations here (vectorized, no loops!)
    # Example: Invert colors
    result = 255 - result

    return np.clip(result, 0, 255).astype(np.uint8)
```

4. Register your filter in `FILTER_REGISTRY`:

```python
FILTER_REGISTRY = {
    'EXPERIMENTAL': [
        # ... existing filters ...
        ('My Awesome Filter', FilterEngine.my_awesome_filter, {'param': 10}),
    ]
}
```

5. Test your filter:

```bash
python main.py
# Load an image, apply your filter, verify performance
```

6. Commit and push:

```bash
git add filters_engine.py
git commit -m "Add: My Awesome Filter (vectorized)"
git push origin feature/my-awesome-filter
```

7. Open a Pull Request

---

### 2. Optimize Existing Filters

If you find a filter that's slow, optimize it!

**Optimization guidelines:**
- **Use Numpy vectorization** — Replace Python loops with Numpy operations
- **Use broadcasting** — Leverage Numpy's automatic broadcasting
- **Profile your changes** — Use `time.time()` to measure speedup
- **Maintain visual quality** — Output must be identical or better

**Example optimization:**

```python
# ❌ SLOW: Python loops
for y in range(height):
    for x in range(width):
        result[y, x] = process(arr[y, x])

# ✅ FAST: Numpy vectorization
result = np.vectorize_process(arr)  # Or use broadcasting
```

---

### 3. Fix Bugs

Found a bug? Great! Please:

1. **Check existing issues** — Make sure it's not already reported
2. **Create an issue** — Describe the bug, steps to reproduce, expected behavior
3. **Submit a fix** — Fork, fix, test, pull request

---

### 4. Improve Documentation

Documentation is crucial! Contributions welcome for:

- **Tutorials** — How-to guides, examples
- **Code comments** — Explain complex algorithms
- **README updates** — Improve clarity, add screenshots
- **Translation** — Translate docs to other languages

---

## 📝 Code Style Guidelines

### Python Code

- **Follow PEP 8** — Use consistent formatting
- **Type hints** — Use `np.ndarray`, `int`, `float`, etc.
- **Docstrings** — Document all functions
- **Comments** — Explain *why*, not *what*

```python
# Good
def invert_colors(arr: np.ndarray) -> np.ndarray:
    """Invert RGB colors (negative effect)."""
    return 255 - arr

# Bad (no docstring, no type hints)
def invert(a):
    return 255 - a
```

### Filter Naming

- **Use descriptive names** — `voronoi_cells`, not `filter42`
- **Snake case** — `pixel_sort_horizontal`, not `PixelSortHorizontal`
- **Be specific** — `sobel_neon_edges`, not `edges`

### Performance Requirements

- **Target:** <500ms on 1200×800 images
- **Test:** Use `time.time()` to measure
- **Profile:** Identify bottlenecks with profiling tools

```python
import time
start = time.time()
result = my_filter(arr)
print(f"Execution time: {time.time() - start:.3f}s")
```

---

## 🧪 Testing

Before submitting a pull request:

1. **Run the application** — `python main.py`
2. **Load a test image** — 1200×800 or larger
3. **Apply your filter** — Verify visual output
4. **Check performance** — Should execute in <500ms
5. **Test edge cases:**
   - Very small images (100×100)
   - Very large images (4000×3000)
   - Grayscale images
   - Images with transparency

---

## 🎨 Filter Categories

Add your filter to the most appropriate category:

- **GLITCH** — Pixel sorting, RGB splits, datamosh, artifacts
- **GENERATIVE** — Procedural patterns, noise, fractals
- **RETRO_TECH** — Dithering, retro palettes, CRT effects
- **GEOMETRIC** — Shapes, tessellation, symmetry
- **EXPERIMENTAL** — Everything else, creative effects

Not sure? Use **EXPERIMENTAL**.

---

## 🚫 What NOT to Do

- ❌ **No Python loops on pixels** — Use Numpy vectorization
- ❌ **No disk I/O during processing** — Keep everything in RAM
- ❌ **No external dependencies** — Stick to numpy, scipy, PIL
- ❌ **No slow filters** — Must execute in <500ms on proxy images
- ❌ **No destructive operations** — Always copy input array first

---

## 📬 Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch** — `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages** — `git commit -m "Add: Feature X"`
6. **Push to your fork** — `git push origin feature/my-feature`
7. **Open a Pull Request** — Describe your changes, attach screenshots if visual

### PR Checklist

- [ ] Filter executes in <500ms on 1200×800 images
- [ ] No Python loops on pixels (fully vectorized)
- [ ] Includes docstring with parameter descriptions
- [ ] Registered in `FILTER_REGISTRY`
- [ ] Tested on multiple images
- [ ] No external dependencies added
- [ ] Code follows PEP 8 style

---

## 🎓 Learning Resources

### Numpy Vectorization
- [Numpy Documentation](https://numpy.org/doc/)
- [Broadcasting Tutorial](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [Vectorization Guide](https://numpy.org/doc/stable/user/quickstart.html)

### Image Processing
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [SciPy Image Processing](https://docs.scipy.org/doc/scipy/reference/ndimage.html)

### Glitch Art
- Rosa Menkman — Glitch Studies Manifesto
- [Databending Techniques](https://github.com/topics/databending)

---

## 💬 Communication

- **Issues** — Bug reports, feature requests
- **Pull Requests** — Code contributions
- **Discussions** — General questions, ideas

---

## 🏆 Recognition

All contributors will be acknowledged in:
- README.md "Contributors" section
- Code comments (for significant contributions)
- Release notes (for major features)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to X-FLTR! 🎨⚡**

**Author:** ANSSAFOU ZINEB
**Lab:** DIGITAL CREATION LAB
**Project:** MMI Portfolio — Creative Coding Tool
