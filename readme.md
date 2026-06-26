# 🖼️ WebP Master v1.0.0

> **Advanced Batch Image Optimizer** — Convert JPG, PNG, BMP, TIFF and more to WebP with full control over quality, compression, and file naming.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)
![Pillow](https://img.shields.io/badge/Image-Pillow-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📸 Screenshot

> ![App Screenshot](/img-01.png)
> ![App Screenshot](/img-02.png)

---

## ✨ Features

- **Batch Conversion** — Select and convert multiple images at once
- **Compression Control** — Adjustable quality (1–100%) and engine effort (0–6)
- **Lossless Mode** — Pixel-perfect WebP output with no quality loss
- **EXIF / Metadata Preservation** — Optionally keep original image metadata
- **Power Rename** — Rename output files on the fly with:
  - Find & Replace
  - Prefix and Suffix
  - Text casing (lowercase / UPPERCASE / Keep Original)
  - Sequential numbering with custom start index
  - Live preview before converting
- **Custom Output Directory** — Save files anywhere on your system
- **Non-blocking UI** — Conversion runs on a background thread so the app stays responsive
- **Dark Mode UI** — Built with CustomTkinter for a modern look

---

## 🗂️ Project Structure

```
webp-master/
├── webp_converter.py     # Main application source
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── dist/
    └── webp_converter.exe  # Compiled executable (after build)
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8** or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/geeymayur/webp-master.git
cd webp-master

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python webp_converter.py
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `customtkinter` | Modern dark-mode UI framework |
| `Pillow` | Image reading, conversion, and saving |

Install all at once:

```bash
pip install customtkinter Pillow
```

Or generate a `requirements.txt` yourself:

```bash
pip freeze > requirements.txt
```

---

## 🔨 Building a Standalone Executable

This project uses **PyInstaller** to compile into a single `.exe` (Windows) or binary (macOS/Linux) with no Python installation required on the end user's machine.

### Build Command

```bash
pyinstaller --noconsole --onefile --windowed --clean webp_converter.py
```

### Flags Explained

| Flag | Description |
|---|---|
| `--noconsole` | Suppresses the terminal/console window on launch |
| `--onefile` | Bundles everything into a single executable file |
| `--windowed` | Runs as a GUI app (no console), same as `--noconsole` on Windows |
| `--clean` | Clears PyInstaller's cache before building for a fresh output |

### Build Output

```
dist/
└── webp_converter.exe    # Your distributable executable
```

> **Tip:** Add `--icon=icon.ico` to the command above to embed a custom app icon.

### Install PyInstaller

```bash
pip install pyinstaller
```

---

## 🎛️ How to Use

1. **Add Images** — Click `+ Select Images` to pick one or more files (JPG, PNG, BMP, TIFF, WebP)
2. **Set Compression** — Use the `Compression` tab to adjust quality and engine effort
3. **Rename (Optional)** — Use the `Power Rename` tab to apply naming rules with a live preview
4. **Choose Output Folder** — Click `Browse` to pick where converted files will be saved
5. **Convert** — Hit `START CONVERSION` and monitor progress via the progress bar

---

## ⚙️ Compression Settings Reference

### Quality (1–100%)
Controls the lossy compression quality. Higher = better image quality, larger file size.

| Range | Use Case |
|---|---|
| 1–50 | Thumbnails, low-bandwidth previews |
| 51–79 | General web use |
| 80–90 | Recommended sweet spot |
| 91–100 | Near-lossless, large files |

### Compression Engine Effort (0–6)
Controls how hard Google's `libwebp` works to compress the image.

| Value | Speed | File Size |
|---|---|---|
| 0 | Fastest | Largest |
| 3 | Balanced | Moderate |
| 6 | Slowest | Smallest |

### Lossless Mode
When enabled, WebP is saved with zero quality loss (like PNG). Quality and method sliders still affect encoding speed and file size but not visual quality.

---

## 🔬 Technical Notes

- **Color Mode Handling** — Images in palette (`P`), greyscale+alpha (`LA`), or other non-standard modes are automatically converted to `RGB` or `RGBA` before saving to ensure WebP compatibility.
- **EXIF Preservation** — If `Keep EXIF/Metadata` is checked and the source image contains EXIF data, it is passed directly to Pillow's `save()` via the `exif` kwarg.
- **Threading** — Conversion runs on a `daemon=True` background thread so the Tkinter main loop is never blocked.
- **Sequential Naming** — Numbers are zero-padded to 2 digits (`_01`, `_02`) for correct alphabetical file sorting.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👨‍💻 Developer

**Mayur Sharma**
Founder & Lead Developer — NexLogic Systems LLP

- 🌐 Website: [www.mayurx.in](https://www.mayurx.in)
- 🐙 GitHub: [@geeymayur](https://github.com/geeymayur)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ by <a href="https://www.mayurx.in">Mayur Sharma</a></p>
