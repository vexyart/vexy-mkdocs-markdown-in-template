# Changelog

## [Unreleased]

### Changed
- Documentation moved from Jekyll (`docs/index.md`, `docs/_config.yml`) to a
  ProperDocs + MaterialX site: sources in `src_docs/md/` (11 pages), config in
  `src_docs/mkdocs.yml`, built into `docs/` by `src_docs/build.sh` and published
  at https://vexy.dev/vexy-mkdocs-markdown-in-template/. The site dog-foods the
  plugin in `src_docs/overrides/main.html`.
- `build.sh` now takes `all|docs|package`; `publish.sh` tags with `gitnextver`,
  builds and uploads with `uv publish`.
- `release.yml` publishes with `skip-existing: true`.

### Added
- `.github/workflows/docs.yml` rebuilds `docs/` on pushes to `main`.
- `Documentation` URL in the package metadata.

## [1.0.5]

### Added
- Test suite (`tests/test_plugin.py`): unit tests for dedent/reset/config plus a
  full `mkdocs build` integration test that renders `{% md %}` in a theme partial.
- GitHub Actions: `ci.yml` (pytest on Python 3.12/3.13 × Linux/Windows, an MkDocs
  1.5/1.6 compatibility matrix, and ruff + mypy lint) and `release.yml` (build,
  trusted-publish to PyPI, GitHub Release with changelog extraction).
- Jekyll + Just the Docs documentation in `docs/` (`_config.yml`, `index.md`).
- Project icon at `docs/assets/icon.png`.
- `mypy` + `types-Markdown` dev dependencies; pytest and mypy tool config.

### Fixed
- The shared `markdown.Markdown` instance is now reset between blocks, so
  footnotes and references no longer leak from one `{% md %}` block into the next.

### Changed
- Added type hints and docstrings throughout `plugin.py`; dropped the unused
  `enabled`/`dirs` attributes.

## [1.0.1]

### Changed
- Renamed PyPI distribution to `vexy-mkdocs-markdown-in-template`.
- Added a `pyproject.toml` (hatchling + hatch-vcs, VCS-derived version in
  `mkdocs_markdown_in_template_plugin/__version__.py`, gitignored); `requires-python = ">=3.12"`.
- `__init__.py` now imports `__version__` from the generated module.
- Repo URLs moved to the `vexyart` org.

### Removed
- `setup.py`, `requirements.txt`.

### Added
- `build.sh` / `publish.sh` convention scripts.
