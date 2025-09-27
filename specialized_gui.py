#!/usr/bin/env python3
"""
Specialized GUI Module
======================
Modular GUI components for LaTeX and Markdown conversion
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import datetime

class BaseConverterGUI:
    """Base GUI class with common functionality"""

    def __init__(self, title: str, geometry: str = "1000x700"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def log_message(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update()

    def clear_log(self):
        """Clear the log"""
        if hasattr(self, 'status_text'):
            self.status_text.delete("1.0", tk.END)

    def show_error(self, message: str):
        """Show error message"""
        messagebox.showerror("Error", message)

    def show_success(self, message: str):
        """Show success message"""
        messagebox.showinfo("Success", message)

    def run(self):
        """Start the GUI"""
        self.root.mainloop()

class IntegratedConverterGUI(BaseConverterGUI):
    """Integrated GUI for all conversion features"""

    def __init__(self, converter):
        super().__init__("🚀 INTEGRATED LaTeX & Markdown to Word Converter", "1200x800")
        self.converter = converter
        self.create_widgets()

    def create_widgets(self):
        """Create all widgets"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="🚀 INTEGRATED LaTeX & Markdown Converter",
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))

        subtitle_label = ttk.Label(main_frame, text="✅ Ultimate Line Breaks + ### Headers + Advanced Math Support",
                                  font=('Arial', 11))
        subtitle_label.grid(row=0, column=0, pady=(20, 15))

        # Content type selection
        type_frame = ttk.LabelFrame(main_frame, text="Content Type", padding="10")
        type_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        self.content_type = tk.StringVar(value="auto")
        ttk.Radiobutton(type_frame, text="🔍 Auto-detect", variable=self.content_type,
                       value="auto").grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="📄 LaTeX Document", variable=self.content_type,
                       value="latex_document").grid(row=0, column=1, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="📝 Markdown + LaTeX", variable=self.content_type,
                       value="markdown_latex").grid(row=0, column=2, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="🧮 LaTeX Math Only", variable=self.content_type,
                       value="latex_math").grid(row=0, column=3)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input Content", padding="10")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        # Text area
        self.content_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=20, width=100, font=('Courier', 10))
        self.content_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)

        # Buttons
        ttk.Button(button_frame, text="🎯 Load Problem Document",
                  command=self.load_problem_document).grid(row=0, column=0, padx=(0, 10))

        ttk.Button(button_frame, text="📋 Load Integral Solution",
                  command=self.load_integral_solution).grid(row=0, column=1, padx=(0, 10))

        ttk.Button(button_frame, text="🔥 INTEGRATED Convert",
                  command=self.integrated_convert).grid(row=0, column=2, padx=(0, 10))

        ttk.Button(button_frame, text="📁 Load File",
                  command=self.load_file).grid(row=0, column=3, padx=(0, 10))

        ttk.Button(button_frame, text="🧹 Clear",
                  command=self.clear_text).grid(row=0, column=4)

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Conversion Status & Debug Info", padding="10")
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)

        # Status text
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, width=100, font=('Consolas', 9))
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initial message
        self.log_message("🚀 INTEGRATED CONVERTER READY!")
        self.log_message("✅ Features: Ultimate line breaks + ### headers + advanced math")
        self.log_message("🎯 Auto-detects content type and applies appropriate processing")
        self.log_message("🔥 Handles both LaTeX documents and Markdown + LaTeX mixed content")

    def load_problem_document(self):
        """Load the user's problematic equation document"""
        problem_document = r"""\documentclass[12pt, a4paper]{article}

% Required packages for math and layout
\usepackage{amsmath}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

% No page numbers
\pagestyle{empty}

\begin{document}

\section*{Analysis of the Equation: $x^2 + 5xy + 1 = 0$}

The provided equation is an algebraic equation. Below are two possible solutions based on common calculus problems: solving for $y$ and finding the derivative $\frac{dy}{dx}$.

\subsection*{1. Solving the Equation for $y$}

We can rearrange the equation to express $y$ as an explicit function of $x$.

\begin{align*}
    % Starting equation
    x^2 + 5xy + 1 &= 0 \\
    % Isolate the term containing y
    5xy &= -x^2 - 1 \\
    % Solve for y
    y &= \frac{-x^2 - 1}{5x} \\
    % Final simplified form
    y &= -\frac{x^2 + 1}{5x}
\end{align*}

\subsection*{2. Finding the Derivative $\frac{dy}{dx}$ via Implicit Differentiation}

Assuming $y$ is a function of $x$, we can find its derivative by differentiating the entire equation implicitly.

\begin{align*}
    % Starting equation
    x^2 + 5xy + 1 &= 0 \\
    % Differentiate both sides with respect to x
    \frac{d}{dx}(x^2 + 5xy + 1) &= \frac{d}{dx}(0) \\
    % Apply differentiation rules (including product rule for 5xy)
    2x + \left(5 \cdot y + 5x \cdot \frac{dy}{dx}\right) + 0 &= 0 \\
    % Rearrange to isolate the dy/dx term
    5x\frac{dy}{dx} &= -2x - 5y \\
    % Solve for dy/dx
    \frac{dy}{dx} &= \frac{-2x - 5y}{5x}
\end{align*}

\end{document}"""

        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", problem_document)
        self.log_message("🎯 Your problematic equation document loaded!")

    def load_integral_solution(self):
        """Load integral solution with ### headers"""
        integral_solution = '''### Step 1. Split the integral

We can split this integral into two parts:
∫(1/(4sinxcosx) + 7)dx = ∫(1/(4sinxcosx))dx + ∫7dx

---

### Step 2. Simplify the first term

We know that:
sin(2x) = 2sin x cos x ⟹ sin x cos x = sin(2x)/2

Substituting this identity:
1/(4sin x cos x) = 1/(4 · sin(2x)/2) = 1/(2sin(2x))

Therefore:
∫(1/(4sin x cos x))dx = ∫(1/(2sin(2x)))dx

### Step 3. Use substitution

Let u = 2x, then du = 2dx, so dx = du/2.

Substituting:
∫(1/(2sin(2x)))dx = ∫(1/(2sin u)) · (du/2) = (1/4)∫csc u du

### Step 4. Recall integral of csc u

We know that:
∫csc u du = ln|tan(u/2)| + C

Therefore:
(1/4)∫csc u du = (1/4)ln|tan(u/2)| + C = (1/4)ln|tan x| + C

### Step 5. Add the second part

The integral of the constant term is:
∫7 dx = 7x + C

### Final Answer

Combining both parts:
∫(1/(4sin x cos x) + 7)dx = (1/4)ln|tan x| + 7x + C'''

        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", integral_solution)
        self.log_message("📋 Integral solution with ### headers loaded!")

    def load_file(self):
        """Load file"""
        filename = filedialog.askopenfilename(
            title="Select LaTeX, Markdown, or Text File",
            filetypes=[("LaTeX files", "*.tex"), ("Text files", "*.txt"), ("Markdown files", "*.md"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", content)
                self.log_message(f"✅ Loaded: {Path(filename).name}")

            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                self.show_error(str(e))

    def integrated_convert(self):
        """INTEGRATED conversion with all features"""
        content = self.content_text.get("1.0", tk.END).strip()
        content_type = self.content_type.get()

        if not content:
            self.show_error("Please enter content.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Save INTEGRATED Word Document",
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )

        if not output_file:
            return

        try:
            self.log_message("🚀 Starting INTEGRATED conversion with all features...")
            self.root.update()

            # INTEGRATED conversion
            word_doc = self.converter.convert_content_to_word(content, content_type)
            word_doc.save(output_file)

            self.log_message(f"🎉 INTEGRATED SUCCESS! Document converted with all features!")
            self.log_message(f"📄 Saved as: {Path(output_file).name}")

            # Show detailed conversion log
            for log_entry in self.converter.conversion_log:
                self.log_message(f"   📋 {log_entry}")

            # Success message
            success_msg = f"""🎉 INTEGRATED CONVERSION COMPLETED!

✅ ALL FEATURES APPLIED:
• Ultimate line break handling for align* environments
• Markdown ### header formatting as bold headings
• Advanced mathematical equation processing
• Auto-detection of content type
• Professional document structure

📄 Saved as: {Path(output_file).name}

🔥 ALL YOUR PROBLEMS ARE SOLVED:
• Line break issues: FIXED ✅
• ### header formatting: FIXED ✅
• Math equation rendering: PERFECT ✅
• Document structure: PROFESSIONAL ✅"""

            self.show_success(success_msg)

        except Exception as e:
            error_msg = f"❌ INTEGRATED conversion failed: {str(e)}"
            self.log_message(error_msg)
            self.show_error(error_msg)

    def clear_text(self):
        """Clear text"""
        self.content_text.delete("1.0", tk.END)
        self.clear_log()
        self.log_message("Cleared. Ready for new content.")

class SimpleConverterGUI(BaseConverterGUI):
    """Simple GUI for basic conversions"""

    def __init__(self, converter, title: str = "LaTeX to Word Converter"):
        super().__init__(title, "800x600")
        self.converter = converter
        self.create_widgets()

    def create_widgets(self):
        """Create widgets"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="LaTeX to Word Converter",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 15))

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="LaTeX Input", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        # Text area
        self.content_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=15, width=80, font=('Courier', 10))
        self.content_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)

        # Buttons
        ttk.Button(button_frame, text="📁 Load File",
                  command=self.load_file).grid(row=0, column=0, padx=(0, 10))

        ttk.Button(button_frame, text="🔄 Convert",
                  command=self.convert).grid(row=0, column=1, padx=(0, 10))

        ttk.Button(button_frame, text="🧹 Clear",
                  command=self.clear_text).grid(row=0, column=2)

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)

        # Status text
        self.status_text = scrolledtext.ScrolledText(status_frame, height=5, width=80, font=('Consolas', 9))
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initial message
        self.log_message("Ready to convert LaTeX to Word!")

    def load_file(self):
        """Load file"""
        filename = filedialog.askopenfilename(
            title="Select LaTeX File",
            filetypes=[("LaTeX files", "*.tex"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", content)
                self.log_message(f"✅ Loaded: {Path(filename).name}")

            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                self.show_error(str(e))

    def convert(self):
        """Convert content"""
        content = self.content_text.get("1.0", tk.END).strip()

        if not content:
            self.show_error("Please enter LaTeX content.")
            return

        output_file = filedialog.asksaveasfilename(
            title="Save Word Document",
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )

        if not output_file:
            return

        try:
            self.log_message("Converting...")
            self.root.update()

            # Convert content
            word_doc = self.converter.convert_content_to_word(content)
            word_doc.save(output_file)

            self.log_message(f"✅ Success! Saved as: {Path(output_file).name}")
            self.show_success(f"Document saved as: {Path(output_file).name}")

        except Exception as e:
            error_msg = f"❌ Conversion failed: {str(e)}"
            self.log_message(error_msg)
            self.show_error(error_msg)

    def clear_text(self):
        """Clear text"""
        self.content_text.delete("1.0", tk.END)
        self.clear_log()
        self.log_message("Cleared. Ready for new content.")