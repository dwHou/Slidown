"""Markdown parsing utilities"""

import re
import mistune
from typing import List, Dict, Any, Optional
from pathlib import Path


class MarkdownParser:
    """Parse Markdown content into structured data"""

    def __init__(self, split_level: int = 2):
        """Initialize parser

        Args:
            split_level: Heading level for slide splitting (1-6)
        """
        self.split_level = max(1, min(6, split_level))
        self.markdown = mistune.create_markdown(
            renderer='ast',
            plugins=['strikethrough', 'table', 'url']
        )

    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Parse Markdown file

        Args:
            filepath: Path to Markdown file

        Returns:
            List of slide dictionaries
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse(content, base_path=Path(filepath).parent)

    def parse(self, content: str, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Parse Markdown content

        Args:
            content: Markdown content string
            base_path: Base path for resolving relative image paths

        Returns:
            List of slide dictionaries
        """
        # Parse to AST
        ast = self.markdown(content)

        # Split into slides
        slides = self._split_into_slides(ast, base_path)

        return slides

    def _split_into_slides(self, ast: List[Dict], base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Split AST into slides based on heading levels

        Args:
            ast: Mistune AST
            base_path: Base path for resolving relative paths

        Returns:
            List of slide dictionaries
        """
        slides = []
        current_slide = None

        for node in ast:
            node_type = node.get('type')

            # Check if this is a split heading
            if node_type == 'heading' and node.get('level', 0) <= self.split_level:
                # Save previous slide if exists
                if current_slide:
                    slides.append(current_slide)

                # Start new slide
                current_slide = {
                    'title': self._extract_text(node),
                    'level': node.get('level', 1),
                    'content': []
                }
            else:
                # Add to current slide
                if current_slide is None:
                    # Create first slide if no heading found
                    current_slide = {
                        'title': 'Untitled',
                        'level': 1,
                        'content': []
                    }

                current_slide['content'].append(
                    self._process_node(node, base_path)
                )

        # Add last slide
        if current_slide:
            slides.append(current_slide)

        return slides

    def _process_node(self, node: Dict, base_path: Optional[Path] = None) -> Dict[str, Any]:
        """Process a single AST node

        Args:
            node: AST node
            base_path: Base path for resolving relative paths

        Returns:
            Processed node dictionary
        """
        node_type = node.get('type')

        if node_type == 'heading':
            return {
                'type': 'heading',
                'level': node.get('level', 1),
                'text': self._extract_text(node)
            }

        elif node_type == 'paragraph':
            return {
                'type': 'paragraph',
                'text': self._extract_text(node),
                'inline_elements': self._extract_inline_elements(node)
            }

        elif node_type == 'list':
            return {
                'type': 'list',
                'ordered': node.get('ordered', False),
                'items': [self._extract_text(item) for item in node.get('children', [])]
            }

        elif node_type == 'block_code':
            return {
                'type': 'code',
                'language': node.get('info', '').strip(),
                'code': node.get('raw', '')
            }

        elif node_type == 'block_quote':
            return {
                'type': 'quote',
                'text': self._extract_text(node)
            }

        elif node_type == 'image':
            img_path = node.get('src', '')
            if base_path and not img_path.startswith(('http://', 'https://', '/')):
                img_path = str(base_path / img_path)

            return {
                'type': 'image',
                'src': img_path,
                'alt': node.get('alt', '')
            }

        elif node_type == 'table':
            return {
                'type': 'table',
                'header': [self._extract_text(cell) for cell in node.get('header', [])],
                'rows': [
                    [self._extract_text(cell) for cell in row]
                    for row in node.get('children', [])
                ]
            }

        elif node_type == 'thematic_break':
            return {
                'type': 'separator'
            }

        else:
            # Default: treat as text
            return {
                'type': 'text',
                'text': self._extract_text(node)
            }

    def _extract_text(self, node: Dict) -> str:
        """Extract plain text from node

        Args:
            node: AST node

        Returns:
            Plain text string
        """
        if isinstance(node, str):
            return node

        node_type = node.get('type')

        if node_type == 'text':
            return node.get('raw', '')

        elif node_type in ['strong', 'em', 'codespan', 'strikethrough']:
            children = node.get('children', [])
            return ''.join(self._extract_text(child) for child in children)

        elif node_type == 'link':
            children = node.get('children', [])
            return ''.join(self._extract_text(child) for child in children)

        elif node_type == 'image':
            return node.get('alt', '')

        elif 'children' in node:
            children = node.get('children', [])
            return ''.join(self._extract_text(child) for child in children)

        return ''

    def _extract_inline_elements(self, node: Dict) -> List[Dict[str, Any]]:
        """Extract inline formatting elements

        Args:
            node: AST node

        Returns:
            List of inline element dictionaries
        """
        elements = []

        def process_children(children):
            for child in children:
                if isinstance(child, str):
                    elements.append({'type': 'text', 'text': child})
                    continue

                child_type = child.get('type')

                if child_type == 'text':
                    elements.append({
                        'type': 'text',
                        'text': child.get('raw', '')
                    })

                elif child_type == 'strong':
                    elements.append({
                        'type': 'bold',
                        'text': self._extract_text(child)
                    })

                elif child_type == 'em':
                    elements.append({
                        'type': 'italic',
                        'text': self._extract_text(child)
                    })

                elif child_type == 'codespan':
                    elements.append({
                        'type': 'code',
                        'text': self._extract_text(child)
                    })

                elif child_type == 'strikethrough':
                    elements.append({
                        'type': 'strikethrough',
                        'text': self._extract_text(child)
                    })

                elif child_type == 'link':
                    elements.append({
                        'type': 'link',
                        'text': self._extract_text(child),
                        'url': child.get('link', '')
                    })

                elif 'children' in child:
                    process_children(child.get('children', []))

        if 'children' in node:
            process_children(node.get('children', []))

        return elements
