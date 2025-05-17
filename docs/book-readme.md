# Codex Development Guide Book Project

This directory contains the necessary files to generate "The Codex Development Guide" book.

## Overview

The Codex Development Guide is a comprehensive resource for building modern Health Management Systems with the Codex Framework. The book is organized into 6 parts containing 23 chapters that cover everything from system architecture to advanced topics.

## Book Structure

- **6 Parts**: Logical groupings of related chapters
- **23 Chapters**: Detailed explorations of specific topics
- **3 Appendices**: Reference materials and supporting content

## Getting Started

To work with the book compilation system:

1. Ensure you have Python 3.6+ installed
2. Review the `book.json` file to understand the book structure
3. Create or edit chapter content in the `chapters/` directory
4. Run the book compiler to generate the complete book

## Usage

```bash
# Generate placeholder chapters and compile the book
./book_compiler.py

# View the compiled book
open compiled_book/index.md
```

## Book Compiler Features

The `book_compiler.py` script provides the following functionality:

- **Automatic Chapter Generation**: Creates placeholder files for all chapters defined in book.json
- **Navigation Elements**: Adds consistent navigation between chapters
- **Table of Contents**: Generates a comprehensive table of contents
- **Cross-References**: Updates references between chapters
- **Metadata Integration**: Incorporates book metadata into the output
- **Part Organization**: Organizes chapters into logical parts
- **Prerequisite Linking**: Creates links to prerequisite chapters

## Directory Structure

```
/
├── book.json                # Book metadata and structure
├── book_compiler.py         # Compilation script
├── chapters/                # Individual chapter markdown files
└── compiled_book/           # Output directory for compiled book
    ├── index.md             # Table of contents
    ├── part1/               # Part 1 chapters
    ├── part2/               # Part 2 chapters
    └── ...
```

## Adding New Chapters

1. Update the `book.json` file to include the new chapter metadata
2. Run `./book_compiler.py` to generate a placeholder file
3. Edit the generated file in the `chapters/` directory
4. Recompile the book to see the changes

## Output Formats

The primary output is in Markdown format. To convert to other formats:

- **HTML**: Use tools like Pandoc or MkDocs to convert to HTML
- **PDF**: Use Pandoc with a PDF engine like LaTeX
- **EPUB**: Convert using Pandoc or specialized tools

## Contributing

To contribute to the book:

1. Write or update chapter content in the `chapters/` directory
2. Ensure content follows the structure defined by placeholder files
3. Add cross-references to related chapters using the chapter ID in square brackets
4. Run the book compiler to validate your changes

## Metadata Management

The `book.json` file contains all metadata including:

- Book title, subtitle, and author information
- Part and chapter organization
- Chapter prerequisites and key concepts
- Navigation flow between chapters
- Appendix information

Edit this file to update the book structure or metadata.