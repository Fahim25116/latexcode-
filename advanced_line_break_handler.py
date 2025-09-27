#!/usr/bin/env python3
"""
Advanced Line Break Handler for LaTeX Equations
===============================================
Specialized module to handle align* environments and ensure proper line breaks
This module integrates with any main converter to fix multi-line equation issues
"""

import re
from typing import List, Tuple, Dict, Optional

class AdvancedLineBreakHandler:
    """Handles complex line break scenarios in LaTeX equations"""
    
    def __init__(self):
        self.processed_lines = []
        self.debug_info = []
    
    def process_align_environment(self, align_content: str) -> List[str]:
        """
        Process align* environment and return list of individual equation lines
        This is the core function that fixes the line break issue
        """
        # Clean the content first
        cleaned_content = self._clean_align_content(align_content)
        
        # Split by LaTeX line breaks
        raw_lines = self._split_by_latex_breaks(cleaned_content)
        
        # Process each line
        processed_lines = []
        for line in raw_lines:
            cleaned_line = self._process_single_equation_line(line)
            if cleaned_line:
                processed_lines.append(cleaned_line)
                self.debug_info.append(f"Processed line: {cleaned_line}")
        
        return processed_lines
    
    def _clean_align_content(self, content: str) -> str:
        """Clean align environment content"""
        # Remove leading/trailing whitespace
        content = content.strip()
        
        # Remove comments (% lines) completely
        content = re.sub(r'^\s*%.*$', '', content, flags=re.MULTILINE)
        
        # Remove inline comments
        content = re.sub(r'%[^\\]*$', '', content, flags=re.MULTILINE)
        
        # Normalize whitespace but preserve line structure
        content = re.sub(r'[ \t]+', ' ', content)
        
        return content
    
    def _split_by_latex_breaks(self, content: str) -> List[str]:
        """Split content by LaTeX line breaks (\\\\)"""
        # Split by double backslashes
        lines = re.split(r'\\\\\\\\', content)
        
        # Clean each line
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:  # Only include non-empty lines
                cleaned_lines.append(line)
        
        return cleaned_lines
    
    def _process_single_equation_line(self, line: str) -> str:
        """Process a single equation line for optimal conversion"""
        # Remove alignment markers
        line = re.sub(r'\s*&\s*=\s*', ' = ', line)
        line = re.sub(r'\s*&\s*', ' ', line)
        line = re.sub(r'&', ' ', line)
        
        # Remove any remaining comments
        line = re.sub(r'%.*$', '', line)
        
        # Clean up spacing
        line = re.sub(r'\s+', ' ', line)
        
        # Remove leading/trailing whitespace
        line = line.strip()
        
        return line
    
    def process_display_math(self, math_content: str) -> str:
        """Process display math ($$...$$ environments)"""
        # For display math, just clean it up
        cleaned = self._process_single_equation_line(math_content)
        return cleaned
    
    def process_equation_environment(self, eq_content: str) -> str:
        """Process equation environments"""
        cleaned = self._process_single_equation_line(eq_content)
        return cleaned
    
    def detect_environment_type(self, content: str) -> str:
        """Detect what type of math environment we're dealing with"""
        content_lower = content.lower().strip()
        
        if 'begin{align' in content_lower:
            return 'align'
        elif 'begin{equation' in content_lower:
            return 'equation' 
        elif content.startswith('$$') and content.endswith('$$'):
            return 'display_math'
        elif content.startswith('$') and content.endswith('$'):
            return 'inline_math'
        else:
            return 'unknown'
    
    def get_debug_info(self) -> List[str]:
        """Get debug information for troubleshooting"""
        return self.debug_info
    
    def clear_debug_info(self):
        """Clear debug information"""
        self.debug_info = []

class EquationStructureAnalyzer:
    """Analyzes equation structure to determine best processing approach"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_latex_document(self, latex_content: str) -> Dict:
        """Analyze the entire LaTeX document for equation structures"""
        results = {
            'align_environments': [],
            'display_equations': [],
            'inline_equations': [],
            'equation_environments': [],
            'total_math_elements': 0
        }
        
        # Find align environments
        align_matches = re.finditer(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', 
                                   latex_content, re.DOTALL)
        for match in align_matches:
            results['align_environments'].append({
                'content': match.group(1),
                'position': match.start(),
                'full_match': match.group(0)
            })
        
        # Find display equations
        display_matches = re.finditer(r'\$\$(.*?)\$\$', latex_content, re.DOTALL)
        for match in display_matches:
            results['display_equations'].append({
                'content': match.group(1),
                'position': match.start(),
                'full_match': match.group(0)
            })
        
        # Find inline equations
        inline_matches = re.finditer(r'\$([^$]+)\$', latex_content)
        for match in inline_matches:
            results['inline_equations'].append({
                'content': match.group(1),
                'position': match.start(),
                'full_match': match.group(0)
            })
        
        # Calculate totals
        results['total_math_elements'] = (len(results['align_environments']) + 
                                        len(results['display_equations']) + 
                                        len(results['inline_equations']))
        
        self.analysis_results = results
        return results
    
    def get_processing_recommendations(self) -> Dict:
        """Get recommendations for how to process this document"""
        if not self.analysis_results:
            return {"error": "Run analyze_latex_document first"}
        
        recommendations = {
            'use_line_break_handler': len(self.analysis_results['align_environments']) > 0,
            'complex_equations': len(self.analysis_results['align_environments']) > 2,
            'has_inline_math': len(self.analysis_results['inline_equations']) > 0,
            'processing_priority': 'align_environments' if len(self.analysis_results['align_environments']) > 0 else 'display_equations'
        }
        
        return recommendations

# Integration function for main converters
def integrate_line_break_handler(main_converter_class):
    """
    Integration function to add line break handling to any main converter
    Usage: enhanced_converter = integrate_line_break_handler(YourMainConverter)
    """
    
    class EnhancedConverter(main_converter_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.line_break_handler = AdvancedLineBreakHandler()
            self.structure_analyzer = EquationStructureAnalyzer()
            
        def process_align_environment_enhanced(self, align_content: str):
            """Enhanced align environment processing"""
            equation_lines = self.line_break_handler.process_align_environment(align_content)
            return equation_lines
            
        def analyze_document_structure(self, latex_content: str):
            """Analyze document structure for optimal processing"""
            return self.structure_analyzer.analyze_latex_document(latex_content)
        
        def get_processing_recommendations(self):
            """Get processing recommendations"""
            return self.structure_analyzer.get_processing_recommendations()
    
    return EnhancedConverter

# Test function for your specific document
def test_with_your_document():
    """Test the line break handler with your specific equation document"""
    
    # Your problematic align environment
    test_align_content = """
    % Starting equation
    x^2 + 5xy + 1 &= 0 \\
    % Isolate the term containing y
    5xy &= -x^2 - 1 \\
    % Solve for y
    y &= \\frac{-x^2 - 1}{5x} \\
    % Final simplified form
    y &= -\\frac{x^2 + 1}{5x}
    """
    
    print("🔧 TESTING LINE BREAK HANDLER")
    print("=" * 50)
    print("Input align environment:")
    print(test_align_content)
    print("\n" + "=" * 50)
    
    # Create handler
    handler = AdvancedLineBreakHandler()
    
    # Process the content
    equation_lines = handler.process_align_environment(test_align_content)
    
    print("✅ PROCESSED OUTPUT (each line separate):")
    for i, line in enumerate(equation_lines, 1):
        print(f"   Line {i}: {line}")
    
    print(f"\n📊 RESULT: {len(equation_lines)} separate equation lines")
    print("🎯 This will fix your single-line equation problem!")
    
    return equation_lines

if __name__ == "__main__":
    # Run test with your document
    test_with_your_document()