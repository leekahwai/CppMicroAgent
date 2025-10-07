"""
CppMicroAgent Source Package
============================

This package contains the core modules and utilities for the C++ Micro Agent
coverage improvement system.

Core Modules:
- ConfigReader: Configuration file parsing and management
- OutputManager: Output generation and management
- Query: Project query and analysis utilities
- CoverageImprovementEngine: Advanced coverage analysis and improvement
- OllamaClient: AI integration for code generation
- CodeWriter: Code generation and file management
- flow_manager: Workflow orchestration and management

Sub-packages:
- advanced_coverage_workflow: Advanced coverage improvement state machines and workflows
- quick_test_generator: Direct test generation and analysis scripts

Main Entry Point:
- Use quick_start.sh for interactive access to all features
"""

__version__ = "2.0.0"
__author__ = "CppMicroAgent Team"
__description__ = "Advanced C++ Coverage Improvement System"

# Core module imports for easy access
from .ConfigReader import ConfigReader
from .OutputManager import OutputManager
from .Query import Query

__all__ = [
    'ConfigReader',
    'OutputManager',
    'Query',
    'CoverageImprovementEngine',
    'OllamaClient',
    'CodeWriter',
    'flow_manager'
]