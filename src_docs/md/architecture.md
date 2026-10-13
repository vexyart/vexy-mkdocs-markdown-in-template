# How it works

The whole plugin is one module, `mkdocs_markdown_in_template_plugin/plugin.py`,
with two classes. This page follows a build from start to end and shows where
each class acts.

## The two classes

| Class | Base class | Job |
|---|---|---|
| `MarkdownInTemplatePlugin` | `mkdocs.plugins.BasePlugin` | Hooks into the MkDocs build and adds the Jinja2 extension to the theme environment. |
| `MarkdownJinjaExtension` | `jinja2.ext.Extension` | Defines the `md` tag, captures the block body and converts it to HTML. |

MkDocs finds the plugin class through the entry point declared in
`pyproject.toml`:

```toml
[project.entry-points."mkdocs.plugins"]
markdown-in-template = "mkdocs_markdown_in_template_plugin.plugin:MarkdownInTemplatePlugin"
```

## Build sequence

```text
mkdocs build
 │
 ├─ load mkdocs.yml ──────────────► markdown_extensions, mdx_configs
 ├─ convert every page's Markdown
 ├─ create the theme's Jinja2 environment
 ├─ on_env  (MarkdownInTemplatePlugin)
 │     ├─ env.globals[...markdown_extensions] = config["markdown_extensions"]
 │     ├─ env.globals[...mdx_configs]         = config["mdx_configs"]
 │     └─ env.add_extension(MarkdownJinjaExtension)
 │            └─ __init__: create one markdown.Markdown instance
 └─ render each page's template
       ├─ Jinja2 compiles templates; parse() turns {% md %}…{% mdend %} into a CallBlock
       └─ at render time: _render_markdown(caller)
             ├─ caller()      → body text, Jinja2 already applied
             ├─ _dedent()     → blank lines trimmed, common indent removed
             ├─ reset()       → converter state cleared
             └─ convert()     → HTML string inserted into the page
```

## Step 1: passing the Markdown settings to the extension

Jinja2 creates extension objects itself when you call `env.add_extension()`.
The extension's constructor receives only the environment, not the MkDocs
configuration. To get the site's Markdown settings into the extension, the
plugin stores them in the environment globals first, under two keys:

- `mkdocs_markdown_in_template_plugin_markdown_extensions`
- `mkdocs_markdown_in_template_plugin_mdx_configs`

`MarkdownJinjaExtension.__init__` reads both keys, with an empty list and an
empty dict as defaults, and creates a `markdown.Markdown` object from them. It
also attaches that object to the environment with
`env.extend(markdowner=...)`, so it is reachable as `env.markdowner`.

Because the values are globals, templates can also read them, for example
`{{ mkdocs_markdown_in_template_plugin_markdown_extensions }}`. This is a side
effect of the design, not a supported interface.

## Step 2: parsing the block

`MarkdownJinjaExtension.tags` is `{"md"}`, so Jinja2 calls the extension's
`parse()` method when it meets `{% md %}`. The method:

1. Reads the `md` token and remembers its line number.
2. Parses everything up to `{% mdend %}` as normal template content, with
   `parser.parse_statements(("name:mdend",), drop_needle=True)`.
3. Returns a `CallBlock` node that calls `_render_markdown` with the parsed body.

Since the body is parsed as template content, it may contain any Jinja2
statements and expressions. They run when the template renders.

## Step 3: rendering the block

At render time, Jinja2 calls `_render_markdown(caller)`. `caller()` renders the
body and returns its text. Then:

1. `_dedent()` calls `textwrap.dedent(text.strip("\n"))`.
2. `self.markdowner.reset()` clears per-document state such as footnotes and
   reference definitions.
3. `self.markdowner.convert(text)` returns the HTML.

The returned string replaces the block in the template output.

## Design choices

**One converter per build.** The converter is created once, when the extension
is added, and reused for every block. The source describes this as matching
how MkDocs renders page bodies. The `reset()` call before each block makes
reuse safe. Version 1.0.5 added that call; before it, footnotes
leaked from one block into the next.

**The site's extensions, not a separate list.** Reusing `markdown_extensions`
means template text renders like page text, and you configure extensions in
one place. The trade-off is that you cannot give template blocks a different
extension set.

**No link rewriting.** MkDocs rewrites relative links in page Markdown with
processors it adds per page. The plugin's converter does not have those
processors, so links in blocks are left as written.

## What the plugin does not do

- It does not read or change page Markdown. It only acts on templates.
- It does not add template filters or global functions other than the two
  settings globals described above.
- It does not cache the HTML of a block between pages. A block in `main.html`
  is converted again for every page.
