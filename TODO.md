# TODO

Bigger ideas beyond the v1.0.5 modernization pass. Nothing here blocks a release.

- [ ] Add a plugin config option to choose the tag names (`md`/`mdend`), so the
      block delimiters don't collide with other Jinja2 extensions a theme may use.
- [ ] Support an inline form (e.g. a `{{ 'text' | md }}` filter) for short strings,
      alongside the current block form.
- [ ] Document interaction ordering with other MkDocs plugins that rewrite HTML,
      with a worked example on the docs site.
- [ ] Add a Material-for-MkDocs integration test (the current test uses the null
      theme with a custom partial) to guard against theme-specific env quirks.
- [ ] Publish the Jekyll docs to GitHub Pages via an Actions workflow.
