# Examples

This directory will contain beautiful example presentations in the future.

## Generate Your Own Examples

You can generate your own examples using SlideDown:

```bash
# Create a simple presentation
python slidedown.py your_notes.md --theme clean

# Try different themes
python slidedown.py document.md --theme cyberpunk
python slidedown.py document.md --theme dark
python slidedown.py document.md --theme light

# Add custom footer
python slidedown.py slides.md --theme clean --footer "© 2026 Your Name"
```

## Sample Markdown

Create a file `demo.md`:

```markdown
# My Presentation

Welcome to SlideDown

## Introduction

- Point 1
- Point 2
- Point 3

## Code Example

​```python
def hello():
    print("Hello, SlideDown!")
​```

## Conclusion

Thank you for watching!
```

Then convert it:

```bash
python slidedown.py demo.md demo.html --theme clean
open demo.html
```

Enjoy creating beautiful presentations!
