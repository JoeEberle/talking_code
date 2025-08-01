"""
story_compiler.py

A modular library to gather multiple markdown files into a single document,
automatically add appendix sections, and render to Word (docx) and PDF using Pandoc.

Now enhanced with DEBUG print statements to track exactly which files
are being added, making it easier to pinpoint any file that causes a
Pandoc error.

Dependencies:
- Python 3.x
- Pandoc installed on the system (https://pandoc.org)

Example usage:
from story_compiler import build_story_document

build_story_document(
    markdown_files=[
        "module1/storyboard.md",
        "module2/storyboard.md"
    ],
    appendix_files=[
        "appendix1/storyboard.md",
        "appendix2/storyboard.md"
    ],
    output_markdown="full_story.md",
    output_docx="final_story.docx",
    title="Comprehensive Data Analysis Report"
)
"""

import os
import subprocess

def combine_markdown_files_with_appendix(markdown_files, appendix_files, output_markdown, title=None):
    """
    Combine main markdown files and appendix files into a single markdown document,
    automatically adding Appendix headings based on filenames, with a proper Pandoc
    metadata block for title page, and debug prints.

    Args:
        markdown_files (list): List of main markdown file paths.
        appendix_files (list): List of appendix markdown file paths.
        output_markdown (str): Output markdown file path.
        title (str, optional): Document title.
    """
    print("[INFO] Starting to combine markdown files with proper title page and TOC...")

    with open(output_markdown, "w", encoding="utf-8") as outfile:
        if title:
            # This is the standard Pandoc metadata header
            outfile.write(f"% {title}\n")
            outfile.write("% Joe Eberle\n")
            outfile.write("% July 2025\n\n")
            # Pandoc will automatically insert the TOC after the title page with --toc

        # Write main content
        for md_file in markdown_files:
            print(f"[DEBUG] Adding main module: {md_file}")
            with open(md_file, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n")

        # Write appendices with auto-titles
        for idx, appendix_file in enumerate(appendix_files, start=1):
            module_name = os.path.basename(os.path.dirname(appendix_file)) or os.path.basename(appendix_file)
            module_name = os.path.splitext(module_name)[0]
            print(f"[DEBUG] Adding appendix module: {appendix_file} as Appendix {idx}: {module_name}")
            
            outfile.write(f"# Appendix {idx}: {module_name}\n\n")
            with open(appendix_file, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n")

    print(f"[INFO] Successfully combined {len(markdown_files)} main files and {len(appendix_files)} appendices into {output_markdown}")

def render_with_pandoc(input_markdown, output_file, extra_args=None):
    """
    Call Pandoc to render a markdown file to DOCX or PDF with TOC and numbering.
    Prints stderr on failure for easier debugging.
    """
    pandoc_path = r"C:\Users\josep\AppData\Local\Pandoc\pandoc.exe"
    cmd = [pandoc_path, input_markdown, "-o", output_file, "--toc", "--number-sections"]
    if extra_args:
        cmd.extend(extra_args)

    print(f"[INFO] Running Pandoc to generate {output_file}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[INFO] Created {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Pandoc failed with exit code {e.returncode}")
        print(f"stdout:\n{e.stdout}")
        print(f"stderr:\n{e.stderr}")
        raise

def render_with_pandoc_no_toc(input_markdown, output_file, extra_args=None):
    """
    Same as render_with_pandoc but without a table of contents.
    """
    pandoc_path = r"C:\Users\josep\AppData\Local\Pandoc\pandoc.exe"
    cmd = [pandoc_path, input_markdown, "-o", output_file, "--number-sections"]
    if extra_args:
        cmd.extend(extra_args)

    print(f"[INFO] Running Pandoc (no TOC) to generate {output_file}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[INFO] Created {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Pandoc failed with exit code {e.returncode}")
        print(f"stdout:\n{e.stdout}")
        print(f"stderr:\n{e.stderr}")
        raise

def build_story_document(markdown_files, appendix_files=None, output_markdown="full_story.md",
                         output_docx=None, output_pdf=None, title=None, no_toc=False):
    """
    High-level function to build a full story document, optionally with appendices,
    and render to DOCX or PDF. Now with debug prints for clarity.

    Args:
        markdown_files (list): Main markdown file paths.
        appendix_files (list, optional): Appendix markdown file paths.
        output_markdown (str): Path to combined markdown file.
        output_docx (str, optional): Path to output Word file.
        output_pdf (str, optional): Path to output PDF file.
        title (str, optional): Document title.
        no_toc (bool): If True, omit the table of contents.
    """
    appendix_files = appendix_files or []
    print(f"[INFO] Building story document with {len(markdown_files)} main sections and {len(appendix_files)} appendices.")
    combine_markdown_files_with_appendix(markdown_files, appendix_files, output_markdown, title=title)

    if output_docx:
        if no_toc:
            render_with_pandoc_no_toc(output_markdown, output_docx)
        else:
            render_with_pandoc(output_markdown, output_docx)

    if output_pdf:
        if no_toc:
            render_with_pandoc_no_toc(output_markdown, output_pdf)
        else:
            render_with_pandoc(output_markdown, output_pdf)

