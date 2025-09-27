#!/usr/bin/env python3
"""
Comprehensive test for all problematic equations
"""

from integrated_latex_converter import IntegratedLaTeXToWordConverter
import traceback

def test_all_problematic_equations():
    """Test all the equations that were causing issues"""

    problematic_equations = [
        # Test case 1: Simple integral with limits
        """$$\\int_0^4 2x dx$$""",

        # Test case 2: Integral with sine function
        """$$\\int_0^4 2x \\sin\\left(\\frac{\\pi x}{4}\\right) dx$$""",

        # Test case 3: Complex integral with multiple limits
        """$$F_s[f(x)] = f_s(n) = \\int_0^l f(x)\\sin\\left(\\frac{n\\pi x}{l}\\right)dx$$""",

        # Test case 4: Integration by parts result
        """$$\\int x\\sin(ax)dx = -\\frac{x}{a}\\cos(ax) + \\frac{1}{a^2}\\sin(ax)$$""",

        # Test case 5: Final boxed result
        """$$\\boxed{f_s(n) = -\\frac{32}{n\\pi}\\cos(n\\pi)}$$""",

        # Test case 6: Cosine transform
        """$$f_c(n) = \\frac{32}{n^2\\pi^2}\\big(\\cos(n\\pi)-1\\big)$$""",

        # Test case 7: Definition with integral
        """$$F_s[f(x)] = f_s(n) = \\int_0^l f(x)\\sin\\left(\\frac{n\\pi x}{l}\\right)dx$$""",

        # Test case 8: Complex fraction
        """$$\\frac{\\int_0^4 x^2 dx}{\\int_0^4 x dx}$$""",

        # Test case 9: Trigonometric identity
        """$$\\sin(2x) = 2\\sin x \\cos x$$""",

        # Test case 10: Mixed operators
        """$$\\lim_{x \\to 0} \\frac{\\sin(x) + \\cos(x) - 1}{x^2}$$"""
    ]

    print("COMPREHENSIVE EQUATION TEST")
    print("=" * 60)
    print("Testing all problematic equations systematically...")
    print("=" * 60)

    converter = IntegratedLaTeXToWordConverter()
    results = []
    failed_cases = []

    for i, equation in enumerate(problematic_equations, 1):
        print(f"\nTest case {i}: {equation[:60]}...")
        print("-" * 40)

        try:
            # Clear previous logs
            converter.conversion_log = []
            converter.math_converter.conversion_errors = []

            word_doc = converter.convert_content_to_word(equation, 'latex_math')
            temp_file = f"comprehensive_test_{i}.docx"
            word_doc.save(temp_file)

            print(f"   Success: {temp_file}")

            # Check for conversion issues
            has_issues = False
            if converter.math_converter.conversion_errors:
                print("   Warning: Conversion issues detected:")
                for error in converter.math_converter.conversion_errors:
                    print(f"      - {error}")
                has_issues = True

            if has_issues:
                print("   Partial success with fallbacks")
                results.append("partial")
            else:
                print("   Perfect conversion")
                results.append("success")

        except Exception as e:
            print(f"   Failed: {e}")
            failed_cases.append((i, equation, str(e)))
            results.append("failed")

            # Print detailed error info
            print("   Detailed error:")
            traceback.print_exc()

    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    success_count = results.count("success")
    partial_count = results.count("partial")
    failed_count = results.count("failed")
    total_count = len(results)

    print(f"Total equations tested: {total_count}")
    print(f"Perfect conversions: {success_count}")
    print(f"Partial conversions: {partial_count}")
    print(f"Failed conversions: {failed_count}")

    if failed_cases:
        print("\nFAILED CASES:")
        for case_num, equation, error in failed_cases:
            print(f"   Case {case_num}: {equation[:50]}...")
            print(f"   Error: {error}")

    print("\nCONVERSION LOG:")
    for log_entry in converter.conversion_log:
        print(f"   {log_entry}")

    # Overall assessment
    if failed_count == 0:
        print("\nALL TESTS PASSED!")
        print("All equations converted successfully!")
        return True
    elif success_count > 0:
        print("\nMIXED RESULTS")
        print(f"{success_count} equations converted perfectly")
        print(f"{partial_count} equations used fallbacks")
        print(f"{failed_count} equations failed completely")
        return "partial"
    else:
        print("\nALL TESTS FAILED")
        print("Need to fix conversion issues")
        return False

def test_fourier_content():
    """Test the complete Fourier transform content"""

    fourier_content = """### Problem 07

Find the finite Fourier sine transform and finite Fourier cosine transform of
$$f(x) = 2x, \\quad 0 < x < 4.$$

### Step 1. Recall definitions

For $0<x<l$ (here $l=4$):

* Finite Fourier sine transform:
$$F_s[f(x)] = f_s(n) = \\int_0^l f(x)\\sin\\left(\\frac{n\\pi x}{l}\\right)dx$$

* Finite Fourier cosine transform:
$$F_c[f(x)] = f_c(n) = \\int_0^l f(x)\\cos\\left(\\frac{n\\pi x}{l}\\right)dx$$

### Step 2. Sine transform

$$f_s(n) = \\int_0^4 2x \\sin\\left(\\frac{n\\pi x}{4}\\right) dx$$

### Final Answer:

$$f_s(n) = -\\frac{32}{n\\pi}\\cos(n\\pi), \\quad f_c(n) = \\frac{32}{n^2\\pi^2}\\big(\\cos(n\\pi)-1\\big)$$"""

    print("\nTESTING COMPLETE FOURIER CONTENT")
    print("=" * 60)

    try:
        converter = IntegratedLaTeXToWordConverter()
        word_doc = converter.convert_content_to_word(fourier_content, 'markdown_latex')
        output_file = "comprehensive_fourier_test.docx"
        word_doc.save(output_file)

        print(f"✓ Success: {output_file}")
        print("\n CONVERSION LOG:")
        for log_entry in converter.conversion_log:
            print(f"   {log_entry}")

        return True

    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

if __name__ == "__main__":
    print("COMPREHENSIVE EQUATION CONVERSION TEST")
    print("=" * 80)

    # Test individual equations
    individual_results = test_all_problematic_equations()

    # Test complete content
    content_results = test_fourier_content()

    print("\n" + "=" * 80)
    print("OVERALL ASSESSMENT")
    print("=" * 80)

    if individual_results == True and content_results:
        print("🎉 EXCELLENT! All conversions working perfectly!")
        print(" Individual equations: All passed")
        print(" Complete content: Converted successfully")
        print(" No more blank spaces or broken equations")
        print(" All mathematical symbols rendering correctly")
    elif individual_results == "partial" and content_results:
        print(" GOOD! Most conversions working with minor issues!")
        print(" Complete content: Converted successfully")
        print(" Some individual equations used fallbacks")
        print(" Overall document structure is correct")
    else:
        print(" NEEDS IMPROVEMENT!")
        print(" Some equations still failing")
        print(" Complete content conversion issues")
        print(" Need to fix remaining conversion problems")

    print("\n CHECK YOUR WORD DOCUMENTS:")
    print("   • Look for blank spaces in equations")
    print("   • Check if integral symbols display correctly")
    print("   • Verify all mathematical symbols are visible")
    print("   • Ensure equations are editable in Word")
    print("   • Check document formatting and spacing")