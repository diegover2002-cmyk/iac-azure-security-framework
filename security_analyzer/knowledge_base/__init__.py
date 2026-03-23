"""
Knowledge base modules for the Security Analyzer.

This package contains modules for managing security knowledge:
- mcsb_matrix: Loads and manages MCSB control matrix
- controls: Contains specific control definitions
"""

from .kb_loader import KnowledgeBaseLoader

__all__ = [
    "KnowledgeBaseLoader"
]
