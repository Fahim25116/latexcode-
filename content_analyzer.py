#!/usr/bin/env python3
"""
Content Analyzer Module
=======================
Analyzes content to determine type and structure
"""

import re
from typing import Dict, List
from advanced_line_break_handler import EquationStructureAnalyzer

class ContentAnalyzer:
    """Analyzes content to determine type and structure"""

    def __init__(self):
        self.structure_analyzer = EquationStructureAnalyzer()
        self.analysis_results = {}

    def detect_content_type(self, content: str) -> str:
        """Detect if content is LaTeX, Markdown+LaTeX, or mixed"""
        content_lower = content.lower().strip()

        # Check for LaTeX document structure
        if '\\documentclass' in content_lower or '\\begin{document}' in content_lower:
            return 'latex_document'

        # Check for Markdown headers
        if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            return 'markdown_latex'

        # Check for align environments
        if '\\begin{align' in content_lower:
            return 'latex_math'

        # Default to mixed content
        return 'mixed'

    def analyze_content_structure(self, content: str) -> Dict:
        """Analyze the structure of the content"""
        content_type = self.detect_content_type(content)

        results = {
            'content_type': content_type,
            'has_math': False,
            'has_headers': False,
            'has_sections': False,
            'math_elements': [],
            'header_elements': [],
            'section_elements': [],
            'total_elements': 0
        }

        # Analyze based on content type
        if content_type == 'latex_document':
            results.update(self._analyze_latex_document(content))
        elif content_type == 'markdown_latex':
            results.update(self._analyze_markdown_content(content))
        elif content_type == 'latex_math':
            results.update(self._analyze_latex_math(content))
        else:
            results.update(self._analyze_mixed_content(content))

        return results

    def _analyze_latex_document(self, content: str) -> Dict:
        """Analyze LaTeX document structure"""
        results = {
            'has_sections': False,
            'has_math': False,
            'math_elements': [],
            'section_elements': []
        }

        # Check for sections
        sections = re.findall(r'\\section\*?\{([^}]+)\}', content)
        subsections = re.findall(r'\\subsection\*?\{([^}]+)\}', content)

        if sections or subsections:
            results['has_sections'] = True
            results['section_elements'] = sections + subsections

        # Check for math elements
        math_elements = []

        # Align environments
        align_matches = re.finditer(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', content, re.DOTALL)
        for match in align_matches:
            math_elements.append({
                'type': 'align',
                'content': match.group(1),
                'position': match.start()
            })

        # Display equations
        display_matches = re.finditer(r'\$\$(.*?)\$\$', content, re.DOTALL)
        for match in display_matches:
            math_elements.append({
                'type': 'display',
                'content': match.group(1),
                'position': match.start()
            })

        # Inline equations
        inline_matches = re.finditer(r'\$([^$]+)\$', content)
        for match in inline_matches:
            math_elements.append({
                'type': 'inline',
                'content': match.group(1),
                'position': match.start()
            })

        if math_elements:
            results['has_math'] = True
            results['math_elements'] = math_elements

        return results

    def _analyze_markdown_content(self, content: str) -> Dict:
        """Analyze Markdown content structure"""
        results = {
            'has_headers': False,
            'has_math': False,
            'header_elements': [],
            'math_elements': []
        }

        # Check for headers
        header_matches = re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        for match in header_matches:
            results['has_headers'] = True
            results['header_elements'].append({
                'level': len(match.group(1)),
                'text': match.group(2).strip(),
                'position': match.start()
            })

        # Check for math elements
        math_elements = []

        # Display equations
        display_matches = re.finditer(r'\$\$(.*?)\$\$', content, re.DOTALL)
        for match in display_matches:
            math_elements.append({
                'type': 'display',
                'content': match.group(1),
                'position': match.start()
            })

        # Inline equations
        inline_matches = re.finditer(r'\$([^$]+)\$', content)
        for match in inline_matches:
            math_elements.append({
                'type': 'inline',
                'content': match.group(1),
                'position': match.start()
            })

        if math_elements:
            results['has_math'] = True
            results['math_elements'] = math_elements

        return results

    def _analyze_latex_math(self, content: str) -> Dict:
        """Analyze LaTeX math content"""
        results = {
            'has_math': True,
            'math_elements': []
        }

        # Align environments
        align_matches = re.finditer(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', content, re.DOTALL)
        for match in align_matches:
            results['math_elements'].append({
                'type': 'align',
                'content': match.group(1),
                'position': match.start()
            })

        # Display equations
        display_matches = re.finditer(r'\$\$(.*?)\$\$', content, re.DOTALL)
        for match in display_matches:
            results['math_elements'].append({
                'type': 'display',
                'content': match.group(1),
                'position': match.start()
            })

        return results

    def _analyze_mixed_content(self, content: str) -> Dict:
        """Analyze mixed content"""
        results = {
            'has_math': False,
            'has_headers': False,
            'math_elements': [],
            'header_elements': []
        }

        # Check for headers
        header_matches = re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        for match in header_matches:
            results['has_headers'] = True
            results['header_elements'].append({
                'level': len(match.group(1)),
                'text': match.group(2).strip(),
                'position': match.start()
            })

        # Check for math
        math_matches = re.finditer(r'\$([^$]+)\$', content)
        for match in math_matches:
            results['has_math'] = True
            results['math_elements'].append({
                'type': 'inline',
                'content': match.group(1),
                'position': match.start()
            })

        return results

    def get_processing_recommendations(self, content: str) -> Dict:
        """Get recommendations for processing this content"""
        analysis = self.analyze_content_structure(content)

        recommendations = {
            'content_type': analysis['content_type'],
            'processing_priority': 'unknown',
            'features_to_use': [],
            'estimated_complexity': 'low'
        }

        # Determine processing priority
        if analysis['content_type'] == 'latex_document':
            recommendations['processing_priority'] = 'document_structure'
            recommendations['features_to_use'] = ['line_breaks', 'sections', 'math']
            recommendations['estimated_complexity'] = 'high'
        elif analysis['content_type'] == 'markdown_latex':
            recommendations['processing_priority'] = 'headers_and_math'
            recommendations['features_to_use'] = ['markdown_headers', 'math']
            recommendations['estimated_complexity'] = 'medium'
        elif analysis['content_type'] == 'latex_math':
            recommendations['processing_priority'] = 'math_only'
            recommendations['features_to_use'] = ['line_breaks', 'math']
            recommendations['estimated_complexity'] = 'medium'
        else:
            recommendations['processing_priority'] = 'mixed_content'
            recommendations['features_to_use'] = ['math']
            recommendations['estimated_complexity'] = 'low'

        return recommendations

    def validate_content(self, content: str) -> Dict:
        """Validate content for potential issues"""
        issues = []
        warnings = []

        # Check for common issues
        if '\\begin{align' in content and '\\\\' not in content:
            warnings.append("Align environment found but no line breaks detected")

        if '$' in content:
            unclosed_math = content.count('$') % 2
            if unclosed_math != 0:
                issues.append("Unclosed math delimiters detected")

        if '\\documentclass' in content and '\\begin{document}' not in content:
            warnings.append("LaTeX document class found but no document environment")

        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }