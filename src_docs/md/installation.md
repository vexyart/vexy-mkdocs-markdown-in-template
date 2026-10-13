# Installation

The plugin is a regular Python package. You install it into the same Python
environment that runs MkDocs, then enable it in `mkdocs.yml`.

## Requirements

| Requirement | Version | Source of the requirement |
|---|---|---|
| Python | 3.12 or later | `requires-python` in `pyproject.toml` |
| MkDocs | 1.5.0 or later | `dependencies` in `pyproject.toml` |
| Jinja2 | 3.0.3 or later | `dependencies` in `pyproject.toml` |
| Markdown | 3.3.6 or later | `dependencies` in `pyproject.toml` |

The CI workflow runs the test suite on Python 3.12 and 3.13, on Linux and
Windows. A separate job runs it on Linux with Python 3.12 against MkDocs 1.5.x
and 1.6.x.

## Install the package

The distribution name is `vexy-mkdocs-markdown-in-template`. The import name
is `mkdocs_markdown_in_template_plugin`. The plugin name you use in
`mkdocs.yml` is `markdown-in-template`.

=== "pip"

    ```bash
    pip install vexy-mkdocs-markdown-in-template
    ```

=== "uv"

    ```bash
    uv add vexy-mkdocs-markdown-in-template
    ```

=== "From GitHub"

    ```bash
    pip install "git+https://github.com/vexyart/vexy-mkdocs-markdown-in-template"
    ```

=== "One-off build with uvx"

    ```bash
    uvx --from mkdocs --with vexy-mkdocs-markdown-in-template mkdocs build
    ```

If you install from a local clone, use an editable install so that code changes
take effect without reinstalling:

```bash
git clone https://github.com/vexyart/vexy-mkdocs-markdown-in-template
cd vexy-mkdocs-markdown-in-template
pip install -e .
```

## Check the installation

1. Print the package version:

    ```bash
    python -c "import mkdocs_markdown_in_template_plugin as m; print(m.__version__)"
    ```

    The version comes from the Git tag through `hatch-vcs`, for example `1.0.5`.
    An editable install made before the version file was generated prints
    `0.0.0+local`.

2. Confirm that MkDocs can see the plugin entry point:

    ```bash
    python -c "from importlib.metadata import entry_points; print([e.name for e in entry_points(group='mkdocs.plugins')])"
    ```

    The list contains `markdown-in-template`.

## Enable the plugin

Add the plugin to the `plugins` list in `mkdocs.yml`:

```yaml
plugins:
  - search
  - markdown-in-template
```

!!! note "Keep the search plugin"
    When you define `plugins` in `mkdocs.yml`, MkDocs no longer adds the
    default `search` plugin for you. List `search` again if you want site search.

The plugin has no options. See [Configuration](configuration.md) for the
settings that do change how template Markdown renders.

## Uninstall

```bash
pip uninstall vexy-mkdocs-markdown-in-template
```

Remove `markdown-in-template` from `plugins` at the same time. Any template that
still contains `{% md %}` then fails with
`TemplateSyntaxError: Encountered unknown tag 'md'`.
