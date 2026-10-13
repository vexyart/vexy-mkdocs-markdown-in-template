# Troubleshooting

Each entry gives the symptom you see, the cause, and the fix.

## "Encountered unknown tag 'md'"

The build stops with:

```text
jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'md'.
```

**Cause:** a template contains `{% md %}`, but the Jinja2 environment has no
extension for it. The plugin is not active.

**Fix:**

1. Check that `markdown-in-template` is in the `plugins` list of the
   `mkdocs.yml` you are building, and that it does not have `enabled: false`.
2. Check that the package is installed in the Python environment that runs
   `mkdocs`:

    ```bash
    python -c "import mkdocs_markdown_in_template_plugin"
    ```

    If you build with `uvx` or `pipx`, the package must be added to that
    tool's environment, for example with
    `uvx --from mkdocs --with vexy-mkdocs-markdown-in-template mkdocs build`.

## "Jinja was looking for the following tags: 'mdend'"

The build stops with:

```text
jinja2.exceptions.TemplateSyntaxError: Unexpected end of template. Jinja was looking for the following tags: 'mdend'. The innermost block that needs to be closed is 'md'.
```

**Cause:** a `{% md %}` block has no closing tag, or the closing tag is
misspelled. The closing tag is `{% mdend %}`, not `{% endmd %}`.

**Fix:** add or correct the closing tag. The error message shows the template
line where the open block starts.

## "The block renders as a code block"

The Markdown appears inside `<pre><code>` instead of as formatted text.

**Cause:** after dedenting, the text still starts with four or more spaces.
This happens when one line of the block is indented less than the others, or
when the block mixes tabs and spaces. The dedent step removes only the
indentation that all non-blank lines share.

**Fix:** indent every line of the block by at least the same amount, using
spaces only. Lines that are part of nested structures, such as an admonition
body, should be indented further than the baseline, not less.

## "The Markdown is shown literally, not converted"

You see `**bold**` or `# Heading` as text in the built page.

**Cause:** the text is outside a `{% md %}` block, or in a template file that
your theme does not use. A common case: you edited a copy of a template outside
`custom_dir`, or the file name does not match the theme file it should replace.

**Fix:** check that the file is in the folder named by `theme.custom_dir`, at
the same relative path as the theme file it replaces.

## "Admonitions, tables or footnotes are not rendered"

You see `!!! note` as a paragraph, or a footnote marker stays as `[^1]`.

**Cause:** template blocks use only the extensions in `markdown_extensions`.
Tables are always available, because MkDocs always loads `tables`. Admonitions
need `admonition`, footnotes need `footnotes`.

**Fix:** add the extension to `markdown_extensions` in `mkdocs.yml`.

## "A link in a template block is broken"

A link such as `[Guide](guide.md)` leads to a 404 page.

**Cause:** MkDocs rewrites `.md` links only in page Markdown. In a template
block, the link stays `guide.md`.

**Fix:** build the URL with Jinja2, relative to the site root:

```html
{% md %}
[Guide]({{ base_url }}/guide/)
{% mdend %}
```

## "Duplicate ids on the page"

An HTML validator reports duplicate `id` attributes, or a permalink or footnote
link jumps to the wrong place.

**Cause:** headings and footnotes in a template block get ids computed from the
block alone. If the page body has a heading with the same text, or a footnote
with the same number, the ids are the same.

**Fix:** in templates, use heading text that does not appear in pages, and use
named footnotes such as `[^support]`.

## "Text from a Jinja2 variable changes the formatting"

A page title or front matter value with `*`, `_` or `#` changes the formatting
of the block.

**Cause:** Jinja2 inserts the variable before the Markdown is converted, and
the plugin does not escape it. Markdown then reads the characters as syntax.

**Fix:** put the variable outside the `{% md %}` block, or escape the characters
in the source value with a backslash.

## Getting more help

If none of these entries matches, open an issue at
<https://github.com/vexyart/vexy-mkdocs-markdown-in-template/issues>. Include
the template that contains the block, the `markdown_extensions` and `plugins`
sections of `mkdocs.yml`, and the full error message.
