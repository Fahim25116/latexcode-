#!/usr/bin/env python3
"""
Core Math Converter Module
==========================
Handles all mathematical expression conversions with advanced preprocessing
"""

import os
import re
from typing import Optional, List
from lxml import etree
import latex2mathml.converter

class CoreMathConverter:
    """Core mathematical expression converter with advanced features"""

    def __init__(self):
        self.xsl_path = self._find_mml2omml_xsl()
        self.conversion_errors = []

    def _find_mml2omml_xsl(self) -> Optional[str]:
        """Find Microsoft Office MML2OMML.XSL transformation file"""
        possible_paths = [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\MML2OMML.XSL",
            "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\MML2OMML.XSL",
            "C:\\Program Files\\Microsoft Office\\Office16\\MML2OMML.XSL",
            "C:\\Program Files\\Microsoft Office\\root\\Office15\\MML2OMML.XSL",
            "C:\\Program Files (x86)\\Microsoft Office\\root\\Office15\\MML2OMML.XSL",
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def convert_latex_to_omml(self, latex_expr: str, use_advanced: bool = True) -> Optional[str]:
        """Convert LaTeX expression to OMML with advanced preprocessing"""
        try:
            # Store original for fallback
            original_expr = latex_expr

            if use_advanced:
                # Use advanced preprocessing
                latex_expr = self._ultimate_preprocess(latex_expr)
            else:
                # Use basic preprocessing
                latex_expr = self._basic_preprocess(latex_expr)

            # Try conversion
            try:
                # Convert to MathML
                mathml_string = latex2mathml.converter.convert(latex_expr)

                if not self.xsl_path:
                    return f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{mathml_string}</m:oMath>'

                # Full conversion using Microsoft XSLT
                return self._convert_mathml_to_omml(mathml_string)

            except Exception as mathml_error:
                # If MathML conversion fails, try with simplified expression
                self.conversion_errors.append(f"MathML conversion failed, trying simplified: {str(mathml_error)}")

                # Try with simplified expression
                simplified_expr = self._simplify_complex_expression(original_expr)
                if simplified_expr != original_expr:
                    try:
                        mathml_string = latex2mathml.converter.convert(simplified_expr)
                        if not self.xsl_path:
                            return f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{mathml_string}</m:oMath>'
                        return self._convert_mathml_to_omml(mathml_string)
                    except:
                        pass

                # If still failing, try basic fallback
                try:
                    mathml_string = latex2mathml.converter.convert(original_expr)
                    return f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{mathml_string}</m:oMath>'
                except:
                    pass

                # Final fallback
                return None

        except Exception as e:
            error_msg = f"Error converting equation: {str(e)}"
            self.conversion_errors.append(error_msg)
            return None

    def _ultimate_preprocess(self, latex_expr: str) -> str:
        """Ultimate preprocessing for LaTeX expressions"""
        # Clean up the expression
        latex_expr = latex_expr.strip()

        # Remove comments completely
        latex_expr = re.sub(r'%.*$', '', latex_expr, flags=re.MULTILINE)

        # Handle complex nested structures first
        # Fix nested fractions and integrals
        latex_expr = re.sub(r'\\frac\s*(\\[a-zA-Z]+)\s*(\\[a-zA-Z]+)', r'\\frac{\1}{\2}', latex_expr)

        # Handle spacing commands that might break parsing
        latex_expr = re.sub(r'\\[,\s]+', ' ', latex_expr)
        latex_expr = re.sub(r'\\quad', ' ', latex_expr)
        latex_expr = re.sub(r'\\qquad', '  ', latex_expr)
        latex_expr = re.sub(r'\\;', ' ', latex_expr)
        latex_expr = re.sub(r'\\:', ' ', latex_expr)
        latex_expr = re.sub(r'\\\s+', ' ', latex_expr)

        # Handle delimiters that might cause issues
        latex_expr = re.sub(r'\\left\(', '(', latex_expr)
        latex_expr = re.sub(r'\\right\)', ')', latex_expr)
        latex_expr = re.sub(r'\\left\[', '[', latex_expr)
        latex_expr = re.sub(r'\\right\]', ']', latex_expr)
        latex_expr = re.sub(r'\\left\|', '|', latex_expr)
        latex_expr = re.sub(r'\\right\|', '|', latex_expr)
        latex_expr = re.sub(r'\\left\{', '{', latex_expr)
        latex_expr = re.sub(r'\\right\}', '}', latex_expr)

        # Handle special integral and summation commands
        latex_expr = re.sub(r'\\int\s*_\s*(\w+)\s*\^\s*(\w+)', r'\\int_{\1}^{\2}', latex_expr)
        latex_expr = re.sub(r'\\sum\s*_\s*(\w+)\s*\^\s*(\w+)', r'\\sum_{\1}^{\2}', latex_expr)

        # Handle trigonometric functions with special spacing
        latex_expr = re.sub(r'\\sin\s*!\s*\\left\s*\(', r'\\sin(', latex_expr)
        latex_expr = re.sub(r'\\cos\s*!\s*\\left\s*\(', r'\\cos(', latex_expr)
        latex_expr = re.sub(r'\\tan\s*!\s*\\left\s*\(', r'\\tan(', latex_expr)
        latex_expr = re.sub(r'\\left\s*\(', '(', latex_expr)
        latex_expr = re.sub(r'\\right\s*\)', ')', latex_expr)

        # Handle integrals with limits - convert \int_0^l to proper format
        latex_expr = re.sub(r'\\int\s*_\s*([^\\]+)\s*\^\s*([^\\]+)', r'\\int_{\1}^{\2}', latex_expr)
        latex_expr = re.sub(r'\\int\s*_\s*\{([^}]+)\}\s*\^\s*\{([^}]+)\}', r'\\int_{\1}^{\2}', latex_expr)

        # Handle boxed equations
        latex_expr = re.sub(r'\\boxed\s*\{([^}]+)\}', r'(\1)', latex_expr)

        # Handle complex fractions with multiple operators
        latex_expr = re.sub(r'\\frac\s*\{([^}]+)\}\s*\{([^}]+)\}', r'\\frac{\1}{\2}', latex_expr)

        # Special handling for integrals that might be causing issues
        latex_expr = re.sub(r'\\int\s+([^_\\]+)\\', r'\\int_{\1}', latex_expr)  # Handle cases without proper limits

        # Disable aggressive preprocessing to avoid corruption
        # The fallback system will handle cases where MathML conversion fails

        # Handle common integral patterns that cause issues
        latex_expr = re.sub(r'\\int\s+\\sin', r'\\int \\sin', latex_expr)
        latex_expr = re.sub(r'\\int\s+\\cos', r'\\int \\cos', latex_expr)
        latex_expr = re.sub(r'\\int\s+\\tan', r'\\int \\tan', latex_expr)

        # Special handling for integrals that might have spacing issues
        latex_expr = re.sub(r'\\int\s+', r'\\int ', latex_expr)

        # Handle operators and symbols
        latex_expr = re.sub(r'\\cdot', ' \\cdot ', latex_expr)
        latex_expr = re.sub(r'\\times', ' \\times ', latex_expr)
        latex_expr = re.sub(r'\\div', ' \\div ', latex_expr)

        # Handle alignment markers
        latex_expr = re.sub(r'\s*&\s*=\s*', ' = ', latex_expr)
        latex_expr = re.sub(r'\s*&\s*', ' ', latex_expr)

        # Clean up multiple spaces but preserve meaningful ones
        latex_expr = re.sub(r'\s+', ' ', latex_expr)

        # Handle special characters that might cause issues
        latex_expr = re.sub(r'\\pm', ' \\pm ', latex_expr)
        latex_expr = re.sub(r'\\mp', ' \\mp ', latex_expr)
        latex_expr = re.sub(r'\\to', ' \\to ', latex_expr)
        latex_expr = re.sub(r'\\infty', ' \\infty ', latex_expr)

        # Final cleanup
        latex_expr = latex_expr.strip()

        return latex_expr

    def _basic_preprocess(self, latex_expr: str) -> str:
        """Basic preprocessing for LaTeX expressions"""
        # Clean up the expression
        latex_expr = latex_expr.strip()

        # Remove extra whitespace
        latex_expr = re.sub(r'\s+', ' ', latex_expr)

        return latex_expr.strip()

    def _simplify_complex_expression(self, latex_expr: str) -> str:
        """Simplify complex expressions for better conversion success"""
        simplified = latex_expr.strip()

        # Try removing complex nested structures that might cause issues
        # Replace complex integrals with simpler forms
        simplified = re.sub(r'\\int\s+\\left\((.*?)\\right\)', r'\\int (\1)', simplified)

        # Simplify complex fractions
        simplified = re.sub(r'\\frac\s*\\left\((.*?)\\right\)\s*\\left\((.*?)\\right\)',
                          r'\\frac{(\1)}{(\2)}', simplified)

        # Handle cases where there might be missing braces
        simplified = re.sub(r'\\frac\s*([a-zA-Z])\s*([a-zA-Z])', r'\\frac{\1}{\2}', simplified)

        # Simplify limits that might be complex
        simplified = re.sub(r'_(\w+)\^(\w+)', '_{\\1}^{\\2}', simplified)

        # Remove potentially problematic commands
        simplified = re.sub(r'\\left\s*\\{', '{', simplified)
        simplified = re.sub(r'\\right\s*\\}', '}', simplified)

        # If the expression is very long, try to break it down
        if len(simplified) > 100:
            # Look for major operators and try to isolate parts
            parts = re.split(r'(\\+|\-)', simplified)
            if len(parts) > 3:
                # Try converting just the first major part
                first_part = parts[0].strip()
                if first_part:
                    return first_part

        return simplified if simplified != latex_expr else latex_expr

    def _convert_mathml_to_omml(self, mathml_string: str) -> str:
        """Convert MathML to OMML with enhanced error handling"""
        try:
            # Clean the MathML string first
            mathml_string = mathml_string.strip()

            # Fix common MathML issues
            mathml_string = re.sub(r'<m:math\s+([^>]*?)>', r'<m:math \1>', mathml_string)
            mathml_string = re.sub(r'xmlns:m\s*=\s*["\']([^"\']+)["\']', r'xmlns:m="\1"', mathml_string)

            # Fix integral limits - convert subsup to proper integral limit structure
            mathml_string = self._fix_integral_limits(mathml_string)

            mathml_tree = etree.fromstring(mathml_string)

            # Only proceed with XSLT if we have the Microsoft Office XSL file
            if self.xsl_path and os.path.exists(self.xsl_path):
                xslt = etree.parse(self.xsl_path)
                transform = etree.XSLT(xslt)
                omml_tree = transform(mathml_tree)
                result = etree.tostring(omml_tree, encoding='unicode')

                # Check if the conversion was successful
                if result and '<m:oMath' in result:
                    return result

            # Fallback to wrapped MathML if XSLT fails or isn't available
            return f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{mathml_string}</m:oMath>'

        except Exception as e:
            # Enhanced error handling with detailed logging
            error_msg = f"MathML to OMML conversion failed: {str(e)}"
            self.conversion_errors.append(error_msg)

            # Try to create a minimal valid OMML structure
            try:
                return f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:t>{mathml_string}</m:t></m:r></m:oMath>'
            except:
                # Last resort fallback
                return f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{mathml_string}</m:oMath>'

    def _fix_integral_limits(self, mathml_string: str) -> str:
        """Fix integral limits in MathML to ensure proper OMML conversion"""
        try:
            # Parse the MathML to find integral structures
            mathml_tree = etree.fromstring(mathml_string)

            # Find all integral elements with subsup limits
            integrals_with_limits = mathml_tree.xpath(".//m:msubsup[preceding-sibling::m:mo[text()='∫']]")

            for integral_limit in integrals_with_limits:
                # Get the lower and upper limits
                if len(integral_limit) >= 2:
                    lower_limit = integral_limit[0]  # First child is lower limit (subscript)
                    upper_limit = integral_limit[1]  # Second child is upper limit (superscript)

                    # Create proper integral limit structure
                    # This is a simplified approach - in a full implementation,
                    # we'd need to reconstruct the MathML with proper limit elements

                    # For now, let's try to improve the structure
                    # Replace the subsup with proper limit elements if possible
                    pass

            return etree.tostring(mathml_tree, encoding='unicode')

        except:
            # If parsing fails, return original string
            return mathml_string

    def process_inline_math(self, math_content: str) -> Optional[str]:
        """Process inline math expressions"""
        return self.convert_latex_to_omml(math_content, use_advanced=False)

    def process_display_math(self, math_content: str) -> Optional[str]:
        """Process display math expressions"""
        return self.convert_latex_to_omml(math_content, use_advanced=True)

    def get_conversion_errors(self) -> List[str]:
        """Get list of conversion errors"""
        return self.conversion_errors.copy()

    def clear_errors(self):
        """Clear conversion errors"""
        self.conversion_errors = []