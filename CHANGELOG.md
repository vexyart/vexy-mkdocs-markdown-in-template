# Changelog

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
