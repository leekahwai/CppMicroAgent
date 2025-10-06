"""
CppMicroAgent Source Package
============================

This package contains the core modules and utilities for the C++ Micro Agent
coverage improvement system.

Core Modules:
- CoverageImprovementEngine: Advanced coverage analysis and improvement
- MLCoverageEnhancer: Machine learning enhanced coverage capabilities  
- StateMachine: State management for coverage workflows
- ConfigReader: Configuration file parsing and management
- OutputManager: Output generation and management
- OllamaClient: AI integration for code generation
- CodeWriter: Code generation and file management
- HeaderFileCleaner: C++ header file processing utilities
- flow_manager: Workflow orchestration and management

states_coverage: Advanced coverage improvement state machines and workflows
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
    'MLCoverageEnhancer', 
    'StateMachine',
    'OllamaClient',
    'CodeWriter',
    'HeaderFileCleaner',
    'flow_manager'
]