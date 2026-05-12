# this_file: mkdocs_markdown_in_template_plugin/__init__.py
"""vexy-mkdocs-markdown-in-template: use Markdown inside the theme's Jinja2 templates."""

try:
    from mkdocs_markdown_in_template_plugin.__version__ import __version__
except ImportError:  # editable install before hatch-vcs has run
    __version__ = "0.0.0+local"

__all__ = ["__version__"]
