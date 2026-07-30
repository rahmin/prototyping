#!/usr/bin/env python3
"""Derive the clean (editor-stripped) invitation page from the editable one.

Usage: make-clean.py <editable.html> <clean.html>

Removes the same three blocks the in-page "Download clean copy" button drops,
plus the attributes the editor leaves on elements it touched, then pins trailing
whitespace so repeat runs produce byte-identical output.

Shared by sync-edits.sh and edit-server.py so the strip logic lives in one place.
"""

import re
import sys

EDITOR_BLOCKS = (
    ("editor stylesheet", r'<style id="editor-style">.*?</style>\n?'),
    ("editor toolbar", r'<div id="editor-ui">.*?</div>\n?'),
    ("editor script", r'<script id="editor-script">.*?</script>\n?'),
)


def strip_editor(html: str) -> str:
    for label, pattern in EDITOR_BLOCKS:
        html, found = re.subn(pattern, "", html, flags=re.S)
        if found != 1:
            raise ValueError(
                f"Expected exactly one {label} block, found {found}. The "
                "editable file's structure may have changed — check it before "
                "regenerating the clean copy."
            )

    html = re.sub(r'\s+data-ce="[^"]*"', "", html)
    html = re.sub(r'\s+contenteditable="[^"]*"', "", html)

    # Removing those blocks leaves a variable number of trailing blank lines.
    html = re.sub(r"\n+(</body></html>\s*)$", r"\n\n\1", html)
    return html


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__.strip())

    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        source = fh.read()

    try:
        result = strip_editor(source)
    except ValueError as exc:
        raise SystemExit(f"make-clean.py: {exc}")

    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(result)


if __name__ == "__main__":
    main()
