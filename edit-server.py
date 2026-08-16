#!/usr/bin/env python3
"""Edit the invitation page in a browser and save straight into this repo.

    ./edit-server.py

Then open the printed URL, double-click any text to edit it, and click
"Save to repo" in the toolbar. The page is written back to this repo, the clean
copy is regenerated from it, and both are committed and pushed.

No GitHub token is involved anywhere — commits use whatever git credentials this
machine already has, and the server only listens on loopback.

Options:
    --port N     port to listen on (default 8765)
    --no-push    commit locally but don't push
"""

import argparse
import json
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO = Path(__file__).resolve().parent
PAGES_URL = "https://rahmin.github.io/prototyping"

# editable source -> published copy. Add a line here to make a new page editable.
PAGES = {
    "bloom-civic-host-invitation-editable.html": "bloom-civic-host-invitation.html",
    "utah-decision-map-delegates-editable.html": "utah-decision-map-delegates.html",
}

PUSH = True


def git(*args: str) -> str:
    proc = subprocess.run(
        ("git",) + args, cwd=REPO, capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "git failed")
    return proc.stdout


def save(editable: str, html: str) -> str:
    if editable not in PAGES:
        raise ValueError(f"{editable} is not an editable page")
    clean = PAGES[editable]

    # Guard against writing garbage over a real page.
    if 'id="editor-script"' not in html:
        raise ValueError("editor block missing — refusing to overwrite")
    if len(html) < 2000:
        raise ValueError("content looks truncated — refusing to overwrite")

    (REPO / editable).write_text(html, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "make-clean.py", editable, clean],
        cwd=REPO, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "could not regenerate published copy")

    if not git("status", "--porcelain", "--", editable, clean).strip():
        return "No changes to save."

    git("add", "--", editable, clean)
    git("commit", "-q", "-m", f"Edit {clean} in browser")

    if not PUSH:
        return "Saved and committed locally."

    git("push", "-q")
    return "Saved and pushed — live in about a minute."


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO), **kwargs)

    def do_POST(self):  # noqa: N802  (stdlib naming)
        parsed = urlparse(self.path)
        if parsed.path != "/__save":
            self.send_error(404)
            return

        page = (parse_qs(parsed.query).get("page") or [""])[0]
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length).decode("utf-8")

        try:
            message = save(page, body)
            ok, status = True, 200
        except Exception as exc:  # surface the reason in the toolbar
            message, ok, status = str(exc), False, 500

        payload = json.dumps({"ok": ok, "message": message}).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
        print(f"  {'saved' if ok else 'FAILED'}: {message}")

    def end_headers(self):
        # The page is being actively edited; never serve it from cache.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # the save handler prints what actually matters


def main() -> None:
    global PUSH

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args()
    PUSH = not args.no_push

    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as exc:
        raise SystemExit(f"Can't listen on port {args.port}: {exc}")

    print(f"Repo     {REPO}")
    print(f"On save  commit{'' if PUSH else ' (no push)'}"
          f"{f' + push -> {PAGES_URL}/' if PUSH else ''}\n")
    print("Editable pages:")
    for editable in PAGES:
        print(f"  http://localhost:{args.port}/{editable}")

    tracked = list(PAGES.keys()) + list(PAGES.values())
    try:
        pending = git("status", "--porcelain", "--", *tracked).strip()
    except RuntimeError:
        pending = ""
    if pending:
        print("\nNote: some of those files already have uncommitted changes, so")
        print("your first save will include them alongside your browser edits.")

    print("\nDouble-click any text to edit, then click \"Save to repo\".")
    print("Ctrl-C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
