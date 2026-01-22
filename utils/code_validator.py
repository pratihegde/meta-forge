"""Code validation utilities"""
import ast
import re
from typing import List, Tuple


def validate_python(code: str) -> Tuple[bool, List[str]]:
    """
    Validate Python code syntax
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    try:
        ast.parse(code)
        return True, []
    except SyntaxError as e:
        errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
        return False, errors
    except Exception as e:
        errors.append(f"Validation error: {str(e)}")
        return False, errors


def validate_javascript(code: str) -> Tuple[bool, List[str]]:
    """
    Basic JavaScript validation (syntax patterns)
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    warnings = []
    
    # Check for common syntax errors
    if code.count('{') != code.count('}'):
        errors.append("Mismatched curly braces")
    
    if code.count('(') != code.count(')'):
        errors.append("Mismatched parentheses")
    
    if code.count('[') != code.count(']'):
        errors.append("Mismatched square brackets")
    
    # Check for dangerous patterns
    if re.search(r'\beval\s*\(', code):
        warnings.append("Use of eval() detected - potential security risk")
    
    if re.search(r'innerHTML\s*=', code):
        warnings.append("Direct innerHTML assignment - potential XSS risk")
    
    return len(errors) == 0, errors + warnings


def validate_html(code: str) -> Tuple[bool, List[str]]:
    """
    Basic HTML validation
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check for basic structure
    if not re.search(r'<!DOCTYPE\s+html>', code, re.IGNORECASE):
        errors.append("Missing DOCTYPE declaration")
    
    if not re.search(r'<html[^>]*>', code, re.IGNORECASE):
        errors.append("Missing <html> tag")
    
    # Check for balanced tags (simplified)
    opening_tags = re.findall(r'<(\w+)[^>]*>', code)
    closing_tags = re.findall(r'</(\w+)>', code)
    
    # Self-closing tags
    self_closing = {'img', 'br', 'hr', 'input', 'meta', 'link'}
    
    for tag in opening_tags:
        if tag.lower() not in self_closing and tag.lower() not in [t.lower() for t in closing_tags]:
            errors.append(f"Unclosed tag: <{tag}>")
    
    return len(errors) == 0, errors


def validate_code(code: str, language: str) -> Tuple[bool, List[str]]:
    """
    Validate code based on language
    Returns: (is_valid, list_of_errors)
    """
    language = language.lower()
    
    if language == "python":
        return validate_python(code)
    elif language in ["javascript", "js"]:
        return validate_javascript(code)
    elif language == "html":
        return validate_html(code)
    elif language == "css":
        # Basic CSS validation
        if code.count('{') != code.count('}'):
            return False, ["Mismatched curly braces in CSS"]
        return True, []
    else:
        # Unknown language, skip validation
        return True, []
