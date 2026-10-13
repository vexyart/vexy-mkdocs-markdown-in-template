# vexy-mkdocs-markdown-in-template

[![CI](https://github.com/vexyart/vexy-mkdocs-markdown-in-template/actions/workflows/ci.yml/badge.svg)](https://github.com/vexyart/vexy-mkdocs-markdown-in-template/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/vexy-mkdocs-markdown-in-template.svg)](https://pypi.org/project/vexy-mkdocs-markdown-in-template/)
[![Python](https://img.shields.io/pypi/pyversions/vexy-mkdocs-markdown-in-template.svg)](https://pypi.org/project/vexy-mkdocs-markdown-in-template/)

**Documentation:** https://vexy.dev/vexy-mkdocs-markdown-in-template/

Write Markdown inside your MkDocs theme's Jinja2 templates.

Theme partials are HTML; your content is Markdown. This plugin lets you write
Markdown right in a template, wrapped in `{% md %} ... {% mdend %}`, and renders it
to HTML while the page builds. The block uses your site's own `markdown_extensions`
and `mdx_configs`, so tables, footnotes, and admonitions behave exactly as they do
in a page body.

## Installation

```bash
pip install vexy-mkdocs-markdown-in-template
```

## Configuration

In `mkdocs.yml`, list the plugin as early as possible so later plugins see the
rendered HTML:

```yaml
plugins:
  - markdown-in-template
```

## Usage

In any HTML template partial, wrap Markdown in `{% md %}` and `{% mdend %}`:

```html
<article>
{% md %}
# Heading

Regular and **bold** text
{% mdend %}
</article>
```

The plugin strips the block's common leading indentation, using the first
non-blank line as the baseline — so you can indent Markdown to line up with the
surrounding HTML without it being read as a code block.

## Development

```bash
pip install -e .[dev]
pytest          # unit + full mkdocs-build integration test
ruff check .    # lint
mypy            # type check
```

## Documentation

Full docs: <https://vexy.dev/vexy-mkdocs-markdown-in-template/>

## License

MIT — see [LICENSE](LICENSE).
