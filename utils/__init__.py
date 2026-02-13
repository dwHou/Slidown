"""Slidown - Transform Markdown into Beautiful HTML Presentations"""

from .parser import MarkdownParser
from .theme import ThemeManager
from .code_highlight import CodeHighlighter

__title__ = 'Slidown'
__version__ = '2.1.2'
__description__ = 'Transform Markdown into beautiful HTML presentations'
__author__ = 'Devonn Hou'

__all__ = ['MarkdownParser', 'ThemeManager', 'CodeHighlighter']
