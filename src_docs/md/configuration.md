# Configuration

The plugin has no options of its own. Its behaviour is controlled by three parts
of `mkdocs.yml` that you already use: the `plugins` list, `markdown_extensions`,
and `theme.custom_dir`.

## Plugin entry

```yaml
plugins:
  - markdown-in-template
```

The plugin class defines an empty `config_scheme`, so it accepts no keys of
its own. If you write one, for example:

```yaml
plugins:
  - markdown-in-template:
      foo: false
```

MkDocs prints
`Plugin 'markdown-in-template' option 'foo': Unrecognised configuration name: foo`.
That is a warning in a normal build and stops the build with
`mkdocs build --strict`.

### Turning the plugin off

MkDocs 1.6 accepts a generic `enabled` key for every plugin that does not define
its own:

```yaml
plugins:
  - markdown-in-template:
      enabled: false
```

With the plugin off, any template that contains `{% md %}` fails to compile.
Disable the plugin only together with the templates that use it. MkDocs 1.5 has
no generic `enabled` key; remove the plugin from the list instead.

### Position in the list

The README recommends that you list the plugin early. The plugin acts in the
`on_env` event. MkDocs fires it once per build, after it has converted the
Markdown of every page and before it renders any page template. The block
conversion then happens while each template renders. By the time other plugins see the page HTML, for example in
`on_post_page`, the Markdown blocks are already HTML.

## Markdown extensions

Template Markdown is converted with the extensions in `markdown_extensions` and
their settings. The plugin reads both values from the MkDocs configuration:

| MkDocs config value | What the plugin uses it for |
|---|---|
| `markdown_extensions` | The list of extensions passed to `markdown.Markdown(extensions=...)` |
| `mdx_configs` | The per-extension settings passed as `extension_configs=...` |

`mdx_configs` is not a key you write. MkDocs builds it from the settings you put
under each extension in `markdown_extensions`.

MkDocs always adds three extensions to the list, even if you do not name them:
`toc`, `tables` and `fenced_code`. Template blocks therefore support tables and
fenced code blocks, and their headings get `id` attributes, in every site.

For this configuration:

```yaml
markdown_extensions:
  - admonition
  - toc:
      permalink: true
```

the plugin passes these values to Python-Markdown:

```python
extensions = ["toc", "tables", "fenced_code", "admonition"]
extension_configs = {"toc": {"permalink": True}}
```

A heading in a template block then gets a `¶` permalink, the same as a heading
in a page.

### Links in template blocks

MkDocs rewrites links such as `[Usage](usage.md)` only in page Markdown. In a
template block, links are converted as written. See
[Links and images](usage.md#links-and-images) for how to build working URLs.

## Theme overrides folder

To add a Markdown block to a theme, you override one of its templates. MkDocs
reads overrides from `theme.custom_dir`:

```yaml
theme:
  name: material
  custom_dir: overrides
```

The folder path is relative to `mkdocs.yml`. A file in it replaces the theme
file with the same relative path. For example, `overrides/main.html` replaces
the theme's `main.html`, and `overrides/partials/footer.html` replaces the
theme's footer partial.

If you build a theme of your own, you can put `{% md %}` blocks directly in the
theme's templates. The plugin must then be enabled in every site that uses the
theme, or the templates fail to compile.

## Configuration of this site

This documentation site uses the plugin itself. The relevant parts of its
`src_docs/mkdocs.yml`:

```yaml
theme:
  name: materialx
  custom_dir: overrides
plugins:
  - search
  - markdown-in-template
```

`src_docs/build.sh` installs the plugin from the repository root with
`uvx ... --with ..`, so the site is always built with the current source.
