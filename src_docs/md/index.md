# vexy-mkdocs-markdown-in-template

`vexy-mkdocs-markdown-in-template` is a MkDocs plugin that lets you write Markdown
inside the Jinja2 template files of your theme. You wrap the Markdown in a
`{% md %} ... {% mdend %}` block, and the plugin converts it to HTML while MkDocs
renders the page.

Theme templates are HTML. Your content is Markdown. Without the plugin, any
text you put in a template override — an announcement bar, a footer note, a
notice above every page — must be written as hand-made HTML. With the plugin,
you write that text in the same Markdown you use for your pages.

## What it does

Here is a template override with one Markdown block:

```html
{% extends "base.html" %}

{% block announce %}
  {% md %}
  Version 2 is out. Read the **[upgrade notes]({{ base_url }}/upgrade/)**.
  {% mdend %}
{% endblock %}
```

When MkDocs renders a page with this template, three things happen in order:

1. Jinja2 renders the block body. `{{ base_url }}` becomes the relative path to
   the site root: `.` on the home page, `..` on a page one level down.
2. The plugin removes the common leading indentation from the block, so the
   two-space indent does not turn the text into a Markdown code block.
3. The plugin converts the text to HTML with the same Markdown extensions that
   your `mkdocs.yml` lists under `markdown_extensions`.

On a page one level down, the result is:

```html
<p>Version 2 is out. Read the <strong><a href="../upgrade/">upgrade notes</a></strong>.</p>
```

The announcement bar at the top of this site is built this way. Its source is
in [Examples](examples.md#announcement-bar-in-materialx).

## Key facts

- The tag pair is `{% md %}` to open and `{% mdend %}` to close.
- The plugin has no configuration options. You enable it by name:
  `markdown-in-template`.
- Template Markdown uses your site's `markdown_extensions` and their settings,
  so tables, admonitions and footnotes work the same way as in page bodies.
- The plugin resets its Markdown converter before each block, so footnotes from
  one block do not appear in the next one.
- The package needs Python 3.12 or later and MkDocs 1.5 or later.

## Where to go next

| If you want to | Read |
|---|---|
| Install the package | [Installation](installation.md) |
| Add a first Markdown block to a theme | [Quickstart](quickstart.md) |
| Learn the block syntax and its rules | [Usage](usage.md) |
| See which settings affect template Markdown | [Configuration](configuration.md) |
| Copy a working override | [Examples](examples.md) |
| Understand the mechanism | [How it works](architecture.md) |
| Look up the classes and methods | [API reference](api.md) |
| Fix a build error | [Troubleshooting](troubleshooting.md) |
| Run the tests or change the code | [Contributing](contributing.md) |

## Project links

- Source: <https://github.com/vexyart/vexy-mkdocs-markdown-in-template>
- Issues: <https://github.com/vexyart/vexy-mkdocs-markdown-in-template/issues>
- Licence: MIT
