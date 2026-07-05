# this_file: mkdocs_markdown_in_template_plugin/plugin.py
"""MkDocs plugin that renders Markdown written inside Jinja2 template files.

A theme partial can wrap Markdown in ``{% md %} ... {% mdend %}``; the block is
converted to HTML while the template is rendered, so authors write Markdown where
they would otherwise hand-write HTML. The plugin reuses the site's own
``markdown_extensions`` and ``mdx_configs`` so template Markdown behaves exactly
like page Markdown.
"""

import textwrap
import typing as t

import markdown
from jinja2 import Environment
from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Node
from jinja2.parser import Parser
from mkdocs.config import Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files


class MarkdownJinjaExtension(Extension):
    """Jinja2 extension providing the ``{% md %} ... {% mdend %}`` block tag.

    The extension owns a single :class:`markdown.Markdown` instance, configured
    with the extension list and config the plugin copies onto the environment
    globals. That instance is reused for every block, matching how MkDocs renders
    page bodies.
    """

    tags = {"md"}

    def __init__(self, env: Environment) -> None:
        super().__init__(env)
        extensions = t.cast(
            "list[t.Any]",
            env.globals.get("mkdocs_markdown_in_template_plugin_markdown_extensions", []),
        )
        extension_configs = t.cast(
            "dict[str, t.Any]",
            env.globals.get("mkdocs_markdown_in_template_plugin_mdx_configs", {}),
        )
        self.markdowner = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs,
        )
        env.extend(markdowner=self.markdowner)

    def parse(self, parser: Parser) -> Node | list[Node]:
        """Parse a ``{% md %}`` block into a call to :meth:`_render_markdown`.

        The body up to ``{% mdend %}`` is captured verbatim and handed to the
        renderer at template-execution time via a Jinja2 ``CallBlock``.
        """
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(("name:mdend",), drop_needle=True)
        return CallBlock(self.call_method("_render_markdown"), [], [], body).set_lineno(lineno)

    def _render_markdown(self, caller: t.Callable[[], str]) -> str:
        """Render the captured block body to HTML.

        ``markdown.Markdown`` keeps per-document state, so reset it first to stop
        one block's footnotes or references from leaking into the next.
        """
        text = self._dedent(caller())
        self.markdowner.reset()
        return self.markdowner.convert(text)

    @staticmethod
    def _dedent(text: str) -> str:
        """Strip the block's common leading indentation.

        Template Markdown is usually indented to match the surrounding HTML; that
        indentation would otherwise read as a Markdown code block. Leading and
        trailing blank lines are removed before dedenting so the first real line
        sets the indentation baseline.
        """
        return textwrap.dedent(text.strip("\n"))


class MarkdownInTemplatePlugin(BasePlugin):
    """MkDocs plugin that registers :class:`MarkdownJinjaExtension` on the env."""

    config_scheme = ()

    def on_env(self, env: Environment, config: Config, files: Files) -> Environment:
        """Copy the site's Markdown config onto the env and add the extension.

        Runs once per build. The extension list and ``mdx_configs`` are stashed in
        env globals because the extension is instantiated by Jinja2 (via
        ``add_extension``) and cannot otherwise reach the MkDocs config.
        """
        env.globals["mkdocs_markdown_in_template_plugin_markdown_extensions"] = config.get(
            "markdown_extensions", []
        )
        env.globals["mkdocs_markdown_in_template_plugin_mdx_configs"] = config.get(
            "mdx_configs", {}
        )
        env.add_extension(MarkdownJinjaExtension)
        return env
