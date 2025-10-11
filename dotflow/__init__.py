"""
DotFlow - A Python-based DOT language interpreter with multiple API styles.
"""

from .core.interpreter import DotInterpreter, Flow
from .core.themes import Theme
from .api.pythonic import PythonicAPI
from .api.natural import NaturalLanguageAPI
from .api.dsl import TextualDSL

try:
    from .cli import cli
except ImportError:
    cli = None

__version__ = "0.1.0"
__all__ = [
    "DotInterpreter",
    "Flow",
    "Theme",
    "PythonicAPI",
    "NaturalLanguageAPI",
    "TextualDSL",
    "create_flow",
    "cli",
]


# Convenience function
def create_flow(name: str = "flow", theme: Theme = Theme.DEFAULT) -> "DotInterpreter":
    """Create a new flow diagram."""
    return DotInterpreter(name, theme)
