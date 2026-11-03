#!/usr/bin/env python3
"""Mini Markdown to HTML parser supporting headings, bold, italic, and lists."""
from __future__ import annotations
import re


def parse_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def markdown_to_html(md: str) -> str:
    html_lines: list[str] = []
    in_list = False

    for raw_line in md.strip().splitlines():
        line = raw_line.strip()
        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if line.startswith("#"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            level = len(line) - len(line.lstrip("#"))
            heading_text = parse_inline(line.lstrip("#").strip())
            html_lines.append(f"<h{level}>{heading_text}</h{level}>")
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item_text = parse_inline(line[2:].strip())
            html_lines.append(f"  <li>{item_text}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{parse_inline(line)}</p>")

    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def self_check() -> None:
    md = "# Hello\n**bold** and *italic*\n- item 1\n- item 2"
    html = markdown_to_html(md)
    assert "<h1>Hello</h1>" in html
    assert "<strong>bold</strong> and <em>italic</em>" in html
    assert "<ul>\n  <li>item 1</li>\n  <li>item 2</li>\n</ul>" in html
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
