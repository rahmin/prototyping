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

REPO = Path(__file__).resolve().parent
EDITABLE = "bloom-civic-host-invitation-editable.html"
CLEAN = "bloom-civic-host-invitation.html"
PAGES_URL = "https://rahmin.github.io/prototyping"

PUSH = True


def git(*args: str) -> str:
    proc = subprocess.run(
        ("git",) + args, cwd=REPO, capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "git failed")
    return proc.stdout


def save(html: str) -> str:
    # Guard against writing garbage over the real page.
    if "BLOOM Civic Host Cohort" not in html:
        raise ValueError("that doesn't look like the invitation page")
    if 'id="editor-script"' not in html:
        raise ValueError("editor block missing — refusing to overwrite")

    (REPO / EDITABLE).write_text(html, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "make-clean.py", EDITABLE, CLEAN],
        cwd=REPO, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "could not regenerate clean copy")

    if not git("status", "--porcelain", "--", EDITABLE, CLEAN).strip():
        return "No changes to save."

    git("add", "--", EDITABLE, CLEAN)
    git("commit", "-q", "-m", "Edit invitation copy in browser")

    if not PUSH:
        return "Saved and committed locally."

    git("push", "-q")
    return "Saved and pushed — live in about a minute."


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO), **kwargs)

    def do_POST(self):  # noqa: N802  (stdlib naming)
        if self.path != "/__save":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length).decode("utf-8")

        try:
            message = save(body)
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

    url = f"http://localhost:{args.port}/{EDITABLE}"
    print(f"Editing  {url}")
    print(f"Repo     {REPO}")
    print(f"On save  commit{'' if PUSH else ' (no push)'}"
          f"{f' + push -> {PAGES_URL}/{CLEAN}' if PUSH else ''}")
    try:
        pending = git("status", "--porcelain", "--", EDITABLE, CLEAN).strip()
    except RuntimeError:
        pending = ""
    if pending:
        print("\nNote: those files already have uncommitted changes, so your")
        print("first save will include them alongside your browser edits.")

    print("\nDouble-click any text to edit, then click \"Save to repo\".")
    print("Ctrl-C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
