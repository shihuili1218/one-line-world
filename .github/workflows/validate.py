#!/usr/bin/env python3
"""One PR adds exactly one line — in a brand-new file or any existing one.

Unified rules cover diff structure and text hygiene; syntax, types and
semantic blacklists are dispatched to validate_<ext>.py when one exists
for the touched file's extension (.ts -> validate_ts.py). File types
without a validator module are accepted unchecked.
"""
import importlib
import subprocess
import sys
from pathlib import Path

MAX_LEN = 400
# zero-width characters, Unicode line separators (U+2028/U+2029 are valid
# JS line terminators and could smuggle two lines into one), and NEL
INVISIBLE = set("\u200b\u200c\u200d\u2060\ufeff\u2028\u2029\u0085")


def fail(msg):
    print(f"FAIL {msg}")
    sys.exit(1)


def parse_diff(diff):
    """Extract (changed files, added lines, deleted lines) from a unified diff.

    Splits on \\n only: splitlines() would also split on \\r and friends,
    which would silently swallow the very characters we are checking for.
    """
    files, added, deleted = [], [], []
    for line in diff.split("\n"):
        if line.startswith("+++ b/"):
            files.append(line[6:])
        elif line.startswith("--- "):
            continue
        elif line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            deleted.append(line[1:])
    return files, added, deleted


def bad_chars(line):
    """Control characters (except tab) and invisible characters."""
    return [c for c in line if (ord(c) < 32 and c != "\t") or c in INVISIBLE]


def check_structure(diff):
    """Unified rules: shared by every file type."""
    if "Binary files" in diff:
        fail("binary files are not allowed")
    if "\\ No newline at end of file" in diff:
        fail("the file must end with a newline")

    files, added, deleted = parse_diff(diff)

    if len(files) != 1:
        fail(f"changed {len(files)} file(s), exactly 1 per PR")
    path = files[0]
    if path == ".github" or path.startswith(".github/"):
        fail("the .github/ directory is off-limits")
    if deleted:
        fail(f"changed or deleted {len(deleted)} existing line(s); lines can only be added")
    if len(added) != 1:
        fail(f"the PR must add exactly 1 line, got {len(added)}")

    line = added[0]
    if not line.strip():
        fail("an empty line is not a contribution")
    if line != line.rstrip():
        fail("trailing whitespace")
    if "\r" in line:
        fail("use LF, not CRLF")
    if len(line) > MAX_LEN:
        fail(f"line is {len(line)} chars, max is {MAX_LEN}")
    invisible = bad_chars(line)
    if invisible:
        fail(f"contains control or invisible characters: {invisible!r}")
    return path, line


def check_language(path, line):
    """Dispatch to validate_<ext>.py based on the touched file's extension."""
    lang = Path(path).suffix.lstrip(".")
    if not lang:
        return
    try:
        mod = importlib.import_module(f"validate_{lang}")
    except ModuleNotFoundError:
        return
    errors = mod.check(path, line)
    if errors:
        fail("\n".join(errors))


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    # decode manually: text=True would run universal-newline translation and
    # turn every CRLF into LF before the CRLF rule could ever see it;
    # quotepath=false keeps non-ASCII filenames as raw UTF-8;
    # no-renames makes a rename a full delete+add so it cannot sneak past
    # the "no deletions" rule
    diff = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--no-renames", "--unified=0", f"{base}...HEAD"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8", "replace")

    path, line = check_structure(diff)
    check_language(path, line)
    print(f"PASS valid line in {path}: {line!r}")


if __name__ == "__main__":
    main()
