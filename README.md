# Bidi Stream 🔄

A lightweight Python library and custom algorithm for transforming logical bidirectional (bidi) text into visual rendering order. Designed specifically to handle mixed-script layouts (such as Arabic, Persian, or Hebrew combined with English, numbers, and punctuation) without relying on massive external bidi engines.

---

## ✨ Features

* **Bidirectional Support:** Seamlessly handles both `ltr` (Left-to-Right) and `rtl` (Right-to-Left) base directions.
* **Mixed Script Handling:** Manages inline script switches (e.g., English words embedded inside Arabic sentences or vice versa).
* **Smart Neutral & Punctuation Tracking:** Correctly positions whitespace (`WS`), separators (`S`), and other neutral characters (`ON`) using dynamic boundary indexing.
* **Automatic Character Mirroring:** Automatically flips directional symbols (like parentheses, brackets, etc.) based on Unicode metadata and custom mappings.
* **Optimized Performance:** Caches local functions for high-speed execution in tight loops.

---

## 📦 Requirements

* Python 3.x
* Built-in `unicodedata` module
* A local `mirror` module containing your `MIRRORED` dictionary mapping. (comes with it)

---

## 🚀 Usage

Here is a quick example of how to use `reshape_bidi_visual` in your project:

```python
from bidi_stream import reshape_bidi_visual

# Example 1: Right-to-Left base text with English and numbers
text_rtl = "السعر 50$ لـ Python"
visual_rtl = reshape_bidi_visual(text_rtl, base_direction='rtl')
print(visual_rtl)

# Example 2: Left-to-Right base text with Arabic elements
text_ltr = "The project starts on 15 يناير"
visual_ltr = reshape_bidi_visual(text_ltr, base_direction='ltr')
print(visual_ltr)

```
## ⚙️ Function Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| text | str | *Required* | The logical text string to be reordered. |
| base_direction | str | 'ltr' | The base layout direction ('ltr' or 'rtl'). |
| prefix | str | '' | Optional prefix string to prepend before processing. |
| strong_run_end | int | 0 | Internal boundary tracker for strong directional runs. |
| neutral_start | int | None | Internal tracking index for neutral/whitespace blocks. |
| num_run_start | int | 0 | Internal tracking index for number runs (EN, AN, etc.). |
| line_start | int | 0 | Anchor index for paragraph/line breaks (B). |
## 🤝 Contributing
Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.
## 📄 License
Distributed under the MIT License. See LICENSE for more information.
```
