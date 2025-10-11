# DotFlow

A Python-based DOT language interpreter with multiple API styles for creating flowcharts and diagrams effortlessly.

## Features

- **Multiple API Styles**: Pythonic, natural language, and textual DSL
- **Auto-shapes**: Predefined shapes for common elements
- **Clustering**: Group nodes logically
- **Themes**: Built-in color schemes
- **Export**: PNG, SVG, PDF and DOT file export

## Installation

```bash
pip install dotflow
```

## Quick Start

```python
from dotflow import Flow, create_flow

# Pythonic API
flow = create_flow("my_flow")
(flow.start("Start")
     .process("Process Data")
     .decision("Valid?")
     .connect("Valid?", "End", label="Yes")
     .connect("Valid?", "Process Data", label="No"))

flow.render("png", "my_flow.png")
```

## API Styles

### Pythonic API
```python
flow.process("A").connect("A", "B", label="Next")
```

### Natural Language
```python
flow >> "A" >> "B" | "Label"
```

### Textual DSL
```python
flow.parse_dsl("""
A -> B : Label
B -> C
""")
```

## Command Line Interface

DotFlow provides a powerful CLI for generating diagrams without writing Python code.

### Basic Usage

```bash
# Generate from DSL text
dotflow generate diagram.png --dsl-text "Start -> Process -> End"

# Generate from DSL file
dotflow generate diagram.svg --dsl-file workflow.dsl --theme dark

# Generate DOT file
dotflow generate workflow.dot --dsl-file workflow.dsl --format dot
```

Interactive Wizard

```bash
# Interactive flow creation
dotflow wizard my_flow.png --interactive

# Quick sample flow
dotflow wizard sample.png
```

Validation

```bash
# Validate DSL syntax
dotflow validate workflow.dsl
```

Examples

```bash
# Generate example diagrams
dotflow examples --format svg --theme blue

# Generate DSL cheat sheet
dotflow cheat-sheet
```

Themes

```bash
# List available themes
dotflow themes
```

DSL Syntax

The textual DSL supports:

```
# Comments
Start -> Process -> End
A -> B : Label
Decision {decision} -> Yes : Approved
Node [shape=rect, label='Custom']
```

```

## Usage Examples

1. **Install the package**:
```bash
pip install -e .
```

1. Basic CLI usage:

```bash
# Generate a simple flow
dotflow generate my_diagram.png --dsl-text "Start -> Process -> Decision -> End"

# Use interactive wizard
dotflow wizard my_flow.png --interactive

# Validate DSL file
dotflow validate my_workflow.dsl

# Generate all examples
dotflow examples --format svg
```

1. Using as Python module:

```bash
python -m dotflow generate diagram.png --dsl-text "A -> B -> C"
```

This CLI implementation provides:

· Multiple Commands: generate, wizard, validate, themes, examples, cheat-sheet
· Interactive Mode: Build flows step-by-step
· Comprehensive Validation: DSL syntax checking
· Theme Support: All available themes accessible via CLI
· Example Generation: Pre-built example diagrams
· Error Handling: Robust error messages and exit codes
· Testing: Complete test suite for CLI functionality
· Flexible Output: Multiple formats (PNG, SVG, PDF, DOT)

The CLI makes the package accessible to users who prefer command-line tools or want to integrate diagram generation into scripts and automation workflows.

## Documentation
See full [documentation](https://dotflow.readthedocs.io/) for advanced usage.


## License
- This product is licensed under MIT license see [license](./LICENSE)

## 🆘 Support

- 📚 [Documentation](https://github.com/skye-cyber/dotflow/docs)
- 🐛 [Issue Tracker](https://github.com/skye-cyber/dotflow/issues)
- 💬 [Discussions](https://github.com/skye-cyber/dotflow/discussions)

---
