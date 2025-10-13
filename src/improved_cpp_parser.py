#!/usr/bin/env python3
"""
Improved C++ Parser with Better Constructor Detection

Key Improvements:
1. Better constructor parameter parsing
2. Detects all constructor overloads
3. Tracks constructor accessibility
4. Better handling of default parameters
5. Improved method signature parsing
6. Better template handling
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field


@dataclass
class ConstructorInfo:
    """Information about a constructor"""
    parameters: List[Tuple[str, str]]  # [(type, name), ...]
    access: str  # public, protected, private
    is_default: bool  # True if no parameters
    is_copy: bool  # True if copy constructor
    is_move: bool  # True if move constructor
    has_default_params: bool  # True if has default parameter values
    is_explicit: bool  # True if marked explicit
    is_deleted: bool  # True if = delete
    is_defaulted: bool  # True if = default


def enhance_class_info(class_info, class_body: str):
    """Enhance ClassInfo with better constructor detection"""
    
    # Track all constructors
    constructors = []
    
    # Default access for class vs struct
    current_access = "public" if class_info.is_struct else "private"
    
    # Split by access specifiers
    parts = re.split(r'\b(public|protected|private)\s*:', class_body)
    
    for i in range(0, len(parts)):
        if i > 0 and parts[i-1] in ['public', 'protected', 'private']:
            current_access = parts[i-1]
        
        section = parts[i]
        
        # Find constructors - pattern for ClassName(params)
        # Handle explicit, default, delete, etc.
        ctor_pattern = rf'\b(explicit\s+)?({class_info.name})\s*\(([^)]*)\)\s*(=\s*(default|delete))?'
        
        for match in re.finditer(ctor_pattern, section):
            is_explicit = bool(match.group(1))
            params_str = match.group(3).strip()
            modifier = match.group(5)  # default or delete
            
            is_deleted = (modifier == 'delete')
            is_defaulted = (modifier == 'default')
            
            # Skip deleted constructors
            if is_deleted:
                continue
            
            # Parse parameters
            parameters = parse_parameters(params_str)
            
            # Determine constructor type
            is_default_ctor = len(parameters) == 0
            is_copy_ctor = False
            is_move_ctor = False
            has_default_params = '=' in params_str
            
            if len(parameters) == 1:
                param_type = parameters[0][0].strip()
                # Check if copy constructor: ClassName(const ClassName&)
                if f'const {class_info.name}&' in param_type or f'const{class_info.name}&' in param_type:
                    is_copy_ctor = True
                # Check if move constructor: ClassName(ClassName&&)
                elif f'{class_info.name}&&' in param_type:
                    is_move_ctor = True
            
            ctor_info = ConstructorInfo(
                parameters=parameters,
                access=current_access,
                is_default=is_default_ctor,
                is_copy=is_copy_ctor,
                is_move=is_move_ctor,
                has_default_params=has_default_params,
                is_explicit=is_explicit,
                is_deleted=is_deleted,
                is_defaulted=is_defaulted
            )
            
            constructors.append(ctor_info)
            
            # Update has_default_constructor if we found one
            if is_default_ctor or is_defaulted:
                class_info.has_default_constructor = True
    
    # Store constructors (add this to ClassInfo if needed)
    if not hasattr(class_info, 'constructors'):
        class_info.constructors = constructors
    else:
        class_info.constructors.extend(constructors)
    
    return constructors


def parse_parameters(params_str: str) -> List[Tuple[str, str]]:
    """Parse parameter list into (type, name) tuples
    
    Handles:
    - Default parameters: int x = 0
    - Templates: std::vector<int> v
    - Function pointers: void (*callback)(int)
    - References and pointers: const T&, T*, T**
    """
    if not params_str or params_str.strip() == '':
        return []
    
    parameters = []
    
    # Split by comma, but respect template brackets and parentheses
    parts = smart_split(params_str, ',')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Remove default value if present
        if '=' in part:
            part = part.split('=')[0].strip()
        
        # Try to split into type and name
        # Look for the last identifier as the parameter name
        tokens = part.split()
        if not tokens:
            continue
        
        # Handle special cases like "const T&" where there's no name
        if len(tokens) == 1 or (len(tokens) == 2 and tokens[1] in ['&', '*', '&&']):
            # Just a type, no name
            param_type = part
            param_name = ""
        else:
            # Last token is likely the name (unless it's a pointer/reference marker)
            if tokens[-1] in ['&', '*', '&&', 'const']:
                # Type only
                param_type = part
                param_name = ""
            else:
                # Name is last token
                param_name = tokens[-1]
                # Remove array brackets if present
                if '[' in param_name:
                    param_name = param_name.split('[')[0]
                
                # Type is everything else
                param_type = ' '.join(tokens[:-1])
        
        # Clean up type
        param_type = param_type.strip()
        param_name = param_name.strip()
        
        # Filter out invalid names (keywords, operators)
        if param_name in ['const', 'static', 'virtual', 'inline', 'explicit']:
            param_name = ""
        
        parameters.append((param_type, param_name))
    
    return parameters


def smart_split(text: str, delimiter: str) -> List[str]:
    """Split text by delimiter, respecting brackets and parentheses"""
    parts = []
    current = []
    depth = 0
    paren_depth = 0
    
    for char in text:
        if char in '<(':
            depth += 1 if char == '<' else 0
            paren_depth += 1 if char == '(' else 0
            current.append(char)
        elif char in '>)':
            depth -= 1 if char == '>' else 0
            paren_depth -= 1 if char == ')' else 0
            current.append(char)
        elif char == delimiter and depth == 0 and paren_depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(char)
    
    if current:
        parts.append(''.join(current))
    
    return parts


def find_usable_constructors(class_info) -> List[ConstructorInfo]:
    """Find constructors that can be used for testing
    
    Returns constructors sorted by preference:
    1. Default constructor
    2. Constructors with default parameters
    3. Constructors with fewest parameters
    """
    if not hasattr(class_info, 'constructors'):
        return []
    
    usable = []
    
    for ctor in class_info.constructors:
        # Skip non-public constructors
        if ctor.access != 'public':
            continue
        
        # Skip deleted constructors
        if ctor.is_deleted:
            continue
        
        # Skip constructors with too many parameters (>5)
        if len(ctor.parameters) > 5:
            continue
        
        usable.append(ctor)
    
    # Sort by preference
    def sort_key(ctor):
        if ctor.is_default:
            return (0, 0)  # Highest priority
        elif ctor.has_default_params:
            return (1, len(ctor.parameters))  # Second priority, fewer params better
        else:
            return (2, len(ctor.parameters))  # Lowest priority
    
    usable.sort(key=sort_key)
    
    return usable


def improve_method_detection(class_body: str, class_info) -> List[dict]:
    """Improved method detection with better patterns
    
    Returns list of method dicts with:
    - name, return_type, parameters, access, modifiers
    """
    methods = []
    
    # Default access
    current_access = "public" if class_info.is_struct else "private"
    
    # Split by access specifiers
    parts = re.split(r'\b(public|protected|private)\s*:', class_body)
    
    for i in range(0, len(parts)):
        if i > 0 and parts[i-1] in ['public', 'protected', 'private']:
            current_access = parts[i-1]
        
        section = parts[i]
        
        # Enhanced method pattern that handles more cases
        # Captures: modifiers, return type, method name, parameters, const, trailing return, pure virtual
        method_pattern = r'''
            (?:^|;|\})\s*                                    # Start of declaration
            ((?:virtual|static|explicit|inline|constexpr)\s+)*  # Modifiers
            ([\w:]+(?:<[^>]+>)?(?:\s*[*&])?|auto)\s+         # Return type (with templates)
            ([\w]+)\s*                                        # Method name
            \(([^)]*)\)                                       # Parameters
            \s*(const)?\s*                                    # Const qualifier
            (?:->\s*[\w:]+(?:<[^>]+>)?(?:\s*[*&])?)?         # Trailing return type
            \s*(?:=\s*0)?                                     # Pure virtual
            \s*(?:override)?                                  # Override
            \s*(?:final)?                                     # Final
            \s*(?:=\s*(?:default|delete))?                   # Default/delete
        '''
        
        for match in re.finditer(method_pattern, section, re.VERBOSE | re.MULTILINE):
            modifiers = match.group(1) or ""
            return_type = match.group(2).strip()
            method_name = match.group(3)
            params_str = match.group(4)
            is_const = bool(match.group(5))
            
            # Skip operators, keywords, destructors for now
            if method_name.startswith('operator') or method_name.startswith('~'):
                continue
            if method_name in ['if', 'else', 'for', 'while', 'return', 'switch', 'case']:
                continue
            
            # Skip if it looks like a constructor (return type matches class name)
            if return_type == class_info.name:
                continue
            
            # Parse parameters
            parameters = parse_parameters(params_str)
            
            methods.append({
                'name': method_name,
                'return_type': return_type,
                'parameters': parameters,
                'access': current_access,
                'is_const': is_const,
                'is_static': 'static' in modifiers,
                'is_virtual': 'virtual' in modifiers,
                'modifiers': modifiers
            })
    
    return methods
