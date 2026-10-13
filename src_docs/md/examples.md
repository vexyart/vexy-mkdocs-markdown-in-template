# Examples

Each example below is a complete template file. Put it in your `custom_dir`
folder (see [Configuration](configuration.md#theme-overrides-folder)) at the
path given in its heading. All examples were built with the plugin enabled.

## Announcement bar in MaterialX

This site shows a bar at the top of every page. Its source is
`src_docs/overrides/main.html` in this repository:

```html
{% extends "base.html" %}

{% block announce %}
  {% md %}
  This bar is Markdown in `src_docs/overrides/main.html`, rendered by the
  **markdown-in-template** plugin. [See how it is built]({{ base_url }}/examples/#announcement-bar-in-materialx).
  {% mdend %}
{% endblock %}
```

How it works:

- `announce` is an empty block in the `base.html` of Material for MkDocs and
  MaterialX. The theme shows the announcement bar only when the block has
  content.
- `{{ base_url }}` makes the link work from every page, because Jinja2 replaces
  it with the relative path to the site root before the Markdown is converted.
- The backticks and asterisks become `<code>` and `<strong>`, as in a page.

## Notice from page front matter

File: `overrides/main.html`

This override shows a note above the content of any page whose front matter
has a `notice` key.

```html
{% extends "base.html" %}

{% block content %}
  {% if page.meta.notice %}
    {% md %}
    !!! note
        {{ page.meta.notice }}
    {% mdend %}
  {% endif %}
  {{ super() }}
{% endblock %}
```

A page that uses it:

```markdown
---
notice: "This page describes the **1.x** API. See [2.x](https://example.com/2/)."
---
# API
```

The rendered note:

```html
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>This page describes the <strong>1.x</strong> API. See <a href="https://example.com/2/">2.x</a>.</p>
</div>
```

The front matter value is plain text, but because it goes through the Markdown
block, the `**1.x**` and the link are rendered. The `!!! note` line needs the
`admonition` extension in `markdown_extensions`.

## Footer text with a licence link

File: `overrides/partials/copyright.html`

Material for MkDocs prints `config.copyright` in the footer as-is. This
override writes the footer line in Markdown and adds a licence link:

```html
<div class="md-copyright">
  {% md %}
  {{ config.copyright }} Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Built with [MkDocs](https://www.mkdocs.org/) and *markdown-in-template*.
  {% mdend %}
</div>
```

With `copyright: "Copyright &copy; 2026 Example Ltd."` in `mkdocs.yml`, the
footer contains:

```html
<div class="md-copyright">
  <p>Copyright &copy; 2026 Example Ltd. Licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
Built with <a href="https://www.mkdocs.org/">MkDocs</a> and <em>markdown-in-template</em>.</p>
</div>
```

Replacing `partials/copyright.html` removes the theme's own "Made with" line,
because your file replaces the whole partial.

## Shared text in an included partial

Files: `overrides/main.html` and `overrides/partials/support.html`

A block works in a partial that another template includes. This lets you keep
reusable Markdown in one file.

`overrides/partials/support.html`:

```html
{% md %}
---

Questions? Open an issue on [GitHub](https://github.com/example/project/issues)[^1].

[^1]: You need a GitHub account.
{% mdend %}
```

`overrides/main.html`:

```html
{% extends "base.html" %}

{% block content %}
  {{ super() }}
  {% include "partials/support.html" %}
{% endblock %}
```

The footnote renders as a normal footnote list under the paragraph, because
`footnotes` is in `markdown_extensions`. The footnote ids (`fn:1`, `fnref:1`)
are computed for the block alone. If the page body also has a footnote 1, the
page contains the same ids twice and the links jump to the first one. Use a
named footnote such as `[^support]` in templates to avoid the clash.

## Minimal theme template

File: `theme/main.html`, with `theme: {name: null, custom_dir: theme}`

The plugin does not depend on any theme. The project's integration test builds
a site whose only template is this file:

```html
<!doctype html><html><body>
{% md %}
# Injected

Regular and **bold** text.
{% mdend %}
</body></html>
```

The built `index.html` contains `<h1 id="injected">Injected</h1>` and
`<strong>bold</strong>`.
