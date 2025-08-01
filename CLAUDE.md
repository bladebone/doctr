# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple PDF translation utility that overlays translated text onto existing PDF documents while preserving the original layout and positioning. The project consists of a single Python script that uses PyMuPDF (fitz) to manipulate PDF files.

## Architecture

The codebase contains:
- `tr_only_text.py`: Main translation function that extracts text from PDF pages, applies translation, and overlays the translated text while maintaining original positioning
- `fonts/`: Directory containing Korean font files (NotoSansKR-Regular.otf) for proper text rendering
- Sample PDFs for testing the translation functionality

## Core Functionality

The `translate_pdf_overlay()` function:
1. Opens a PDF document using PyMuPDF
2. Extracts text blocks with position information
3. Applies a translation function to each text span
4. Covers original text with white rectangles
5. Inserts translated text at the same position using specified fonts
6. Saves the result as a new PDF with "_translated" suffix

## Dependencies

The project requires:
- `PyMuPDF` (fitz) for PDF manipulation
- Korean font file (NotoSansKR-Regular.otf) for proper text rendering

## Running the Code

To run the translation:
```bash
python tr_only_text.py
```

The script is currently configured to translate "1.pdf" and output "1_translated.pdf" using a simple lambda function that returns "번역됨" for all text.

## Development Notes

- The script includes error handling for missing fonts and font insertion failures
- Text positioning uses baseline calculations to maintain proper alignment
- The translation function can be easily swapped by modifying the lambda function passed to `translate_pdf_overlay()`