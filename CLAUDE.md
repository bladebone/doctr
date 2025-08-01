# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PDF translation utility that overlays translated text onto existing PDF documents while preserving the original layout and positioning. The project uses PyMuPDF (fitz) for PDF manipulation and integrates with the Anthropic Claude API for text translation.

## Setup and Dependencies

Install dependencies:
```bash
pip install -r requirements.txt
```

Required environment setup:
- Create a `.env` file with `ANTHROPIC_API_KEY` for Claude API access
- Korean font file `fonts/NotoSerifKR-Regular.ttf` must be present for proper text rendering

## Architecture

The codebase structure:
- `tr_only_text.py`: Main script containing PDF processing and translation logic
- `fonts/NotoSerifKR-Regular.ttf`: Korean font for translated text rendering
- `.env`: Environment variables (ANTHROPIC_API_KEY)
- `requirements.txt`: Python dependencies (PyMuPDF, dotenv, anthropic)

## Core Functions

**`translate_pdf_overlay(pdf_path, translator_func)`**: Main function that processes PDF pages by extracting text blocks with position information, applying translation, covering original text with white rectangles, and overlaying translated text at the same positions.

**`translate_with_claude(text)`**: Translation function using Claude API (claude-3-haiku-20240307 model) that translates text to Korean with error handling for API failures.

## Running the Code

Execute the translation process:
```bash
python tr_only_text.py
```

The script processes "1.pdf" and outputs "1_translated.pdf" using Claude API for translation.

## Development Notes

- Text positioning uses baseline calculations (`rect.y1 - 2`) for proper alignment
- Fallback to "TRANSLATED" text if font insertion fails
- Font objects are created using `fitz.Font(fontfile=font_path)`
- API key assertion ensures environment is properly configured