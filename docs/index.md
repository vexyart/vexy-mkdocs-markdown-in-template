---
title: Home
layout: default
nav_order: 1
---

# vexy-mkdocs-markdown-in-template

Theme templates are HTML. Your content is Markdown. The seam between them is where
`<p>` tags and `&mdash;` entities creep into files that used to read cleanly. This
plugin removes the seam: write Markdown right inside a Jinja2 partial, wrapped in
`{% md %} ... {% mdend %}`, and it renders to HTML while the page builds.

The block uses your site's own `markdown_extensions` and `mdx_configs`, so a table
or a footnote behaves exactly as it does on a normal page.

## Install

```bash
pip install vexy-mkdocs-markdown-in-template
```

## Enable

In `mkdocs.yml`, list the plugin as early as possible so other plugins see the
rendered HTML:

```yaml
plugins:
  - markdown-in-template
```

## Use

In any theme partial (`main.html`, a `base.html` override, a custom block), wrap
Markdown in the tag pair:

```html
<article>
{% md %}
# Heading

Regular and **bold** text, a [link](https://example.com), and a list:

- one
- two
{% mdend %}
</article>
```

That renders to the same HTML MkDocs would produce for the same Markdown in a page
body.

## Indentation

Templates are usually indented to match the surrounding HTML. The plugin strips
the common leading indentation of the block before rendering, using the first
non-blank line as the baseline — so indenting your Markdown to line up with the
HTML around it does not turn it into a code block.

## Links

- [Source on GitHub](https://github.com/vexyart/vexy-mkdocs-markdown-in-template)
- [Package on PyPI](https://pypi.org/project/vexy-mkdocs-markdown-in-template/)
- [Changelog](https://github.com/vexyart/vexy-mkdocs-markdown-in-template/blob/main/CHANGELOG.md)
