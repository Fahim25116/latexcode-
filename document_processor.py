#!/usr/bin/env python3
"""
Document Processor Module
=========================
Handles document structure, formatting, and content processing
"""

import re
from typing import List, Dict, Tuple
from docx import Document
from docx.oxml import parse_xml
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from advanced_line_break_handler import AdvancedLineBreakHandler

class DocumentProcessor:
    """Processes document structure and formatting"""

    def __init__(self, math_converter):
        self.math_converter = math_converter
        self.line_break_handler = AdvancedLineBreakHandler()
        self.conversion_log = []

    def process_latex_document(self, doc: Document, latex_content: str):
        """Process complete LaTeX document"""
        # Extract body content
        body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
        if body_match:
            body = body_match.group(1).strip()
        else:
            body = latex_content

        # Find all structural elements with their positions
        elements = []

        # Find sections
        for match in re.finditer(r'\\section\*\{([^}]+)\}', body):
            elements.append((match.start(), match.end(), 'section', match.group(1), match.group(0)))

        # Find subsections
        for match in re.finditer(r'\\subsection\*\{([^}]+)\}', body):
            elements.append((match.start(), match.end(), 'subsection', match.group(1), match.group(0)))

        # Find align environments with ULTIMATE processing
        for match in re.finditer(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', body, re.DOTALL):
            elements.append((match.start(), match.end(), 'align', match.group(1), match.group(0)))

        # Find display equations
        for match in re.finditer(r'\$\$(.*?)\$\$', body, re.DOTALL):
            elements.append((match.start(), match.end(), 'display_eq', match.group(1), match.group(0)))

        # Sort by position
        elements.sort(key=lambda x: x[0])

        # Process elements in order with ULTIMATE handling
        current_pos = 0

        for start, end, element_type, content, full_match in elements:
            # Add text before this element
            if start > current_pos:
                text_before = body[current_pos:start].strip()
                if text_before:
                    self._add_text_paragraph_ultimate(doc, text_before)

            # Process the element with ULTIMATE methods
            if element_type == 'section':
                self._add_section_with_math_ultimate(doc, content, 1)
            elif element_type == 'subsection':
                self._add_section_with_math_ultimate(doc, content, 2)
            elif element_type == 'align':
                self._add_align_with_ULTIMATE_breaks(doc, content)
            elif element_type == 'display_eq':
                self._add_display_equation_ultimate(doc, content)

            current_pos = end

        # Add remaining text
        if current_pos < len(body):
            remaining = body[current_pos:].strip()
            if remaining:
                self._add_text_paragraph_ultimate(doc, remaining)

    def process_markdown_content(self, doc: Document, content: str):
        """Process Markdown + LaTeX mixed content"""
        # Split content into logical blocks
        blocks = self._split_content_into_blocks(content)

        for block in blocks:
            block_type = self._identify_block_type(block)

            if block_type == 'markdown_header':
                self._add_markdown_header(doc, block)
            elif block_type == 'latex_equation':
                self._add_latex_equation(doc, block)
            elif block_type == 'mixed_text':
                self._add_mixed_text_paragraph(doc, block)
            elif block_type == 'plain_text':
                self._add_plain_text(doc, block)

    def process_latex_math_content(self, doc: Document, content: str):
        """Process LaTeX math content"""
        # Handle align environments
        align_matches = re.finditer(r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', content, re.DOTALL)
        for match in align_matches:
            self._add_align_with_ULTIMATE_breaks(doc, match.group(1))

        # Handle display equations
        display_matches = re.finditer(r'\$\$(.*?)\$\$', content, re.DOTALL)
        for match in display_matches:
            self._add_display_equation_ultimate(doc, match.group(1))

    def _split_content_into_blocks(self, content: str) -> List[str]:
        """Split content into logical blocks"""
        # Split by double newlines to get paragraphs/blocks
        blocks = re.split(r'\n\s*\n', content)

        # Clean and filter blocks
        cleaned_blocks = []
        for block in blocks:
            block = block.strip()
            if block:
                cleaned_blocks.append(block)

        return cleaned_blocks

    def _identify_block_type(self, block: str) -> str:
        """Identify the type of content block"""
        block_lower = block.lower().strip()

        # Check for Markdown headers (### headings)
        if re.match(r'^#{1,6}\s+', block):
            return 'markdown_header'

        # Check for LaTeX equations (display math)
        if ('\\int' in block or '\\frac' in block or '\\sum' in block or
            '\\sin' in block or '\\cos' in block or '\\tan' in block):
            return 'latex_equation'

        # Check for mixed text (contains both $ math and regular text)
        if '$' in block and len(re.findall(r'[a-zA-Z]', block)) > 5:
            return 'mixed_text'

        # Default to plain text
        return 'plain_text'

    def _add_section_with_math_ultimate(self, doc: Document, title: str, level: int):
        """Add section heading with ULTIMATE math support"""
        if '$' in title:
            # Create heading with math
            heading_para = doc.add_heading(level=level)
            heading_para.clear()  # Clear default text
            self._process_mixed_text_ultimate(heading_para, title, is_heading=True)
        else:
            doc.add_heading(self._clean_text_ultimate(title), level=level)

    def _add_align_with_ULTIMATE_breaks(self, doc: Document, align_content: str):
        """Add align environment with ULTIMATE line breaks - THIS FIXES YOUR PROBLEM"""

        # Use our advanced line break handler
        equation_lines = self.line_break_handler.process_align_environment(align_content)

        self.conversion_log.append(f"Processing align environment: {len(equation_lines)} separate lines")

        # Process each line separately - NO MORE SINGLE-LINE EQUATIONS!
        for i, line in enumerate(equation_lines):
            line = line.strip()
            if not line:
                continue

            self.conversion_log.append(f"Processing equation line {i+1}: {line[:30]}...")

            # Convert and add each line as separate equation
            omml = self.math_converter.convert_latex_to_omml(line)
            if omml:
                try:
                    eq_para = doc.add_paragraph()
                    eq_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    math_element = parse_xml(omml)
                    eq_para._element.append(math_element)

                    # Add proper spacing between equations
                    eq_para.paragraph_format.space_after = Pt(6)
                    eq_para.paragraph_format.space_before = Pt(3)

                except Exception as e:
                    # Fallback with better formatting
                    fallback_para = doc.add_paragraph(f"Equation: {line}")
                    fallback_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    self.conversion_log.append(f"Used fallback for line: {line}")
            else:
                # Fallback with better formatting
                fallback_para = doc.add_paragraph(f"Equation: {line}")
                fallback_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        self.conversion_log.append(f"✅ Successfully processed align environment with {len(equation_lines)} separate lines")

    def _add_display_equation_ultimate(self, doc: Document, equation_content: str):
        """Add display equation with ULTIMATE processing"""
        cleaned_content = self.math_converter._ultimate_preprocess(equation_content)

        omml = self.math_converter.convert_latex_to_omml(cleaned_content)
        if omml:
            try:
                eq_para = doc.add_paragraph()
                eq_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                math_element = parse_xml(omml)
                eq_para._element.append(math_element)
            except Exception as e:
                doc.add_paragraph(f"Equation: {cleaned_content}")
        else:
            doc.add_paragraph(f"Equation: {cleaned_content}")

    def _add_text_paragraph_ultimate(self, doc: Document, text: str):
        """Add text paragraph with ULTIMATE inline math support"""

        # Clean text with ultimate method
        text = self._clean_text_ultimate(text)

        if '$' in text:
            # Contains inline math
            para = doc.add_paragraph()
            self._process_mixed_text_ultimate(para, text)
        else:
            # Regular text
            if text.strip():
                doc.add_paragraph(text)

    def _process_mixed_text_ultimate(self, paragraph, text: str, is_heading: bool = False):
        """Process text with inline math - ULTIMATE version"""

        # Split by inline math
        parts = re.split(r'(\$[^$]+\$)', text)

        for part in parts:
            if part.startswith('$') and part.endswith('$') and len(part) > 2:
                # Inline math
                math_content = part[1:-1]
                omml = self.math_converter.convert_latex_to_omml(math_content)
                if omml:
                    try:
                        math_element = parse_xml(omml)
                        run = paragraph.add_run()
                        run._element.append(math_element)
                        if is_heading:
                            run.font.bold = True
                            run.font.size = Pt(14)
                    except:
                        run = paragraph.add_run(f"[{math_content}]")
                        if is_heading:
                            run.font.bold = True
                else:
                    run = paragraph.add_run(f"[{math_content}]")
                    if is_heading:
                        run.font.bold = True
            else:
                # Regular text
                if part.strip():
                    run = paragraph.add_run(part)
                    if is_heading:
                        run.font.bold = True
                        run.font.size = Pt(14)

    def _clean_text_ultimate(self, text: str) -> str:
        """ULTIMATE text cleaning"""

        # Remove LaTeX commands
        text = re.sub(r'\\textbf\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+\*?\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+\*?', '', text)

        # Handle spacing and line breaks perfectly
        text = re.sub(r'\\\\', '\n', text)
        text = re.sub(r'^\s*%.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        return text.strip()

    def _add_markdown_header(self, doc: Document, header_block: str):
        """Add Markdown-style header with proper bold formatting"""
        # Extract header level and text
        header_match = re.match(r'^(#{1,6})\s+(.+)$', header_block.strip(), re.MULTILINE)

        if header_match:
            hash_count = len(header_match.group(1))
            header_text = header_match.group(2).strip()

            # Map ### to heading level (### = level 3, but make it prominent)
            if hash_count <= 3:
                # Use Word heading styles for better formatting
                heading_level = min(hash_count, 3)
                heading_para = doc.add_heading(level=heading_level)
                heading_para.clear()  # Clear default text

                # Add the text with proper formatting
                run = heading_para.add_run(header_text)
                run.font.bold = True
                run.font.size = Pt(14 if hash_count == 3 else 16)

                self.conversion_log.append(f"Added header (level {hash_count}): {header_text}")
            else:
                # For #### and beyond, use bold paragraph
                para = doc.add_paragraph()
                run = para.add_run(header_text)
                run.font.bold = True
                run.font.size = Pt(12)

    def _add_latex_equation(self, doc: Document, equation_block: str):
        """Add LaTeX equation with proper formatting"""
        # Check if it's a display equation or inline
        if ('\\int' in equation_block or '\\frac' in equation_block or
            '=' in equation_block):
            # Treat as display equation
            omml = self.math_converter.convert_latex_to_omml(equation_block)
            if omml:
                try:
                    eq_para = doc.add_paragraph()
                    eq_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    math_element = parse_xml(omml)
                    eq_para._element.append(math_element)

                    # Add spacing
                    eq_para.paragraph_format.space_after = Pt(6)
                    eq_para.paragraph_format.space_before = Pt(6)

                    self.conversion_log.append(f"Added equation: {equation_block[:30]}...")

                except Exception as e:
                    # Fallback
                    fallback_para = doc.add_paragraph(f"Equation: {equation_block}")
                    fallback_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                # Fallback
                fallback_para = doc.add_paragraph(f"Equation: {equation_block}")
                fallback_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def _add_mixed_text_paragraph(self, doc: Document, text_block: str):
        """Add paragraph with mixed text and inline math"""
        para = doc.add_paragraph()

        # Split by inline math markers
        parts = re.split(r'(\$[^$]+\$)', text_block)

        for part in parts:
            if part.startswith('$') and part.endswith('$') and len(part) > 2:
                # Inline math
                math_content = part[1:-1]
                omml = self.math_converter.convert_latex_to_omml(math_content)
                if omml:
                    try:
                        math_element = parse_xml(omml)
                        run = para.add_run()
                        run._element.append(math_element)
                    except:
                        para.add_run(f"[{math_content}]")
                else:
                    para.add_run(f"[{math_content}]")
            else:
                # Regular text
                if part.strip():
                    para.add_run(part)

    def _add_plain_text(self, doc: Document, text_block: str):
        """Add plain text paragraph"""
        if text_block.strip():
            doc.add_paragraph(text_block.strip())

    def get_conversion_log(self) -> List[str]:
        """Get conversion log"""
        return self.conversion_log.copy()

    def clear_log(self):
        """Clear conversion log"""
        self.conversion_log = []