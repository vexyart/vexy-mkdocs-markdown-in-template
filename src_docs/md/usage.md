# Usage

This page describes the `{% md %}` block: where you can use it, what happens to
the text inside it, and which rules it follows.

## Block syntax

A Markdown block starts with `{% md %}` and ends with `{% mdend %}`:

```html
{% md %}
Markdown text
{% mdend %}
```

The tag takes no arguments. The closing tag is `mdend`, not `endmd`.

You can use the block in any template that MkDocs renders with the theme's
Jinja2 environment:

- `main.html` and other templates in your `custom_dir`
- partials pulled in with `{% include %}`
- inside `{% block %}` overrides of a parent template
- inside `{% if %}` and `{% for %}` statements

## Processing order

For each block, at the moment the template renders, the plugin does this:

1. **Jinja2 renders the body.** Variables, filters, `{% if %}` tests and loops
   inside the block run first. The plugin receives plain text.
2. **The text is dedented.** Blank lines at the start and end are removed, and
   the indentation common to all lines is stripped.
3. **The Markdown converter is reset.** State from the previous block, such as
   footnotes and reference links, is cleared.
4. **The text is converted to HTML** with the site's Markdown extensions.
5. **The HTML replaces the block** in the template output.

Follow one block through these steps. The template contains:

```html
<footer>
    {% md %}
    Built with **{{ config.site_name }}**.
    {% mdend %}
</footer>
```

With `site_name: Demo`, step 1 produces `"\n    Built with **Demo**.\n    "`.
Step 2 turns it into `Built with **Demo**.`. Step 4 produces:

```html
<p>Built with <strong>Demo</strong>.</p>
```

## Indentation

Template files are usually indented to show the HTML structure. In Markdown,
four spaces of indentation start a code block. To let you indent freely, the
plugin removes the indentation that all lines of the block share.

The baseline is the common indentation of the non-blank lines. After leading
blank lines are removed, the first line of text is usually where that baseline
shows. Lines indented further than the baseline keep their extra indentation,
so nested lists and admonition bodies still work:

```html
<div class="notice">
    {% md %}
    !!! warning
        Indented by four more spaces: this is the admonition body.

    - item
        - nested item
    {% mdend %}
</div>
```

!!! warning "Mixed tabs and spaces"
    The dedent step uses Python's `textwrap.dedent`. It treats a tab and spaces
    as different characters, so a block that mixes them may keep its
    indentation and render as a code block. Use spaces in templates that
    contain Markdown blocks.

## Jinja2 inside the block

Because Jinja2 renders the body before conversion, you can build Markdown from
template data:

```html
{% if page.parent %}
{% md %}
## Pages in this section

{% for nav_item in page.parent.children %}
- [{{ nav_item.title }}]({{ nav_item.url | url }})
{%- endfor %}
{% mdend %}
{% endif %}
```

The `-` in `{%- endfor %}` removes the newline at the end of each loop pass.
Without it, the loop leaves a blank line between items, and Markdown renders a
loose list with every item wrapped in `<p>`.

Two consequences follow:

- Text that Jinja2 outputs is not escaped by the plugin. If a variable contains
  `*` or `_`, Markdown reads those characters as formatting.
- Jinja2 syntax in the block is never shown literally. To print `{{` in the
  output, use Jinja2's own escaping, such as `{{ '{{' }}` or a
  `{% raw %} ... {% endraw %}` section.

## Links and images

Page Markdown and template Markdown handle links differently:

- In a page, MkDocs rewrites a link such as `[Usage](usage.md)` to the URL of
  the built page.
- In a template block, the plugin converts the link as written. `usage.md` stays
  `usage.md` in the HTML, which is a broken link on the built site.

In template blocks, build URLs with Jinja2 instead:

```html
{% md %}
[Read the usage guide]({{ base_url }}/usage/)
{% mdend %}
```

`base_url` is the relative path from the current page to the site root. For
paths to files in `docs/`, MkDocs also provides the `url` filter, for example
`{{ 'assets/logo.png' | url }}`.

## Headings and anchors

If `toc` is active (MkDocs always loads it), a heading in a block gets an `id`
attribute, and a permalink if `toc` is configured with `permalink: true`. The
id is computed from the block alone. A heading with the same text in the page
body gets the same id, so the page then contains a duplicate id. Use different
heading text in templates, or use bold text instead of a heading.

Headings in a template block do not appear in the page's table of contents.
The table of contents comes from the page body.

## Several blocks on one page

A template can contain any number of blocks. Each block is converted on its
own. The converter is reset before each block, so a footnote defined in one
block is not printed again under the next one. A footnote reference and its
definition must be in the same block.
