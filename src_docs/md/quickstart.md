# Quickstart

This walkthrough adds a Markdown notice above the content of every page in a
site that uses Material for MkDocs. It takes about five minutes.

## Before you start

You need:

- A MkDocs project with an `mkdocs.yml` and a `docs/` folder.
- The `mkdocs-material` theme installed, or another theme that lets you
  override templates (see [step 6](#6-use-another-theme)).
- The plugin installed (see [Installation](installation.md)).

## 1. Enable the plugin

Open `mkdocs.yml` and add `markdown-in-template` to `plugins`:

```yaml
plugins:
  - search
  - markdown-in-template
```

## 2. Point the theme at an overrides folder

MkDocs looks for template overrides in the folder named by `theme.custom_dir`.
The path is relative to `mkdocs.yml`.

```yaml
theme:
  name: material
  custom_dir: overrides
```

Create the folder next to `mkdocs.yml`:

```bash
mkdir overrides
```

## 3. Write a Markdown block in a template

Create `overrides/main.html` with this content:

```html
{% extends "base.html" %}

{% block content %}
  {% md %}
  !!! info "Draft"
      This page belongs to the **{{ config.site_name }}** draft.
      Send corrections to the [issue tracker](https://example.com/issues).
  {% mdend %}
  {{ super() }}
{% endblock %}
```

What each part does:

- `{% extends "base.html" %}` keeps the theme's own layout.
- `{% block content %}` replaces the page content block. `{{ super() }}` puts the
  original page content back after your notice.
- `{% md %}` and `{% mdend %}` mark the text that the plugin converts from
  Markdown to HTML.
- `{{ config.site_name }}` is a normal Jinja2 expression. Jinja2 fills it in
  before the plugin converts the block.
- `!!! info` is an admonition. It renders only if `admonition` is in your
  `markdown_extensions` (step 4).

## 4. Enable the Markdown extensions the block uses

The block is converted with the extensions listed in `mkdocs.yml`. Add
`admonition` so the `!!! info` line works:

```yaml
markdown_extensions:
  - admonition
```

## 5. Build and check the result

1. Build the site:

    ```bash
    mkdocs build
    ```

2. Open `site/index.html` in a browser.

Every page now starts with a "Draft" info box that contains the site name and a
link. In the HTML source, the box is a `<div class="admonition info">` element,
the same markup MkDocs produces for an admonition in a page body.

## 6. Use another theme

The plugin works with any theme, because it adds a tag to the Jinja2
environment rather than changing a theme. What differs between themes is the
name of the template blocks you can override. Look in the theme's `base.html`
or `main.html` for `{% block ... %}` names. For example, the built-in `mkdocs`
theme has a `content` block in `base.html`.

## Next steps

- Learn the indentation and nesting rules in [Usage](usage.md).
- Copy more overrides from [Examples](examples.md).
