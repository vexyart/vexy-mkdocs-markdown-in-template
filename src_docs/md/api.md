# API reference

You do not call the plugin's Python API to use it; MkDocs does. This page is
for contributors and for anyone who wants to reuse the Jinja2 extension outside
MkDocs.

## Package `mkdocs_markdown_in_template_plugin`

### `__version__`

```python
from mkdocs_markdown_in_template_plugin import __version__
```

A string with the package version. At build time, `hatch-vcs` writes it into
the generated module `mkdocs_markdown_in_template_plugin/__version__.py` from
the Git tag. If that module does not exist, for example in an editable install
made before the first build, `__version__` is `"0.0.0+local"`.

## Module `mkdocs_markdown_in_template_plugin.plugin`

### `class MarkdownInTemplatePlugin(BasePlugin)`

The MkDocs plugin, registered under the name `markdown-in-template`.

`config_scheme = ()`
:   The plugin has no configuration options.

`on_env(env, config, files) -> Environment`
:   MkDocs event handler. Stores `config.get("markdown_extensions", [])` and
    `config.get("mdx_configs", {})` in `env.globals`, calls
    `env.add_extension(MarkdownJinjaExtension)`, and returns the same `env`
    object.

    | Parameter | Type | Description |
    |---|---|---|
    | `env` | `jinja2.Environment` | The theme's template environment. |
    | `config` | `mkdocs.config.Config` | The loaded site configuration. |
    | `files` | `mkdocs.structure.files.Files` | The site's files. Not used. |

### `class MarkdownJinjaExtension(Extension)`

A Jinja2 extension that adds the `{% md %} ... {% mdend %}` block tag.

`tags = {"md"}`
:   The tag names this extension handles.

`__init__(env)`
:   Reads two globals from `env` and creates a `markdown.Markdown` instance:

    | Global | Default | Passed to `markdown.Markdown` as |
    |---|---|---|
    | `mkdocs_markdown_in_template_plugin_markdown_extensions` | `[]` | `extensions` |
    | `mkdocs_markdown_in_template_plugin_mdx_configs` | `{}` | `extension_configs` |

    Stores the instance as `self.markdowner` and on the environment with
    `env.extend(markdowner=...)`.

`parse(parser) -> Node | list[Node]`
:   Called by Jinja2 for each `{% md %}` tag. Parses the body up to
    `{% mdend %}` and returns a `jinja2.nodes.CallBlock` that calls
    `_render_markdown` at render time.

`_render_markdown(caller) -> str`
:   Calls `caller()` to render the body, dedents it with `_dedent`, resets
    `self.markdowner`, and returns `self.markdowner.convert(text)`.

`_dedent(text) -> str` (static method)
:   Returns `textwrap.dedent(text.strip("\n"))`: blank lines at both ends are
    removed, then the common leading whitespace of all lines.

## Using the extension without MkDocs

The extension works in any Jinja2 environment. Set the two globals before you
add it, because `__init__` reads them:

```python
from jinja2 import Environment

from mkdocs_markdown_in_template_plugin.plugin import MarkdownJinjaExtension

env = Environment()
env.globals["mkdocs_markdown_in_template_plugin_markdown_extensions"] = ["tables"]
env.globals["mkdocs_markdown_in_template_plugin_mdx_configs"] = {}
env.add_extension(MarkdownJinjaExtension)

template = env.from_string(
    "<main>\n"
    "  {% md %}\n"
    "  # {{ title }}\n"
    "\n"
    "  | Key | Value |\n"
    "  |-----|-------|\n"
    "  | a   | 1     |\n"
    "  {% mdend %}\n"
    "</main>"
)
print(template.render(title="Report"))
```

Output:

```html
<main>
  <h1>Report</h1>
<table>
<thead>
<tr>
<th>Key</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>a</td>
<td>1</td>
</tr>
</tbody>
</table>
</main>
```

Without the globals, the extension uses no Markdown extensions, so tables and
other extended syntax are not converted.

The `_render_markdown` and `_dedent` methods have a leading underscore. Treat
them as internal: the tests call them directly, but their names and signatures
may change.
