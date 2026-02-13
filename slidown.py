#!/usr/bin/env python3
"""
Markdown to HTML Presentation Converter

Convert Markdown documents to beautiful HTML presentations with slide navigation.
Supports multiple themes, custom footers, and automatic resource management.
"""

import sys
import argparse
import re
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import markdown
from markdown.extensions import fenced_code, tables, toc
import html
import urllib.parse


class MarkdownSlideParser:
    """Parse Markdown into slides"""

    def __init__(self, split_level: int = 2, max_content_length: int = 800,
                 max_elements: int = 15, show_page_numbers: bool = False,
                 viewport_height: Optional[int] = None, content_threshold: float = 0.8):
        """
        Args:
            split_level: Heading level for slide splitting (1-6, default: 2 = H2)
            max_content_length: Maximum content length per slide in characters
            max_elements: Maximum number of elements per slide
            show_page_numbers: Show page numbers in titles (e.g., "Title (1/3)")
            viewport_height: Viewport height in pixels (None = auto-detect)
            content_threshold: Content threshold as fraction of viewport height (default: 0.8)
        """
        self.split_level = split_level
        self.max_content_length = max_content_length
        self.max_elements = max_elements
        self.show_page_numbers = show_page_numbers
        self.viewport_height = viewport_height or 900  # Default viewport height
        self.content_threshold = content_threshold
        self.max_height = int(self.viewport_height * self.content_threshold)
        self.md = markdown.Markdown(
            extensions=['fenced_code', 'tables', 'toc', 'nl2br'],
            extension_configs={
                'toc': {'anchorlink': False}
            }
        )
        # Storage for protected math formulas
        self.math_blocks = []

    def _protect_math(self, text: str) -> str:
        """Protect LaTeX math formulas from being processed by markdown parser

        This method prevents the markdown parser from escaping or transforming
        LaTeX math notation ($...$ and $$...$$) which would break KaTeX rendering.

        The strategy is to:
        1. Replace all math blocks with HTML comment placeholders (which markdown ignores)
        2. Process the markdown normally
        3. Restore the math blocks in their original form for KaTeX to render

        Args:
            text: Markdown text that may contain math formulas

        Returns:
            Text with math formulas replaced by placeholders
        """
        self.math_blocks = []

        # Protect display math ($$...$$) first - must come before inline math
        # Use DOTALL to handle multi-line formulas
        def replace_display_math(match):
            # Use HTML comment as placeholder to avoid markdown processing
            placeholder = f"<!--MATH_DISPLAY_{len(self.math_blocks)}-->"
            self.math_blocks.append(('display', match.group(1)))
            return placeholder

        # Match $$...$$ - use non-greedy matching to handle multiple display math blocks
        text = re.sub(r'\$\$(.*?)\$\$', replace_display_math, text, flags=re.DOTALL)

        # Protect inline math ($...$)
        def replace_inline_math(match):
            # Use HTML comment as placeholder to avoid markdown processing
            placeholder = f"<!--MATH_INLINE_{len(self.math_blocks)}-->"
            self.math_blocks.append(('inline', match.group(1)))
            return placeholder

        # Match $...$ but ensure:
        # 1. Content doesn't contain $ (to avoid matching across formulas)
        # 2. Content doesn't span multiple lines (to keep inline math inline)
        # Note: [^\$\n]+ ensures at least one character and no $ or newlines inside
        text = re.sub(r'\$([^\$\n]+?)\$', replace_inline_math, text)

        return text

    def _restore_math(self, html: str) -> str:
        """Restore LaTeX math formulas after markdown processing

        Args:
            html: HTML with math formula placeholders

        Returns:
            HTML with math formulas restored
        """
        for i, (math_type, formula) in enumerate(self.math_blocks):
            if math_type == 'display':
                # Restore display math with $$ delimiters for KaTeX
                html = html.replace(f"<!--MATH_DISPLAY_{i}-->", f"$${formula}$$")
            else:
                # Restore inline math with $ delimiters for KaTeX
                html = html.replace(f"<!--MATH_INLINE_{i}-->", f"${formula}$")

        return html

    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Parse Markdown file into slides

        Returns:
            List of slides, each slide is a dict with:
            - title: slide title (optional)
            - content: HTML content
            - is_title_slide: whether this is a title slide (first H1)
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse_content(content)

    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        """Parse Markdown content into slides"""
        # Split by heading level
        split_pattern = rf'^(#{{{self.split_level}}})\s+(.+)$'

        # Also detect H1 for title slides
        h1_pattern = r'^#\s+(.+)$'

        lines = content.split('\n')
        slides = []
        current_slide = []
        current_title = None
        is_first_h1 = True

        for line in lines:
            # Check for H1 (potential title slide)
            h1_match = re.match(h1_pattern, line)
            if h1_match and is_first_h1 and self.split_level != 1:
                # Create title slide
                if current_slide:
                    slides.append(self._create_slide(current_title, current_slide, False))
                    current_slide = []

                title_text = h1_match.group(1)
                current_title = title_text
                current_slide = [line]
                is_first_h1 = False
                continue

            # Check for split heading
            split_match = re.match(split_pattern, line)
            if split_match:
                # Save previous slide
                if current_slide:
                    is_title = is_first_h1 and len(slides) == 0
                    slides.append(self._create_slide(current_title, current_slide, is_title))

                # Start new slide
                current_title = split_match.group(2)
                current_slide = [line]
                is_first_h1 = False
            else:
                current_slide.append(line)

        # Add last slide
        if current_slide:
            is_title = is_first_h1 and len(slides) == 0
            slides.append(self._create_slide(current_title, current_slide, is_title))

        # Apply smart pagination
        slides = self._apply_smart_pagination(slides)

        return slides

    def _create_slide(self, title: str, lines: List[str], is_title_slide: bool) -> Dict[str, Any]:
        """Create slide dictionary"""
        content_md = '\n'.join(lines)

        # Protect math formulas before markdown processing
        protected_md = self._protect_math(content_md)

        # Convert markdown to HTML
        content_html = self.md.convert(protected_md)

        # Restore math formulas after markdown processing
        content_html = self._restore_math(content_html)

        return {
            'title': title,
            'content': content_html,
            'is_title_slide': is_title_slide,
            'raw_lines': lines  # Keep raw lines for pagination
        }

    def _apply_smart_pagination(self, slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply smart pagination to slides that are too long"""
        paginated_slides = []

        for slide in slides:
            if slide['is_title_slide']:
                # Don't paginate title slides
                paginated_slides.append(slide)
                continue

            # Check if slide needs splitting
            if self._should_split_slide(slide):
                split_slides = self._split_slide(slide)
                paginated_slides.extend(split_slides)
            else:
                paginated_slides.append(slide)

        return paginated_slides

    def _estimate_element_height(self, element: str) -> int:
        """Estimate the visual height of an HTML element in pixels

        Args:
            element: HTML element string

        Returns:
            Estimated height in pixels
        """
        # Heading heights (based on font-size in CSS)
        if '<h1>' in element or '<h1 ' in element:
            return 120
        if '<h2>' in element or '<h2 ' in element:
            return 100
        if '<h3>' in element or '<h3 ' in element:
            return 80
        if '<h4>' in element or '<h4 ' in element:
            return 70
        if '<h5>' in element or '<h5 ' in element:
            return 60
        if '<h6>' in element or '<h6 ' in element:
            return 60

        # Code blocks (estimate lines)
        if '<pre>' in element:
            code_lines = element.count('\n') + 1
            return code_lines * 20 + 40  # 20px per line + 40px padding

        # Tables (estimate rows)
        if '<table>' in element:
            row_count = element.count('<tr>')
            return row_count * 40 + 50  # 40px per row + 50px header

        # Images (default height if not specified)
        if '<img' in element:
            # Try to extract height attribute
            height_match = re.search(r'height=["\']?(\d+)', element)
            if height_match:
                return int(height_match.group(1))
            return 300  # Default image height

        # List items
        if '<li>' in element:
            li_count = element.count('<li>')
            return li_count * 32

        # Paragraphs (estimate lines based on character count)
        if '<p>' in element:
            text_content = re.sub(r'<[^>]+>', '', element)
            char_count = len(text_content)
            # Assume ~80 chars per line, 24px per line
            lines = max(1, char_count // 80)
            return lines * 24 + 12  # 24px per line + 12px margin

        # Blockquote
        if '<blockquote>' in element:
            text_content = re.sub(r'<[^>]+>', '', element)
            char_count = len(text_content)
            lines = max(1, char_count // 70)
            return lines * 24 + 36  # Lines + padding

        # Horizontal rule
        if '<hr>' in element or '<hr />' in element:
            return 36

        # Default for other elements
        return 40

    def _should_split_slide(self, slide: Dict[str, Any]) -> bool:
        """Determine if a slide should be split based on visual height estimation"""
        content = slide['content']

        # Split content into top-level HTML elements
        # Simple split by common block-level tags
        elements = re.split(r'(<(?:h[1-6]|p|pre|table|ul|ol|blockquote|hr)[^>]*>.*?</(?:h[1-6]|p|pre|table|ul|ol|blockquote)>|<hr\s*/?>)',
                           content, flags=re.DOTALL)

        total_height = 0
        for element in elements:
            if element.strip():
                total_height += self._estimate_element_height(element)

        # Also check character count and element count as fallback
        text_content = re.sub(r'<[^>]+>', '', content)
        char_count = len(text_content)

        element_count = (
            len(re.findall(r'<p>', content)) +
            len(re.findall(r'<li>', content)) +
            len(re.findall(r'<pre>', content)) +
            len(re.findall(r'<table>', content))
        )

        return (total_height > self.max_height or
                char_count > self.max_content_length or
                element_count > self.max_elements)

    def _estimate_line_height(self, line: str) -> int:
        """Estimate the visual height of a markdown line in pixels"""
        stripped = line.strip()

        if not stripped:
            return 12  # Empty line spacing

        # Headings
        if stripped.startswith('# '):
            return 120
        if stripped.startswith('## '):
            return 100
        if stripped.startswith('### '):
            return 80
        if stripped.startswith('#### '):
            return 70
        if stripped.startswith('##### ') or stripped.startswith('###### '):
            return 60

        # Code block fence
        if stripped.startswith('```'):
            return 20

        # List items
        if stripped.startswith(('-', '*', '+')) or re.match(r'^\d+\.', stripped):
            return 32

        # Table row
        if '|' in stripped:
            return 40

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            return 36

        # Regular paragraph line (estimate ~24px per line)
        return 24

    def _contains_inline_math(self, line: str) -> bool:
        """Check if line contains inline math formulas ($...$)"""
        import re
        # Match $...$ but not $$
        # This pattern matches inline math that doesn't contain $ or newlines inside
        pattern = r'(?<!\$)\$(?!\$)[^\$\n]+?\$(?!\$)'
        return bool(re.search(pattern, line))

    def _extract_display_math_block(self, lines: List[str], start_index: int) -> tuple:
        """Extract complete display math block ($$...$$)

        Returns:
            (block_lines, block_height)
        """
        block = [lines[start_index]]  # Starting $$
        i = start_index + 1

        # Find ending $$
        while i < len(lines):
            block.append(lines[i])
            if lines[i].strip() == '$$':
                break
            i += 1

        # Estimate height: formula lines + padding
        height = len(block) * 30 + 40
        return block, height

    def _split_slide(self, slide: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split a slide into multiple slides based on visual height estimation

        Preserves atomic units:
        1. Code blocks (```...```)
        2. Tables
        3. Display math ($$...$$)
        4. Lines with inline math ($...$)
        """
        lines = slide['raw_lines']
        title = slide['title']

        chunks = []
        current_chunk = []
        current_height = 0
        current_char_count = 0
        current_element_count = 0
        in_code_block = False
        in_table = False
        in_display_math = False
        code_block_lines = []
        table_lines = []
        math_block_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # 1. Track code blocks (don't split them)
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lines = [line]
                else:
                    in_code_block = False
                    code_block_lines.append(line)
                    # Estimate code block height
                    code_height = len(code_block_lines) * 20 + 40

                    # Check if adding code block exceeds limit
                    if current_height + code_height > self.max_height and current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = code_block_lines[:]
                        current_height = code_height
                        current_char_count = sum(len(l) for l in code_block_lines)
                        current_element_count = 1
                    else:
                        current_chunk.extend(code_block_lines)
                        current_height += code_height
                        current_char_count += sum(len(l) for l in code_block_lines)
                        current_element_count += 1

                    code_block_lines = []
                i += 1
                continue

            if in_code_block:
                code_block_lines.append(line)
                i += 1
                continue

            # 2. Track display math blocks ($$...$$) - don't split them
            if line.strip() == '$$' and not in_code_block:
                if not in_display_math:
                    in_display_math = True
                    math_block_lines = [line]
                else:
                    in_display_math = False
                    math_block_lines.append(line)
                    # Estimate display math block height
                    math_height = len(math_block_lines) * 30 + 40

                    # Check if adding math block exceeds limit
                    if current_height + math_height > self.max_height and current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = math_block_lines[:]
                        current_height = math_height
                        current_char_count = sum(len(l) for l in math_block_lines)
                        current_element_count = 1
                    else:
                        current_chunk.extend(math_block_lines)
                        current_height += math_height
                        current_char_count += sum(len(l) for l in math_block_lines)
                        current_element_count += 1

                    math_block_lines = []
                i += 1
                continue

            if in_display_math:
                math_block_lines.append(line)
                i += 1
                continue

            # 3. Check for inline math ($...$) - keep the whole line intact
            if self._contains_inline_math(line) and not in_code_block:
                line_height = self._estimate_line_height(line)
                line_chars = len(line)

                # If adding this line would exceed limit, start new chunk
                if current_height + line_height > self.max_height and current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = [line]
                    current_height = line_height
                    current_char_count = line_chars
                    current_element_count = 1
                else:
                    current_chunk.append(line)
                    current_height += line_height
                    current_char_count += line_chars
                    current_element_count += 1

                i += 1
                continue

            # 4. Track tables (don't split them)
            if '|' in line and not in_code_block:
                if not in_table:
                    in_table = True
                    table_lines = [line]
                else:
                    table_lines.append(line)
                i += 1
                continue
            elif in_table:
                if line.strip() == '':
                    in_table = False
                    # Estimate table height
                    table_height = len(table_lines) * 40 + 50

                    # Check if adding table exceeds limit
                    if current_height + table_height > self.max_height and current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = table_lines[:]
                        current_height = table_height
                        current_char_count = sum(len(l) for l in table_lines)
                        current_element_count = 1
                    else:
                        current_chunk.extend(table_lines)
                        current_height += table_height
                        current_char_count += sum(len(l) for l in table_lines)
                        current_element_count += 1

                    table_lines = []
                else:
                    table_lines.append(line)
                    i += 1
                    continue

            # 5. Handle normal lines
            line_height = self._estimate_line_height(line)
            line_chars = len(line)
            line_elements = 0

            if line.strip().startswith(('-', '*', '+', '1.')) or line.strip().startswith('<li>'):
                line_elements = 1
            elif line.strip() and not line.startswith('#'):
                line_elements = 1

            # Check if adding this line would exceed limits
            would_exceed = (
                current_height + line_height > self.max_height or
                current_char_count + line_chars > self.max_content_length or
                current_element_count + line_elements > self.max_elements
            )

            # Don't split if current chunk is empty
            if would_exceed and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_height = 0
                current_char_count = 0
                current_element_count = 0

            current_chunk.append(line)
            current_height += line_height
            current_char_count += line_chars
            current_element_count += line_elements
            i += 1

        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)

        # Handle case where we didn't close code block, table, or math block
        if code_block_lines:
            if chunks and chunks[-1]:
                chunks[-1].extend(code_block_lines)
            else:
                chunks.append(code_block_lines)

        if table_lines:
            if chunks and chunks[-1]:
                chunks[-1].extend(table_lines)
            else:
                chunks.append(table_lines)

        if math_block_lines:
            if chunks and chunks[-1]:
                chunks[-1].extend(math_block_lines)
            else:
                chunks.append(math_block_lines)

        # Create slides from chunks
        split_slides = []
        for i, chunk in enumerate(chunks):
            page_num_suffix = f" ({i+1}/{len(chunks)})" if self.show_page_numbers else ""
            chunk_title = title + page_num_suffix if title else None

            content_md = '\n'.join(chunk)

            # Protect math formulas before markdown processing
            protected_md = self._protect_math(content_md)

            # Convert markdown to HTML
            content_html = self.md.convert(protected_md)

            # Restore math formulas after markdown processing
            content_html = self._restore_math(content_html)

            split_slides.append({
                'title': chunk_title,
                'content': content_html,
                'is_title_slide': False,
                'raw_lines': chunk,
                'original_title': title,
                'page_number': i + 1,
                'total_pages': len(chunks)
            })

        return split_slides


class HTMLPresentationRenderer:
    """Render slides to HTML presentation"""

    def __init__(self, theme: str = 'tech', footer: Optional[str] = None,
                 enable_chapter_nav: bool = True, chapter_level: int = 3):
        """
        Args:
            theme: Theme name (tech/cyberpunk, clean/fresh, corporate)
            footer: Optional footer text to display on each slide
            enable_chapter_nav: Enable chapter navigation bar
            chapter_level: Heading level to use for chapters (1-6, default: 2)
        """
        self.theme = theme
        self.footer = footer
        self.enable_chapter_nav = enable_chapter_nav
        self.chapter_level = chapter_level

        # Theme aliases
        self.theme_map = {
            'tech': 'tech',
            'cyberpunk': 'tech',
            'clean': 'clean',
            'fresh': 'clean',
            'corporate': 'corporate',
        }

    def render(self, slides: List[Dict[str, Any]], output_path: str, title: str = "Presentation"):
        """Render slides to HTML file

        Args:
            slides: List of slide dictionaries
            output_path: Output HTML file path
            title: Presentation title for HTML <title> tag
        """
        html_content = self._generate_html(slides, title)

        # Create parent directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _generate_html(self, slides: List[Dict[str, Any]], title: str) -> str:
        """Generate complete HTML document"""
        slides_html = self._generate_slides(slides)
        css = self._get_css()

        # Extract chapters for navigation (returns two lists: nav and toc)
        nav_chapters, toc_chapters = self._extract_chapters(slides)
        chapter_nav_html = self._generate_chapter_nav(nav_chapters, toc_chapters) if self.enable_chapter_nav else ''

        # Use nav_chapters for JavaScript (progress bar tracking)
        js = self._get_js(len(slides), nav_chapters)

        # Get actual theme name
        actual_theme = self.theme_map.get(self.theme, 'tech')

        # Theme-specific elements
        if actual_theme == 'tech':
            bg_elements = '''    <div class="matrix-bg"></div>
    <div class="scanlines"></div>'''
        else:
            bg_elements = ''

        # Footer HTML (independent, no container)
        footer_html = ''
        if self.footer:
            footer_html = f'''    <div class="footer-text">{html.escape(self.footer)}</div>'''

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>

    <!-- KaTeX for LaTeX math rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMath()"></script>

    <style>
{css}
    </style>
</head>
<body>
{bg_elements}

    <button class="fullscreen-btn" onclick="toggleFullscreen()">[ F11 全屏 ]</button>

    <div class="presentation">
{slides_html}
    </div>

    <!-- Progress bar -->
    <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
    </div>

    <!-- Footer (left bottom) -->
{footer_html}

    <!-- Page number (right bottom) -->
    <div class="page-number">
        <span id="currentSlide">1</span> / <span id="totalSlides">{len(slides)}</span>
    </div>

    <!-- Navigation hint -->
    <div class="nav-hint">
        <kbd>←</kbd> <kbd>→</kbd> 或 <kbd>空格</kbd> 导航
    </div>

{chapter_nav_html}

    <script>
{js}
    </script>
</body>
</html>
"""

    def _extract_chapters(self, slides: List[Dict[str, Any]]) -> tuple:
        """Extract chapters for both navigation bar and TOC.

        Returns:
            tuple: (nav_chapters, toc_chapters)
                - nav_chapters: Used for bottom progress bar (filtered by chapter_level)
                - toc_chapters: Used for TOC panel (all heading levels 1-5)
        """
        nav_chapters = []  # Progress bar chapters (filtered by chapter_level)
        toc_chapters = []  # TOC chapters (all levels 1-5)
        seen_nav_titles = set()
        seen_toc_titles = set()

        for i, slide in enumerate(slides):
            slide_num = i + 1

            # Skip title slide
            if slide.get('is_title_slide'):
                continue

            # Extract ALL headings from this slide's raw lines
            raw_lines = slide.get('raw_lines', [])

            for line in raw_lines:
                stripped = line.strip()
                heading_level = None
                heading_text = None

                # Detect heading level and extract text
                if stripped.startswith('# ') and not stripped.startswith('##'):
                    heading_level = 1
                    heading_text = stripped[2:].strip()
                elif stripped.startswith('## ') and not stripped.startswith('###'):
                    heading_level = 2
                    heading_text = stripped[3:].strip()
                elif stripped.startswith('### ') and not stripped.startswith('####'):
                    heading_level = 3
                    heading_text = stripped[4:].strip()
                elif stripped.startswith('#### ') and not stripped.startswith('#####'):
                    heading_level = 4
                    heading_text = stripped[5:].strip()
                elif stripped.startswith('##### ') and not stripped.startswith('######'):
                    heading_level = 5
                    heading_text = stripped[6:].strip()

                # If we found a heading, add it to the appropriate lists
                if heading_level and heading_text:
                    chapter_data = {
                        'title': heading_text,
                        'slide_number': slide_num,
                        'level': heading_level
                    }

                    # 1. TOC: Include all headings level 1-5 (complete outline)
                    if 1 <= heading_level <= 5 and heading_text not in seen_toc_titles:
                        toc_chapters.append(chapter_data.copy())
                        seen_toc_titles.add(heading_text)

                    # 2. Navigation bar: Only include headings <= chapter_level
                    if heading_level <= self.chapter_level and heading_text not in seen_nav_titles:
                        nav_chapters.append(chapter_data.copy())
                        seen_nav_titles.add(heading_text)

        return nav_chapters, toc_chapters

    def _generate_chapter_nav(self, nav_chapters: List[Dict[str, Any]], toc_chapters: List[Dict[str, Any]]) -> str:
        """Generate chapter navigation HTML and TOC panel.

        Args:
            nav_chapters: Chapters for bottom progress bar (filtered by chapter_level)
            toc_chapters: All chapters for TOC panel (levels 1-5)

        Returns:
            str: Combined HTML for both components
        """
        if not nav_chapters and not toc_chapters:
            return ''

        # Generate progress bar navigation (truncated titles, simplified)
        nav_html = ''
        if nav_chapters:
            nav_items = []
            for chapter in nav_chapters:
                title = html.escape(chapter['title'])
                # Truncate long titles for progress bar
                display_title = title[:17] + '...' if len(title) > 20 else title

                nav_items.append(
                    f'        <span class="chapter" data-level="{chapter["level"]}" data-slide="{chapter["slide_number"]}">{display_title}</span>'
                )

            nav_html = '\n        <span class="separator">|</span>\n'.join(nav_items)

        # Generate TOC panel (full titles with complete hierarchy, all levels 1-5)
        toc_content = ''
        if toc_chapters:
            toc_items = []
            for chapter in toc_chapters:
                title = html.escape(chapter['title'])
                level = chapter['level']

                toc_items.append(
                    f'        <div class="toc-item" data-level="{level}" data-slide="{chapter["slide_number"]}">\n'
                    f'            <span class="toc-title">{title}</span>\n'
                    f'        </div>'
                )

            toc_content = '\n'.join(toc_items)

        return f'''    <!-- TOC Icon -->
    <div class="toc-icon" id="tocIcon" title="目录">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
    </div>

    <!-- TOC Panel -->
    <div class="toc-panel" id="tocPanel">
        <div class="toc-header">
            <h3>目录</h3>
            <button class="toc-close" id="tocClose">×</button>
        </div>
        <div class="toc-content">
{toc_content}
        </div>
    </div>

    <!-- Chapter navigation (progress bar) -->
    <div class="chapter-nav">
{nav_html}
    </div>
'''

    def _generate_slides(self, slides: List[Dict[str, Any]]) -> str:
        """Generate HTML for all slides"""
        slides_html = []

        for i, slide in enumerate(slides):
            slide_num = i + 1
            is_active = (i == 0)
            is_title = slide.get('is_title_slide', False)

            # Determine slide class
            slide_class = 'slide'
            if is_title:
                slide_class += ' title-slide'
            if is_active:
                slide_class += ' active'

            # Add chapter attribute for navigation tracking
            original_title = slide.get('original_title', slide.get('title', ''))
            chapter_attr = f' data-chapter="{html.escape(original_title)}"' if original_title else ''

            slides_html.append(f'''        <!-- Slide {slide_num} -->
        <div class="{slide_class}" data-slide="{slide_num}"{chapter_attr}>
{slide['content']}
        </div>
''')

        return '\n'.join(slides_html)

    def _get_css(self) -> str:
        """Get CSS styles based on theme"""
        actual_theme = self.theme_map.get(self.theme, 'tech')

        if actual_theme == 'tech':
            return self._get_tech_css()
        elif actual_theme == 'clean':
            return self._get_clean_css()
        elif actual_theme == 'corporate':
            return self._get_corporate_css()
        else:
            return self._get_tech_css()  # Fallback

    def _get_tech_css(self) -> str:
        """Get tech/cyberpunk theme CSS"""
        return '''        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-tertiary: #1a1a2e;
            --cyan: #00d4ff;
            --magenta: #ff00ff;
            --green: #00ff88;
            --yellow: #ffff00;
            --orange: #ff8800;
            --red: #ff4444;
            --text-primary: #e0e0e0;
            --text-secondary: #888;
            --grid-color: rgba(0, 212, 255, 0.03);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans SC', 'JetBrains Mono', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
        }

        /* Matrix grid background */
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
        }

        /* Scanline effect */
        .scanlines {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 0, 0, 0.1),
                rgba(0, 0, 0, 0.1) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
            z-index: 1000;
            opacity: 0.3;
        }

        /* Presentation container */
        .presentation {
            position: relative;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        /* Individual slides */
        .slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 60px 80px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            opacity: 0;
            visibility: hidden;
            transform: translateX(100px);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            overflow-y: auto;
        }

        .slide.active {
            opacity: 1;
            visibility: visible;
            transform: translateX(0);
        }

        .slide.exit {
            opacity: 0;
            transform: translateX(-100px);
        }

        /* Typography */
        h1 {
            font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
            font-size: 4.4rem;
            font-weight: 700;
            color: var(--cyan);
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
            margin-bottom: 24px;
            letter-spacing: 2px;
        }

        h2 {
            font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
            font-size: 2.75rem;
            font-weight: 600;
            color: var(--cyan);
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
            margin-bottom: 36px;
            padding-bottom: 18px;
            border-bottom: 2px solid var(--cyan);
            display: inline-block;
        }

        h3 {
            font-size: 1.75rem;
            color: var(--magenta);
            margin: 30px 0 18px 0;
            text-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
        }

        h4 {
            font-size: 1.5rem;
            color: var(--green);
            margin: 24px 0 12px 0;
        }

        h5, h6 {
            font-size: 1.3rem;
            color: var(--yellow);
            margin: 20px 0 10px 0;
        }

        p, li {
            font-size: 1.4rem;
            line-height: 1.9;
            color: var(--text-primary);
            margin-bottom: 12px;
        }

        /* Code blocks */
        pre {
            background: var(--bg-secondary);
            border: 1px solid var(--cyan);
            border-radius: 8px;
            padding: 24px;
            margin: 18px 0;
            font-size: 1.2rem;
            overflow-x: auto;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.1),
                        inset 0 0 30px rgba(0, 0, 0, 0.5);
            font-family: 'JetBrains Mono', monospace;
        }

        code {
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-tertiary);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            color: var(--green);
        }

        pre code {
            background: none;
            padding: 0;
            font-size: 1em;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 1.2rem;
        }

        th {
            background: var(--bg-tertiary);
            color: var(--cyan);
            padding: 18px;
            text-align: left;
            border: 1px solid var(--cyan);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 1.1rem;
        }

        td {
            padding: 15px 18px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            background: var(--bg-secondary);
        }

        tr:hover td {
            background: var(--bg-tertiary);
            box-shadow: inset 0 0 20px rgba(0, 212, 255, 0.1);
        }

        /* Lists */
        ul, ol {
            margin: 18px 0 18px 36px;
        }

        li {
            margin: 12px 0;
            position: relative;
        }

        li::marker {
            color: var(--cyan);
        }

        /* Links */
        a {
            color: var(--cyan);
            text-decoration: none;
            text-shadow: 0 0 10px var(--cyan);
            transition: all 0.3s ease;
        }

        a:hover {
            color: var(--magenta);
            text-shadow: 0 0 15px var(--magenta);
        }

        /* Images */
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            border: 2px solid var(--cyan);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
            margin: 18px 0;
        }

        /* Blockquotes */
        blockquote {
            background: var(--bg-secondary);
            border-left: 4px solid var(--cyan);
            padding: 18px 24px;
            margin: 18px 0;
            font-style: italic;
            color: var(--text-secondary);
        }

        /* Horizontal rule */
        hr {
            border: none;
            border-top: 2px solid var(--cyan);
            margin: 36px 0;
            box-shadow: 0 0 10px var(--cyan);
        }

        /* Progress bar */
        .progress-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--bg-secondary);
            z-index: 100;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--cyan), var(--magenta));
            box-shadow: 0 0 20px var(--cyan);
            transition: width 0.3s ease;
        }

        /* Footer - centered bottom, semi-transparent */
        .footer-text {
            position: fixed;
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 0.85rem;
            color: rgba(136, 136, 136, 0.5);
            opacity: 0.5;
            z-index: 50;
            pointer-events: none;
        }

        /* Page number - right bottom corner */
        .page-number {
            position: fixed;
            bottom: 15px;
            right: 20px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            color: var(--cyan);
            background: rgba(18, 18, 26, 0.5);
            padding: 5px 12px;
            border-radius: 15px;
            text-shadow: 0 0 10px var(--cyan);
            z-index: 50;
            pointer-events: none;
            backdrop-filter: blur(5px);
        }

        /* Navigation hints */
        .nav-hint {
            position: fixed;
            bottom: 20px;
            left: 30px;
            font-size: 1.05rem;
            color: var(--text-secondary);
            z-index: 100;
        }

        .nav-hint kbd {
            background: var(--bg-tertiary);
            border: 1px solid var(--cyan);
            border-radius: 4px;
            padding: 4px 10px;
            margin: 0 4px;
        }

        /* Title slide special */
        .slide.title-slide {
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .slide.title-slide h1 {
            font-size: 6.25rem;
            margin-bottom: 36px;
            animation: glowPulse 2s ease-in-out infinite;
        }

        @keyframes glowPulse {
            0%, 100% { text-shadow: 0 0 30px rgba(0, 212, 255, 0.5); }
            50% { text-shadow: 0 0 50px rgba(0, 212, 255, 0.8), 0 0 80px rgba(0, 212, 255, 0.4); }
        }

        /* Fullscreen button */
        .fullscreen-btn {
            position: fixed;
            top: 20px;
            right: 30px;
            background: var(--bg-tertiary);
            border: 1px solid var(--cyan);
            color: var(--cyan);
            padding: 12px 18px;
            border-radius: 4px;
            cursor: pointer;
            font-family: 'Noto Sans SC', 'JetBrains Mono', monospace;
            font-size: 1.05rem;
            z-index: 100;
            transition: all 0.3s ease;
        }

        .fullscreen-btn:hover {
            background: var(--cyan);
            color: var(--bg-primary);
            box-shadow: 0 0 20px var(--cyan);
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .slide {
                padding: 48px;
            }

            h1 {
                font-size: 3.1rem;
            }

            h2 {
                font-size: 2.25rem;
            }
        }

        @media (max-width: 768px) {
            .slide {
                padding: 36px 24px;
            }

            h1 {
                font-size: 2.5rem;
            }

            h2 {
                font-size: 1.9rem;
            }

            table {
                font-size: 1rem;
            }

            th, td {
                padding: 10px;
            }
        }

        /* Single-tier chapter navigation (flattened) */
        .chapter-nav {
            position: fixed;
            bottom: 50px;
            left: 0;
            right: 0;
            text-align: center;
            z-index: 100;
            padding: 10px 20px;
            overflow-x: auto;
            white-space: nowrap;
        }

        .chapter-nav::-webkit-scrollbar {
            height: 4px;
        }

        .chapter-nav::-webkit-scrollbar-thumb {
            background: rgba(0, 217, 255, 0.3);
            border-radius: 2px;
        }

        .chapter-nav .chapter {
            cursor: pointer;
            padding: 6px 12px;
            font-size: 0.9rem;
            font-weight: 400;
            color: #888;
            transition: all 0.3s ease;
            border-radius: 4px;
            white-space: nowrap;
            display: inline-block;
        }

        .chapter-nav .chapter:hover {
            color: var(--cyan);
            text-shadow: 0 0 10px var(--cyan);
        }

        .chapter-nav .chapter.active {
            color: #00D9FF;
            font-weight: 600;
            border-bottom: 2px solid #00D9FF;
            text-shadow: 0 0 15px var(--cyan);
        }

        .chapter-nav .chapter[data-level="1"] {
            font-weight: 500;
        }

        .chapter-nav .chapter[data-level="2"] {
            font-size: 0.85rem;
        }

        .chapter-nav .chapter[data-level="3"] {
            font-size: 0.8rem;
            font-style: italic;
        }

        .chapter-nav .separator {
            color: #444;
            padding: 0 8px;
            display: inline-block;
        }

        /* TOC Icon */
        .toc-icon {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 44px;
            height: 44px;
            background: rgba(18, 18, 26, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid var(--cyan);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 200;
            transition: all 0.3s ease;
            color: #888;
        }

        .toc-icon:hover {
            background: rgba(0, 217, 255, 0.2);
            color: var(--cyan);
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
            transform: scale(1.05);
        }

        /* TOC Panel */
        .toc-panel {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 320px;
            max-height: 80vh;
            background: rgba(18, 18, 26, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid var(--cyan);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 217, 255, 0.2);
            z-index: 200;
            display: none;
            flex-direction: column;
            overflow: hidden;
        }

        .toc-panel.active {
            display: flex;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .toc-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 1px solid rgba(0, 217, 255, 0.3);
        }

        .toc-header h3 {
            margin: 0;
            font-size: 1.1rem;
            color: var(--cyan);
            font-weight: 600;
            text-shadow: 0 0 10px var(--cyan);
        }

        .toc-close {
            background: none;
            border: none;
            color: #888;
            font-size: 1.8rem;
            line-height: 1;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .toc-close:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
        }

        .toc-content {
            flex: 1;
            overflow-y: auto;
            padding: 12px 0;
        }

        .toc-content::-webkit-scrollbar {
            width: 6px;
        }

        .toc-content::-webkit-scrollbar-thumb {
            background: rgba(0, 217, 255, 0.3);
            border-radius: 3px;
        }

        .toc-item {
            display: flex;
            align-items: baseline;
            padding: 10px 20px;
            cursor: pointer;
            transition: all 0.2s;
            color: #aaa;
            border-left: 3px solid transparent;
        }

        .toc-item:hover {
            background: rgba(0, 217, 255, 0.1);
            border-left-color: var(--cyan);
            color: #fff;
        }

        .toc-item.active {
            background: rgba(0, 217, 255, 0.15);
            border-left-color: var(--cyan);
            color: var(--cyan);
            text-shadow: 0 0 10px var(--cyan);
        }

        .toc-item[data-level="1"] {
            padding-left: 20px;
            font-weight: 500;
            font-size: 0.95rem;
        }

        .toc-item[data-level="2"] {
            padding-left: 40px;
            font-size: 0.85rem;
        }

        .toc-item[data-level="3"] {
            padding-left: 60px;
            font-size: 0.8rem;
            font-style: italic;
        }

        .toc-item[data-level="4"] {
            padding-left: 80px;
            font-size: 0.75rem;
            color: #999;
        }

        .toc-item[data-level="5"] {
            padding-left: 100px;
            font-size: 0.7rem;
            color: #888;
            font-style: italic;
        }

        .toc-title {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        @media (max-width: 1024px) {
            .chapter-nav {
                bottom: 45px;
                padding: 8px 16px;
            }

            .chapter-nav .chapter {
                font-size: 0.85rem;
                padding: 5px 10px;
            }

            .toc-panel {
                width: 280px;
            }
        }

        @media (max-width: 768px) {
            .chapter-nav {
                bottom: 40px;
                padding: 6px 12px;
            }

            .chapter-nav .chapter {
                font-size: 0.75rem;
                padding: 4px 8px;
            }

            .footer-text {
                font-size: 0.7rem;
            }

            .page-number {
                font-size: 0.8rem;
                bottom: 10px;
                right: 10px;
            }

            .toc-panel {
                width: calc(100vw - 40px);
                left: 20px;
                right: 20px;
            }

            .toc-icon {
                width: 40px;
                height: 40px;
            }
        }'''

    def _get_clean_css(self) -> str:
        """Get clean/fresh theme CSS"""
        return '''        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --primary: #0066cc;
            --secondary: #00a896;
            --accent: #ff6b6b;
            --text-primary: #2c3e50;
            --text-secondary: #6c757d;
            --border-color: #dee2e6;
            --shadow-light: rgba(0, 0, 0, 0.05);
            --shadow-medium: rgba(0, 0, 0, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans SC', 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
        }

        /* Presentation container */
        .presentation {
            position: relative;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        /* Individual slides */
        .slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 60px 80px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            opacity: 0;
            visibility: hidden;
            transform: translateX(50px);
            transition: all 0.4s ease;
            overflow-y: auto;
            background: var(--bg-primary);
        }

        .slide.active {
            opacity: 1;
            visibility: visible;
            transform: translateX(0);
        }

        .slide.exit {
            opacity: 0;
            transform: translateX(-50px);
        }

        /* Typography */
        h1 {
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 24px;
            letter-spacing: -0.5px;
        }

        h2 {
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 32px;
            padding-bottom: 16px;
            border-bottom: 3px solid var(--secondary);
        }

        h3 {
            font-size: 1.75rem;
            color: var(--secondary);
            margin: 28px 0 16px 0;
            font-weight: 600;
        }

        h4 {
            font-size: 1.4rem;
            color: var(--text-primary);
            margin: 24px 0 12px 0;
            font-weight: 600;
        }

        h5, h6 {
            font-size: 1.2rem;
            color: var(--text-primary);
            margin: 20px 0 10px 0;
            font-weight: 600;
        }

        p, li {
            font-size: 1.3rem;
            line-height: 1.8;
            color: var(--text-primary);
            margin-bottom: 12px;
        }

        /* Code blocks */
        pre {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin: 16px 0;
            font-size: 1.1rem;
            overflow-x: auto;
            font-family: 'Source Code Pro', monospace;
            box-shadow: 0 2px 8px var(--shadow-light);
        }

        code {
            font-family: 'Source Code Pro', monospace;
            background: var(--bg-tertiary);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            color: var(--accent);
        }

        pre code {
            background: none;
            padding: 0;
            font-size: 1em;
            color: var(--text-primary);
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 1.1rem;
            box-shadow: 0 2px 8px var(--shadow-light);
        }

        th {
            background: var(--primary);
            color: white;
            padding: 16px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 14px 16px;
            border: 1px solid var(--border-color);
            background: var(--bg-primary);
        }

        tr:hover td {
            background: var(--bg-secondary);
        }

        /* Lists */
        ul, ol {
            margin: 16px 0 16px 32px;
        }

        li {
            margin: 10px 0;
        }

        li::marker {
            color: var(--secondary);
        }

        /* Links */
        a {
            color: var(--primary);
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }

        a:hover {
            color: var(--secondary);
            border-bottom-color: var(--secondary);
        }

        /* Images */
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px var(--shadow-medium);
            margin: 16px 0;
        }

        /* Blockquotes */
        blockquote {
            background: var(--bg-secondary);
            border-left: 4px solid var(--secondary);
            padding: 16px 20px;
            margin: 16px 0;
            font-style: italic;
            color: var(--text-secondary);
        }

        /* Horizontal rule */
        hr {
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 32px 0;
        }

        /* Progress bar */
        .progress-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--bg-tertiary);
            z-index: 100;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            transition: width 0.3s ease;
        }

        /* Footer - centered bottom, semi-transparent */
        .footer-text {
            position: fixed;
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 0.85rem;
            color: rgba(108, 117, 125, 0.5);
            opacity: 0.5;
            z-index: 50;
            pointer-events: none;
        }

        /* Page number - right bottom corner */
        .page-number {
            position: fixed;
            bottom: 15px;
            right: 20px;
            font-size: 0.9rem;
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.5);
            padding: 5px 12px;
            border-radius: 15px;
            border: 1px solid var(--border-color);
            z-index: 50;
            pointer-events: none;
            box-shadow: 0 2px 8px var(--shadow-light);
        }

        /* Navigation hints */
        .nav-hint {
            position: fixed;
            bottom: 20px;
            left: 30px;
            font-size: 1rem;
            color: var(--text-secondary);
            z-index: 100;
        }

        .nav-hint kbd {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 4px 10px;
            margin: 0 4px;
            font-family: 'Inter', sans-serif;
        }

        /* Title slide special */
        .slide.title-slide {
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .slide.title-slide h1 {
            font-size: 5rem;
            margin-bottom: 32px;
            color: var(--primary);
        }

        /* Fullscreen button */
        .fullscreen-btn {
            position: fixed;
            top: 20px;
            right: 30px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-family: 'Noto Sans SC', 'Inter', sans-serif;
            font-size: 1rem;
            z-index: 100;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px var(--shadow-light);
        }

        .fullscreen-btn:hover {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        /* Single-tier chapter navigation (flattened) */
        .chapter-nav {
            position: fixed;
            bottom: 50px;
            left: 0;
            right: 0;
            text-align: center;
            z-index: 100;
            padding: 10px 20px;
            overflow-x: auto;
            white-space: nowrap;
        }

        .chapter-nav::-webkit-scrollbar {
            height: 4px;
        }

        .chapter-nav::-webkit-scrollbar-thumb {
            background: rgba(0, 102, 204, 0.3);
            border-radius: 2px;
        }

        .chapter-nav .chapter {
            cursor: pointer;
            padding: 6px 12px;
            font-size: 0.9rem;
            font-weight: 400;
            color: #888;
            transition: all 0.3s ease;
            border-radius: 4px;
            white-space: nowrap;
            display: inline-block;
        }

        .chapter-nav .chapter:hover {
            color: var(--primary);
            background: var(--bg-secondary);
        }

        .chapter-nav .chapter.active {
            color: #0066cc;
            font-weight: 600;
            background: var(--bg-secondary);
            border-bottom: 2px solid #0066cc;
        }

        .chapter-nav .chapter[data-level="1"] {
            font-weight: 500;
        }

        .chapter-nav .chapter[data-level="2"] {
            font-size: 0.85rem;
        }

        .chapter-nav .chapter[data-level="3"] {
            font-size: 0.8rem;
            font-style: italic;
        }

        .chapter-nav .separator {
            color: #444;
            padding: 0 8px;
            display: inline-block;
        }

        /* TOC Icon */
        .toc-icon {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 44px;
            height: 44px;
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 200;
            transition: all 0.3s ease;
            color: #888;
            box-shadow: 0 2px 8px var(--shadow-light);
        }

        .toc-icon:hover {
            background: var(--bg-secondary);
            color: var(--primary);
            box-shadow: 0 4px 12px var(--shadow-medium);
            transform: scale(1.05);
        }

        /* TOC Panel */
        .toc-panel {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 320px;
            max-height: 80vh;
            background: white;
            border: 2px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 8px 32px var(--shadow-medium);
            z-index: 200;
            display: none;
            flex-direction: column;
            overflow: hidden;
        }

        .toc-panel.active {
            display: flex;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .toc-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 2px solid var(--border-color);
            background: var(--bg-secondary);
        }

        .toc-header h3 {
            margin: 0;
            font-size: 1.1rem;
            color: var(--primary);
            font-weight: 600;
        }

        .toc-close {
            background: none;
            border: none;
            color: #888;
            font-size: 1.8rem;
            line-height: 1;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .toc-close:hover {
            background: rgba(0, 0, 0, 0.05);
            color: #000;
        }

        .toc-content {
            flex: 1;
            overflow-y: auto;
            padding: 12px 0;
        }

        .toc-content::-webkit-scrollbar {
            width: 6px;
        }

        .toc-content::-webkit-scrollbar-thumb {
            background: rgba(0, 102, 204, 0.3);
            border-radius: 3px;
        }

        .toc-item {
            display: flex;
            align-items: baseline;
            padding: 10px 20px;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text-secondary);
            border-left: 3px solid transparent;
        }

        .toc-item:hover {
            background: var(--bg-secondary);
            border-left-color: var(--primary);
            color: var(--text-primary);
        }

        .toc-item.active {
            background: var(--bg-secondary);
            border-left-color: var(--primary);
            color: var(--primary);
            font-weight: 500;
        }

        .toc-item[data-level="1"] {
            padding-left: 20px;
            font-weight: 500;
            font-size: 0.95rem;
        }

        .toc-item[data-level="2"] {
            padding-left: 40px;
            font-size: 0.85rem;
        }

        .toc-item[data-level="3"] {
            padding-left: 60px;
            font-size: 0.8rem;
            font-style: italic;
        }

        .toc-item[data-level="4"] {
            padding-left: 80px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .toc-item[data-level="5"] {
            padding-left: 100px;
            font-size: 0.7rem;
            color: var(--text-muted);
            opacity: 0.8;
            font-style: italic;
        }

        .toc-title {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .slide { padding: 48px; }
            h1 { font-size: 2.8rem; }
            h2 { font-size: 2rem; }

            .chapter-nav {
                bottom: 45px;
                padding: 8px 16px;
            }

            .chapter-nav .chapter {
                font-size: 0.85rem;
                padding: 5px 10px;
            }

            .toc-panel {
                width: 280px;
            }
        }

        @media (max-width: 768px) {
            .slide { padding: 36px 24px; }
            h1 { font-size: 2.2rem; }
            h2 { font-size: 1.6rem; }
            table { font-size: 1rem; }
            th, td { padding: 10px; }

            .chapter-nav {
                bottom: 40px;
                padding: 6px 12px;
            }

            .chapter-nav .chapter {
                font-size: 0.75rem;
                padding: 4px 8px;
            }

            .footer-text {
                font-size: 0.7rem;
            }

            .page-number {
                font-size: 0.8rem;
                bottom: 10px;
                right: 10px;
            }

            .toc-panel {
                width: calc(100vw - 40px);
                left: 20px;
                right: 20px;
            }

            .toc-icon {
                width: 40px;
                height: 40px;
            }
        }'''

    def _get_corporate_css(self) -> str:
        """Get corporate theme CSS"""
        return '''        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&family=Roboto+Mono:wght@400;500&family=Noto+Sans+SC:wght@300;400;600;700&display=swap');

        :root {
            --bg-primary: #f5f5f5;
            --bg-secondary: #ffffff;
            --bg-tertiary: #e8e8e8;
            --primary: #1a3a5c;
            --secondary: #2e5984;
            --accent: #c0392b;
            --text-primary: #333333;
            --text-secondary: #666666;
            --border-color: #d0d0d0;
            --shadow: rgba(0, 0, 0, 0.15);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans SC', 'Open Sans', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
        }

        /* Presentation container */
        .presentation {
            position: relative;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        /* Individual slides */
        .slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 60px 80px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            opacity: 0;
            visibility: hidden;
            transform: translateX(30px);
            transition: all 0.5s ease;
            overflow-y: auto;
            background: var(--bg-secondary);
        }

        .slide.active {
            opacity: 1;
            visibility: visible;
            transform: translateX(0);
        }

        .slide.exit {
            opacity: 0;
            transform: translateX(-30px);
        }

        /* Typography */
        h1 {
            font-family: 'Open Sans', 'Noto Sans SC', sans-serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        h2 {
            font-family: 'Open Sans', 'Noto Sans SC', sans-serif;
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 32px;
            padding-bottom: 12px;
            border-bottom: 4px solid var(--secondary);
        }

        h3 {
            font-size: 1.8rem;
            color: var(--secondary);
            margin: 28px 0 16px 0;
            font-weight: 600;
        }

        h4 {
            font-size: 1.4rem;
            color: var(--text-primary);
            margin: 24px 0 12px 0;
            font-weight: 600;
        }

        h5, h6 {
            font-size: 1.2rem;
            color: var(--text-primary);
            margin: 20px 0 10px 0;
            font-weight: 600;
        }

        p, li {
            font-size: 1.25rem;
            line-height: 1.7;
            color: var(--text-primary);
            margin-bottom: 12px;
        }

        /* Code blocks */
        pre {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 20px;
            margin: 16px 0;
            font-size: 1.1rem;
            overflow-x: auto;
            font-family: 'Roboto Mono', monospace;
            box-shadow: 0 2px 4px var(--shadow);
        }

        code {
            font-family: 'Roboto Mono', monospace;
            background: var(--bg-tertiary);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
            color: var(--accent);
        }

        pre code {
            background: none;
            padding: 0;
            font-size: 1em;
            color: var(--text-primary);
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 1.1rem;
            box-shadow: 0 2px 8px var(--shadow);
        }

        th {
            background: var(--primary);
            color: white;
            padding: 16px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 1rem;
            letter-spacing: 0.5px;
        }

        td {
            padding: 14px 16px;
            border: 1px solid var(--border-color);
            background: var(--bg-secondary);
        }

        tr:nth-child(even) td {
            background: var(--bg-primary);
        }

        tr:hover td {
            background: var(--bg-tertiary);
        }

        /* Lists */
        ul, ol {
            margin: 16px 0 16px 32px;
        }

        li {
            margin: 10px 0;
        }

        li::marker {
            color: var(--secondary);
        }

        /* Links */
        a {
            color: var(--secondary);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.3s ease;
        }

        a:hover {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }

        /* Images */
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 4px 12px var(--shadow);
            margin: 16px 0;
            border: 1px solid var(--border-color);
        }

        /* Blockquotes */
        blockquote {
            background: var(--bg-tertiary);
            border-left: 5px solid var(--secondary);
            padding: 16px 20px;
            margin: 16px 0;
            font-style: italic;
            color: var(--text-secondary);
        }

        /* Horizontal rule */
        hr {
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 32px 0;
        }

        /* Progress bar */
        .progress-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: var(--bg-tertiary);
            z-index: 100;
        }

        .progress-bar {
            height: 100%;
            background: var(--primary);
            transition: width 0.3s ease;
            box-shadow: 0 0 10px var(--primary);
        }

        /* Footer - centered bottom, semi-transparent */
        .footer-text {
            position: fixed;
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 0.85rem;
            color: rgba(102, 102, 102, 0.5);
            opacity: 0.5;
            z-index: 50;
            pointer-events: none;
        }

        /* Page number - right bottom corner */
        .page-number {
            position: fixed;
            bottom: 15px;
            right: 20px;
            font-size: 0.9rem;
            color: var(--text-secondary);
            background: var(--bg-secondary);
            padding: 5px 12px;
            border-radius: 15px;
            border: 1px solid var(--border-color);
            font-weight: 600;
            z-index: 50;
            pointer-events: none;
            box-shadow: 0 2px 8px var(--shadow);
        }

        /* Navigation hints */
        .nav-hint {
            position: fixed;
            bottom: 20px;
            left: 30px;
            font-size: 1rem;
            color: var(--text-secondary);
            z-index: 100;
        }

        .nav-hint kbd {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 3px;
            padding: 4px 10px;
            margin: 0 4px;
            font-family: 'Open Sans', sans-serif;
            font-weight: 600;
        }

        /* Title slide special */
        .slide.title-slide {
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
        }

        .slide.title-slide h1 {
            font-size: 5rem;
            margin-bottom: 32px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .slide.title-slide p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.5rem;
        }

        /* Fullscreen button */
        .fullscreen-btn {
            position: fixed;
            top: 20px;
            right: 30px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 10px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-family: 'Noto Sans SC', 'Open Sans', sans-serif;
            font-size: 1rem;
            z-index: 100;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px var(--shadow);
            font-weight: 600;
        }

        .fullscreen-btn:hover {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        /* Single-tier chapter navigation (flattened) */
        .chapter-nav {
            position: fixed;
            bottom: 50px;
            left: 0;
            right: 0;
            text-align: center;
            z-index: 100;
            padding: 10px 20px;
            overflow-x: auto;
            white-space: nowrap;
        }

        .chapter-nav::-webkit-scrollbar {
            height: 4px;
        }

        .chapter-nav::-webkit-scrollbar-thumb {
            background: rgba(26, 58, 92, 0.3);
            border-radius: 2px;
        }

        .chapter-nav .chapter {
            cursor: pointer;
            padding: 6px 12px;
            font-size: 0.9rem;
            font-weight: 400;
            color: #888;
            transition: all 0.3s ease;
            border-radius: 4px;
            white-space: nowrap;
            display: inline-block;
            letter-spacing: 0.3px;
        }

        .chapter-nav .chapter:hover {
            color: var(--primary);
            background: var(--bg-tertiary);
        }

        .chapter-nav .chapter.active {
            color: white;
            font-weight: 600;
            background: var(--primary);
            box-shadow: 0 2px 8px var(--shadow);
        }

        .chapter-nav .chapter[data-level="1"] {
            font-weight: 500;
            text-transform: uppercase;
        }

        .chapter-nav .chapter[data-level="2"] {
            font-size: 0.85rem;
        }

        .chapter-nav .chapter[data-level="3"] {
            font-size: 0.8rem;
            font-style: italic;
        }

        .chapter-nav .separator {
            color: #444;
            padding: 0 8px;
            display: inline-block;
        }

        /* TOC Icon */
        .toc-icon {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 44px;
            height: 44px;
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 200;
            transition: all 0.3s ease;
            color: #888;
            box-shadow: 0 2px 8px var(--shadow);
        }

        .toc-icon:hover {
            background: var(--bg-tertiary);
            color: var(--primary);
            box-shadow: 0 4px 12px var(--shadow);
            transform: scale(1.05);
        }

        /* TOC Panel */
        .toc-panel {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 320px;
            max-height: 80vh;
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 4px;
            box-shadow: 0 8px 32px var(--shadow);
            z-index: 200;
            display: none;
            flex-direction: column;
            overflow: hidden;
        }

        .toc-panel.active {
            display: flex;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .toc-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 2px solid var(--border-color);
            background: var(--bg-tertiary);
        }

        .toc-header h3 {
            margin: 0;
            font-size: 1.1rem;
            color: var(--primary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .toc-close {
            background: none;
            border: none;
            color: #888;
            font-size: 1.8rem;
            line-height: 1;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .toc-close:hover {
            background: rgba(0, 0, 0, 0.05);
            color: var(--primary);
        }

        .toc-content {
            flex: 1;
            overflow-y: auto;
            padding: 12px 0;
        }

        .toc-content::-webkit-scrollbar {
            width: 6px;
        }

        .toc-content::-webkit-scrollbar-thumb {
            background: rgba(26, 58, 92, 0.3);
            border-radius: 3px;
        }

        .toc-item {
            display: flex;
            align-items: baseline;
            padding: 10px 20px;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text-secondary);
            border-left: 3px solid transparent;
        }

        .toc-item:hover {
            background: var(--bg-tertiary);
            border-left-color: var(--primary);
            color: var(--text-primary);
        }

        .toc-item.active {
            background: var(--bg-tertiary);
            border-left-color: var(--primary);
            color: var(--primary);
            font-weight: 600;
        }

        .toc-item[data-level="1"] {
            padding-left: 20px;
            font-weight: 500;
            font-size: 0.95rem;
            text-transform: uppercase;
        }

        .toc-item[data-level="2"] {
            padding-left: 40px;
            font-size: 0.85rem;
        }

        .toc-item[data-level="3"] {
            padding-left: 60px;
            font-size: 0.8rem;
            font-style: italic;
        }

        .toc-item[data-level="4"] {
            padding-left: 80px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .toc-item[data-level="5"] {
            padding-left: 100px;
            font-size: 0.7rem;
            color: var(--text-muted);
            opacity: 0.8;
            font-style: italic;
        }

        .toc-title {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .slide { padding: 48px; }
            h1 { font-size: 2.8rem; }
            h2 { font-size: 2rem; }

            .chapter-nav {
                bottom: 45px;
                padding: 8px 16px;
            }

            .chapter-nav .chapter {
                font-size: 0.85rem;
                padding: 5px 10px;
            }

            .toc-panel {
                width: 280px;
            }
        }

        @media (max-width: 768px) {
            .slide { padding: 36px 24px; }
            h1 { font-size: 2.2rem; }
            h2 { font-size: 1.6rem; }
            table { font-size: 1rem; }
            th, td { padding: 10px; }

            .chapter-nav {
                bottom: 40px;
                padding: 6px 12px;
            }

            .chapter-nav .chapter {
                font-size: 0.75rem;
                padding: 4px 8px;
            }

            .footer-text {
                font-size: 0.7rem;
            }

            .page-number {
                font-size: 0.8rem;
                bottom: 10px;
                right: 10px;
            }

            .toc-panel {
                width: calc(100vw - 40px);
                left: 20px;
                right: 20px;
            }

            .toc-icon {
                width: 40px;
                height: 40px;
            }
        }'''

    def _get_js(self, total_slides: int, chapters: List[Dict[str, Any]]) -> str:
        """Get JavaScript for slide navigation with flattened chapters and TOC"""
        # Generate chapters data for JS (flattened structure)
        chapters_js = '[]'

        if chapters:
            chapters_data = [f'{{"title": "{html.escape(ch["title"])}", "slide": {ch["slide_number"]}, "level": {ch["level"]}}}'
                           for ch in chapters]
            chapters_js = '[' + ','.join(chapters_data) + ']'

        return f'''        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        let currentSlide = 1;
        const chapters = {chapters_js};

        // Update chapter navigation highlighting (flattened structure)
        function updateChapterNav(slideNum) {{
            const chapterElements = document.querySelectorAll('.chapter-nav .chapter');
            if (chapterElements.length === 0) return;

            // Find which chapter this slide belongs to
            let activeIndex = -1;
            for (let i = 0; i < chapters.length; i++) {{
                const nextSlide = i + 1 < chapters.length ? chapters[i + 1].slide : Infinity;
                if (slideNum >= chapters[i].slide && slideNum < nextSlide) {{
                    activeIndex = i;
                    break;
                }}
            }}

            // Update active state
            chapterElements.forEach((el, index) => {{
                if (index === activeIndex) {{
                    el.classList.add('active');
                }} else {{
                    el.classList.remove('active');
                }}
            }});
        }}

        // Update TOC active item
        function updateTocActive(slideNum) {{
            const tocItems = document.querySelectorAll('.toc-item');
            if (tocItems.length === 0) return;

            let activeIndex = -1;
            for (let i = 0; i < chapters.length; i++) {{
                const nextSlide = i + 1 < chapters.length ? chapters[i + 1].slide : Infinity;
                if (slideNum >= chapters[i].slide && slideNum < nextSlide) {{
                    activeIndex = i;
                    break;
                }}
            }}

            tocItems.forEach((item, index) => {{
                if (index === activeIndex) {{
                    item.classList.add('active');
                }} else {{
                    item.classList.remove('active');
                }}
            }});
        }}

        // Navigate to specific slide
        function goToSlide(slideNum) {{
            if (slideNum < 1 || slideNum > totalSlides) return;
            updateSlide(slideNum);
        }}

        // Update display
        function updateSlide(newSlide) {{
            if (newSlide < 1 || newSlide > totalSlides) return;

            const current = document.querySelector('.slide.active');
            const next = document.querySelector(`[data-slide="${{newSlide}}"]`);

            if (current) {{
                current.classList.remove('active');
                current.classList.add('exit');
                setTimeout(() => current.classList.remove('exit'), 500);
            }}

            if (next) {{
                next.classList.add('active');
            }}

            currentSlide = newSlide;
            document.getElementById('currentSlide').textContent = currentSlide;
            document.getElementById('progressBar').style.width =
                ((currentSlide / totalSlides) * 100) + '%';

            updateChapterNav(currentSlide);
            updateTocActive(currentSlide);
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            switch(e.key) {{
                case 'ArrowRight':
                case ' ':
                case 'PageDown':
                    e.preventDefault();
                    updateSlide(currentSlide + 1);
                    break;
                case 'ArrowLeft':
                case 'PageUp':
                    e.preventDefault();
                    updateSlide(currentSlide - 1);
                    break;
                case 'Home':
                    e.preventDefault();
                    updateSlide(1);
                    break;
                case 'End':
                    e.preventDefault();
                    updateSlide(totalSlides);
                    break;
                case 'Escape':
                    // Close TOC if open
                    const tocPanel = document.getElementById('tocPanel');
                    if (tocPanel && tocPanel.classList.contains('active')) {{
                        tocPanel.classList.remove('active');
                        document.getElementById('tocIcon').style.display = 'flex';
                    }}
                    break;
            }}
        }});

        // Touch navigation
        let touchStartX = 0;
        let touchEndX = 0;

        document.addEventListener('touchstart', (e) => {{
            touchStartX = e.changedTouches[0].screenX;
        }});

        document.addEventListener('touchend', (e) => {{
            touchEndX = e.changedTouches[0].screenX;
            const diff = touchStartX - touchEndX;
            if (Math.abs(diff) > 50) {{
                if (diff > 0) {{
                    updateSlide(currentSlide + 1);
                }} else {{
                    updateSlide(currentSlide - 1);
                }}
            }}
        }});

        // Fullscreen toggle
        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else {{
                document.exitFullscreen();
            }}
        }}

        // TOC Icon click handler
        const tocIcon = document.getElementById('tocIcon');
        const tocPanel = document.getElementById('tocPanel');
        const tocClose = document.getElementById('tocClose');

        if (tocIcon && tocPanel) {{
            tocIcon.addEventListener('click', () => {{
                tocPanel.classList.add('active');
                tocIcon.style.display = 'none';
            }});
        }}

        if (tocClose && tocPanel) {{
            tocClose.addEventListener('click', () => {{
                tocPanel.classList.remove('active');
                tocIcon.style.display = 'flex';
            }});
        }}

        // Chapter navigation click handlers
        document.querySelectorAll('.chapter-nav .chapter').forEach((chapter) => {{
            chapter.addEventListener('click', () => {{
                const targetSlide = parseInt(chapter.getAttribute('data-slide'));
                if (targetSlide && targetSlide > 0) {{
                    goToSlide(targetSlide);
                }}
            }});
        }});

        // TOC item click handlers
        document.querySelectorAll('.toc-item').forEach((item) => {{
            item.addEventListener('click', () => {{
                const targetSlide = parseInt(item.getAttribute('data-slide'));
                if (targetSlide && targetSlide > 0) {{
                    goToSlide(targetSlide);
                    // Close TOC after navigation
                    tocPanel.classList.remove('active');
                    tocIcon.style.display = 'flex';
                }}
            }});
        }});

        // Initialize
        document.getElementById('totalSlides').textContent = totalSlides;
        updateSlide(1);

        // Render LaTeX math with KaTeX
        function renderMath() {{
            renderMathInElement(document.body, {{
                delimiters: [
                    {{left: "$$", right: "$$", display: true}},
                    {{left: "$", right: "$", display: false}},
                    {{left: "\\\\[", right: "\\\\]", display: true}},
                    {{left: "\\\\(", right: "\\\\)", display: false}}
                ],
                throwOnError: false,
                errorColor: '#cc0000',
                strict: false
            }});
        }}'''


class ResourceManager:
    """Manage resources (images, assets) and output organization"""

    def __init__(self, input_path: str, output_dir: str, preserve_paths: bool = False):
        """
        Args:
            input_path: Path to input Markdown file
            output_dir: Output directory for presentation
            preserve_paths: If True, preserve original image paths without copying
        """
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.assets_dir = self.output_dir / 'assets' / 'images'
        self.copied_images = {}  # Track original -> new path mapping
        self.preserve_paths = preserve_paths

    def setup_directories(self):
        """Create output directory structure"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def process_images_in_slides(self, slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process images in slides and copy local images to assets directory

        Args:
            slides: List of slide dictionaries

        Returns:
            Updated slides with corrected image paths
        """
        for slide in slides:
            slide['content'] = self._process_html_images(slide['content'])
        return slides

    def _process_html_images(self, html_content: str) -> str:
        """Process images in HTML content

        Args:
            html_content: HTML content with img tags

        Returns:
            HTML content with updated image paths
        """
        # Pattern to find img tags
        img_pattern = r'<img\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*?)>'

        def replace_img(match):
            before_src = match.group(1)
            src = match.group(2)
            after_src = match.group(3)

            # Skip if already processed or is a URL
            if src.startswith(('http://', 'https://', 'data:')):
                return match.group(0)

            # Handle relative paths
            src_path = self.input_path.parent / src
            if src_path.exists():
                # Process image (copy or preserve path)
                new_path = self._copy_image(src_path)
                if new_path:
                    return f'<img {before_src}src="{new_path}"{after_src}>'

            return match.group(0)

        return re.sub(img_pattern, replace_img, html_content)

    def _copy_image(self, image_path: Path) -> Optional[str]:
        """Copy image to assets directory or preserve original path

        Args:
            image_path: Path to source image

        Returns:
            Relative path to image (copied or original), or None if processing failed
        """
        try:
            # If preserve_paths is True, return original relative path
            if self.preserve_paths:
                # Calculate relative path from Markdown file to image
                try:
                    rel_path = image_path.relative_to(self.input_path.parent)
                    return str(rel_path)
                except ValueError:
                    # If image is not relative to Markdown file (e.g., absolute path)
                    # Return the path as-is
                    return str(image_path)

            # Check if already copied
            image_key = str(image_path)
            if image_key in self.copied_images:
                return self.copied_images[image_key]

            # Create unique filename if needed
            dest_path = self.assets_dir / image_path.name
            counter = 1
            while dest_path.exists():
                stem = image_path.stem
                suffix = image_path.suffix
                dest_path = self.assets_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            # Copy file
            shutil.copy2(image_path, dest_path)

            # Calculate relative path from HTML file
            rel_path = f"assets/images/{dest_path.name}"
            self.copied_images[image_key] = rel_path

            return rel_path

        except Exception as e:
            print(f"Warning: Failed to process image {image_path}: {e}")
            return None

    def create_readme(self):
        """Create README.txt with usage instructions"""
        readme_path = self.output_dir / 'README.txt'
        content = """HTML Presentation
==================

This presentation was generated from Markdown using SlideDown

Usage:
------
1. Open presentation.html in a web browser
2. Use arrow keys (← →) or spacebar to navigate
3. Press F11 for fullscreen mode

Navigation:
-----------
- → or Space: Next slide
- ← : Previous slide
- Home: First slide
- End: Last slide

Files:
------
- presentation.html: Main presentation file
- assets/images/: Image resources

Tips:
-----
- Works best in modern browsers (Chrome, Firefox, Safari, Edge)
- Can be hosted on a web server or used locally
- All resources are self-contained in this directory
"""
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)


def convert_file(input_path: str, output_path: str = None,
                theme: str = 'tech',
                split_level: int = 2,
                footer: Optional[str] = None,
                max_content_length: int = 800,
                max_elements: int = 15,
                show_page_numbers: bool = False,
                enable_chapter_nav: bool = True,
                chapter_level: int = 3,
                viewport_height: Optional[int] = None,
                content_threshold: float = 0.8,
                preserve_image_paths: bool = False) -> bool:
    """Convert a single Markdown file to HTML presentation

    Args:
        input_path: Path to input Markdown file
        output_path: Output directory (optional, defaults to markdown file's directory)
        theme: Theme name (tech/cyberpunk, clean/fresh, corporate)
        split_level: Heading level for slide splitting
        footer: Optional footer text
        no_date: Don't add date suffix to output folder
        max_content_length: Maximum content length per slide in characters
        max_elements: Maximum number of elements per slide
        show_page_numbers: Show page numbers in titles
        enable_chapter_nav: Enable chapter navigation bar
        chapter_level: Heading level to use for chapters (1-6)
        viewport_height: Viewport height in pixels (None = auto-detect)
        content_threshold: Content threshold as fraction of viewport height
        preserve_image_paths: If True, preserve original image paths without copying

    Returns:
        True if successful, False otherwise
    """
    try:
        input_file = Path(input_path)
        print(f"Converting: {input_path}")

        # Determine output directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        folder_name = f"{input_file.stem}_{timestamp}"

        if output_path is None:
            # Default: markdown file's directory
            base_dir = input_file.parent
        else:
            # User-specified output directory
            base_dir = Path(output_path)

        output_dir = base_dir / folder_name
        html_output_path = output_dir / 'presentation.html'

        print(f"  Output directory: {output_dir}")

        # Setup resource manager
        resource_mgr = ResourceManager(input_path, output_dir, preserve_paths=preserve_image_paths)
        resource_mgr.setup_directories()

        # Parse Markdown
        parser = MarkdownSlideParser(
            split_level=split_level,
            max_content_length=max_content_length,
            max_elements=max_elements,
            show_page_numbers=show_page_numbers,
            viewport_height=viewport_height,
            content_threshold=content_threshold
        )
        slides = parser.parse_file(input_path)

        if not slides:
            print(f"Warning: No content found in {input_path}")
            return False

        print(f"  Parsed {len(slides)} slides")

        # Process images in slides
        slides = resource_mgr.process_images_in_slides(slides)

        # Extract title from filename or first slide
        title = input_file.stem
        if slides and slides[0].get('title'):
            title = slides[0]['title']

        # Render to HTML
        renderer = HTMLPresentationRenderer(
            theme=theme,
            footer=footer,
            enable_chapter_nav=enable_chapter_nav,
            chapter_level=chapter_level
        )
        renderer.render(slides, html_output_path, title=title)

        # Create README
        resource_mgr.create_readme()

        print(f"  Success!")
        print(f"  HTML: {html_output_path}")
        print(f"  Assets: {resource_mgr.assets_dir}")
        return True

    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Convert Markdown documents to HTML presentations with multiple themes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Convert with auto-generated output directory (includes timestamp)
  python slidedown.py document.md

  # Convert with specific theme
  python slidedown.py document.md --theme clean

  # Convert with custom footer
  python slidedown.py document.md --theme corporate --footer "© 2026 Devonn"

  # Convert with custom split level (H1 creates new slides)
  python slidedown.py document.md --split-level 1

  # Smart pagination with custom content length
  python slidedown.py document.md --max-content-length 600 --max-elements 12

  # Show page numbers for split slides
  python slidedown.py document.md --show-page-numbers

  # Disable chapter navigation
  python slidedown.py document.md --no-chapter-nav

  # Use H2 headings for chapter navigation
  python slidedown.py document.md --chapter-level 2

  # Specify custom output base directory (timestamped folder created inside)
  python slidedown.py document.md --output /tmp

Available Themes:
  tech, cyberpunk    - Dark cyberpunk theme with neon colors and grid effects
  clean, fresh       - Light, clean theme suitable for long reading
  corporate          - Professional business theme with formal styling

Smart Pagination:
  Automatically splits long slides into multiple pages
  Preserves code blocks and tables (won't split them)
  Configurable via --max-content-length and --max-elements

Chapter Navigation:
  Bottom navigation bar showing all major chapters
  Click to jump between chapters
  Current chapter is highlighted
  Configurable via --chapter-level (default: H2)

Navigation:
  Use arrow keys (← →) or spacebar to navigate slides
  Click chapter names to jump between sections
  Press F11 for fullscreen mode
        '''
    )

    parser.add_argument(
        'input',
        help='Input Markdown file path'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output base directory (default: same as markdown file). A timestamped folder will be created here.'
    )

    parser.add_argument(
        '--theme', '-t',
        default='tech',
        choices=['tech', 'cyberpunk', 'clean', 'fresh', 'corporate'],
        help='Presentation theme (default: tech)'
    )

    parser.add_argument(
        '--footer', '-f',
        help='Custom footer text (e.g., copyright notice, confidential warning)'
    )

    parser.add_argument(
        '--split-level', '-s',
        type=int,
        default=2,
        choices=[1, 2, 3, 4, 5, 6],
        help='Heading level for slide splitting (default: 2 = H2)'
    )


    parser.add_argument(
        '--max-content-length',
        type=int,
        default=800,
        help='Maximum content length per slide in characters (default: 800)'
    )

    parser.add_argument(
        '--max-elements',
        type=int,
        default=15,
        help='Maximum number of elements per slide (default: 15)'
    )

    parser.add_argument(
        '--show-page-numbers',
        action='store_true',
        help='Show page numbers in titles (e.g., "Title (1/3)")'
    )

    parser.add_argument(
        '--chapter-nav',
        action='store_true',
        default=True,
        help='Enable chapter navigation bar (default: enabled)'
    )

    parser.add_argument(
        '--no-chapter-nav',
        action='store_true',
        help='Disable chapter navigation bar'
    )

    parser.add_argument(
        '--chapter-level',
        type=int,
        default=2,
        choices=[1, 2, 3, 4, 5, 6],
        help='Heading level to use for chapters (default: 2 = H2)'
    )

    parser.add_argument(
        '--viewport-height',
        type=int,
        help='Viewport height in pixels for pagination (default: auto-detect, 900px)'
    )

    parser.add_argument(
        '--content-threshold',
        type=float,
        default=0.8,
        help='Content threshold as fraction of viewport height (default: 0.8 = 80%%)'
    )

    parser.add_argument(
        '--preserve-image-paths',
        '--no-copy-images',
        action='store_true',
        dest='preserve_image_paths',
        help='Preserve original image paths from Markdown without copying to assets directory. '
             'Useful when the HTML file will be placed in the same directory as the Markdown file. '
             'Default: False (images are copied to assets/)'
    )

    args = parser.parse_args()

    # Handle chapter nav flag
    enable_chapter_nav = args.chapter_nav and not args.no_chapter_nav

    # Display banner
    print("=" * 60)
    print("Markdown to HTML Presentation Converter")
    print("=" * 60)

    # Convert
    success = convert_file(
        args.input,
        args.output,
        theme=args.theme,
        split_level=args.split_level,
        footer=args.footer,
        max_content_length=args.max_content_length,
        max_elements=args.max_elements,
        show_page_numbers=args.show_page_numbers,
        enable_chapter_nav=enable_chapter_nav,
        chapter_level=args.chapter_level,
        viewport_height=args.viewport_height,
        content_threshold=args.content_threshold,
        preserve_image_paths=args.preserve_image_paths
    )

    if success:
        print("=" * 60)
        print("Conversion completed successfully!")
        print("=" * 60)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
