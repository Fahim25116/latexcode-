# LaTeX to Word Converter - Installation Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the converter:**
   ```bash
   python fixed_latex_to_word.py
   ```

## Requirements

- **Python 3.9 or higher** (required by python-docx)
- The packages listed in requirements.txt

## Package Details

- **latex2mathml (3.78.1)**: Converts LaTeX equations to MathML format
- **python-docx (1.2.0)**: Creates and modifies Word documents
- **lxml (6.0.2)**: XML processing for MathML to OMML conversion

## Alternative Installation

For development or if you want to allow minor updates:
```bash
pip install -r requirements-flexible.txt
```

## Microsoft Office Integration

The converter attempts to find Microsoft's MML2OMML.XSL file for full equation editability:
- **Windows**: Looks in Office installation directories
- **Mac**: Checks Applications folder
- **Fallback**: Uses basic OMML structure if file not found

## Troubleshooting

If installation fails:
1. Ensure Python 3.9+ is installed
2. Update pip: `pip install --upgrade pip`
3. Try installing packages individually:
   ```bash
   pip install latex2mathml
   pip install python-docx
   pip install lxml
   ```
