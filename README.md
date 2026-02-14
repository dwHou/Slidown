<div align="center">

# Slidown

<h3 style="font-family: system-ui, -apple-system, sans-serif; font-size: 2.5rem; font-weight: 300; letter-spacing: -0.5px; margin: 1rem 0;">
  <span style="font-weight: 700; color: #00D9FF;">Sli</span><span style="color: #888; padding: 0 0.3rem;">|</span><span style="color: #666;">down</span>
</h3>

**Transform Markdown into Beautiful HTML Presentations**

[![PyPI version](https://img.shields.io/pypi/v/slidown-md.svg?color=00D9FF&style=for-the-badge)](https://pypi.org/project/slidown-md/)
[![Python versions](https://img.shields.io/pypi/pyversions/slidown-md.svg?color=0099FF&style=for-the-badge)](https://pypi.org/project/slidown-md/)
[![License](https://img.shields.io/github/license/dwHou/slidown.svg?color=00FF41&style=for-the-badge)](https://github.com/dwHou/slidown/blob/master/LICENSE)

[English](#) | [简体中文](README.zh.md)

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- **Single-File Output** - All CSS/JS inlined, zero dependencies
- **Smart Pagination** - Auto-adjusts content based on viewport height
- **Three Beautiful Themes** - Tech, Clean, Corporate
- **LaTeX Math Support** - Full KaTeX rendering for formulas
- **Code Highlighting** - Pygments-powered syntax for 30+ languages
- **Lightning Fast** - Lightweight architecture, works completely offline

</td>
<td width="50%">

### 🧭 Navigation System
- **Chapter Progress Bar** - Bottom navigation with quick jumps
- **Table of Contents** - Expandable sidebar with full outline
- **Keyboard Shortcuts** - Arrow keys, spacebar, Home/End
- **Touch/Mouse Support** - Swipe gestures and click navigation
- **Responsive Design** - Perfectly adapts to any screen size

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Installation

#### Option 1: Install from PyPI (Recommended)

```bash
pip install slidown-md
```

#### Option 2: Install from Source

```bash
git clone https://github.com/dwHou/slidown.git
cd Slidown
pip install markdown pygments
```

### Basic Usage

```bash
# Convert Markdown document (auto-generates timestamped output folder)
slidown your_notes.md

# Use specific theme
slidown your_notes.md --theme clean

# Add custom footer
slidown your_notes.md --theme corporate --footer "© 2026 Your Company"
```

### Output Structure

```
your_notes_20260213143025/
├── your_notes-slidown.html    # Self-contained presentation
├── assets/
│   └── images/               # Image resources (default mode)
└── README.txt                # Usage instructions
```

Open `your_notes-slidown.html` in your browser to view the presentation.

---

## 🎨 Themes

<table>
<tr>
<td width="33%">

### Tech / Cyberpunk
**Default Theme**

Dark background with neon colors (cyan, blue, green) and grid effects.

**Best for:**
- Technical talks
- Programming tutorials
- Product launches

```bash
slidown doc.md --theme tech
```

</td>
<td width="33%">

### Clean / Fresh

Bright white background with soft, minimal design.

**Best for:**
- Documentation
- Teaching materials
- Academic presentations

```bash
slidown doc.md --theme clean
```

</td>
<td width="33%">

### Corporate

Professional business style with deep blue/gray colors.

**Best for:**
- Enterprise presentations
- Formal reports
- Investor pitches

```bash
slidown doc.md --theme corporate
```

</td>
</tr>
</table>

---

## 📖 Documentation

### Command Line Arguments

```bash
slidown INPUT [OPTIONS]

Required:
  INPUT                     Input Markdown file path

Output Options:
  -o, --output DIR          Output base directory (default: same as input)
  -t, --theme THEME         Theme: tech/cyberpunk, clean/fresh, corporate
  -f, --footer TEXT         Custom footer text

Pagination Control:
  --split-level N           Heading level for pagination (1-6, default: 2)
  --viewport-height PX      Viewport height in pixels (default: 900)
  --content-threshold N     Content threshold 0-1 (default: 0.8)
  --max-content-length N    Max characters per page (default: 800)
  --max-elements N          Max elements per page (default: 15)
  --show-page-numbers       Show page numbers (e.g., "Title (1/3)")

Navigation Control:
  --chapter-level N         Heading level for progress bar (1-6, default: 2)
  --no-chapter-nav          Disable chapter progress bar

Image Processing:
  --preserve-image-paths    Preserve original image paths (don't copy)
  --no-copy-images          Same as above
```

### Usage Examples

<details>
<summary><b>📝 Basic Conversion</b></summary>

```bash
slidown lecture.md
# Output: lecture_20260213143025/lecture-slidown.html
```

</details>

<details>
<summary><b>🎨 Specify Theme and Output Directory</b></summary>

```bash
slidown notes.md -o ~/Desktop/presentation --theme clean
```

</details>

<details>
<summary><b>🏢 Enterprise Presentation with Custom Footer</b></summary>

```bash
slidown pitch.md --theme corporate --footer "Confidential - © 2026 Company Inc."
```

</details>

<details>
<summary><b>⚙️ Adjust Pagination and Navigation</b></summary>

```bash
# Use H1 headings for pagination, show more chapters (H1-H3)
slidown doc.md --split-level 1 --chapter-level 3

# Adjust page height and content threshold
slidown doc.md --viewport-height 1080 --content-threshold 0.75
```

</details>

<details>
<summary><b>🖼️ Preserve Image Paths (No Copy)</b></summary>

```bash
slidown article.md --preserve-image-paths
# HTML can be placed directly in same directory as Markdown
```

</details>

<details>
<summary><b>📊 Smart Pagination with Custom Content Length</b></summary>

```bash
slidown long_tutorial.md --max-content-length 600 --max-elements 12
```

</details>

---

## ⚡ Advanced Features

### LaTeX Math Support

Slidown fully supports LaTeX math formulas, rendered with KaTeX:

**Inline formulas:**
```markdown
The mass-energy equation $E=mc^2$ is fundamental to physics.
```

**Block formulas:**
```markdown
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### Smart Pagination

- **Auto-detect content length** based on viewport height and content threshold
- **Guaranteed no scrolling** - each page content within configured max height
- **Preserve integrity** - never breaks code blocks, formulas, or tables
- **Configurable** via `--viewport-height` and `--content-threshold`

**How it works:**
1. Initial pagination based on heading level (`--split-level`)
2. Detect content length of each page
3. If exceeds threshold, intelligently split into sub-pages
4. Protect code blocks, tables, formulas from being broken

### Image Processing

**Default mode (copy):**
```bash
slidown doc.md
# Images copied to doc_20260213143025/assets/images/
# Self-contained presentation, perfect for sharing and archiving
```

**Path preservation mode:**
```bash
slidown doc.md --preserve-image-paths
# Preserve original paths from Markdown
# Ideal when HTML and Markdown are in same directory
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **→** or **Space** or **PageDown** | Next page |
| **←** or **PageUp** | Previous page |
| **Home** | Jump to first page |
| **End** | Jump to last page |
| **F11** | Fullscreen mode |

---

## 🛠️ Technical Implementation

<table>
<tr>
<td>

**Parser**
- Python `markdown` library
- Extensions: fenced_code, tables, toc, nl2br

**Code Highlighting**
- Pygments syntax highlighting
- 30+ languages supported

**Math Formulas**
- KaTeX rendering engine
- CDN delivery

</td>
<td>

**Styling**
- Three built-in themes
- CSS3 transitions and animations
- Responsive media queries

**Navigation**
- Pure JavaScript implementation
- No external library dependencies
- Touch and keyboard support

</td>
</tr>
</table>

---

## 📋 Supported Markdown Syntax

- **Headings** (H1-H6)
- **Lists** (ordered and unordered)
- **Code blocks** (with syntax highlighting)
- **Inline code**
- **Text formatting** (bold, italic, strikethrough)
- **Links**
- **Images** (local and network)
- **Tables**
- **Blockquotes**
- **Horizontal rules**
- **Line breaks**
- **LaTeX math formulas** (inline and block)

---

## 💼 Use Cases

<table>
<tr>
<td width="50%">

### Professional
- Enterprise presentations
- Product demonstrations
- Quarterly reports
- Investor pitches
- Formal documentation

</td>
<td width="50%">

### Technical
- Technical talks
- Code demonstrations
- Architecture explanations
- API documentation
- Tutorial materials

</td>
</tr>
<tr>
<td width="50%">

### Educational
- Teaching materials
- Math/science lectures
- Academic presentations
- Student projects
- Training courses

</td>
<td width="50%">

### Personal
- Blog visualization
- Note sharing
- Personal knowledge base
- Portfolio presentations
- Creative projects

</td>
</tr>
</table>

---

## 🎯 Why Slidown?

### vs. Traditional PowerPoint
- ✅ No software installation required
- ✅ Smaller file size (plain text HTML)
- ✅ Easy version control (Git-friendly)
- ✅ Code syntax highlighting built-in
- ✅ LaTeX math formula support
- ✅ Responsive design for all devices
- ✅ Fast sharing (open directly in browser)

### vs. Online Tools (Google Slides, Notion)
- ✅ Fully offline capable
- ✅ No login required
- ✅ Privacy and security (local storage)
- ✅ Fast loading
- ✅ Flexible custom themes

---

## ❓ FAQ

<details>
<summary><b>Can the generated HTML files be used offline?</b></summary>

Yes. All CSS and JavaScript are inlined in the HTML. Math formulas require internet (KaTeX CDN), but you can download KaTeX locally.

</details>

<details>
<summary><b>Does it support math formulas?</b></summary>

Full support! Use `$...$` (inline) and `$$...$$` (block) syntax, KaTeX renders automatically.

</details>

<details>
<summary><b>How to customize themes?</b></summary>

Currently supports 3 built-in themes (tech, clean, corporate), selectable via `--theme` parameter. Future versions will support custom theme configuration.

</details>

<details>
<summary><b>How are image paths handled?</b></summary>

Default mode auto-copies images to `assets/images/` directory. To preserve original paths, use `--preserve-image-paths` parameter.

</details>

<details>
<summary><b>Can I export to PDF?</b></summary>

Yes. Open HTML file in browser, use "Print" function, select "Save as PDF".

</details>

<details>
<summary><b>Which browsers are supported?</b></summary>

All modern browsers (Chrome, Firefox, Safari, Edge). IE is not supported.

</details>

<details>
<summary><b>How to share presentations?</b></summary>

Three methods:
1. Directly send HTML file (if using default image copy mode)
2. Compress entire output folder (including assets)
3. Upload to static website hosting service (GitHub Pages, Netlify, etc.)

</details>

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

**Contribution areas:**
- New theme designs
- Improved smart pagination algorithm
- Add animation effects
- Performance optimization
- Bug fixes
- Documentation improvements

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🔗 Links

- **GitHub Repository**: [github.com/dwHou/slidown](https://github.com/dwHou/slidown)
- **Issue Tracker**: [Issues](https://github.com/dwHou/slidown/issues)
- **PyPI Package**: [pypi.org/project/slidown-md](https://pypi.org/project/slidown-md/)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">

**Made with ❤️ by [Devonn Hou](https://github.com/dwHou)**

*Slidown = "Slide" (slideshow) + "Markdown" (markup language)*

Transform your Markdown notes into beautiful presentations

</div>
