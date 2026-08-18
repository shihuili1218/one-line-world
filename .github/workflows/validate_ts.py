#!/usr/bin/env python3
"""TypeScript checks: full-file tsc type check plus a TS blacklist.

check(target, line) -> list of error strings; empty list means pass.
"""
import subprocess

# Without @types/node, tsc itself rejects process / child_process etc.,
# so the blacklist only covers runtime dangers and loophole directives
# that tsc happily accepts.
# typescript ships two bins, so name the package with -p and the bin explicitly.
# moduleResolution mirrors the site build (tsc --module amd) so that what
# passes the gate is exactly what runs on the gallery.
TSC = [
    "npx", "-y", "-p", "typescript@5", "tsc", "--noEmit", "--strict",
    "--target", "es2022", "--module", "esnext", "--moduleResolution", "node",
    "--lib", "es2022,dom",
]

# matched against the lowercased line with spaces and tabs stripped
BANNED = (
    "eval(",
    "function(",
    "while(true)",
    "for(;;)",
    "debugger",
    "@ts-ignore",
    "@ts-nocheck",
    "@ts-expect-error",
)


def check(target, line):
    errors = []
    low = line.lower().replace(" ", "").replace("\t", "")
    for ban in BANNED:
        if ban in low:
            errors.append(f"blacklisted: {ban}")

    r = subprocess.run(TSC + [target], capture_output=True, text=True)
    if r.returncode != 0:
        errors.append("tsc failed:\n" + (r.stdout + r.stderr).strip())
    return errors
