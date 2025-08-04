# Method Detail Pages

This document describes the new method detail page system that was implemented for the Bad PDFs.

## Overview

When users search for a method name (like "extract_text") and click on it in the search results, they are now taken to a dedicated page that shows all usages of that method across all PDFs in the gallery.

## Features

### 1. Dynamic Route
- Created a new dynamic route at `/methods/[method].astro`
- Each unique method used across all PDFs gets its own page
- URLs are like `/methods/extract_text`, `/methods/show`, etc.

### 2. Method Usage Display
Each usage shows:
- **PDF document name** - Clickable link to the full PDF page
- **Code snippet with context** - Shows 3 lines before and after the method usage
- **Line numbers** - GitHub-style line numbers with highlighting
- **Link to full example** - "View full example →" link that jumps to the specific code cell

### 3. Visual Design
- **Header** - Purple gradient background matching the site theme
- **Method name** - Large monospace font
- **Usage statistics** - "X usages across Y PDFs"
- **Back link** - "← Back to Gallery" for easy navigation
- **Code highlighting** - The line containing the method call is highlighted
- **Responsive design** - Works well on mobile devices

### 4. Search Integration
Updated the Search component to:
- Link method names to their detail pages
- Show usage count next to each method
- Display up to 2 code snippets inline
- Add "View all X examples →" link for methods with more than 2 usages

### 5. Deep Linking
- PDF detail pages now have anchors on code cells (`#code-0`, `#code-1`, etc.)
- Clicking "View full example" scrolls to the specific code cell
- The existing method highlighting still works with hash fragments

## Technical Implementation

### Data Flow
1. `all_metadata.json` contains method usage information
2. Method detail page loads execution data for each PDF to get code context
3. Searches through code cells to find exact usage locations
4. Extracts surrounding lines for context

### Code Context Extraction
- Finds the exact line containing the method call
- Extracts 3 lines before and after for context
- Preserves line numbers from the original file
- Highlights the specific line containing the method

### Error Handling
- Gracefully handles missing execution data
- Shows "No usages found" message for methods with no examples
- Continues processing even if some PDFs fail to load

## Usage

1. **From Search**: Type a method name in the search box, click on the method name
2. **Direct URL**: Navigate directly to `/methods/[method-name]`
3. **From Method Page**: Click on PDF titles or "View full example" links to explore specific usages

## Future Enhancements

Potential improvements could include:
- Method signature/parameter information
- Grouping by usage pattern
- Filtering by PDF category
- Method documentation links
- Copy code button for snippets