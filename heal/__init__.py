"""
Heal - A Python package for healing shell errors with LLM.

This package provides tools for fixing shell command errors using LLM assistance.
"""

__version__ = "0.1.24"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .main import *
from .cli import main

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "main",
]
