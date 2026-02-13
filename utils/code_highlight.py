"""Code syntax highlighting utilities"""

from typing import List, Tuple
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


class CodeHighlighter:
    """Handles syntax highlighting for code blocks"""

    # Language aliases
    LANGUAGE_ALIASES = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'cpp': 'c++',
        'cxx': 'c++',
        'c++': 'cpp',
        'cs': 'csharp',
        'sh': 'bash',
        'shell': 'bash',
        'yml': 'yaml',
        'md': 'markdown',
        'rb': 'ruby',
        'rs': 'rust',
        'go': 'go',
    }

    # Color scheme for syntax highlighting
    SYNTAX_COLORS = {
        'keyword': RGBColor(0, 0, 255),       # Blue
        'string': RGBColor(163, 21, 21),      # Red
        'comment': RGBColor(0, 128, 0),       # Green
        'number': RGBColor(9, 134, 88),       # Teal
        'function': RGBColor(121, 93, 163),   # Purple
        'class': RGBColor(43, 145, 175),      # Cyan
        'operator': RGBColor(0, 0, 0),        # Black
        'default': RGBColor(51, 51, 51),      # Dark gray
    }

    def __init__(self, enable_highlight: bool = True):
        """Initialize code highlighter

        Args:
            enable_highlight: Whether to enable syntax highlighting
        """
        self.enable_highlight = enable_highlight

    def normalize_language(self, language: str) -> str:
        """Normalize language name

        Args:
            language: Original language name

        Returns:
            Normalized language name
        """
        lang = language.lower().strip()
        return self.LANGUAGE_ALIASES.get(lang, lang)

    def get_lexer(self, code: str, language: str = None):
        """Get appropriate lexer for code

        Args:
            code: Code content
            language: Programming language

        Returns:
            Pygments lexer
        """
        if language:
            try:
                lang = self.normalize_language(language)
                return get_lexer_by_name(lang)
            except:
                pass

        # Try to guess the language
        try:
            return guess_lexer(code)
        except:
            return TextLexer()

    def tokenize_code(self, code: str, language: str = None) -> List[Tuple[str, str]]:
        """Tokenize code into (token_type, text) pairs

        Args:
            code: Code content
            language: Programming language

        Returns:
            List of (token_type, text) tuples
        """
        if not self.enable_highlight:
            return [('default', code)]

        lexer = self.get_lexer(code, language)
        tokens = []

        for token_type, text in lexer.get_tokens(code):
            token_name = str(token_type).split('.')[-1].lower()
            tokens.append((token_name, text))

        return tokens

    def get_token_color(self, token_type: str) -> RGBColor:
        """Get color for token type

        Args:
            token_type: Type of token

        Returns:
            RGB color for token
        """
        # Map token types to color categories
        token_type = token_type.lower()

        if 'keyword' in token_type:
            return self.SYNTAX_COLORS['keyword']
        elif 'string' in token_type or 'text' in token_type:
            return self.SYNTAX_COLORS['string']
        elif 'comment' in token_type:
            return self.SYNTAX_COLORS['comment']
        elif 'number' in token_type or 'literal' in token_type:
            return self.SYNTAX_COLORS['number']
        elif 'function' in token_type or 'name.function' in token_type:
            return self.SYNTAX_COLORS['function']
        elif 'class' in token_type or 'name.class' in token_type:
            return self.SYNTAX_COLORS['class']
        elif 'operator' in token_type:
            return self.SYNTAX_COLORS['operator']
        else:
            return self.SYNTAX_COLORS['default']

    def apply_highlighting(self, paragraph, tokens: List[Tuple[str, str]]):
        """Apply syntax highlighting to paragraph

        Args:
            paragraph: PPT paragraph object
            tokens: List of (token_type, text) tuples
        """
        for token_type, text in tokens:
            run = paragraph.add_run()
            run.text = text
            run.font.color.rgb = self.get_token_color(token_type)
            run.font.name = 'Courier New'

    def format_code_block(self, code: str, language: str = None,
                         max_lines: int = 20) -> List[str]:
        """Format code block, splitting if necessary

        Args:
            code: Code content
            language: Programming language
            max_lines: Maximum lines per slide

        Returns:
            List of code chunks
        """
        lines = code.split('\n')

        if len(lines) <= max_lines:
            return [code]

        # Split into chunks
        chunks = []
        for i in range(0, len(lines), max_lines):
            chunk = '\n'.join(lines[i:i + max_lines])
            chunks.append(chunk)

        return chunks
