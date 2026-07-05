# this_file: tests/test_plugin.py
"""Tests for the markdown-in-template MkDocs plugin.

Unit tests exercise the dedent/reset behaviour of the Jinja2 extension directly;
the integration test drives a real ``mkdocs build`` against a throwaway site with
a custom theme template that uses ``{% md %}``.
"""

from pathlib import Path

import pytest
from jinja2 import Environment
from markdown import Markdown

from mkdocs_markdown_in_template_plugin.plugin import (
    MarkdownInTemplatePlugin,
    MarkdownJinjaExtension,
)


def _make_extension() -> MarkdownJinjaExtension:
    """Build the extension on a bare Jinja2 environment, as MkDocs would."""
    env = Environment()
    env.globals["mkdocs_markdown_in_template_plugin_markdown_extensions"] = []
    env.globals["mkdocs_markdown_in_template_plugin_mdx_configs"] = {}
    return MarkdownJinjaExtension(env)


def test_dedent_strips_common_indentation() -> None:
    assert MarkdownJinjaExtension._dedent("    # Heading\n    body") == "# Heading\nbody"


def test_dedent_trims_surrounding_blank_lines() -> None:
    assert MarkdownJinjaExtension._dedent("\n\n  text\n\n") == "text"


def test_render_converts_markdown_to_html() -> None:
    ext = _make_extension()
    html = ext._render_markdown(lambda: "# Title\n\nRegular and **bold** text")
    assert "<h1>Title</h1>" in html
    assert "<strong>bold</strong>" in html


def test_render_resets_between_blocks() -> None:
    """A footnote in one block must not bleed into the next rendered block."""
    ext = _make_extension()
    ext.markdowner = Markdown(extensions=["footnotes"])
    first = ext._render_markdown(lambda: "Text[^1]\n\n[^1]: A note.")
    second = ext._render_markdown(lambda: "Plain paragraph.")
    assert 'class="footnote"' in first
    assert 'class="footnote"' not in second


def test_on_env_registers_extension_and_copies_config() -> None:
    plugin = MarkdownInTemplatePlugin()
    env = Environment()
    config = {"markdown_extensions": ["tables"], "mdx_configs": {"tables": {}}}

    returned = plugin.on_env(env, config, files=None)  # type: ignore[arg-type]

    assert returned is env
    assert env.globals["mkdocs_markdown_in_template_plugin_markdown_extensions"] == ["tables"]
    assert "md" in {tag for ext in env.extensions.values() for tag in ext.tags}


@pytest.mark.parametrize("theme", ["mkdocs"])
def test_integration_mkdocs_build(tmp_path: Path, theme: str) -> None:
    """A full ``mkdocs build`` renders ``{% md %}`` in a theme partial to HTML."""
    from mkdocs.commands.build import build
    from mkdocs.config import load_config

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Home\n", encoding="utf-8")

    # A minimal custom theme whose main template embeds Markdown via the plugin.
    theme_dir = tmp_path / "theme"
    theme_dir.mkdir()
    (theme_dir / "main.html").write_text(
        "<!doctype html><html><body>\n"
        "{% md %}\n"
        "# Injected\n\n"
        "Regular and **bold** text.\n"
        "{% mdend %}\n"
        "</body></html>\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    mkdocs_yml = tmp_path / "mkdocs.yml"
    mkdocs_yml.write_text(
        f"site_name: Test\n"
        f"docs_dir: {docs_dir}\n"
        f"site_dir: {site_dir}\n"
        f"theme:\n"
        f"  name: null\n"
        f"  custom_dir: {theme_dir}\n"
        f"plugins:\n"
        f"  - markdown-in-template\n",
        encoding="utf-8",
    )

    config = load_config(str(mkdocs_yml))
    build(config)

    rendered = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Injected</h1>" in rendered
    assert "<strong>bold</strong>" in rendered
