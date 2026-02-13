# Changelog - Slidown

Transform Markdown into Beautiful HTML Presentations

## Version 2.1.2 - Project Rename to Slidown (2026-02-13)

### Breaking Changes

**Project renamed from "SlideDown" to "Slidown"**

The project has been further refined with a cleaner, more streamlined brand identity:
- Old name: SlideDown
- New name: **Slidown** (simplified spelling, modern tech aesthetic)
- Main script: `slidown.py` (already renamed in v2.1.1)

### Brand Identity

**Pure CSS Logo Design:**
```html
<div class="logo">
  <span class="logo-sli">Sli</span><span class="logo-separator">|</span><span class="logo-down">down</span>
</div>
```

**Logo Philosophy:**
- "Sli" - Bold, cyan (#00D9FF), glowing effect - represents transformation and technology
- "|" - Separator, subtle gray - represents the bridge between formats
- "down" - Light, gray (#888888) - represents Markdown foundation

**Key Features:**
- No SVG/PNG files needed - pure CSS implementation
- Fully responsive and animatable
- Matches the cyberpunk tech aesthetic of the project
- Easy to customize and maintain

### What Changed

1. **Project Name**
   - Project name: `SlideDown` → `Slidown`
   - All documentation updated with new branding

2. **Brand Assets**
   - Added official website at `website/index.html`
   - Pure CSS logo (no image files)
   - Cyan (#00D9FF) + Gray (#888888) color scheme

3. **Documentation Updates**
   - README.md: Updated to "Slidown"
   - QUICKSTART.md: Updated all references
   - USAGE_GUIDE.md: Updated project name
   - CHANGELOG.md: Added this v2.1.2 entry

### Official Website

New single-page website includes:
- Pure CSS logo with hover effects
- Hero section with CTA
- Features showcase (6 core features)
- Theme previews (Tech/Clean/Corporate)
- Quick Start guide
- Usage examples
- Responsive design (desktop/tablet/mobile)

### Migration Note

The script name remains `slidown.py` (unchanged from v2.1.1), so no command changes are needed. Only the project branding has been updated.

---

## Version 2.1.1 - Project Rename to SlideDown (2026-02-13)

### Breaking Changes

**Project renamed from "MarkDown2PPT" to "SlideDown"**

The project has been rebranded to better reflect its purpose and modern identity:
- Old name: MarkDown2PPT
- New name: **SlideDown** (a play on "Slide" + "Markdown")
- Main script renamed: `md2html.py` → `slidown.py`

### What Changed

1. **Directory Structure**
   - Project directory: `MarkDown2PPT/` → `SlideDown/`
   - All documentation updated with new name

2. **Script Rename**
   - Main script: `md2html.py` → `slidedown.py`
   - Usage: `python slidedown.py input.md output.html`

3. **Documentation Updates**
   - README.md: Updated project title and description
   - QUICKSTART.md: All commands now use `slidedown.py`
   - USAGE_GUIDE.md: Complete documentation refresh
   - CHANGELOG.md: This file

4. **Project Description**
   - New tagline: "Transform Markdown into Beautiful HTML Presentations"
   - Emphasizes the dual meaning: Slide presentations + Markdown format
   - More memorable and descriptive brand

### Migration Guide

If you were using the old version:

**Old command:**
```bash
python md2html.py document.md output.html --theme clean
```

**New command:**
```bash
python slidedown.py document.md output.html --theme clean
```

All functionality remains identical - only the script name has changed.

### Examples Cleanup

- The `examples/` directory has been cleaned up
- Old example outputs removed
- Directory is ready for new example presentations

---

## Version 2.1.0 - Smart Pagination & Chapter Navigation (2026-02-13)

### New Features

#### 1. Smart Content Pagination
Automatically splits long slides into multiple pages to improve readability:

**Features:**
- **Content Length Detection**: Monitors character count and element count per slide
- **Intelligent Splitting**: Breaks slides at natural boundaries (paragraphs, lists)
- **Preserves Integrity**: Never splits code blocks, tables, or other atomic elements
- **Configurable Thresholds**: Customize via `--max-content-length` and `--max-elements`
- **Optional Page Numbers**: Show page indicators like "Title (1/3)" with `--show-page-numbers`

**Usage:**
```bash
# Use default thresholds (800 chars, 15 elements)
python slidedown.py document.md

# Custom thresholds
python slidedown.py document.md --max-content-length 600 --max-elements 12

# Enable page numbers
python slidedown.py document.md --show-page-numbers
```

**Splitting Logic:**
- Checks each slide against thresholds
- Finds safe split points (avoids breaking code/tables)
- Creates multiple slides with same title
- Links them as a chapter group for navigation

#### 2. Chapter Navigation Bar
Interactive navigation bar at the bottom of each slide:

**Features:**
- **Visual Chapter List**: Shows all major chapters in one bar
- **Active Highlighting**: Current chapter is visually emphasized
- **Quick Jump**: Click any chapter name to jump to that section
- **Theme-Adaptive**: Styled to match each presentation theme
- **Responsive**: Adapts to screen size, scrollable on mobile

**Configuration:**
```bash
# Default (H1 headings as chapters)
python slidedown.py document.md

# Use H2 headings as chapters
python slidedown.py document.md --chapter-level 2

# Disable chapter navigation
python slidedown.py document.md --no-chapter-nav
```

**Theme-Specific Styling:**
- **Tech Theme**: Neon cyan borders with glowing effects
- **Clean Theme**: Simple borders with soft shadows
- **Corporate Theme**: Professional tabs with uppercase text

#### 3. Enhanced JavaScript Navigation
Updated navigation system:
- Tracks current chapter automatically
- Updates highlighting as you navigate
- Click handlers for chapter navigation
- Maintains compatibility with keyboard shortcuts

### Command-Line Arguments (New)

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `--max-content-length` | int | Max chars per slide | 800 |
| `--max-elements` | int | Max elements per slide | 15 |
| `--show-page-numbers` | flag | Show "(1/3)" in titles | False |
| `--chapter-nav` | flag | Enable chapter nav | True |
| `--no-chapter-nav` | flag | Disable chapter nav | - |
| `--chapter-level` | 1-6 | Heading level for chapters | 1 (H1) |

### CSS Enhancements

Added chapter navigation styles to all themes:

**Common Styles:**
- Fixed position at bottom center
- Flexbox layout with separators
- Hover effects on chapter names
- Active state highlighting
- Responsive breakpoints for mobile

**Tech Theme:**
```css
.chapter.active {
    color: var(--cyan);
    text-shadow: 0 0 15px var(--cyan);
    border-bottom: 2px solid var(--cyan);
}
```

**Clean Theme:**
```css
.chapter.active {
    color: var(--primary);
    background: var(--bg-secondary);
    border-bottom: 2px solid var(--secondary);
}
```

**Corporate Theme:**
```css
.chapter.active {
    color: white;
    background: var(--primary);
    box-shadow: 0 2px 8px var(--shadow);
}
```

### Algorithm Details

**Content Splitting Algorithm:**
```python
def _split_slide(slide):
    1. Track code blocks and tables (don't split)
    2. Count chars/elements per line
    3. When threshold exceeded:
       - Check if in code block or table
       - If not, create new chunk
    4. Generate slides from chunks
    5. Add metadata (page_number, total_pages)
```

**Chapter Extraction:**
```python
def _extract_chapters(slides):
    1. Iterate through all slides
    2. Skip title slides
    3. Use original_title for paginated slides
    4. Deduplicate based on title
    5. Record slide number for each chapter
```

### Testing Results

Tested with `3DGS_OpenCVTeam.md`:

**Scenario 1: Default Settings**
- Input: 927-line Markdown
- Output: 35 slides
- Chapters detected: 3 ("资源", "3D GS原理理解", "OpenCV Team 讲座笔记")

**Scenario 2: Aggressive Pagination**
- `--max-content-length 600 --max-elements 12`
- Output: 35 slides (some sections split)
- Page numbers added where splits occurred

**Scenario 3: Different Chapter Levels**
- `--chapter-level 2`: More granular chapters (H2 level)
- Output: 32 slides
- More chapters in navigation bar

### Examples

**1. Long Document with Smart Pagination**
```bash
python slidedown.py long_tutorial.md \
  --theme clean \
  --max-content-length 600 \
  --show-page-numbers
```

**2. Multi-Section Report with Chapter Nav**
```bash
python slidedown.py annual_report.md \
  --theme corporate \
  --chapter-level 2 \
  --footer "Confidential"
```

**3. Technical Docs (Disable Auto-Split)**
```bash
python slidedown.py api_reference.md \
  --theme tech \
  --max-content-length 2000 \
  --no-chapter-nav
```

### Benefits

**For Readers:**
- Less scrolling per page
- Easy chapter navigation
- Clear visual progress indicators

**For Presenters:**
- Better content organization
- Quick section jumping
- Professional appearance

**For Content Creators:**
- No manual slide splitting needed
- Automatic navigation generation
- Flexible configuration

### Backward Compatibility

- All v2.0 features fully preserved
- Default behavior similar (pagination is gentle)
- Can disable all new features with flags

---

## Version 2.0 - Enhanced Features (2026-02-13)

### Major Enhancements

#### 1. Multi-Theme Support
Added three distinct presentation themes:

**Tech/Cyberpunk Theme** (`--theme tech` or `--theme cyberpunk`)
- Dark background with neon colors
- Matrix grid background effect
- Scanline overlay for retro-futuristic look
- Ideal for technical presentations

**Clean/Fresh Theme** (`--theme clean` or `--theme fresh`)
- Bright, minimalist design
- White/light backgrounds
- Soft color palette (blues, greens)
- Perfect for long reading sessions
- Professional and easy on the eyes

**Corporate Theme** (`--theme corporate`)
- Professional business styling
- Formal color scheme (navy, gray)
- Corporate gradient on title slides
- Suitable for internal company presentations

#### 2. Custom Footer/Watermark Support
- Add copyright notices, confidential warnings, or any custom text
- Displayed at bottom of each slide
- Automatically styled to match theme
- Example: `--footer "Confidential - For Internal Use Only. © 2023"`

#### 3. Enhanced Output Organization
New structured output format:
```
document_20260213/
├── presentation.html          # Main presentation
├── assets/                    # Resource folder
│   └── images/               # All images
└── README.txt                # Usage instructions
```

Features:
- Automatic date-stamped folder names (`document_YYYYMMDD`)
- Option to disable date stamp with `--no-date`
- Self-contained: all resources in one folder
- Portable: can be moved or hosted anywhere

#### 4. Automatic Image Management
- Detects all images in Markdown
- Copies local images to `assets/images/`
- Updates paths to relative references
- Handles duplicate filenames automatically
- Supports both local images and remote URLs

#### 5. Comprehensive Command-Line Interface
Complete argument system with help:

```bash
# Basic usage (auto-generates output with date)
python slidedown.py document.md

# Theme selection
python slidedown.py document.md --theme clean

# Custom footer
python slidedown.py document.md --footer "Copyright 2023"

# Without date in folder name
python slidedown.py document.md --no-date

# Custom output location
python slidedown.py document.md --output /path/to/output

# Adjust slide splitting level
python slidedown.py document.md --split-level 1

# View all options
python slidedown.py --help
```

### Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `input` | - | Input Markdown file path | Required |
| `--output` | `-o` | Output directory/file path | Auto-generated |
| `--theme` | `-t` | Theme selection | `tech` |
| `--footer` | `-f` | Custom footer text | None |
| `--split-level` | `-s` | Heading level for slides | `2` (H2) |
| `--no-date` | - | Omit date from folder name | False |

### Theme Comparison

| Feature | Tech | Clean | Corporate |
|---------|------|-------|-----------|
| Background | Dark (#0a0a0f) | Light (#ffffff) | Light gray (#f5f5f5) |
| Primary Color | Cyan (#00d4ff) | Blue (#0066cc) | Navy (#1a3a5c) |
| Best For | Technical, coding | Documentation, reading | Business, formal |
| Special Effects | Grid + scanlines | None | Gradient title |
| Font Style | Orbitron, JetBrains | Inter, Source Code Pro | Open Sans, Roboto |

### Technical Improvements

1. **Resource Management Class**
   - Dedicated `ResourceManager` for handling assets
   - Automatic directory structure creation
   - Image path resolution and copying

2. **Theme System**
   - Modular CSS for each theme
   - Theme aliases (e.g., `tech` = `cyberpunk`)
   - Easy to extend with new themes

3. **Better Error Handling**
   - Informative console output
   - Success/failure banners
   - Detailed file path reporting

4. **Documentation**
   - Auto-generated README.txt in output
   - Comprehensive help text
   - Usage examples

### Backward Compatibility

All original functionality preserved:
- Original cyberpunk theme (now called `tech`)
- Slide navigation and controls
- Markdown parsing with extensions
- Responsive design

### Example Use Cases

**1. Technical Workshop**
```bash
python slidedown.py workshop.md --theme tech
```

**2. Company Internal Presentation**
```bash
python slidedown.py quarterly_review.md --theme corporate \
  --footer "Confidential - Internal Use Only. © 2023 Company Inc."
```

**3. Clean Documentation**
```bash
python slidedown.py user_guide.md --theme clean --no-date
```

**4. Quick Prototype (H1 splits)**
```bash
python slidedown.py outline.md --split-level 1 --theme clean
```

### Files Modified

- `slidedown.py` (formerly `md2html.py`) - Main script with all enhancements

### Dependencies

No new dependencies required. Uses existing:
- `markdown` - Markdown to HTML conversion
- `python 3.x` standard library

### Testing

Tested with:
- Sample file: `3DGS_OpenCVTeam.md`
- All three themes verified
- Footer functionality confirmed
- Image copying validated
- Output structure verified

### Future Enhancements (Possible)

- Custom theme files (CSS injection)
- Slide transitions configuration
- Export to PDF
- Video/audio embedding
- Speaker notes support
- Multi-language UI
