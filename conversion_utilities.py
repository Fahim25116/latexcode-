#!/usr/bin/env python3
"""
Conversion Utilities Module
============================
Utility functions for LaTeX and Markdown conversion
"""

import re
from typing import List, Dict, Tuple, Optional
from advanced_line_break_handler import AdvancedLineBreakHandler, EquationStructureAnalyzer

class TextProcessor:
    """Utility class for text processing"""

    @staticmethod
    def clean_latex_text(text: str) -> str:
        """Clean LaTeX text by removing commands and formatting"""
        # Remove LaTeX commands
        text = re.sub(r'\\textbf\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\textsf\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+\*?\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+\*?', '', text)

        # Handle spacing and line breaks
        text = re.sub(r'\\\\', '\n', text)
        text = re.sub(r'^\s*%.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        return text.strip()

    @staticmethod
    def extract_math_expressions(text: str) -> List[Dict]:
        """Extract math expressions from text"""
        expressions = []

        # Display math
        display_matches = re.finditer(r'\$\$(.*?)\$\$', text, re.DOTALL)
        for match in display_matches:
            expressions.append({
                'type': 'display',
                'content': match.group(1),
                'position': match.start(),
                'full_match': match.group(0)
            })

        # Inline math
        inline_matches = re.finditer(r'\$([^$]+)\$', text)
        for match in inline_matches:
            expressions.append({
                'type': 'inline',
                'content': match.group(1),
                'position': match.start(),
                'full_match': match.group(0)
            })

        return expressions

    @staticmethod
    def split_by_math(text: str) -> List[Tuple[str, Optional[str]]]:
        """Split text by math expressions"""
        parts = re.split(r'(\$[^\$]+\$)', text)
        result = []

        for part in parts:
            if part.startswith('$') and part.endswith('$') and len(part) > 2:
                result.append(('math', part[1:-1]))
            else:
                result.append(('text', part))

        return result

class FileHandler:
    """Utility class for file operations"""

    @staticmethod
    def read_file(filename: str, encoding: str = 'utf-8') -> str:
        """Read file with error handling"""
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try different encodings
            for enc in ['latin-1', 'cp1252', 'utf-16']:
                try:
                    with open(filename, 'r', encoding=enc) as f:
                        return f.read()
                except:
                    continue
            raise Exception(f"Could not decode file {filename}")

    @staticmethod
    def write_file(filename: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write file with error handling"""
        try:
            with open(filename, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {filename}: {e}")
            return False

    @staticmethod
    def get_file_info(filename: str) -> Dict:
        """Get file information"""
        import os
        from pathlib import Path

        path = Path(filename)
        return {
            'name': path.name,
            'extension': path.suffix,
            'size': path.stat().st_size,
            'exists': path.exists(),
            'is_file': path.is_file()
        }

class ValidationUtils:
    """Utility class for validation"""

    @staticmethod
    def validate_latex_content(content: str) -> Dict:
        """Validate LaTeX content"""
        issues = []
        warnings = []

        # Check for balanced delimiters
        if content.count('\\begin{') != content.count('\\end{'):
            issues.append("Unbalanced \\begin{}\\end{} pairs")

        if content.count('$$') % 2 != 0:
            issues.append("Unbalanced $$ delimiters")

        if content.count('$') % 2 != 0:
            issues.append("Unbalanced $ delimiters")

        # Check for common issues
        if '\\documentclass' in content and '\\begin{document}' not in content:
            warnings.append("Document class found but no document environment")

        if '\\begin{align' in content and '\\\\' not in content:
            warnings.append("Align environment found but no line breaks")

        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }

    @staticmethod
    def validate_markdown_content(content: str) -> Dict:
        """Validate Markdown content"""
        issues = []
        warnings = []

        # Check for balanced math delimiters
        if content.count('$$') % 2 != 0:
            issues.append("Unbalanced $$ delimiters")

        if content.count('$') % 2 != 0:
            issues.append("Unbalanced $ delimiters")

        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }

class ConversionStats:
    """Track conversion statistics"""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset statistics"""
        self.files_processed = 0
        self.equations_converted = 0
        self.errors = 0
        self.warnings = 0
        self.processing_time = 0.0

    def increment_files(self):
        """Increment file count"""
        self.files_processed += 1

    def add_equations(self, count: int):
        """Add equation count"""
        self.equations_converted += count

    def add_error(self):
        """Add error count"""
        self.errors += 1

    def add_warning(self):
        """Add warning count"""
        self.warnings += 1

    def set_processing_time(self, time: float):
        """Set processing time"""
        self.processing_time = time

    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return {
            'files_processed': self.files_processed,
            'equations_converted': self.equations_converted,
            'errors': self.errors,
            'warnings': self.warnings,
            'processing_time': self.processing_time
        }

class DebugUtils:
    """Utility class for debugging"""

    @staticmethod
    def print_content_analysis(content: str):
        """Print content analysis for debugging"""
        print("=== CONTENT ANALYSIS ===")

        # Basic info
        print(f"Length: {len(content)} characters")
        print(f"Lines: {len(content.splitlines())}")

        # Math expressions
        math_exprs = TextProcessor.extract_math_expressions(content)
        print(f"Math expressions: {len(math_exprs)}")

        for expr in math_exprs:
            print(f"  {expr['type']}: {expr['content'][:50]}...")

        # LaTeX structures
        align_count = len(re.findall(r'\\begin\{align', content))
        equation_count = len(re.findall(r'\\begin\{equation', content))
        section_count = len(re.findall(r'\\section', content))

        print(f"Align environments: {align_count}")
        print(f"Equation environments: {equation_count}")
        print(f"Sections: {section_count}")

        # Markdown headers
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        print(f"Markdown headers: {len(headers)}")

        for level, text in headers:
            print(f"  {'#' * len(level)} {text}")

    @staticmethod
    def test_line_break_handler():
        """Test the line break handler"""
        handler = AdvancedLineBreakHandler()

        test_content = """
        x^2 + 5xy + 1 &= 0 \\\\
        5xy &= -x^2 - 1 \\\\
        y &= \\frac{-x^2 - 1}{5x}
        """

        print("=== LINE BREAK HANDLER TEST ===")
        print(f"Input: {test_content.strip()}")

        lines = handler.process_align_environment(test_content)
        print(f"Output: {len(lines)} lines")

        for i, line in enumerate(lines, 1):
            print(f"  Line {i}: {line}")

class PerformanceMonitor:
    """Monitor performance metrics"""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.checkpoints = {}

    def start(self):
        """Start monitoring"""
        import time
        self.start_time = time.time()

    def checkpoint(self, name: str):
        """Add checkpoint"""
        import time
        self.checkpoints[name] = time.time()

    def end(self):
        """End monitoring"""
        import time
        self.end_time = time.time()

    def get_duration(self, start: str = None, end: str = None) -> float:
        """Get duration between points"""
        import time

        start_time = self.start_time if start is None else self.checkpoints.get(start, self.start_time)
        end_time = self.end_time if end is None else self.checkpoints.get(end, self.end_time)

        if start_time and end_time:
            return end_time - start_time
        return 0.0

    def get_checkpoint_duration(self, checkpoint: str) -> float:
        """Get duration from start to checkpoint"""
        return self.get_duration(end=checkpoint)

    def print_report(self):
        """Print performance report"""
        if not self.start_time:
            print("Performance monitoring not started")
            return

        print("=== PERFORMANCE REPORT ===")
        print(f"Total time: {self.get_duration():.2f}s")

        for name, timestamp in self.checkpoints.items():
            duration = timestamp - (self.start_time or 0)
            print(f"{name}: {duration:.2f}s")

        if self.end_time:
            print(f"End: {self.get_duration():.2f}s")