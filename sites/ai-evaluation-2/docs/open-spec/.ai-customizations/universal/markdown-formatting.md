# Markdown Formatting Standards - Universal Application

All modes MUST follow these markdown formatting standards to ensure consistency, compatibility, and professional presentation across all UDX documentation.

## Header Standards

### Prohibited Characters in Headers
Headers MUST NOT contain:
- ❌ Special characters: `! @ # $ % ^ & * ( ) [ ] { } < > ? / \ | ~ ` = +`
- ❌ Emojis: 🚫 😊 ⚠️ ✅ ❌
- ❌ Punctuation at end: `?` `!` `.` `,`
- ❌ Leading numbers with periods: `1.` `2.` (use `1` `2` or spell out)

### Allowed Header Formats
✅ **CORRECT**:
```markdown
# System Architecture
## Component Overview
### API Gateway Design
#### Authentication Flow
```

❌ **INCORRECT**:
```markdown
# System Architecture!
## Component Overview (Draft)
### API Gateway Design?
#### 1. Authentication Flow
```

### Header Hierarchy Rules
- Start with single `#` for document title
- Maximum depth: 4 levels (`####`)
- Maintain logical hierarchy (no skipping levels)
- Use consistent capitalization (Title Case preferred)

## Document Structure

### Standard Sections Order
1. Title (H1)
2. Overview/Introduction
3. Background/Context (if needed)
4. Main Content Sections
5. Implementation/Next Steps
6. References/Appendices

### Section Spacing
- Two blank lines before H1 headers
- One blank line before H2-H4 headers
- One blank line after all headers
- One blank line between paragraphs

## Text Formatting

### Emphasis Standards
- **Bold** for important terms or warnings
- *Italic* for emphasis or first use of terms
- `Code` for technical terms, commands, file names
- ***Bold italic*** sparingly for critical warnings only

### Lists

#### Bulleted Lists
- Use `-` for bullets (not `*` or `+`)
- Maintain consistent indentation (2 spaces)
- One blank line before and after list
- Sub-items indented 2 additional spaces

#### Numbered Lists
- Use `1.` format (not `1)` or `(1)`)
- Let markdown auto-number (all items can be `1.`)
- For sub-items, use letters: `a.`, `b.`, etc.

#### Checklists
- Use `- [ ]` for unchecked items
- Use `- [x]` for checked items
- Maintain consistent spacing

## Code Formatting

### Inline Code
- Use single backticks: `variable_name`
- Include file extensions: `config.yaml`
- For paths: `/usr/local/bin/script.sh`
- For commands: `npm install`

### Code Blocks
Always specify language:
````markdown
```python
def calculate_total(items):
    return sum(items)
```
````

Supported languages:
- `bash` or `shell` for commands
- `yaml` for configuration
- `json` for data structures
- `python`, `javascript`, `java`, etc. for code
- `plaintext` when no syntax highlighting needed

## Tables

### Table Standards
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

Rules:
- Always include header separator
- Align columns with spaces
- Use pipes `|` for all borders
- Keep columns reasonably sized

## Links and References

### Link Formats
- Inline links: `[Display Text](url)`
- Reference links: `[Display Text][ref]` with `[ref]: url` at bottom
- Always use descriptive link text (never "click here")

### File Path References
- Use relative paths when possible
- Forward slashes for all platforms: `docs/api/guide.md`
- Include file extensions
- Use code formatting for paths

## Special Formatting

### Blockquotes
Use for:
- Important notes
- External quotes
- Warnings or cautions

```markdown
> **Note**: This is important information that readers should pay attention to.
```

### Horizontal Rules
- Use only when necessary for major section breaks
- Format: `---` (three hyphens on its own line)
- Include blank line before and after

## Prohibited HTML

Markdown files MUST NOT contain raw HTML tags. HTML breaks rendering in Confluence, VSFlow, and other markdown consumers. Use standard markdown alternatives instead.

| Prohibited HTML | Markdown Alternative |
|----------------|---------------------|
| `<details>` / `<summary>` | Heading + code block, or move content to an appendix section |
| `<br>` | Blank line between paragraphs |
| `<div>` / `<span>` | Standard markdown formatting (bold, italic, headers) |
| `<img>` | `![alt text](path/to/image.png)` |
| `<a>` | `[link text](url)` |
| `<table>` / `<tr>` / `<td>` | Pipe-delimited markdown tables |
| `<b>` / `<i>` / `<em>` / `<strong>` | `**bold**` / `*italic*` |
| `<code>` / `<pre>` | Backticks or fenced code blocks |
| `<hr>` | `---` |

No exceptions. If markdown cannot express the desired layout, simplify the layout.

## File Naming Conventions

### Documentation Files
- Lowercase with hyphens: `api-design-guide.md`
- No spaces or special characters
- Descriptive names: `authentication-flow.md` not `auth.md`
- Date prefix for time-sensitive: `2024-03-15-release-notes.md`

### Directory Structure
```
documentation/
├── guides/
│   ├── getting-started.md
│   └── advanced-configuration.md
├── api/
│   ├── rest-endpoints.md
│   └── graphql-schema.md
└── architecture/
    ├── system-overview.md
    └── component-design.md
```

## Common Mistakes to Avoid

### Headers
- ❌ `## Overview:`  → ✅ `## Overview`
- ❌ `# 1. Introduction` → ✅ `# Introduction`
- ❌ `### API Design!!!` → ✅ `### API Design`

### Formatting
- ❌ Multiple consecutive blank lines
- ❌ Tabs for indentation (use spaces)
- ❌ Trailing whitespace
- ❌ Inconsistent list markers

### Code Blocks
- ❌ No language specified
- ❌ Using indent instead of fences
- ❌ Incorrect language identifier

## Validation Checklist

Before submitting any markdown document:
- [ ] No special characters in headers
- [ ] Consistent header hierarchy
- [ ] Proper spacing between sections
- [ ] Code blocks have language specified
- [ ] File names are lowercase-hyphenated
- [ ] No emojis anywhere
- [ ] Links have descriptive text
- [ ] Tables are properly formatted
- [ ] No trailing whitespace
- [ ] No raw HTML tags (`<details>`, `<div>`, `<br>`, `<img>`, etc.)

---

**Remember**: Clean, consistent markdown formatting ensures documentation remains professional, maintainable, and compatible across all platforms and tools.