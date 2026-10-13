# Contributing

This page explains how to set up the project, run the checks that CI runs,
build the documentation and the package, and make a release.

## Repository layout

| Path | Contents |
|---|---|
| `mkdocs_markdown_in_template_plugin/plugin.py` | The plugin and the Jinja2 extension |
| `mkdocs_markdown_in_template_plugin/__init__.py` | Exposes `__version__` |
| `tests/test_plugin.py` | Unit tests and a full `mkdocs build` integration test |
| `src_docs/md/` | Documentation source (this site) |
| `src_docs/mkdocs.yml` | Documentation configuration |
| `src_docs/overrides/` | Theme override that uses the plugin |
| `docs/` | Built documentation, served by GitHub Pages. Do not edit by hand. |
| `build.sh` | Builds the documentation and the package |
| `publish.sh` | Tags a release and uploads it to PyPI |
| `.github/workflows/` | CI, documentation and release workflows |

## Set up a development environment

Prerequisites: Git, Python 3.12 or later, and optionally
[uv](https://docs.astral.sh/uv/).

1. Clone the repository with its tags. `hatch-vcs` needs the tags to compute
   the version.

    ```bash
    git clone https://github.com/vexyart/vexy-mkdocs-markdown-in-template
    cd vexy-mkdocs-markdown-in-template
    ```

2. Install the package in editable mode with the `dev` extra:

    ```bash
    pip install -e ".[dev]"
    ```

    The `dev` extra installs `pytest`, `pytest-cov`, `ruff`, `mypy` and
    `types-Markdown`.

## Run the checks

These are the same commands that `.github/workflows/ci.yml` runs.

| Check | Command |
|---|---|
| Tests | `pytest -v` |
| Tests with coverage | `pytest -v --cov=mkdocs_markdown_in_template_plugin --cov-report=term` |
| Lint | `ruff check .` |
| Formatting | `ruff format --check .` |
| Types | `mypy` |

Without an editable install, run the tests with uv:

```bash
uv run --with pytest pytest -q
```

### What the tests cover

`tests/test_plugin.py` contains:

- `test_dedent_strips_common_indentation` and
  `test_dedent_trims_surrounding_blank_lines` for `_dedent`.
- `test_render_converts_markdown_to_html` for basic conversion.
- `test_render_resets_between_blocks`, which checks that a footnote from one
  block does not appear in the next.
- `test_on_env_registers_extension_and_copies_config` for the plugin hook.
- `test_integration_mkdocs_build`, which runs a real `mkdocs build` with a
  minimal theme whose `main.html` contains a `{% md %}` block.

CI runs the suite on Python 3.12 and 3.13, on Ubuntu and Windows, and in a
separate job against MkDocs `>=1.5,<1.6` and `>=1.6,<2.0`.

## Build the documentation

The site is built with [ProperDocs](https://pypi.org/project/properdocs/) and
the MaterialX theme. `src_docs/build.sh` runs both through `uvx` at pinned
versions, and installs this repository with `--with ..` so that the site's own
template override uses the current plugin code.

1. Build into `docs/`:

    ```bash
    src_docs/build.sh
    ```

    The build runs in strict mode, so any warning stops it.

2. Or start a live preview at `http://127.0.0.1:8000`:

    ```bash
    src_docs/build.sh serve
    ```

Edit the pages in `src_docs/md/`, never the HTML in `docs/`. On every push to
`main` that changes `src_docs/`, the `Docs` workflow rebuilds `docs/` and
commits the result.

## Build the package

```bash
./build.sh package
```

This removes `dist/`, runs `uv build`, and checks the result with
`uvx twine check dist/*`. `./build.sh` with no argument builds the
documentation and the package. `./build.sh docs` builds only the documentation.

The wheel contains only the `mkdocs_markdown_in_template_plugin` package. The
sdist contains the package, `README.md`, `CHANGELOG.md` and `LICENSE`.

## Versioning

The version comes from Git tags through `hatch-vcs`. There is no version number
in `pyproject.toml`. At build time, `hatch-vcs` writes
`mkdocs_markdown_in_template_plugin/__version__.py`. That file is in
`.gitignore`; do not commit it.

On a tagged commit with a clean tree, the version equals the tag without the
`v`, for example `1.0.5`. Between tags, it is a development version such as
`1.0.6.dev3+g1a2b3c4`.

## Release

Releases go to PyPI as `vexy-mkdocs-markdown-in-template`.

1. Add the changes to `CHANGELOG.md`.
2. Set a PyPI token for uv, for example in `UV_PUBLISH_TOKEN`.
3. Run:

    ```bash
    ./publish.sh
    ```

`publish.sh` runs `uvx gitnextver`, which commits pending changes, creates the
next `vX.Y.Z` tag and pushes it. The script then checks that `HEAD` carries a
`vX.Y.Z` tag, builds the package with `./build.sh package`, and uploads `dist/*`
with `uv publish`.

The pushed tag also starts `.github/workflows/release.yml`. That workflow builds
the package, uploads it to PyPI with trusted publishing (`skip-existing: true`,
so a version that `publish.sh` already uploaded is skipped), and creates a
GitHub release with the matching `CHANGELOG.md` section.

## Code style

- Line length 100, target Python 3.12, checked by `ruff` with the rule sets
  `E`, `F`, `I`, `UP`, `B` and `SIM`.
- Type hints on all functions; `mypy` checks the package.
- Each source file starts with a `this_file` comment that gives its path.
